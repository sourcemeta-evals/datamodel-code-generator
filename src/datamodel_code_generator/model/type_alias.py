from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.imports import IMPORT_TYPE_ALIAS, Import
from datamodel_code_generator.model import DataModel, DataModelFieldBase
from datamodel_code_generator.model.base import UNDEFINED

if TYPE_CHECKING:
    from pathlib import Path

    from datamodel_code_generator.format import PythonVersion
    from datamodel_code_generator.reference import Reference


IMPORT_TYPE_ALIAS_TYPE = Import.from_full_path("typing_extensions.TypeAliasType")


class TypeAlias(DataModel):
    """Type alias model for generating type aliases instead of RootModel classes.

    Handles the matrix of Python versions and Pydantic versions:
    - Python 3.12+: Uses native `type` statement
    - Python 3.9-3.11 with Pydantic v2: Uses `TypeAliasType` from `typing_extensions`
    - Python 3.9-3.11 with Pydantic v1 or non-Pydantic: Uses `TypeAlias` annotation
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
        treat_dot_as_module: bool = False,
        python_version: PythonVersion | None = None,
        use_pydantic_v2: bool = False,
    ) -> None:
        extra_template_data = extra_template_data or defaultdict(dict)

        # Determine which type alias style to use based on Python version
        use_native_type_statement = False
        use_type_alias_type = False

        if python_version is not None:
            # Parse version for proper comparison
            version_parts = python_version.value.split(".")
            major = int(version_parts[0])
            minor = int(version_parts[1]) if len(version_parts) > 1 else 0

            # Python 3.12+ uses native `type` statement
            if (major, minor) >= (3, 12):
                use_native_type_statement = True
            elif use_pydantic_v2:
                # Pydantic v2 with Python 3.9-3.11 uses TypeAliasType
                use_type_alias_type = True
            # else: Pydantic v1 or non-Pydantic uses TypeAlias annotation

        extra_template_data[reference.name] = extra_template_data.get(reference.name, {})
        extra_template_data[reference.name]["use_native_type_statement"] = use_native_type_statement
        extra_template_data[reference.name]["use_type_alias_type"] = use_type_alias_type

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

        # Add appropriate imports based on the type alias style
        if not use_native_type_statement:
            if use_type_alias_type:
                self._additional_imports.append(IMPORT_TYPE_ALIAS_TYPE)
            else:
                self._additional_imports.append(IMPORT_TYPE_ALIAS)

    def render(self, *, class_name: str | None = None) -> str:
        if not self.fields:
            return ""

        field = self.fields[0]
        type_hint = field.annotated if field.annotated else field.type_hint

        return self._render(
            class_name=class_name or self.class_name,
            type_hint=type_hint,
            description=self.description,
            **self.extra_template_data,
        )
