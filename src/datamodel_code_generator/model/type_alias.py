from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS_EXTENSIONS,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model.base import DataModel


class TypeAliasAnnotation(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "type_alias_annotation.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_EXTENSIONS,)

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeAliasTypeModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "type_alias_type.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeStatement(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "type_statement.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)
