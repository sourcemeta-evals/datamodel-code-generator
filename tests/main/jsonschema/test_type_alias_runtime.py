"""Runtime checks for generated type aliases: recursion and model reuse.

A snapshot cannot express that generated code imports, so these tests execute
the generated module instead of comparing it against an expected file.
"""

from __future__ import annotations

import importlib.util
import json
import sys
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


def generate_module(tmp_path: Path, schema: dict[str, Any], *arguments: str) -> Path:
    """Generate a module from an inline schema and return the output path."""
    input_file = tmp_path / "schema.json"
    input_file.write_text(json.dumps(schema), encoding="utf-8")
    output_file = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(input_file),
        "--input-file-type",
        "jsonschema",
        "--output",
        str(output_file),
        "--use-type-alias",
        *arguments,
    ])
    assert return_code == Exit.OK
    return output_file


def import_module(output_file: Path, name: str) -> Any:
    """Import a generated module by path, so unresolved names surface here."""
    specification = importlib.util.spec_from_file_location(name, output_file)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    try:
        specification.loader.exec_module(module)
    finally:
        del sys.modules[name]
    return module


def test_recursive_alias_backport_imports(tmp_path: Path) -> None:
    """A self-recursive alias imports before Python 3.12."""
    output_file = generate_module(
        tmp_path,
        RECURSIVE_SCHEMA,
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    module = import_module(output_file, "eval_alias_recursive_backport")
    assert module.Node is not None


def test_recursive_alias_annotation_imports(tmp_path: Path) -> None:
    """A self-recursive alias imports in the TypeAlias annotation form."""
    output_file = generate_module(tmp_path, RECURSIVE_SCHEMA)
    module = import_module(output_file, "eval_alias_recursive_annotation")
    assert module.Node is not None


def test_mutually_recursive_aliases_import(tmp_path: Path) -> None:
    """Aliases that reference each other import regardless of their order."""
    output_file = generate_module(
        tmp_path,
        MUTUAL_SCHEMA,
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.9",
    )
    module = import_module(output_file, "eval_alias_mutual")
    assert module.Left is not None
    assert module.Right is not None


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
    """Duplicate aliases render and validate when models are reused."""
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
