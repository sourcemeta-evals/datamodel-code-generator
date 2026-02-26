from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest
from freezegun import freeze_time

from datamodel_code_generator import DataModelType, InputFileType, generate
from datamodel_code_generator.__main__ import Exit, main
from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.model.type_alias import (
    TypeAliasAnnotation,
    TypeAliasAnnotationExt,
    TypeAliasTypeModel,
    TypeStatement,
)


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)
    monkeypatch.setattr("datamodel_code_generator.arguments.namespace", namespace_)


DATA_PATH: Path = Path(__file__).parent.parent / "data"
JSON_SCHEMA_DATA_PATH: Path = DATA_PATH / "jsonschema"


# ── get_data_model_types selection tests ─────────────────────────────────


class TestGetDataModelTypesTypeAlias:
    """Test that get_data_model_types selects the correct type alias model."""

    def test_pydantic_v2_py312_returns_type_statement(self) -> None:
        result = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_312,
            use_type_alias=True,
        )
        assert result.root_model is TypeStatement

    def test_pydantic_v2_py313_returns_type_statement(self) -> None:
        result = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_313,
            use_type_alias=True,
        )
        assert result.root_model is TypeStatement

    def test_pydantic_v2_py39_returns_type_alias_type(self) -> None:
        result = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_39,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasTypeModel

    def test_pydantic_v2_py311_returns_type_alias_type(self) -> None:
        result = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_311,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasTypeModel

    def test_pydantic_v1_py39_returns_type_alias_ext(self) -> None:
        result = get_data_model_types(
            DataModelType.PydanticBaseModel,
            PythonVersion.PY_39,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasAnnotationExt

    def test_pydantic_v1_py310_returns_type_alias_ext(self) -> None:
        """Pydantic v1 always uses typing_extensions even on 3.10+."""
        result = get_data_model_types(
            DataModelType.PydanticBaseModel,
            PythonVersion.PY_310,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasAnnotationExt

    def test_pydantic_v1_py312_returns_type_statement(self) -> None:
        result = get_data_model_types(
            DataModelType.PydanticBaseModel,
            PythonVersion.PY_312,
            use_type_alias=True,
        )
        assert result.root_model is TypeStatement

    def test_typed_dict_py310_returns_type_alias_annotation(self) -> None:
        result = get_data_model_types(
            DataModelType.TypingTypedDict,
            PythonVersion.PY_310,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasAnnotation

    def test_typed_dict_py39_returns_type_alias_ext(self) -> None:
        result = get_data_model_types(
            DataModelType.TypingTypedDict,
            PythonVersion.PY_39,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasAnnotationExt

    def test_typed_dict_py312_returns_type_statement(self) -> None:
        result = get_data_model_types(
            DataModelType.TypingTypedDict,
            PythonVersion.PY_312,
            use_type_alias=True,
        )
        assert result.root_model is TypeStatement

    def test_dataclass_py310_returns_type_alias_annotation(self) -> None:
        result = get_data_model_types(
            DataModelType.DataclassesDataclass,
            PythonVersion.PY_310,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasAnnotation

    def test_dataclass_py312_returns_type_statement(self) -> None:
        result = get_data_model_types(
            DataModelType.DataclassesDataclass,
            PythonVersion.PY_312,
            use_type_alias=True,
        )
        assert result.root_model is TypeStatement

    def test_msgspec_py310_returns_type_alias_annotation(self) -> None:
        result = get_data_model_types(
            DataModelType.MsgspecStruct,
            PythonVersion.PY_310,
            use_type_alias=True,
        )
        assert result.root_model is TypeAliasAnnotation

    def test_use_type_alias_false_does_not_change_root_model(self) -> None:
        """When use_type_alias=False, root_model should remain the default."""
        result_default = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_312,
            use_type_alias=False,
        )
        result_no_flag = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_312,
        )
        assert result_default.root_model is result_no_flag.root_model
        assert result_default.root_model is not TypeStatement


# ── generate() integration tests ─────────────────────────────────────────


class TestGenerateTypeAlias:
    """Integration tests using generate() to verify end-to-end output."""

    @freeze_time("2019-07-26")
    def test_pydantic_v2_py312_type_statement(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.py"
        generate(
            JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
            input_file_type=InputFileType.JsonSchema,
            output=output_file,
            output_model_type=DataModelType.PydanticV2BaseModel,
            target_python_version=PythonVersion.PY_312,
            use_type_alias=True,
        )
        result = output_file.read_text()
        assert "type SimpleString = str" in result
        assert "type UnionType = Union[str, int]" in result
        assert "type AnnotatedType =" in result
        assert "class " not in result
        # Should NOT import TypeAlias or TypeAliasType
        assert "TypeAlias" not in result
        assert "TypeAliasType" not in result

    @freeze_time("2019-07-26")
    def test_pydantic_v2_py39_type_alias_type(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.py"
        generate(
            JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
            input_file_type=InputFileType.JsonSchema,
            output=output_file,
            output_model_type=DataModelType.PydanticV2BaseModel,
            target_python_version=PythonVersion.PY_39,
            use_type_alias=True,
        )
        result = output_file.read_text()
        assert 'SimpleString = TypeAliasType("SimpleString", str)' in result
        assert 'UnionType = TypeAliasType("UnionType", Union[str, int])' in result
        assert "from typing_extensions import TypeAliasType" in result
        assert "class " not in result

    @freeze_time("2019-07-26")
    def test_pydantic_v1_py39_type_alias_ext(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.py"
        generate(
            JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
            input_file_type=InputFileType.JsonSchema,
            output=output_file,
            output_model_type=DataModelType.PydanticBaseModel,
            target_python_version=PythonVersion.PY_39,
            use_type_alias=True,
        )
        result = output_file.read_text()
        assert "SimpleString: TypeAlias = str" in result
        assert "UnionType: TypeAlias = Union[str, int]" in result
        assert "from typing_extensions import TypeAlias" in result
        assert "class " not in result

    @freeze_time("2019-07-26")
    def test_pydantic_v1_py310_type_alias_ext(self, tmp_path: Path) -> None:
        """Pydantic v1 uses typing_extensions.TypeAlias even on Python 3.10+."""
        output_file = tmp_path / "output.py"
        generate(
            JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
            input_file_type=InputFileType.JsonSchema,
            output=output_file,
            output_model_type=DataModelType.PydanticBaseModel,
            target_python_version=PythonVersion.PY_310,
            use_type_alias=True,
        )
        result = output_file.read_text()
        assert "SimpleString: TypeAlias = str" in result
        assert "from typing_extensions import TypeAlias" in result
        assert "class " not in result

    @freeze_time("2019-07-26")
    def test_typed_dict_py310_type_alias_typing(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.py"
        generate(
            JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
            input_file_type=InputFileType.JsonSchema,
            output=output_file,
            output_model_type=DataModelType.TypingTypedDict,
            target_python_version=PythonVersion.PY_310,
            use_type_alias=True,
        )
        result = output_file.read_text()
        assert "SimpleString: TypeAlias = str" in result
        assert "from typing import" in result
        assert "TypeAlias" in result
        # Should use typing, not typing_extensions
        assert "typing_extensions" not in result
        assert "class " not in result

    @freeze_time("2019-07-26")
    def test_pydantic_v2_py311_type_alias_type(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.py"
        generate(
            JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
            input_file_type=InputFileType.JsonSchema,
            output=output_file,
            output_model_type=DataModelType.PydanticV2BaseModel,
            target_python_version=PythonVersion.PY_311,
            use_type_alias=True,
        )
        result = output_file.read_text()
        assert 'SimpleString = TypeAliasType("SimpleString", str)' in result
        assert "from typing_extensions import TypeAliasType" in result
        assert "class " not in result

    @freeze_time("2019-07-26")
    def test_without_use_type_alias_generates_root_model(self, tmp_path: Path) -> None:
        """Without --use-type-alias, output should still use RootModel."""
        output_file = tmp_path / "output.py"
        generate(
            JSON_SCHEMA_DATA_PATH / "type_alias_test.json",
            input_file_type=InputFileType.JsonSchema,
            output=output_file,
            output_model_type=DataModelType.PydanticV2BaseModel,
            target_python_version=PythonVersion.PY_312,
            use_type_alias=False,
        )
        result = output_file.read_text()
        assert "class SimpleString" in result
        assert "RootModel" in result


# ── CLI tests ────────────────────────────────────────────────────────────


class TestCLITypeAlias:
    """Test --use-type-alias CLI flag."""

    @freeze_time("2019-07-26")
    def test_cli_use_type_alias_flag(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.py"
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
        ])
        assert return_code == Exit.OK
        result = output_file.read_text()
        assert "type SimpleString = str" in result
        assert "class " not in result

    @freeze_time("2019-07-26")
    def test_cli_use_type_alias_pydantic_v1(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.py"
        return_code: Exit = main([
            "--input",
            str(JSON_SCHEMA_DATA_PATH / "type_alias_test.json"),
            "--output",
            str(output_file),
            "--input-file-type",
            "jsonschema",
            "--output-model-type",
            "pydantic.BaseModel",
            "--target-python-version",
            "3.9",
            "--use-type-alias",
        ])
        assert return_code == Exit.OK
        result = output_file.read_text()
        assert "SimpleString: TypeAlias = str" in result
        assert "from typing_extensions import TypeAlias" in result

    @freeze_time("2019-07-26")
    def test_cli_without_use_type_alias(self, tmp_path: Path) -> None:
        """Without the flag, normal RootModel output."""
        output_file = tmp_path / "output.py"
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
        ])
        assert return_code == Exit.OK
        result = output_file.read_text()
        assert "class SimpleString" in result
