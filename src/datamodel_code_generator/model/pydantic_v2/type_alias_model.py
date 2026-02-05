from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator.model.pydantic_v2.base_model import BaseModelBase


class TypeAliasModel(BaseModelBase):
    """A model that generates type aliases using Annotated instead of RootModel classes.

    This generates output like:
        Total = Annotated[int, Field(ge=0, title="Total")]

    Instead of:
        class Total(RootModel[int]):
            root: Annotated[int, Field(ge=0, title="Total")]
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "root.jinja2"
    BASE_CLASS: ClassVar[str] = ""
