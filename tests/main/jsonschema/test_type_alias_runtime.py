"""Runtime checks for generated type aliases: recursion, model reuse and imports.

A snapshot cannot express that generated code imports and validates, so these
tests execute the generated module instead of comparing it against an expected
file. Recursion is exercised with the default ``Union[...]`` rendering, which is
what the task requires.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import sys
from argparse import Namespace
from typing import TYPE_CHECKING, Any

import pytest
from pydantic import TypeAdapter, ValidationError, validate_call

from datamodel_code_generator import PythonVersion
from datamodel_code_generator.__main__ import Exit, main
from datamodel_code_generator.format import is_supported_in_black

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

RECURSIVE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"tree": {"$ref": "#/definitions/Node"}},
    "definitions": {
        "Node": {
            "description": "It's a Node value",
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"$ref": "#/definitions/Node"}},
            ],
        }
    },
}

MUTUAL_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"left": {"$ref": "#/definitions/Left"}},
    "definitions": {
        "Left": {"anyOf": [{"type": "string"}, {"$ref": "#/definitions/Right"}]},
        "Right": {"anyOf": [{"type": "integer"}, {"type": "array", "items": {"$ref": "#/definitions/Left"}}]},
    },
}

ARRAY_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"tree": {"$ref": "#/definitions/Tree"}},
    "definitions": {"Tree": {"type": "array", "items": {"$ref": "#/definitions/Tree"}}},
}

DUPLICATE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"a": {"$ref": "#/definitions/CodeA"}, "b": {"$ref": "#/definitions/CodeB"}},
    "definitions": {
        "CodeA": {"type": "string", "pattern": "^[a-z]+$", "minLength": 3},
        "CodeB": {"type": "string", "pattern": "^[a-z]+$", "minLength": 3},
    },
}

CONSTRAINED_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"code": {"$ref": "#/definitions/Code"}},
    "definitions": {"Code": {"type": "string", "maxLength": 4}},
}

PACKAGE_COMMON: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "definitions": {"Code": {"type": "string", "maxLength": 4}},
}

PACKAGE_MAIN: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Main",
    "type": "object",
    "properties": {"codes": {"$ref": "#/definitions/Codes"}},
    "definitions": {"Codes": {"type": "array", "items": {"$ref": "common.json#/definitions/Code"}}},
}

DUPLICATE_UNION_GRAPHQL = """
type Person {
  name: String
}

type Pet {
  name: String
}

union Being = Person | Pet

union Creature = Person | Pet

type Query {
  being: Being
  creature: Creature
}
"""


SKIP_WITHOUT_BLACK_312 = pytest.mark.skipif(
    not is_supported_in_black(PythonVersion.PY_312),
    reason="Installed black doesn't support Python version 3.12",
)

IMPORTED_MODULES: list[str] = []


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Keep CLI arguments and imported modules from leaking between generations."""
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)
    monkeypatch.setattr("datamodel_code_generator.arguments.namespace", namespace_)
    yield
    for name in IMPORTED_MODULES:
        sys.modules.pop(name, None)
    IMPORTED_MODULES.clear()


def generate_module(tmp_path: Path, source: dict[str, Any] | str, *arguments: str) -> Path:
    """Generate a module from an inline schema and return the output path."""
    if isinstance(source, str):
        input_file = tmp_path / "schema.graphql"
        input_file.write_text(source, encoding="utf-8")
        input_file_type = "graphql"
    else:
        input_file = tmp_path / "schema.json"
        input_file.write_text(json.dumps(source), encoding="utf-8")
        input_file_type = "jsonschema"
    output_file = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(input_file),
        "--input-file-type",
        input_file_type,
        "--output",
        str(output_file),
        "--use-type-alias",
        *arguments,
    ])
    assert return_code == Exit.OK
    return output_file


def generate_package(tmp_path: Path) -> Path:
    """Generate a package from two schema files and return the output directory."""
    input_directory = tmp_path / "schemas"
    input_directory.mkdir()
    (input_directory / "common.json").write_text(json.dumps(PACKAGE_COMMON), encoding="utf-8")
    (input_directory / "main.json").write_text(json.dumps(PACKAGE_MAIN), encoding="utf-8")
    output_directory = tmp_path / "generated"
    return_code: Exit = main([
        "--input",
        str(input_directory),
        "--input-file-type",
        "jsonschema",
        "--output",
        str(output_directory),
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
        "--use-type-alias",
    ])
    assert return_code == Exit.OK
    return output_directory


def import_package_module(output_directory: Path, module_name: str) -> Any:
    """Import one module of a generated package, so imported names resolve here."""
    sys.path.insert(0, str(output_directory.parent))
    try:
        return importlib.import_module(f"{output_directory.name}.{module_name}")
    finally:
        sys.path.remove(str(output_directory.parent))
        for name in [name for name in sys.modules if name.split(".")[0] == output_directory.name]:
            del sys.modules[name]


def import_module(output_file: Path, name: str) -> Any:
    """Import a generated module by path, so unresolved names surface here.

    The module stays registered until the test ends, so that a reference it
    defers still resolves against its own namespace.
    """
    specification = importlib.util.spec_from_file_location(name, output_file)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    IMPORTED_MODULES.append(name)
    specification.loader.exec_module(module)
    return module


def alias_value(generated: str, name: str) -> ast.expr:
    """Return the parsed right-hand side of the annotated alias ``name``."""
    for node in ast.walk(ast.parse(generated)):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            assert node.value is not None
            return node.value
    message = f"no annotated definition of {name} in:\n{generated}"
    raise AssertionError(message)


def alias_defers_its_self_reference(generated: str, name: str) -> bool:
    """Return whether the alias names itself only inside a string.

    Both ``Union[str, List["Node"]]`` and ``"Union[str, List[Node]]"`` defer the
    self-reference; an unquoted ``List[Node]`` evaluates it during assignment and
    raises ``NameError`` on import.
    """
    return not any(isinstance(child, ast.Name) and child.id == name for child in ast.walk(alias_value(generated, name)))


def alias_reference_names(generated: str, name: str) -> set[str]:
    """Return the names an alias refers to, reading deferred references out of their strings.

    ``Union[str, List["Node"]]`` and ``"Union[str, List[Node]]"`` both refer to
    ``str`` and ``Node``, so dropping either branch is visible whichever form a
    solution emits. A string that is not an expression, such as a description,
    contributes nothing.
    """
    referenced: set[str] = set()
    for node in ast.walk(alias_value(generated, name)):
        if isinstance(node, ast.Name):
            referenced.add(node.id)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            try:
                deferred = ast.parse(node.value, mode="eval")
            except SyntaxError:
                continue
            referenced |= {child.id for child in ast.walk(deferred) if isinstance(child, ast.Name)}
    return referenced


def assert_union_over_person_and_pet(module: Any, name: str) -> None:
    """Check that a generated union alias validates both members and nothing else."""
    adapter: TypeAdapter[Any] = TypeAdapter(getattr(module, name))
    assert isinstance(adapter.validate_python(module.Person(name="a")), module.Person)
    assert isinstance(adapter.validate_python(module.Pet(name="a")), module.Pet)
    with pytest.raises(ValidationError):
        adapter.validate_python(1)


def test_recursive_alias_backport_imports_and_validates(tmp_path: Path) -> None:
    """A self-recursive alias imports and validates nested values before Python 3.12."""
    output_file = generate_module(
        tmp_path,
        RECURSIVE_SCHEMA,
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    module = import_module(output_file, "eval_alias_recursive_backport")
    assert "It's a Node value" in output_file.read_text(encoding="utf-8")
    assert module.Root(tree=["a", ["b"]]).tree == ["a", ["b"]]
    with pytest.raises(ValidationError):
        module.Root(tree=1)


def test_recursive_alias_annotation_defers_its_self_reference(tmp_path: Path) -> None:
    """The annotation form keeps both branches and defers its self-reference.

    Pydantic v1 output cannot be executed against the installed Pydantic v2, so
    this path is checked through the emitted expression. A solution that replaces
    the recursive branch with a scalar leaves an alias that imports but no longer
    describes the schema.
    """
    output_file = generate_module(
        tmp_path,
        RECURSIVE_SCHEMA,
        "--output-model-type",
        "pydantic.BaseModel",
        "--target-python-version",
        "3.9",
    )
    generated = output_file.read_text(encoding="utf-8")
    assert {"str", "Node"} <= alias_reference_names(generated, "Node")
    assert alias_defers_its_self_reference(generated, "Node")


def test_mutually_recursive_aliases_import_and_validate(tmp_path: Path) -> None:
    """Aliases that reference each other import and validate regardless of order."""
    output_file = generate_module(
        tmp_path,
        MUTUAL_SCHEMA,
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    module = import_module(output_file, "eval_alias_mutual")
    assert module.Root(left="a").left == "a"
    assert module.Root(left=["a"]).left == ["a"]


def test_recursive_array_alias_keeps_its_item_type(tmp_path: Path) -> None:
    """A recursive array alias keeps validating its elements."""
    output_file = generate_module(
        tmp_path,
        ARRAY_SCHEMA,
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    module = import_module(output_file, "eval_alias_recursive_array")
    assert module.Root(tree=[[], [[]]]).tree == [[], [[]]]
    with pytest.raises(ValidationError):
        module.Root(tree=[1])


@SKIP_WITHOUT_BLACK_312
def test_recursive_type_statement_has_no_rebuild_call(tmp_path: Path) -> None:
    """The Python 3.12 form defers evaluation and gets no model_rebuild call.

    Older interpreters cannot execute the native statement, so they check the
    emitted text alone.
    """
    output_file = generate_module(
        tmp_path,
        RECURSIVE_SCHEMA,
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.12",
    )
    generated = output_file.read_text(encoding="utf-8")
    assert "type Node = " in generated
    assert "Node.model_rebuild()" not in generated
    assert "Node.update_forward_refs()" not in generated
    if sys.version_info >= (3, 12):
        module = import_module(output_file, "eval_alias_recursive_native")
        assert module.Root(tree=["a", ["b"]]).tree == ["a", ["b"]]
        with pytest.raises(ValidationError):
            module.Root(tree=1)


def test_reuse_model_renders_duplicate_aliases(tmp_path: Path) -> None:
    """Duplicate aliases render and keep validating when models are reused."""
    output_file = generate_module(
        tmp_path,
        DUPLICATE_SCHEMA,
        "--reuse-model",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    module = import_module(output_file, "eval_alias_reuse")
    assert module.CodeA is not None
    assert module.CodeB is not None
    assert module.Root(a="abc", b="abc").a == "abc"
    with pytest.raises(ValidationError):
        module.Root(a="AB", b="abc")


def test_reuse_model_imports_duplicate_graphql_unions(tmp_path: Path) -> None:
    """Duplicate GraphQL unions keep their members when models are reused."""
    output_file = generate_module(
        tmp_path,
        DUPLICATE_UNION_GRAPHQL,
        "--reuse-model",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    module = import_module(output_file, "eval_alias_graphql_reuse")
    assert_union_over_person_and_pet(module, "Being")
    assert_union_over_person_and_pet(module, "Creature")


@SKIP_WITHOUT_BLACK_312
@pytest.mark.skipif(sys.version_info < (3, 12), reason="The native type statement needs Python 3.12")
def test_reuse_model_imports_duplicate_graphql_unions_natively(tmp_path: Path) -> None:
    """The Python 3.12 form keeps every member of the reused union."""
    output_file = generate_module(
        tmp_path,
        DUPLICATE_UNION_GRAPHQL,
        "--reuse-model",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.12",
    )
    module = import_module(output_file, "eval_alias_graphql_reuse_native")
    assert_union_over_person_and_pet(module, "Being")
    assert_union_over_person_and_pet(module, "Creature")


def test_constrained_alias_validates_a_call_argument(tmp_path: Path) -> None:
    """A constrained alias keeps its constraint when it annotates a validated call.

    The callable is appended to the generated module so that its annotation
    resolves against the alias the module defines.
    """
    output_file = generate_module(
        tmp_path,
        CONSTRAINED_SCHEMA,
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    output_file.write_text(
        output_file.read_text(encoding="utf-8") + "\n\ndef shorten(code: Code) -> str:\n    return code\n",
        encoding="utf-8",
    )
    module = import_module(output_file, "eval_alias_validate_call")
    checked = validate_call(module.shorten)
    assert checked("ok") == "ok"
    with pytest.raises(ValidationError):
        checked("too long")


def test_imported_alias_keeps_its_module_qualification(tmp_path: Path) -> None:
    """An alias referring to another module's alias keeps the name its import binds.

    The short name is not bound in the referring module, so quoting it there
    leaves a model that cannot be built.
    """
    output_directory = generate_package(tmp_path)
    module = import_package_module(output_directory, "main")
    assert module.Main(codes=["ok"]).codes == ["ok"]
    with pytest.raises(ValidationError):
        module.Main(codes=["too long"])
