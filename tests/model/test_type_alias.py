from __future__ import annotations

from datamodel_code_generator.model import DataModelFieldBase
from datamodel_code_generator.model.type_alias import (
    TypeAliasAnnotation,
    TypeAliasTypeAliasType,
    TypeAliasTypeStatement,
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
    rendered = model.render()
    assert "SimpleString: TypeAlias = str" in rendered
    assert "class " not in rendered


def test_type_alias_annotation_custom_base_class_is_ignored() -> None:
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


def test_type_alias_type_alias_type() -> None:
    model = TypeAliasTypeAliasType(
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
    rendered = model.render()
    assert "SimpleString = TypeAliasType('SimpleString', str)" in rendered
    assert "class " not in rendered


def test_type_alias_type_alias_type_custom_base_class_is_ignored() -> None:
    model = TypeAliasTypeAliasType(
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


def test_type_alias_type_statement() -> None:
    model = TypeAliasTypeStatement(
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
    rendered = model.render()
    assert "type SimpleString = str" in rendered
    assert "class " not in rendered


def test_type_alias_type_statement_custom_base_class_is_ignored() -> None:
    model = TypeAliasTypeStatement(
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
