from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.imports import IMPORT_TYPE_ALIAS, Import
from datamodel_code_generator.model.base import DataModel, DataModelFieldBase
from datamodel_code_generator.types import chain_as_tuple

if TYPE_CHECKING:
    from collections import defaultdict
    from pathlib import Path

    from datamodel_code_generator.reference import Reference


class TypeAliasModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic_v2/TypeAliasModel.jinja2"
    BASE_CLASS: ClassVar[str] = ""

    def __init__(
        self,
        *,
        reference: Reference,
        fields: list[DataModelFieldBase],
        decorators: list[str] | None = None,
        base_classes: list[Reference] | None = None,
        custom_base_class: str | None = None,
        custom_template_dir: Path | None = None,
        extra_template_data: defaultdict[str, Any] | None = None,
        path: Path | None = None,
        description: str | None = None,
        default: Any = None,
        nullable: bool = False,
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
            path=path,
            description=description,
            default=default,
            nullable=nullable,
            treat_dot_as_module=treat_dot_as_module,
        )

    def set_base_class(self) -> None:
        self.base_classes = []

    @property
    def imports(self) -> tuple[Import, ...]:
        return chain_as_tuple(
            (i for f in self.fields for i in f.imports),
            self._additional_imports,
            (IMPORT_TYPE_ALIAS,),
        )
