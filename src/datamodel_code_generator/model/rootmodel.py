from __future__ import annotations

from enum import Enum
from typing import Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_EXTENSIONS,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model import DataModel
from datamodel_code_generator.types import chain_as_tuple


class RootModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "root.jinja2"


class TypeAliasKind(Enum):
    TYPE_ALIAS = "type_alias"
    TYPE_ALIAS_TYPE = "type_alias_type"
    TYPE_STATEMENT = "type_statement"


class TypeAliasRootModel(RootModel):
    def __init__(
        self,
        *args: Any,
        type_alias_kind: TypeAliasKind,
        use_typing_extensions_type_alias: bool = False,
        **kwargs: Any,
    ) -> None:
        self.type_alias_kind = type_alias_kind
        self.use_typing_extensions_type_alias = use_typing_extensions_type_alias
        super().__init__(*args, **kwargs)

    @property
    def imports(self) -> tuple[Import, ...]:
        extra_imports: tuple[Import, ...] = ()
        if self.type_alias_kind is TypeAliasKind.TYPE_ALIAS:
            extra_imports = (
                (IMPORT_TYPE_ALIAS_EXTENSIONS,)
                if self.use_typing_extensions_type_alias
                else (IMPORT_TYPE_ALIAS,)
            )
        elif self.type_alias_kind is TypeAliasKind.TYPE_ALIAS_TYPE:
            extra_imports = (IMPORT_TYPE_ALIAS_TYPE,)
        return chain_as_tuple(super().imports, extra_imports)

    def render(self, *, class_name: str | None = None) -> str:
        alias_name = class_name or self.class_name
        if not self.fields:
            type_hint = "None"
        else:
            field = self.fields[0]
            type_hint = field.annotated or field.type_hint

        if self.type_alias_kind is TypeAliasKind.TYPE_STATEMENT:
            line = f"type {alias_name} = {type_hint}"
        elif self.type_alias_kind is TypeAliasKind.TYPE_ALIAS_TYPE:
            line = f'{alias_name} = TypeAliasType("{alias_name}", {type_hint})'
        else:
            line = f"{alias_name}: TypeAlias = {type_hint}"

        if self.description:
            return f'{line}\n"""\n{self.description}\n"""'
        return line
