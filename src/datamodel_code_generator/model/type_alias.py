from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator import DataModelType, PythonVersion
from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_BACKPORT,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model import DataModel


class TypeAliasDataModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()
    TYPE_ALIAS_KIND: ClassVar[str] = "annotation"

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            description=self.description,
            type_alias_kind=self.TYPE_ALIAS_KIND,
            **self.extra_template_data,
        )


class BackportAnnotationTypeAliasDataModel(TypeAliasDataModel):
    TYPE_ALIAS_KIND: ClassVar[str] = "annotation"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_BACKPORT,)


class TypingAnnotationTypeAliasDataModel(TypeAliasDataModel):
    TYPE_ALIAS_KIND: ClassVar[str] = "annotation"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)


class TypeAliasTypeDataModel(TypeAliasDataModel):
    TYPE_ALIAS_KIND: ClassVar[str] = "type_alias_type"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)


class NativeTypeAliasDataModel(TypeAliasDataModel):
    TYPE_ALIAS_KIND: ClassVar[str] = "native"


def get_type_alias_data_model(
    data_model_type: DataModelType,
    target_python_version: PythonVersion,
) -> type[TypeAliasDataModel]:
    if target_python_version in {PythonVersion.PY_312, PythonVersion.PY_313, PythonVersion.PY_314}:
        if data_model_type != DataModelType.PydanticBaseModel:
            return NativeTypeAliasDataModel
        return TypingAnnotationTypeAliasDataModel

    if data_model_type == DataModelType.PydanticV2BaseModel:
        return TypeAliasTypeDataModel
    if target_python_version == PythonVersion.PY_39:
        return BackportAnnotationTypeAliasDataModel
    return TypingAnnotationTypeAliasDataModel
