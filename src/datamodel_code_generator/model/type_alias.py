from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.imports import IMPORT_TYPE_ALIAS, Import
from datamodel_code_generator.model import DataModel, DataModelFieldBase
from datamodel_code_generator.model.base import UNDEFINED

if TYPE_CHECKING:
    from collections import defaultdict
    from pathlib import Path

    from datamodel_code_generator.format import PythonVersion
    from datamodel_code_generator.reference import Reference

IMPORT_TYPE_ALIAS_TYPE = Import(from_="typing_extensions", import_="TypeAliasType")
IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS = Import(from_="typing_extensions", import_="TypeAlias")


class TypeAliasModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasAnnotation.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS,)

    def __init__(
        self,
        *,
        reference: Reference,
        fields: list[DataModelFieldBase],
        decorators: list[str] | None = None,
        base_classes: list[Reference] | None = None,
        custom_base_class: str | None = None,
        custom_template_dir: Path | None = None,
        extra_template_data: defaultdict[str, dict[str, Any]] | None = None,
        methods: list[str] | None = None,
        path: Path | None = None,
        description: str | None = None,
        default: Any = UNDEFINED,
        nullable: bool = False,
        keyword_only: bool = False,
        frozen: bool = False,
        treat_dot_as_module: bool = False,
    ) -> None:
        super().__init__(
            reference=reference,
            fields=fields,
            decorators=decorators,
            base_classes=base_classes,
            custom_base_class=custom_base_class,
            custom_template_dir=custom_template_dir,
            extra_template_data=extra_template_data,
            methods=methods,
            path=path,
            description=description,
            default=default,
            nullable=nullable,
            keyword_only=keyword_only,
            frozen=frozen,
            treat_dot_as_module=treat_dot_as_module,
        )


class TypeAliasModelPy312(TypeAliasModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()


class TypeAliasModelTypeAliasType(TypeAliasModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasType.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)


class TypeAliasModelPy39(TypeAliasModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasAnnotation.jinja2"
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,)


def get_type_alias_model(
    python_version: PythonVersion,
    is_pydantic_v2: bool,
) -> type[TypeAliasModel]:
    from datamodel_code_generator.format import PythonVersion  # noqa: PLC0415

    is_py312_or_later = python_version.value not in {
        PythonVersion.PY_39.value,
        PythonVersion.PY_310.value,
        PythonVersion.PY_311.value,
    }

    if is_py312_or_later:
        return TypeAliasModelPy312

    if is_pydantic_v2:
        return TypeAliasModelTypeAliasType

    if python_version == PythonVersion.PY_39:
        return TypeAliasModelPy39

    return TypeAliasModel
