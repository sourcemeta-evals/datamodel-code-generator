from __future__ import annotations

from datamodel_code_generator.model.pydantic_v2 import DataModelField
from datamodel_code_generator.model.pydantic_v2.type_alias_model import TypeAliasModel
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType


def test_type_alias_model() -> None:
    """Test that TypeAliasModel generates type aliases instead of RootModel classes."""
    type_alias_model = TypeAliasModel(
        fields=[
            DataModelField(
                name="root",
                data_type=DataType(type="int"),
                required=True,
                use_annotated=True,
                extras={"title": "Total"},
            )
        ],
        reference=Reference(name="Total", path="total"),
    )

    assert type_alias_model.name == "Total"
    assert type_alias_model.base_class == ""
    rendered = type_alias_model.render()
    assert "Total = Annotated[int, Field(" in rendered
    assert "title='Total'" in rendered


def test_type_alias_model_without_annotated() -> None:
    """Test TypeAliasModel without use_annotated generates simple type alias."""
    type_alias_model = TypeAliasModel(
        fields=[
            DataModelField(
                name="root",
                data_type=DataType(type="str"),
                required=True,
                use_annotated=False,
            )
        ],
        reference=Reference(name="Name", path="name"),
    )

    assert type_alias_model.name == "Name"
    rendered = type_alias_model.render()
    assert rendered.strip() == "Name = str"
