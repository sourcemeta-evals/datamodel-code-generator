from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest
from freezegun import freeze_time

from datamodel_code_generator import (
    DataModelType,
    InputFileType,
    generate,
)
from datamodel_code_generator.__main__ import Exit, main
from datamodel_code_generator.format import PythonVersion
from tests.main.test_main_general import DATA_PATH, EXPECTED_MAIN_PATH

JSON_SCHEMA_DATA_PATH: Path = DATA_PATH / "jsonschema"
EXPECTED_JSON_SCHEMA_PATH: Path = EXPECTED_MAIN_PATH / "jsonschema"


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)
    monkeypatch.setattr("datamodel_code_generator.arguments.namespace", namespace_)


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v2_py39(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v2_py39.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v2_py312(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v2_py312.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v1_py39(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v1_py39.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v1_py310(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_310,
        use_type_alias=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v1_py310.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v1_py312(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v1_py312.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v2_py39_annotated(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        use_annotated=True,
        field_constraints=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v2_py39_annotated.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_dataclass_py39(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.DataclassesDataclass,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_dataclass_py39.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_dataclass_py312(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.DataclassesDataclass,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
        disable_timestamp=True,
    )
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_dataclass_py312.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_cli(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.12",
        "--use-type-alias",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text()
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v2_py312.py").read_text()
    )
