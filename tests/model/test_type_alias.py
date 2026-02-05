from __future__ import annotations

from datamodel_code_generator.model import DataModelFieldBase
from datamodel_code_generator.model.type_alias import (
    TypeAliasAnnotation,
    TypeAliasAnnotationTypingExtensions,
    TypeAliasStatement,
    TypeAliasTypeModel,
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
    assert model.custom_base_class is None
    rendered = model.render()
    assert "SimpleString: TypeAlias = str" in rendered


def test_type_alias_annotation_typing_extensions() -> None:
    model = TypeAliasAnnotationTypingExtensions(
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


def test_type_alias_statement() -> None:
    model = TypeAliasStatement(
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
    assert "SimpleString = TypeAliasType('SimpleString', str)" in rendered


def test_type_alias_custom_base_class_ignored() -> None:
    model = TypeAliasAnnotation(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
        custom_base_class="some.CustomBase",
    )
    assert model.custom_base_class is None


def test_type_alias_statement_custom_base_class_ignored() -> None:
    model = TypeAliasStatement(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
        custom_base_class="some.CustomBase",
    )
    assert model.custom_base_class is None


def test_type_alias_type_model_custom_base_class_ignored() -> None:
    model = TypeAliasTypeModel(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="SimpleString", path="simple_string"),
        custom_base_class="some.CustomBase",
    )
    assert model.custom_base_class is None
