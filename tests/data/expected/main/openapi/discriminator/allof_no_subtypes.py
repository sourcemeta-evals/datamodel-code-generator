from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Base2(BaseModel):
    type2: str


class TypeX(BaseModel):
    propX: Optional[str] = None


class TypeY(BaseModel):
    propY: Optional[int] = None


class Container2(BaseModel):
    field2: Base2 = Field(..., discriminator='type2')
