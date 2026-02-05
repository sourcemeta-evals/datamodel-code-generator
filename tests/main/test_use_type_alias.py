from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest
from freezegun import freeze_time

from datamodel_code_generator import DataModelType, InputFileType, generate
from datamodel_code_generator.__main__ import Exit, main
from datamodel_code_generator.format import PythonVersion

DATA_PATH: Path = Path(__file__).parent.parent / "data"
EXPECTED_MAIN_PATH = DATA_PATH / "expected" / "main" / "use_type_alias"

TIMESTAMP = "1985-10-26T01:21:00-07:00"


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)
    monkeypatch.setattr("datamodel_code_generator.arguments.namespace", namespace_)


@freeze_time(TIMESTAMP)
def test_use_type_alias_py312_pydantic_v2(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        DATA_PATH / "jsonschema" / "simple_type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_312,
        use_type_alias=True,
    )
    assert output_file.read_text() == (EXPECTED_MAIN_PATH / "py312_pydantic_v2.py").read_text()


@freeze_time(TIMESTAMP)
def test_use_type_alias_py310_pydantic_v2(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        DATA_PATH / "jsonschema" / "simple_type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_310,
        use_type_alias=True,
    )
    assert output_file.read_text() == (EXPECTED_MAIN_PATH / "py310_pydantic_v2.py").read_text()


@freeze_time(TIMESTAMP)
def test_use_type_alias_py39_pydantic_v2(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        DATA_PATH / "jsonschema" / "simple_type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
    )
    assert output_file.read_text() == (EXPECTED_MAIN_PATH / "py39_pydantic_v2.py").read_text()


@freeze_time(TIMESTAMP)
def test_use_type_alias_py39_pydantic_v1(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        DATA_PATH / "jsonschema" / "simple_type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_39,
        use_type_alias=True,
    )
    assert output_file.read_text() == (EXPECTED_MAIN_PATH / "py39_pydantic_v1.py").read_text()


@freeze_time(TIMESTAMP)
def test_use_type_alias_command_line(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(DATA_PATH / "jsonschema" / "simple_type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.12",
        "--use-type-alias",
    ])
    assert return_code == Exit.OK
    assert output_file.read_text(encoding="utf-8") == (EXPECTED_MAIN_PATH / "py312_pydantic_v2.py").read_text()
