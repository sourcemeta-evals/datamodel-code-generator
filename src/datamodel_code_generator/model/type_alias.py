from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.imports import Import
from datamodel_code_generator.model.base import DataModel
from datamodel_code_generator.types import chain_as_tuple
from datamodel_code_generator.util import PYDANTIC_V2

if TYPE_CHECKING:
    from datamodel_code_generator.reference import Reference


IMPORT_TYPE_ALIAS = Import(from_="typing", import_="TypeAlias")
IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS = Import(from_="typing_extensions", import_="TypeAlias")
IMPORT_TYPE_ALIAS_TYPE = Import(from_="typing_extensions", import_="TypeAliasType")


class TypeAliasModel(DataModel):
    """Model for generating Python type aliases instead of RootModel classes.

    This model generates type aliases in different formats based on Python version
    and Pydantic version:
    - Python 3.12+: Uses native `type` statement (e.g., `type Foo = str`)
    - Python 3.9-3.11 with Pydantic v2: Uses `TypeAliasType` from typing_extensions
    - Python 3.9-3.11 with Pydantic v1 or non-Pydantic: Uses `TypeAlias` annotation
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""

    def __init__(
        self,
        *,
        reference: Reference,
        python_version: PythonVersion = PythonVersion.PY_39,
        use_pydantic_v2: bool = PYDANTIC_V2,
        **kwargs: Any,
    ) -> None:
        self._python_version = python_version
        self._use_pydantic_v2 = use_pydantic_v2
        super().__init__(reference=reference, **kwargs)

    def set_base_class(self) -> None:
        self.base_classes = []

    @property
    def use_type_statement(self) -> bool:
        # Use set membership check instead of string comparison
        # because "3.9" >= "3.12" is True in lexicographic comparison
        return self._python_version not in {
            PythonVersion.PY_39,
            PythonVersion.PY_310,
            PythonVersion.PY_311,
        }

    @property
    def use_type_alias_type(self) -> bool:
        return not self.use_type_statement and self._use_pydantic_v2

    @property
    def use_type_alias_annotation(self) -> bool:
        return not self.use_type_statement and not self._use_pydantic_v2

    @property
    def imports(self) -> tuple[Import, ...]:
        imports_list: list[Import] = list(super().imports)

        if self.use_type_alias_type:
            imports_list.append(IMPORT_TYPE_ALIAS_TYPE)
        elif self.use_type_alias_annotation:
            if self._python_version == PythonVersion.PY_39:
                imports_list.append(IMPORT_TYPE_ALIAS_TYPING_EXTENSIONS)
            else:
                imports_list.append(IMPORT_TYPE_ALIAS)

        return chain_as_tuple(imports_list)

    def render(self, *, class_name: str | None = None) -> str:
        if not self.fields:
            return ""

        field = self.fields[0]
        type_hint = field.annotated if field.annotated else field.type_hint

        return self._render(
            class_name=class_name or self.class_name,
            type_hint=type_hint,
            use_type_statement=self.use_type_statement,
            use_type_alias_type=self.use_type_alias_type,
            use_type_alias_annotation=self.use_type_alias_annotation,
            description=self.description,
            **self.extra_template_data,
        )
