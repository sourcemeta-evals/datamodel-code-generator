from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator.imports import (
    IMPORT_ANNOTATED,
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_BACKPORT,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model import DataModel
from datamodel_code_generator.types import chain_as_tuple


class _BaseRootTypeAlias(DataModel):
    BASE_CLASS: ClassVar[str] = ""
    SYNTAX_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    @property
    def _root_field(self):
        return self.fields[0]

    @property
    def _use_field_metadata_as_annotated(self) -> bool:
        field = self._root_field
        return bool(not field.annotated and field.field and not field.has_default)

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = super().imports
        if self.SYNTAX_IMPORTS:
            imports = chain_as_tuple(imports, self.SYNTAX_IMPORTS)
        if self._use_field_metadata_as_annotated:
            imports = chain_as_tuple(imports, (IMPORT_ANNOTATED,))
        return imports

    @property
    def type_expression(self) -> str:
        field = self._root_field
        if field.annotated:
            return field.annotated
        if self._use_field_metadata_as_annotated:
            return f"Annotated[{field.type_hint}, {field.field}]"
        return field.type_hint

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            type_expression=self.type_expression,
            description=self.description,
            **self.extra_template_data,
        )


class RootTypeAlias(_BaseRootTypeAlias):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    SYNTAX_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)


class RootTypeAliasBackport(_BaseRootTypeAlias):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    SYNTAX_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_BACKPORT,)


class RootTypeAliasType(_BaseRootTypeAlias):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasType.jinja2"
    SYNTAX_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)


class RootNativeTypeAlias(_BaseRootTypeAlias):
    TEMPLATE_FILE_PATH: ClassVar[str] = "NativeTypeAlias.jinja2"
