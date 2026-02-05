from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.imports import (
    IMPORT_ANNOTATED,
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_TYPE,
    IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,
    Import,
)
from datamodel_code_generator.model.base import DataModel
from datamodel_code_generator.types import chain_as_tuple

if TYPE_CHECKING:
    from collections.abc import Iterator


class TypeAliasModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "type_alias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    _class_target_python_version: ClassVar[PythonVersion] = PythonVersion.PY_39
    _class_use_pydantic_v2: ClassVar[bool] = True

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        if "custom_base_class" in kwargs:
            kwargs.pop("custom_base_class")

        super().__init__(**kwargs)

    def set_base_class(self) -> None:
        self.base_classes = []

    @property
    def _is_py_312_or_later(self) -> bool:
        return self._class_target_python_version in {
            PythonVersion.PY_312,
            PythonVersion.PY_313,
            PythonVersion.PY_314,
        }

    @property
    def type_alias_style(self) -> str:
        if self._is_py_312_or_later:
            return "type_statement"
        elif self._class_use_pydantic_v2:
            return "type_alias_type"
        else:
            return "type_alias_annotation"

    @property
    def imports(self) -> tuple[Import, ...]:
        imports: list[tuple[Import, ...] | Iterator[Import]] = [
            tuple(i for f in self.fields for i in f.imports),
            tuple(self._additional_imports),
        ]

        style = self.type_alias_style
        if style == "type_alias_type":
            imports.append((IMPORT_TYPE_ALIAS_TYPE,))
        elif style == "type_alias_annotation":
            if self._class_target_python_version == PythonVersion.PY_39:
                imports.append((IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,))
            else:
                imports.append((IMPORT_TYPE_ALIAS,))

        if self.fields and self.fields[0].use_annotated and self.fields[0].annotated:
            imports.append((IMPORT_ANNOTATED,))

        return chain_as_tuple(*imports)

    def render(self, *, class_name: str | None = None) -> str:
        field = self.fields[0] if self.fields else None
        if field is None:
            return ""

        if field.annotated:
            type_value = field.annotated
        else:
            type_value = field.type_hint

        style = self.type_alias_style
        name = class_name or self.class_name

        if style == "type_statement":
            result = f"type {name} = {type_value}"
        elif style == "type_alias_type":
            result = f'{name} = TypeAliasType("{name}", {type_value})'
        else:
            result = f"{name}: TypeAlias = {type_value}"

        return result


def create_type_alias_model_class(
    target_python_version: PythonVersion,
    use_pydantic_v2: bool,
) -> type[TypeAliasModel]:
    class ConfiguredTypeAliasModel(TypeAliasModel):
        _class_target_python_version: ClassVar[PythonVersion] = target_python_version
        _class_use_pydantic_v2: ClassVar[bool] = use_pydantic_v2

    return ConfiguredTypeAliasModel
