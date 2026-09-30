from __future__ import annotations

from typing import Dict
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class Prompt(BaseModel):
    prompt: str = Field(min_length=1)


class Type(BaseModel):
    type: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_type(self) -> Self:
        if self.type not in ["number", "integer", "string", "boolean"]:
            raise ValueError(
                "Invalid type. Must be one of:"
                "number, integer, string, boolean"
            )
        return self


class FunctionDefinition(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: Dict[str, Type] = Field(default_factory=dict)
    returns: Type
