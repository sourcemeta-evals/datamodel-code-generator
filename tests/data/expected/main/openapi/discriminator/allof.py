from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


class Base1(BaseModel):
    type1: str


class TypeA(Base1):
    prop1: str | None = None
    type1: Literal['a']


class TypeB(Base1):
    prop2: str | None = None
    type1: Literal['b']


class TypeC(Base1):
    prop3: bool | None = None
    type1: Literal['c']


class Container1(BaseModel):
    field1: Annotated[Union[TypeA, TypeB, TypeC], Field(discriminator='type1')]
