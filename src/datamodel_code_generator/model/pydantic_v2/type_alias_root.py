from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.model.pydantic_v2.base_model import BaseModel


class TypeAliasRoot(BaseModel):
    """A model that generates type aliases with Annotated instead of RootModel classes.
    
    This generates output like:
        Total = Annotated[int, Field(ge=0, title="Total")]
    
    Instead of:
        class Total(RootModel[int]):
            root: Annotated[int, Field(ge=0, title="Total")]
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic_v2/TypeAliasRoot.jinja2"
    BASE_CLASS: ClassVar[str] = ""

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        # Remove custom_base_class for type alias models
        if "custom_base_class" in kwargs:
            kwargs.pop("custom_base_class")

        super().__init__(**kwargs)
