"""Version matrix checks for generated type aliases.

The emitted alias form depends on the Pydantic family and the target Python
version, and GraphQL scalars and unions are aliases whether or not
``--use-type-alias`` is passed. These tests pin that matrix through the emitted
expressions, so an implementation stays free to organise its dispatch.
"""

from __future__ import annotations

import json
from argparse import Namespace
from typing import TYPE_CHECKING, Any

import pytest

from datamodel_code_generator.__main__ import Exit, main

if TYPE_CHECKING:
    from pathlib import Path

SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"name": {"$ref": "#/definitions/SimpleString"}, "either": {"$ref": "#/definitions/UnionType"}},
    "definitions": {
        "SimpleString": {"type": "string"},
        "UnionType": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
    },
}

GRAPHQL = """
scalar Date

type Person {
  name: String
  born: Date
}

type Pet {
  name: String
}

union Being = Person | Pet

type Query {
  being: Being
}
"""

NON_PYDANTIC_MODELS = ["dataclasses.dataclass", "typing.TypedDict", "msgspec.Struct"]


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep CLI arguments from leaking between generations."""
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)
    monkeypatch.setattr("datamodel_code_generator.arguments.namespace", namespace_)


def generate(tmp_path: Path, output_model: str, target: str, *arguments: str) -> str:
    """Generate from the JSON Schema fixture and return the output."""
    input_file = tmp_path / "schema.json"
    input_file.write_text(json.dumps(SCHEMA), encoding="utf-8")
    output_file = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(input_file),
        "--input-file-type",
        "jsonschema",
        "--output",
        str(output_file),
        "--output-model-type",
        output_model,
        "--target-python-version",
        target,
        *arguments,
    ])
    assert return_code == Exit.OK
    return output_file.read_text(encoding="utf-8")


def generate_graphql(tmp_path: Path, output_model: str, target: str, *arguments: str) -> str:
    """Generate from the GraphQL fixture and return the output."""
    input_file = tmp_path / "schema.graphql"
    input_file.write_text(GRAPHQL, encoding="utf-8")
    output_file = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(input_file),
        "--input-file-type",
        "graphql",
        "--output",
        str(output_file),
        "--output-model-type",
        output_model,
        "--target-python-version",
        target,
        *arguments,
    ])
    assert return_code == Exit.OK
    return output_file.read_text(encoding="utf-8")


def imports_from_typing_extensions(generated: str, name: str) -> bool:
    """Return whether ``name`` is imported from ``typing_extensions``."""
    return any(line.startswith("from typing_extensions import") and name in line for line in generated.splitlines())


def alias_definition(generated: str, name: str) -> str:
    """Return the definition of the alias ``name`` on one line, however it is wrapped."""
    lines = generated.splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if line.startswith((f"{name} ", f"{name}:", f"type {name} ", f"type {name}="))
    ]
    assert starts, f"no definition of {name} in:\n{generated}"
    start = starts[0]
    end = start + 1
    while end < len(lines) and lines[end].startswith((" ", ")", "]")):
        end += 1
    return " ".join(line.strip() for line in lines[start:end])


def test_pydantic_v1_python_39_uses_the_backport_annotation(tmp_path: Path) -> None:
    """Pydantic v1 on Python 3.9 annotates with the typing_extensions backport."""
    generated = generate(tmp_path, "pydantic.BaseModel", "3.9", "--use-type-alias")
    assert "SimpleString: TypeAlias = str" in generated
    assert "from typing_extensions import TypeAlias" in generated
    assert "TypeAliasType(" not in generated
    assert "type SimpleString" not in generated


@pytest.mark.parametrize("target", ["3.10", "3.11", "3.12"])
def test_pydantic_v1_keeps_annotations_on_newer_targets(target: str, tmp_path: Path) -> None:
    """Pydantic v1 annotates on every target, taking TypeAlias from typing after 3.9."""
    generated = generate(tmp_path, "pydantic.BaseModel", target, "--use-type-alias")
    assert "SimpleString: TypeAlias = str" in generated
    assert "from typing_extensions import TypeAlias" not in generated
    assert "TypeAliasType(" not in generated
    assert "type SimpleString" not in generated


@pytest.mark.parametrize("target", ["3.9", "3.10", "3.11"])
def test_pydantic_v2_uses_the_type_alias_type_backport(target: str, tmp_path: Path) -> None:
    """Pydantic v2 before 3.12 constructs TypeAliasType from typing_extensions."""
    generated = generate(tmp_path, "pydantic_v2.BaseModel", target, "--use-type-alias")
    assert 'SimpleString = TypeAliasType("SimpleString", str)' in generated
    assert "from typing_extensions import TypeAliasType" in generated
    assert "type SimpleString" not in generated


def test_pydantic_v2_python_312_uses_the_type_statement(tmp_path: Path) -> None:
    """Pydantic v2 on Python 3.12 emits the native type statement."""
    generated = generate(tmp_path, "pydantic_v2.BaseModel", "3.12", "--use-type-alias")
    assert "type SimpleString = str" in generated
    assert "TypeAliasType(" not in generated
    assert "TypeAlias" not in generated


def test_graphql_scalars_are_aliases_without_the_flag(tmp_path: Path) -> None:
    """GraphQL scalars are version-correct aliases whether or not the flag is passed."""
    for arguments in ((), ("--use-type-alias",)):
        generated = generate_graphql(tmp_path, "pydantic_v2.BaseModel", "3.9", *arguments)
        assert 'Date = TypeAliasType("Date", str)' in generated
        assert "from typing_extensions import TypeAliasType" in generated


def test_graphql_scalars_use_the_type_statement_on_python_312(tmp_path: Path) -> None:
    """GraphQL scalars use the native statement on Python 3.12 without the flag."""
    generated = generate_graphql(tmp_path, "pydantic_v2.BaseModel", "3.12")
    assert "type Date = str" in generated
    assert "TypeAliasType(" not in generated


@pytest.mark.parametrize("arguments", [(), ("--use-type-alias",)], ids=["flag-off", "flag-on"])
@pytest.mark.parametrize("target", ["3.9", "3.11"])
@pytest.mark.parametrize("output_model", NON_PYDANTIC_MODELS)
def test_non_pydantic_roots_use_the_backport_before_python_312(
    output_model: str, target: str, arguments: tuple[str, ...], tmp_path: Path
) -> None:
    """Dataclass, TypedDict and msgspec roots construct TypeAliasType before 3.12, flag or not."""
    generated = generate(tmp_path, output_model, target, *arguments)
    assert 'SimpleString = TypeAliasType("SimpleString", str)' in generated
    assert 'UnionType = TypeAliasType("UnionType", Union[str, int])' in generated
    assert imports_from_typing_extensions(generated, "TypeAliasType")
    assert "type SimpleString" not in generated
    assert "RootModel" not in generated


@pytest.mark.parametrize("arguments", [(), ("--use-type-alias",)], ids=["flag-off", "flag-on"])
@pytest.mark.parametrize("output_model", NON_PYDANTIC_MODELS)
def test_non_pydantic_roots_use_the_type_statement_on_python_312(
    output_model: str, arguments: tuple[str, ...], tmp_path: Path
) -> None:
    """Dataclass, TypedDict and msgspec roots use the native statement on 3.12, flag or not."""
    generated = generate(tmp_path, output_model, "3.12", *arguments)
    assert "type SimpleString = str" in generated
    assert "type UnionType = Union[str, int]" in generated
    assert "TypeAliasType(" not in generated
    assert "RootModel" not in generated
    assert not any(line.startswith("SimpleString") for line in generated.splitlines())


@pytest.mark.parametrize("arguments", [(), ("--use-type-alias",)], ids=["flag-off", "flag-on"])
def test_graphql_unions_are_aliases_before_python_312(arguments: tuple[str, ...], tmp_path: Path) -> None:
    """A GraphQL union is a backported alias over its members whether or not the flag is passed."""
    generated = generate_graphql(tmp_path, "pydantic_v2.BaseModel", "3.9", *arguments)
    definition = alias_definition(generated, "Being")
    assert "TypeAliasType" in definition
    assert '"Being"' in definition
    assert "Person" in definition
    assert "Pet" in definition
    assert imports_from_typing_extensions(generated, "TypeAliasType")


@pytest.mark.parametrize("arguments", [(), ("--use-type-alias",)], ids=["flag-off", "flag-on"])
def test_graphql_unions_use_the_type_statement_on_python_312(arguments: tuple[str, ...], tmp_path: Path) -> None:
    """A GraphQL union uses the native statement on Python 3.12 whether or not the flag is passed."""
    generated = generate_graphql(tmp_path, "pydantic_v2.BaseModel", "3.12", *arguments)
    definition = alias_definition(generated, "Being")
    assert definition.startswith("type Being")
    assert "Person" in definition
    assert "Pet" in definition
    assert "TypeAliasType" not in definition
