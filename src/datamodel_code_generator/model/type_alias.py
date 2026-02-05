from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.imports import Import
from datamodel_code_generator.model.base import DataModel
from datamodel_code_generator.types import chain_as_tuple

if TYPE_CHECKING:
    from collections.abc import Iterator

    from datamodel_code_generator.reference import Reference


class TypeAliasStyle:
    """Enum-like class for type alias styles."""

    TYPE_STATEMENT = "type_statement"  # Python 3.12+ native `type X = ...`
    TYPE_ALIAS_TYPE = "type_alias_type"  # TypeAliasType for Pydantic v2 + Python 3.9-3.11
    TYPE_ALIAS_ANNOTATION = "type_alias_annotation"  # TypeAlias annotation for Pydantic v1


IMPORT_TYPE_ALIAS = Import(from_="typing", import_="TypeAlias")
IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS = Import(from_="typing_extensions", import_="TypeAlias")
IMPORT_TYPE_ALIAS_TYPE = Import(from_="typing_extensions", import_="TypeAliasType")


def get_type_alias_style(
    python_version: PythonVersion,
    is_pydantic_v2: bool,
) -> str:
    """Determine the appropriate type alias style based on Python version and Pydantic version."""
    is_py_312_or_later = python_version.value not in {
        PythonVersion.PY_39.value,
        PythonVersion.PY_310.value,
        PythonVersion.PY_311.value,
    }

    if is_py_312_or_later:
        return TypeAliasStyle.TYPE_STATEMENT
    if is_pydantic_v2:
        return TypeAliasStyle.TYPE_ALIAS_TYPE
    return TypeAliasStyle.TYPE_ALIAS_ANNOTATION


def get_type_alias_import(
    python_version: PythonVersion,
    is_pydantic_v2: bool,
) -> Import | None:
    """Get the appropriate import for the type alias style."""
    style = get_type_alias_style(python_version, is_pydantic_v2)

    if style == TypeAliasStyle.TYPE_STATEMENT:
        return None
    if style == TypeAliasStyle.TYPE_ALIAS_TYPE:
        return IMPORT_TYPE_ALIAS_TYPE
    # TypeAlias annotation - use typing_extensions for Python 3.9
    if python_version == PythonVersion.PY_39:
        return IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS
    return IMPORT_TYPE_ALIAS


class TypeAliasBase(DataModel):
    """Base class for TypeAlias models. Used for isinstance() checks."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""

    def set_base_class(self) -> None:
        self.base_classes = []


class TypeAlias(TypeAliasBase):
    """Model class for generating type aliases instead of RootModel classes.

    This class generates TypeAlias annotation style (e.g., `X: TypeAlias = str`).
    Used for Pydantic v1 and non-Pydantic output types with Python < 3.12.
    """

    _type_alias_style: ClassVar[str] = TypeAliasStyle.TYPE_ALIAS_ANNOTATION
    _python_version: ClassVar[PythonVersion] = PythonVersion.PY_39
    _is_pydantic_v2: ClassVar[bool] = False

    def __init__(
        self,
        *,
        reference: Reference,
        **kwargs: Any,
    ) -> None:
        # Remove base_classes since type aliases don't have base classes
        kwargs.pop("base_classes", None)
        kwargs.pop("custom_base_class", None)

        super().__init__(reference=reference, **kwargs)

    @property
    def imports(self) -> tuple[Import, ...]:
        type_alias_import = get_type_alias_import(self._python_version, self._is_pydantic_v2)
        additional: Iterator[Import] = iter(())
        if type_alias_import:
            additional = iter((type_alias_import,))
        return chain_as_tuple(
            (i for f in self.fields for i in f.imports),
            self._additional_imports,
            additional,
        )

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            type_alias_style=self._type_alias_style,
            description=self.description,
            **self.extra_template_data,
        )


def create_type_alias_class(
    python_version: PythonVersion,
    is_pydantic_v2: bool,
) -> type[TypeAlias]:
    """Create a TypeAlias class configured for the given Python and Pydantic versions."""
    style = get_type_alias_style(python_version, is_pydantic_v2)

    class ConfiguredTypeAlias(TypeAlias):
        _type_alias_style: ClassVar[str] = style
        _python_version: ClassVar[PythonVersion] = python_version
        _is_pydantic_v2: ClassVar[bool] = is_pydantic_v2

    return ConfiguredTypeAlias
