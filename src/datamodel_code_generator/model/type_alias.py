from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.imports import (
    IMPORT_ANNOTATED,
    IMPORT_TYPE_ALIAS,
    IMPORT_TYPE_ALIAS_TYPE,
    Import,
)
from datamodel_code_generator.model import DataModel, DataModelFieldBase
from datamodel_code_generator.model.base import UNDEFINED

if TYPE_CHECKING:
    from collections import defaultdict
    from pathlib import Path

    from datamodel_code_generator.format import PythonVersion
    from datamodel_code_generator.reference import Reference


class TypeAliasModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

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
        python_version: PythonVersion | None = None,
        use_pydantic_v2: bool = False,
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
        self._python_version = python_version
        self._use_pydantic_v2 = use_pydantic_v2

    @property
    def imports(self) -> tuple[Import, ...]:
        base_imports = list(super().imports)

        if self._python_version is not None:
            from datamodel_code_generator.format import PythonVersion

            if self._python_version.has_type_statement:
                pass
            elif self._use_pydantic_v2:
                base_imports.append(IMPORT_TYPE_ALIAS_TYPE)
            else:
                if self._python_version.value == PythonVersion.PY_39.value:
                    base_imports.append(Import(from_="typing_extensions", import_="TypeAlias"))
                else:
                    base_imports.append(IMPORT_TYPE_ALIAS)

        if self.fields and self.fields[0].annotated:
            base_imports.append(IMPORT_ANNOTATED)

        return tuple(base_imports)

    def render(self, *, class_name: str | None = None) -> str:
        use_type_statement = (
            self._python_version is not None
            and self._python_version.has_type_statement
        )
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            decorators=self.decorators,
            base_class=self.base_class,
            methods=self.methods,
            description=self.description,
            use_type_statement=use_type_statement,
            use_pydantic_v2=self._use_pydantic_v2,
            **self.extra_template_data,
        )
