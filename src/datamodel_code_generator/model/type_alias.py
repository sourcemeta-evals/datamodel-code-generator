from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_TYPE,
    IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,
    Import,
)
from datamodel_code_generator.model import DataModel


class TypeAliasModel(DataModel):
    """Generates: MyType: TypeAlias = str

    Used for Pydantic v1 (all Python versions) and non-Pydantic output types
    on Python 3.9-3.11.
    For Python 3.9, TypeAlias is imported from typing_extensions.
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,)


class TypeAliasTypeModel(DataModel):
    """Generates: MyType = TypeAliasType('MyType', str)

    Used for Pydantic v2 on Python 3.9-3.11 where TypeAliasType from
    typing_extensions is needed for runtime compatibility with Pydantic.
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasType.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)


class TypeStatementModel(DataModel):
    """Generates: type MyType = str

    Used on Python 3.12+ (all output types) using the native type statement.
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeStatement.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()
