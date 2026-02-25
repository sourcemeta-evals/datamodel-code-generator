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
    """Type alias using `X: TypeAlias = Y` with TypeAlias from typing (Python 3.10-3.11)."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)


class TypeAliasModelPy39(DataModel):
    """Type alias using `X: TypeAlias = Y` with TypeAlias from typing_extensions (Python 3.9)."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,)


class TypeAliasTypeModel(DataModel):
    """Type alias using `X = TypeAliasType('X', Y)` (Pydantic v2, Python 3.9-3.11)."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasType.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)


class TypeStatementModel(DataModel):
    """Type alias using `type X = Y` (Python 3.12+)."""

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeStatement.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()
