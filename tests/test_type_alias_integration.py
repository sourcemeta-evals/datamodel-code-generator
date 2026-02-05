from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest

from datamodel_code_generator import DataModelType, InputFileType, PythonVersion, generate
from datamodel_code_generator.__main__ import Exit, main


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)


SCHEMA = json.dumps({
    "definitions": {
        "SimpleString": {"type": "string"},
        "UnionType": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        "AnnotatedType": {
            "title": "MyAnnotatedType",
            "description": "An annotated union type",
            "anyOf": [{"type": "string"}, {"type": "boolean"}],
        },
    }
})


def test_use_type_alias_pydantic_v2_py312(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "type SimpleString = str" in result
    assert "type UnionType = " in result
    assert "RootModel" not in result
    assert "TypeAlias" not in result
    assert "TypeAliasType" not in result


def test_use_type_alias_pydantic_v2_py39(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "TypeAliasType" in result
    assert "SimpleString = TypeAliasType(" in result
    assert "UnionType = TypeAliasType(" in result
    assert "RootModel" not in result
    assert "type SimpleString" not in result


def test_use_type_alias_pydantic_v2_py310(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_310,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "TypeAliasType" in result
    assert "SimpleString = TypeAliasType(" in result
    assert "RootModel" not in result


def test_use_type_alias_pydantic_v1_py39(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "from typing_extensions import TypeAlias" in result
    assert "SimpleString: TypeAlias = str" in result
    assert "UnionType: TypeAlias = " in result
    assert "RootModel" not in result
    assert "TypeAliasType" not in result
    assert "type SimpleString" not in result


def test_use_type_alias_pydantic_v1_py310(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_310,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "from typing_extensions import TypeAlias" in result
    assert "SimpleString: TypeAlias = str" in result
    assert "RootModel" not in result


def test_use_type_alias_pydantic_v1_py312(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "type SimpleString = str" in result
    assert "RootModel" not in result


def test_use_type_alias_dataclass_py39(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.DataclassesDataclass,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "from typing_extensions import TypeAlias" in result
    assert "SimpleString: TypeAlias = str" in result
    assert "RootModel" not in result


def test_use_type_alias_dataclass_py312(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.DataclassesDataclass,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "type SimpleString = str" in result
    assert "RootModel" not in result


def test_use_type_alias_typed_dict_py39(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.TypingTypedDict,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "from typing_extensions import TypeAlias" in result
    assert "SimpleString: TypeAlias = str" in result
    assert "RootModel" not in result


def test_use_type_alias_typed_dict_py312(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.TypingTypedDict,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "type SimpleString = str" in result
    assert "RootModel" not in result


def test_use_type_alias_dataclass_py310(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.DataclassesDataclass,
        target_python_version=PythonVersion.PY_310,
        use_type_alias=True,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "TypeAlias" in result
    assert "SimpleString: TypeAlias = str" in result
    assert "RootModel" not in result


def test_use_type_alias_cli_flag(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(Path("tests/data/jsonschema/type_alias_test.json")),
        "--input-file-type",
        "jsonschema",
        "--output",
        str(output_file),
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.12",
        "--use-type-alias",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    result = output_file.read_text()
    assert "type SimpleString = str" in result
    assert "RootModel" not in result


def test_without_use_type_alias_generates_root_model(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=False,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "RootModel" in result
    assert "type SimpleString" not in result
    assert "TypeAlias" not in result
