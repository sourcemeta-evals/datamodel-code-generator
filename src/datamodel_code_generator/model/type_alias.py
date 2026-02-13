from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS_BACKPORT,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model.base import DataModel


class TypeAliasAnnotation(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasAnnotation.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_BACKPORT,)

    def __init__(self, **kwargs: Any) -> None:
        if "custom_base_class" in kwargs:
            kwargs.pop("custom_base_class")
        super().__init__(**kwargs)


class TypeAliasTypeAliasType(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasTypeAliasType.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)

    def __init__(self, **kwargs: Any) -> None:
        if "custom_base_class" in kwargs:
            kwargs.pop("custom_base_class")
        super().__init__(**kwargs)


class TypeAliasTypeStatement(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasTypeStatement.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    def __init__(self, **kwargs: Any) -> None:
        if "custom_base_class" in kwargs:
            kwargs.pop("custom_base_class")
        super().__init__(**kwargs)
