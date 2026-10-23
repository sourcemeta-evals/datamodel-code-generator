"""Runtime checks for generated type aliases: recursion, model reuse and imports.

A snapshot cannot express that generated code imports and validates, so these
tests execute the generated module instead of comparing it against an expected
file. Recursion is exercised with the default ``Union[...]`` rendering, which is
what the task requires.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from argparse import Namespace
from typing import TYPE_CHECKING, Any

import pytest
from pydantic import ValidationError

from datamodel_code_generator.__main__ import Exit, main

if TYPE_CHECKING:
    from pathlib import Path

RECURSIVE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"tree": {"$ref": "#/definitions/Node"}},
    "definitions": {
        "Node": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"$ref": "#/definitions/Node"}},
            ]
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


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep CLI arguments from leaking between generations."""
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)
    monkeypatch.setattr("datamodel_code_generator.arguments.namespace", namespace_)


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
    """Import a generated module by path, so unresolved names surface here."""
    specification = importlib.util.spec_from_file_location(name, output_file)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    try:
        specification.loader.exec_module(module)
        return module
    finally:
        del sys.modules[name]


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
    assert module.Root(tree=["a", ["b"]]).tree == ["a", ["b"]]
    with pytest.raises(ValidationError):
        module.Root(tree=1)


def test_recursive_alias_annotation_quotes_its_self_reference(tmp_path: Path) -> None:
    """The annotation form quotes its self-reference so the module can import.

    Pydantic v1 output cannot be executed against the installed Pydantic v2, so
    this path is checked through the emitted expression.
    """
    output_file = generate_module(
        tmp_path,
        RECURSIVE_SCHEMA,
        "--output-model-type",
        "pydantic.BaseModel",
        "--target-python-version",
        "3.9",
    )
    definition = next(line for line in output_file.read_text(encoding="utf-8").splitlines() if line.startswith("Node"))
    assert '"Node"' in definition or "'Node'" in definition


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


def test_recursive_type_statement_has_no_rebuild_call(tmp_path: Path) -> None:
    """The Python 3.12 form defers evaluation and gets no model_rebuild call."""
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
    assert module.Being is not None
    assert module.Creature is not None


def test_reuse_model_renders_duplicate_graphql_unions_natively(tmp_path: Path) -> None:
    """The Python 3.12 form names the reused union rather than a placeholder.

    Native statements cannot be imported on older interpreters, so the
    definition is checked through the emitted expression.
    """
    output_file = generate_module(
        tmp_path,
        DUPLICATE_UNION_GRAPHQL,
        "--reuse-model",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.12",
    )
    definition = next(
        line for line in output_file.read_text(encoding="utf-8").splitlines() if line.startswith("type Creature")
    )
    assert "Being" in definition or "Person" in definition


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
