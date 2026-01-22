from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class Pet(BaseModel):
    pet_type: Annotated[str, Field(alias='petType')]


class Cat(Pet):
    name: str | None = None
    pet_type: Literal['cat'] = Field(..., alias='petType')


class Dog(Pet):
    bark: str | None = None
    pet_type: Literal['dog'] = Field(..., alias='petType')


class Lizard(Pet):
    loves_rocks: Annotated[bool | None, Field(alias='lovesRocks')] = None
    pet_type: Literal['lizard'] = Field(..., alias='petType')


class PetContainer(BaseModel):
    pet: Annotated[Cat | Dog | Lizard, Field(discriminator='pet_type')]
