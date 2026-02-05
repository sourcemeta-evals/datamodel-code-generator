from __future__ import annotations

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
    from collections import defaultdict
    from pathlib import Path

    from datamodel_code_generator.format import PythonVersion
    from datamodel_code_generator.reference import Reference


class TypeAliasModel(DataModel):
    """Model for generating type aliases instead of RootModel classes.

    Handles the version matrix:
    - Python 3.12+: Uses native `type` statement
    - Pydantic v2 + Python 3.9-3.11: Uses `TypeAliasType` from `typing_extensions`
    - Pydantic v1 / non-Pydantic: Uses `TypeAlias` annotation from `typing_extensions`
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
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
        self._python_version = python_version
        self._use_pydantic_v2 = use_pydantic_v2

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

    @property
    def _is_py_312_or_later(self) -> bool:
        if self._python_version is None:
            return False
        from datamodel_code_generator.format import PythonVersion  # noqa: PLC0415

        return self._python_version in (
            PythonVersion.PY_312,
            PythonVersion.PY_313,
            PythonVersion.PY_314,
        )

    @property
    def _use_type_statement(self) -> bool:
        return self._is_py_312_or_later

    @property
    def _use_type_alias_type(self) -> bool:
        return self._use_pydantic_v2 and not self._is_py_312_or_later

    @property
    def imports(self) -> tuple[Import, ...]:
        base_imports = list(super().imports)

        if self._use_type_statement:
            pass
        elif self._use_type_alias_type:
            base_imports.append(IMPORT_TYPE_ALIAS_TYPE)
        else:
            base_imports.append(IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS)

        return tuple(base_imports)

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            decorators=self.decorators,
            base_class=self.base_class,
            methods=self.methods,
            description=self.description,
            keyword_only=self.keyword_only,
            frozen=self.frozen,
            use_type_statement=self._use_type_statement,
            use_type_alias_type=self._use_type_alias_type,
            **self.extra_template_data,
        )
