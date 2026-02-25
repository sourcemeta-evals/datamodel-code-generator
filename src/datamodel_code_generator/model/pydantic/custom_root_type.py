from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator.model.pydantic.base_model import BaseModel
from datamodel_code_generator.model.rootmodel import (
    TypeAliasRootModel,
    TypeAliasRootModelBackport,
)


class CustomRootType(BaseModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic/BaseModel_root.jinja2"
    BASE_CLASS: ClassVar[str] = "pydantic.BaseModel"


class CustomRootTypeTypeAlias(TypeAliasRootModel):
    pass


class CustomRootTypeTypeAliasBackport(TypeAliasRootModelBackport):
    pass
