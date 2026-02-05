from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.imports import IMPORT_ANNOTATED, IMPORT_TYPE_ALIAS, Import
from datamodel_code_generator.model.base import UNDEFINED, DataModel, DataModelFieldBase

if TYPE_CHECKING:
    from collections import defaultdict
    from pathlib import Path

    from datamodel_code_generator.reference import Reference


class AnnotatedTypeAlias(DataModel):
    """A type alias model that generates `TypeName: TypeAlias = Annotated[type, Field(...)]`.

    This is an alternative to RootModel for simple types that allows better
    interoperability with `validate_call` and f-strings.
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic_v2/AnnotatedTypeAlias.jinja2"
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
            treat_dot_as_module=treat_dot_as_module,
        )

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = list(super().imports)
        # Add Annotated import if any field uses annotated
        for field in self.fields:
            if field.annotated:
                imports.append(IMPORT_ANNOTATED)
                break
        return tuple(imports)
