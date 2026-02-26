from __future__ import annotations

from datamodel_code_generator.model import DataModelFieldBase
from datamodel_code_generator.model.type_alias import (
    TypeAliasAnnotation,
    TypeAliasAnnotationExt,
    TypeAliasTypeModel,
    TypeStatement,
)
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType


def test_type_alias_annotation() -> None:
    model = TypeAliasAnnotation(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.name == "SimpleString"
    assert model.base_class == ""
    rendered = model.render()
    assert "SimpleString: TypeAlias = str" in rendered
    assert "class " not in rendered


def test_type_alias_annotation_ext() -> None:
    model = TypeAliasAnnotationExt(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.name == "SimpleString"
    assert model.base_class == ""
    rendered = model.render()
    assert "SimpleString: TypeAlias = str" in rendered
    assert "class " not in rendered


def test_type_alias_type_model() -> None:
    model = TypeAliasTypeModel(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.name == "SimpleString"
    assert model.base_class == ""
    rendered = model.render()
    assert 'SimpleString = TypeAliasType("SimpleString", str)' in rendered
    assert "class " not in rendered


def test_type_statement() -> None:
    model = TypeStatement(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.name == "SimpleString"
    assert model.base_class == ""
    rendered = model.render()
    assert "type SimpleString = str" in rendered
    assert "class " not in rendered


def test_type_alias_annotation_custom_base_class_ignored() -> None:
    """custom_base_class is silently ignored for type aliases."""
    model = TypeAliasAnnotation(
        custom_base_class="test.Test",
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.custom_base_class is None
    assert model.base_class == ""


def test_type_alias_annotation_ext_custom_base_class_ignored() -> None:
    model = TypeAliasAnnotationExt(
        custom_base_class="test.Test",
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.custom_base_class is None


def test_type_alias_type_model_custom_base_class_ignored() -> None:
    model = TypeAliasTypeModel(
        custom_base_class="test.Test",
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.custom_base_class is None


def test_type_statement_custom_base_class_ignored() -> None:
    model = TypeStatement(
        custom_base_class="test.Test",
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
    )
    assert model.custom_base_class is None
