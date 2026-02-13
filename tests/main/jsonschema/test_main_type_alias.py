from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest
from freezegun import freeze_time

from datamodel_code_generator import DataModelType, InputFileType, generate
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
def test_use_type_alias_pydantic_v1_py39(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--use-type-alias",
        "--target-python-version",
        "3.9",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_py39.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v1_py310(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--use-type-alias",
        "--target-python-version",
        "3.10",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_py310.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v1_py312(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--use-type-alias",
        "--target-python-version",
        "3.12",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_py312.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v2_py310(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--use-type-alias",
        "--target-python-version",
        "3.10",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v2_py310.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_pydantic_v2_py312(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--use-type-alias",
        "--target-python-version",
        "3.12",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_pydantic_v2_py312.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_annotated_py39(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--use-type-alias",
        "--use-annotated",
        "--target-python-version",
        "3.9",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_annotated_py39.py").read_text()
    )


@freeze_time("2019-07-26")
def test_use_type_alias_annotated_pydantic_v2_py312(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--use-type-alias",
        "--use-annotated",
        "--target-python-version",
        "3.12",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--disable-timestamp",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_JSON_SCHEMA_PATH / "type_alias_annotated_pydantic_v2_py312.py").read_text()
    )


def test_use_type_alias_generate_api(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        use_type_alias=True,
        target_python_version=PythonVersion.PY_39,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "TypeAlias" in result
    assert "class " not in result
    assert "SimpleString: TypeAlias = str" in result


def test_use_type_alias_generate_api_pydantic_v2(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        use_type_alias=True,
        target_python_version=PythonVersion.PY_310,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "TypeAliasType" in result
    assert "class " not in result
    assert "SimpleString = TypeAliasType('SimpleString', str)" in result


def test_use_type_alias_generate_api_type_statement(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    generate(
        input_=JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        use_type_alias=True,
        target_python_version=PythonVersion.PY_312,
        disable_timestamp=True,
    )
    result = output_file.read_text()
    assert "type SimpleString = str" in result
    assert "class " not in result
    assert "TypeAlias" not in result
