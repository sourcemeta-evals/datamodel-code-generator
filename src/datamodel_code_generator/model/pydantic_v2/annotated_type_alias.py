from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.imports import IMPORT_ANNOTATED, Import
from datamodel_code_generator.model.pydantic_v2.base_model import BaseModel
from datamodel_code_generator.types import chain_as_tuple


class AnnotatedTypeAlias(BaseModel):
    """Model class that generates Annotated type aliases instead of RootModel classes.

    For example, instead of:
        class UID(RootModel[int]):
            root: Annotated[int, Field(ge=0)]

    This generates:
        UID = Annotated[int, Field(ge=0)]
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic_v2/AnnotatedTypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""

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
    def imports(self) -> tuple[Import, ...]:
        base_imports = super().imports
        if self.fields and self.fields[0].annotated:
            return chain_as_tuple(base_imports, (IMPORT_ANNOTATED,))
        return base_imports
