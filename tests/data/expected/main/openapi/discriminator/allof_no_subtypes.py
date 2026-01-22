from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class BaseItem(BaseModel):
    itemType: str


class FooItem(BaseModel):
    fooValue: Optional[str] = None


class BarItem(BaseModel):
    barValue: Optional[int] = None


class ItemContainer(BaseModel):
    item: BaseItem = Field(..., discriminator='itemType')
