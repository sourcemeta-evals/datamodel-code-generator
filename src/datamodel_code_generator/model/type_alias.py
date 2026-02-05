from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.imports import Import
from datamodel_code_generator.model.base import DataModel
from datamodel_code_generator.types import chain_as_tuple

if TYPE_CHECKING:
    from datamodel_code_generator.format import PythonVersion


class TypeAliasStyle:
    """Enum-like class for type alias generation styles."""

    TYPE_STATEMENT = "type_statement"  # Python 3.12+ native `type` statement
    TYPE_ALIAS_TYPE = "type_alias_type"  # TypeAliasType from typing_extensions (Pydantic v2)
    TYPE_ALIAS_ANNOTATION = "type_alias_annotation"  # TypeAlias annotation (Pydantic v1)


def get_type_alias_style(
    python_version: PythonVersion,
    is_pydantic_v2: bool,
) -> str:
    """Determine the appropriate type alias style based on Python version and Pydantic version."""
    if python_version.has_type_statement:
        return TypeAliasStyle.TYPE_STATEMENT
    if is_pydantic_v2:
        return TypeAliasStyle.TYPE_ALIAS_TYPE
    return TypeAliasStyle.TYPE_ALIAS_ANNOTATION


# Import for TypeAliasType from typing_extensions (Python 3.9-3.11 with Pydantic v2)
IMPORT_TYPE_ALIAS_TYPE = Import(from_="typing_extensions", import_="TypeAliasType")

# Import for TypeAlias from typing_extensions (Python 3.9)
IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS = Import(from_="typing_extensions", import_="TypeAlias")

# Import for TypeAlias from typing (Python 3.10+)
IMPORT_TYPE_ALIAS_TYPING = Import(from_="typing", import_="TypeAlias")


class TypeAlias(DataModel):
    """Model class for generating type aliases instead of RootModel classes."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""

    def __init__(
        self,
        *,
        type_alias_style: str = TypeAliasStyle.TYPE_STATEMENT,
        python_version: PythonVersion | None = None,
        **kwargs: Any,
    ) -> None:
        # Remove base_classes and custom_base_class as type aliases don't have base classes
        kwargs.pop("base_classes", None)
        kwargs.pop("custom_base_class", None)

        super().__init__(**kwargs)

        self.type_alias_style = type_alias_style
        self._python_version = python_version

        # Clear base classes since type aliases don't inherit
        self.base_classes = []

    @property
    def imports(self) -> tuple[Import, ...]:
        """Return imports needed for the type alias."""
        base_imports = list(super().imports)

        # Add style-specific imports
        if self.type_alias_style == TypeAliasStyle.TYPE_ALIAS_TYPE:
            base_imports.append(IMPORT_TYPE_ALIAS_TYPE)
        elif self.type_alias_style == TypeAliasStyle.TYPE_ALIAS_ANNOTATION:
            # For Python 3.9, TypeAlias must come from typing_extensions
            # For Python 3.10+, it can come from typing
            if self._python_version is not None and self._python_version.value == "3.9":
                base_imports.append(IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS)
            else:
                base_imports.append(IMPORT_TYPE_ALIAS_TYPING)

        return chain_as_tuple(base_imports)

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            type_alias_style=self.type_alias_style,
            description=self.description,
            **self.extra_template_data,
        )
