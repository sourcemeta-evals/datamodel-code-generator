from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_BACKPORT,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model import DataModel
from datamodel_code_generator.types import chain_as_tuple

if TYPE_CHECKING:
    from datamodel_code_generator.model.base import DataModelFieldBase


_TARGET_PYTHON_VERSION_EXTRA = "__target_python_version"


class RootModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "root.jinja2"


class TypeAliasRootModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "root.jinja2"
    TYPE_ALIAS_KIND: ClassVar[str] = "default"

    @property
    def target_python_version(self) -> PythonVersion:
        version = self.extra_template_data.get(_TARGET_PYTHON_VERSION_EXTRA)
        if isinstance(version, PythonVersion):
            return version
        return PythonVersion.PY_39

    @property
    def use_native_type_statement(self) -> bool:
        return (
            self.target_python_version.value in {PythonVersion.PY_312.value, PythonVersion.PY_313.value, PythonVersion.PY_314.value}
            and self.TYPE_ALIAS_KIND != "pydantic_v1"
        )

    @property
    def use_type_alias_type(self) -> bool:
        return self.TYPE_ALIAS_KIND == "pydantic_v2" and not self.use_native_type_statement

    @property
    def imports(self) -> tuple[Import, ...]:
        extra_imports: tuple[Import, ...]
        if self.use_native_type_statement:
            extra_imports = ()
        elif self.use_type_alias_type:
            extra_imports = (IMPORT_TYPE_ALIAS_TYPE,)
        elif self.target_python_version == PythonVersion.PY_39:
            extra_imports = (IMPORT_TYPE_ALIAS_BACKPORT,)
        else:
            extra_imports = (IMPORT_TYPE_ALIAS,)
        return chain_as_tuple(super().imports, extra_imports)

    def _type_expression(self, field: DataModelFieldBase) -> str:
        if self.TYPE_ALIAS_KIND == "pydantic_v1":
            return field.type_hint
        return field.annotated or field.type_hint

    def render(self, *, class_name: str | None = None) -> str:
        field = self.fields[0]
        rendered_class_name = class_name or self.class_name
        type_expression = self._type_expression(field)
        if self.use_native_type_statement:
            return f"type {rendered_class_name} = {type_expression}"
        if self.use_type_alias_type:
            return f"{rendered_class_name} = TypeAliasType({rendered_class_name!r}, {type_expression})"
        return f"{rendered_class_name}: TypeAlias = {type_expression}"
