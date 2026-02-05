from __future__ import annotations

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.model import DataModelFieldBase
from datamodel_code_generator.model.type_alias import TypeAlias
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType


def test_type_alias_py312_native_type_statement() -> None:
    """Test that Python 3.12+ uses native `type` statement."""
    type_alias = TypeAlias(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="UserId", path="user_id"),
        python_version=PythonVersion.PY_312,
        use_pydantic_v2=True,
    )

    assert type_alias.name == "UserId"
    rendered = type_alias.render()
    assert "type UserId = str" in rendered


def test_type_alias_py39_pydantic_v2_type_alias_type() -> None:
    """Test that Python 3.9-3.11 with Pydantic v2 uses TypeAliasType."""
    type_alias = TypeAlias(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="UserId", path="user_id"),
        python_version=PythonVersion.PY_39,
        use_pydantic_v2=True,
    )

    assert type_alias.name == "UserId"
    rendered = type_alias.render()
    assert 'UserId = TypeAliasType("UserId", str)' in rendered


def test_type_alias_py39_pydantic_v1_type_alias_annotation() -> None:
    """Test that Python 3.9-3.11 with Pydantic v1 uses TypeAlias annotation."""
    type_alias = TypeAlias(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="UserId", path="user_id"),
        python_version=PythonVersion.PY_39,
        use_pydantic_v2=False,
    )

    assert type_alias.name == "UserId"
    rendered = type_alias.render()
    assert "UserId: TypeAlias = str" in rendered


def test_type_alias_py310_pydantic_v2_type_alias_type() -> None:
    """Test that Python 3.10 with Pydantic v2 uses TypeAliasType."""
    type_alias = TypeAlias(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="UserId", path="user_id"),
        python_version=PythonVersion.PY_310,
        use_pydantic_v2=True,
    )

    assert type_alias.name == "UserId"
    rendered = type_alias.render()
    assert 'UserId = TypeAliasType("UserId", str)' in rendered


def test_type_alias_py311_pydantic_v2_type_alias_type() -> None:
    """Test that Python 3.11 with Pydantic v2 uses TypeAliasType."""
    type_alias = TypeAlias(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="UserId", path="user_id"),
        python_version=PythonVersion.PY_311,
        use_pydantic_v2=True,
    )

    assert type_alias.name == "UserId"
    rendered = type_alias.render()
    assert 'UserId = TypeAliasType("UserId", str)' in rendered


def test_type_alias_py313_native_type_statement() -> None:
    """Test that Python 3.13+ uses native `type` statement."""
    type_alias = TypeAlias(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="str"),
                required=True,
            )
        ],
        reference=Reference(name="UserId", path="user_id"),
        python_version=PythonVersion.PY_313,
        use_pydantic_v2=True,
    )

    assert type_alias.name == "UserId"
    rendered = type_alias.render()
    assert "type UserId = str" in rendered


def test_type_alias_with_description() -> None:
    """Test that description is rendered as a comment."""
    type_alias = TypeAlias(
        fields=[
            DataModelFieldBase(
                name="root",
                data_type=DataType(type="int"),
                required=True,
            )
        ],
        reference=Reference(name="Total", path="total"),
        python_version=PythonVersion.PY_312,
        use_pydantic_v2=True,
        description="The total count",
    )

    rendered = type_alias.render()
    assert "# The total count" in rendered
    assert "type Total = int" in rendered


def test_type_alias_empty_fields() -> None:
    """Test that empty fields returns empty string."""
    type_alias = TypeAlias(
        fields=[],
        reference=Reference(name="Empty", path="empty"),
        python_version=PythonVersion.PY_312,
        use_pydantic_v2=True,
    )

    rendered = type_alias.render()
    assert rendered == ""
