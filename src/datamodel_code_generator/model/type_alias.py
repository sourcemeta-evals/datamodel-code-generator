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


class TypeAlias(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)
    IS_ALIAS: bool = True
    ALIAS_SYNTAX: ClassVar[str] = "annotation"

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = super().imports
        if self.fields and (self.fields[0].annotated or self.fields[0].field):
            imports = chain_as_tuple(imports, (IMPORT_ANNOTATED,))

        return imports


class TypeAliasBackport(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_BACKPORT,)
    IS_ALIAS: bool = True
    ALIAS_SYNTAX: ClassVar[str] = "annotation"

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = super().imports
        if self.fields and (self.fields[0].annotated or self.fields[0].field):
            imports = chain_as_tuple(imports, (IMPORT_ANNOTATED,))

        return imports


class TypeAliasTypeBackport(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)
    IS_ALIAS: bool = True
    ALIAS_SYNTAX: ClassVar[str] = "alias_type"

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = super().imports
        if self.fields and (self.fields[0].annotated or self.fields[0].field):
            imports = chain_as_tuple(imports, (IMPORT_ANNOTATED,))

        return imports


class TypeStatement(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()
    IS_ALIAS: bool = True
    DEFERS_EVALUATION: bool = True
    ALIAS_SYNTAX: ClassVar[str] = "statement"

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = super().imports
        if self.fields and (self.fields[0].annotated or self.fields[0].field):
            imports = chain_as_tuple(imports, (IMPORT_ANNOTATED,))

        return imports
