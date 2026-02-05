from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator.model import DataModel


class RootModelTypeAlias(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic_v2/RootModelTypeAlias.jinja2"
