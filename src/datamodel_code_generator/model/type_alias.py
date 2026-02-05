from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_TYPE,
    IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,
    Import,
)
from datamodel_code_generator.model import DataModel, DataModelFieldBase
from datamodel_code_generator.model.base import UNDEFINED

if TYPE_CHECKING:
    from pathlib import Path

    from datamodel_code_generator.reference import Reference


class TypeAliasModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS,)

    def __init__(  # noqa: PLR0913
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
        treat_dot_as_module: bool = False,
    ) -> None:
        if "custom_base_class" in (extra_template_data or {}):
            custom_base_class = None

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
            treat_dot_as_module=treat_dot_as_module,
        )


class TypeAliasModelTypeAliasType(TypeAliasModel):
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_TYPE,)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.extra_template_data["use_type_alias_type"] = True


class TypeAliasModelNativeType(TypeAliasModel):
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.extra_template_data["use_type_statement"] = True
