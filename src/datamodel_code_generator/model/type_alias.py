from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_TYPE,
    IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,
    Import,
)
from datamodel_code_generator.model import DataModel


class _BaseTypeAliasModel(DataModel):
    BASE_CLASS: ClassVar[str] = ""

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeAliasAnnotationModel(_BaseTypeAliasModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasAnnotation.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)


class TypeAliasAnnotationExtModel(_BaseTypeAliasModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasAnnotation.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,)


class TypeAliasTypeModel(_BaseTypeAliasModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasType.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)


class TypeStatementModel(_BaseTypeAliasModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeStatement.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()
