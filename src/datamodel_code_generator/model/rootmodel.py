from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_ANNOTATED,
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_BACKPORT,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model import DataModel
from datamodel_code_generator.types import chain_as_tuple


class RootModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "root.jinja2"


class TypeAliasRootModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasRoot.jinja2"
    TYPE_ALIAS_IMPORT: ClassVar[Import | None] = IMPORT_TYPE_ALIAS
    USE_NATIVE_TYPE_STATEMENT: ClassVar[bool] = False
    USE_TYPE_ALIAS_TYPE: ClassVar[bool] = False

    def __init__(self, **kwargs: Any) -> None:
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)

    @property
    def imports(self) -> tuple[Import, ...]:
        extra_imports: list[Import] = []
        if self.TYPE_ALIAS_IMPORT is not None:
            extra_imports.append(self.TYPE_ALIAS_IMPORT)
        if self.fields:
            field = self.fields[0]
            field_definition = field.field
            if field_definition and field_definition.startswith("Field(") and not field.annotated:
                extra_imports.append(IMPORT_ANNOTATED)
        return chain_as_tuple(super().imports, extra_imports)

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            description=self.description,
            use_native_type_statement=self.USE_NATIVE_TYPE_STATEMENT,
            use_type_alias_type=self.USE_TYPE_ALIAS_TYPE,
        )


class TypeAliasRootModelBackport(TypeAliasRootModel):
    TYPE_ALIAS_IMPORT: ClassVar[Import | None] = IMPORT_TYPE_ALIAS_BACKPORT


class NativeTypeAliasRootModel(TypeAliasRootModel):
    TYPE_ALIAS_IMPORT: ClassVar[Import | None] = None
    USE_NATIVE_TYPE_STATEMENT: ClassVar[bool] = True


class TypeAliasTypeRootModel(TypeAliasRootModel):
    TYPE_ALIAS_IMPORT: ClassVar[Import | None] = IMPORT_TYPE_ALIAS_TYPE
    USE_TYPE_ALIAS_TYPE: ClassVar[bool] = True
