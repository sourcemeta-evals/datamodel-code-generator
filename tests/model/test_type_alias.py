from __future__ import annotations

import pytest

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.model import DataModelFieldBase, get_data_model_types
from datamodel_code_generator.model.type_alias import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_TYPE,
    IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,
    TypeAliasModel,
)
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType
from datamodel_code_generator import DataModelType


class TestTypeAliasModel:
    """Tests for TypeAliasModel class."""

    def test_type_alias_model_python_312(self) -> None:
        """Test that Python 3.12+ uses native type statement."""
        model = TypeAliasModel(
            reference=Reference(name="TestAlias", path="test_alias"),
            fields=[
                DataModelFieldBase(
                    name="root",
                    data_type=DataType(type="str"),
                    required=True,
                )
            ],
            python_version=PythonVersion.PY_312,
            use_pydantic_v2=True,
        )

        assert model.use_type_statement is True
        assert model.use_type_alias_type is False
        assert model.use_type_alias_annotation is False
        assert "type TestAlias = str" in model.render()

    def test_type_alias_model_python_39_pydantic_v2(self) -> None:
        """Test that Python 3.9 with Pydantic v2 uses TypeAliasType."""
        model = TypeAliasModel(
            reference=Reference(name="TestAlias", path="test_alias"),
            fields=[
                DataModelFieldBase(
                    name="root",
                    data_type=DataType(type="str"),
                    required=True,
                )
            ],
            python_version=PythonVersion.PY_39,
            use_pydantic_v2=True,
        )

        assert model.use_type_statement is False
        assert model.use_type_alias_type is True
        assert model.use_type_alias_annotation is False
        assert 'TypeAliasType("TestAlias", str)' in model.render()
        assert IMPORT_TYPE_ALIAS_TYPE in model.imports

    def test_type_alias_model_python_39_pydantic_v1(self) -> None:
        """Test that Python 3.9 with Pydantic v1 uses TypeAlias annotation."""
        model = TypeAliasModel(
            reference=Reference(name="TestAlias", path="test_alias"),
            fields=[
                DataModelFieldBase(
                    name="root",
                    data_type=DataType(type="str"),
                    required=True,
                )
            ],
            python_version=PythonVersion.PY_39,
            use_pydantic_v2=False,
        )

        assert model.use_type_statement is False
        assert model.use_type_alias_type is False
        assert model.use_type_alias_annotation is True
        assert "TestAlias: TypeAlias = str" in model.render()
        assert IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS in model.imports

    def test_type_alias_model_python_310_pydantic_v1(self) -> None:
        """Test that Python 3.10 with Pydantic v1 uses TypeAlias from typing."""
        model = TypeAliasModel(
            reference=Reference(name="TestAlias", path="test_alias"),
            fields=[
                DataModelFieldBase(
                    name="root",
                    data_type=DataType(type="str"),
                    required=True,
                )
            ],
            python_version=PythonVersion.PY_310,
            use_pydantic_v2=False,
        )

        assert model.use_type_statement is False
        assert model.use_type_alias_type is False
        assert model.use_type_alias_annotation is True
        assert "TestAlias: TypeAlias = str" in model.render()
        assert IMPORT_TYPE_ALIAS in model.imports

    def test_type_alias_model_no_base_class(self) -> None:
        """Test that TypeAliasModel has no base class."""
        model = TypeAliasModel(
            reference=Reference(name="TestAlias", path="test_alias"),
            fields=[
                DataModelFieldBase(
                    name="root",
                    data_type=DataType(type="str"),
                    required=True,
                )
            ],
            python_version=PythonVersion.PY_312,
            use_pydantic_v2=True,
        )

        assert model.base_classes == []
        assert model.BASE_CLASS == ""


class TestGetDataModelTypesWithTypeAlias:
    """Tests for get_data_model_types with use_type_alias flag."""

    def test_pydantic_v2_with_type_alias(self) -> None:
        """Test that Pydantic v2 with use_type_alias returns TypeAliasModel."""
        data_model_types = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_312,
            use_type_alias=True,
        )

        # The root_model should be a TypeAliasModel subclass
        model = data_model_types.root_model(
            reference=Reference(name="Test", path="test"),
            fields=[DataModelFieldBase(name="root", data_type=DataType(type="str"))],
        )
        assert model.use_type_statement is True

    def test_pydantic_v1_with_type_alias(self) -> None:
        """Test that Pydantic v1 with use_type_alias returns TypeAliasModel."""
        data_model_types = get_data_model_types(
            DataModelType.PydanticBaseModel,
            PythonVersion.PY_39,
            use_type_alias=True,
        )

        model = data_model_types.root_model(
            reference=Reference(name="Test", path="test"),
            fields=[DataModelFieldBase(name="root", data_type=DataType(type="str"))],
        )
        assert model.use_type_alias_annotation is True

    def test_dataclass_with_type_alias(self) -> None:
        """Test that dataclass with use_type_alias returns TypeAliasModel."""
        data_model_types = get_data_model_types(
            DataModelType.DataclassesDataclass,
            PythonVersion.PY_312,
            use_type_alias=True,
        )

        model = data_model_types.root_model(
            reference=Reference(name="Test", path="test"),
            fields=[DataModelFieldBase(name="root", data_type=DataType(type="str"))],
        )
        assert model.use_type_statement is True

    def test_typed_dict_with_type_alias(self) -> None:
        """Test that TypedDict with use_type_alias returns TypeAliasModel."""
        data_model_types = get_data_model_types(
            DataModelType.TypingTypedDict,
            PythonVersion.PY_312,
            use_type_alias=True,
        )

        model = data_model_types.root_model(
            reference=Reference(name="Test", path="test"),
            fields=[DataModelFieldBase(name="root", data_type=DataType(type="str"))],
        )
        assert model.use_type_statement is True

    def test_without_type_alias_returns_original_root_model(self) -> None:
        """Test that without use_type_alias, original root model is returned."""
        from datamodel_code_generator.model.pydantic_v2.root_model import RootModel

        data_model_types = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_312,
            use_type_alias=False,
        )

        assert data_model_types.root_model is RootModel
