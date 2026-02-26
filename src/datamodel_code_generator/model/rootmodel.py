from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_BACKPORT,
    IMPORT_TYPE_ALIAS_TYPE_BACKPORT,
    Import,
)
from datamodel_code_generator.model import DataModel


class RootModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "root.jinja2"


class _TypeAliasRootModelBase(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "root.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()
    USE_ANNOTATED: ClassVar[bool] = True

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = super().imports
        if self.USE_ANNOTATED:
            return imports
        return tuple(i for i in imports if (i.from_, i.import_) not in {("typing", "Annotated"), ("pydantic", "Field")})

    def _alias_value(self) -> str:
        field = self.fields[0]
        if self.USE_ANNOTATED and field.annotated:
            return field.annotated
        return field.type_hint


class TypeAliasRootModel(_TypeAliasRootModelBase):
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)

    def render(self, *, class_name: str | None = None) -> str:
        name = class_name or self.class_name
        return f"{name}: TypeAlias = {self._alias_value()}"


class TypeAliasBackportRootModel(_TypeAliasRootModelBase):
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_BACKPORT,)

    def render(self, *, class_name: str | None = None) -> str:
        name = class_name or self.class_name
        return f"{name}: TypeAlias = {self._alias_value()}"


class PydanticV1TypeAliasRootModel(TypeAliasRootModel):
    USE_ANNOTATED: ClassVar[bool] = False


class PydanticV1TypeAliasBackportRootModel(TypeAliasBackportRootModel):
    USE_ANNOTATED: ClassVar[bool] = False


class NativeTypeAliasRootModel(_TypeAliasRootModelBase):
    def render(self, *, class_name: str | None = None) -> str:
        name = class_name or self.class_name
        return f"type {name} = {self._alias_value()}"


class TypeAliasTypeRootModel(_TypeAliasRootModelBase):
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE_BACKPORT,)

    def render(self, *, class_name: str | None = None) -> str:
        name = class_name or self.class_name
        return f"{name} = TypeAliasType({name!r}, {self._alias_value()})"
