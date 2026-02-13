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
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,)

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeAliasAnnotationFromTyping(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeAliasTypeModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasType.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class TypeStatementModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeStatement.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)
