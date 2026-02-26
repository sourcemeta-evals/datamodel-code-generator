from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_TYPE,
    IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,
    Import,
)
from datamodel_code_generator.model import DataModel


class TypeAliasAnnotation(DataModel):
    """Uses `Name: TypeAlias = type_hint` with import from typing (Python 3.10+)."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)

    def __init__(self, **kwargs: Any) -> None:
        # Type aliases don't have a custom base class
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeAliasAnnotationExt(DataModel):
    """Uses `Name: TypeAlias = type_hint` with import from typing_extensions (Python 3.9)."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,)

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeAliasTypeModel(DataModel):
    """Uses `Name = TypeAliasType("Name", type_hint)` for Pydantic v2 + Python 3.9-3.11."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasType.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeStatement(DataModel):
    """Uses `type Name = type_hint` for Python 3.12+."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeStatement.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)
