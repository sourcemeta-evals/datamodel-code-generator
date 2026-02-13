from __future__ import annotations

from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Extra, Field


class Type(Enum):
    eq = 'eq'
    ne = 'ne'


class ComparisonFilter(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Literal['ComparisonFilter']
    key: str
    value: str


class Type1(Enum):
    and_ = 'and'
    or_ = 'or'


class Filters(BaseModel):
    __root__: Union[ComparisonFilter, CompoundFilter] = Field(..., discriminator='type')


class CompoundFilter(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Literal['CompoundFilter']
    filters: List[Filters]


class Filters1(BaseModel):
    __root__: Union[ComparisonFilter, CompoundFilter]


class SearchRequest(BaseModel):
    query: str
    filters: Optional[Filters1] = None
