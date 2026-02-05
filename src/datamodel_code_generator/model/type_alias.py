from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.imports import Import
from datamodel_code_generator.model.base import DataModel
from datamodel_code_generator.types import chain_as_tuple


IMPORT_TYPE_ALIAS = Import(from_="typing", import_="TypeAlias")
IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS = Import(from_="typing_extensions", import_="TypeAlias")
IMPORT_TYPE_ALIAS_TYPE = Import(from_="typing_extensions", import_="TypeAliasType")


class TypeAliasModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    _python_version: ClassVar[PythonVersion] = PythonVersion.PY_39
    _use_pydantic_v2: ClassVar[bool] = True

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
    def use_type_statement(self) -> bool:
        return self._python_version in {
            PythonVersion.PY_312,
            PythonVersion.PY_313,
            PythonVersion.PY_314,
        }

    @property
    def use_type_alias_type(self) -> bool:
        return self._use_pydantic_v2 and not self.use_type_statement

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = list(super().imports)
        if self.use_type_statement:
            pass
        elif self.use_type_alias_type:
            imports.append(IMPORT_TYPE_ALIAS_TYPE)
        else:
            if self._python_version == PythonVersion.PY_39:
                imports.append(IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS)
            else:
                imports.append(IMPORT_TYPE_ALIAS)
        return chain_as_tuple(imports)

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            use_type_statement=self.use_type_statement,
            use_type_alias_type=self.use_type_alias_type,
            **self.extra_template_data,
        )


def create_type_alias_model_class(
    python_version: PythonVersion,
    use_pydantic_v2: bool,
) -> type[TypeAliasModel]:
    class ConfiguredTypeAliasModel(TypeAliasModel):
        _python_version: ClassVar[PythonVersion] = python_version
        _use_pydantic_v2: ClassVar[bool] = use_pydantic_v2

    return ConfiguredTypeAliasModel
