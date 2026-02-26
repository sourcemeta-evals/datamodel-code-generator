from __future__ import annotations

import json
from pathlib import Path

import pytest

from datamodel_code_generator import DataModelType, InputFileType, PythonVersion, generate
from datamodel_code_generator.__main__ import Exit, main

SCHEMA = {
    "definitions": {
        "SimpleString": {"type": "string"},
        "UnionType": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        "AnnotatedType": {
            "title": "MyAnnotatedType",
            "description": "An annotated union type",
            "anyOf": [{"type": "string"}, {"type": "boolean"}],
        },
    }
}


@pytest.mark.parametrize(
    ("output_model_type", "target_python_version", "expected_snippets", "unexpected_snippets"),
    [
        (
            DataModelType.PydanticBaseModel,
            PythonVersion.PY_39,
            [
                "from typing_extensions import TypeAlias",
                "SimpleString: TypeAlias = str",
                "UnionType: TypeAlias = Union[str, int]",
                "AnnotatedType: TypeAlias = Annotated[",
                "description='An annotated union type'",
            ],
            ["class SimpleString(", "RootModel[", "TypeAliasType("],
        ),
        (
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_39,
            [
                "from typing_extensions import TypeAliasType",
                'SimpleString = TypeAliasType("SimpleString", str)',
                'UnionType = TypeAliasType("UnionType", Union[str, int])',
            ],
            ["class SimpleString(", "RootModel["],
        ),
        (
            DataModelType.PydanticBaseModel,
            PythonVersion.PY_312,
            [
                "TypeAlias",
                "SimpleString: TypeAlias = str",
            ],
            ["type SimpleString = str", "TypeAliasType("],
        ),
        (
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_312,
            [
                "type SimpleString = str",
                "type UnionType = Union[str, int]",
            ],
            ["TypeAliasType(", "RootModel["],
        ),
        (
            DataModelType.DataclassesDataclass,
            PythonVersion.PY_312,
            [
                "type SimpleString = str",
                "type UnionType = Union[str, int]",
            ],
            ["TypeAliasType(", "class SimpleString("],
        ),
    ],
)
def test_generate_use_type_alias_matrix(
    tmp_path: Path,
    output_model_type: DataModelType,
    target_python_version: PythonVersion,
    expected_snippets: list[str],
    unexpected_snippets: list[str],
) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=json.dumps(SCHEMA),
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=output_model_type,
        target_python_version=target_python_version,
        use_type_alias=True,
        disable_timestamp=True,
    )

    result = output_file.read_text(encoding="utf-8")
    for snippet in expected_snippets:
        assert snippet in result
    for snippet in unexpected_snippets:
        assert snippet not in result


def test_main_cli_use_type_alias(tmp_path: Path) -> None:
    input_file = tmp_path / "schema.json"
    output_file = tmp_path / "output.py"
    input_file.write_text(json.dumps(SCHEMA), encoding="utf-8")

    return_code = main(
        [
            "--input",
            str(input_file),
            "--output",
            str(output_file),
            "--input-file-type",
            "jsonschema",
            "--use-type-alias",
        ]
    )

    assert return_code == Exit.OK
    result = output_file.read_text(encoding="utf-8")
    assert "from typing_extensions import TypeAlias" in result
    assert "class SimpleString(" not in result
