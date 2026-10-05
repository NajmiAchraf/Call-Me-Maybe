from __future__ import annotations

from typing import Dict
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class Prompt(BaseModel):
    """Input prompt expected from the JSON test data.

    Attributes:
        prompt: The natural-language request to process.
    """

    prompt: str = Field(min_length=1)


class Type(BaseModel):
    """Simple schema type descriptor used for function signatures.

    Attributes:
        type: The supported parameter or return type name.
    """

    type: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_type(self) -> Self:
        """Ensure the type name is one of the supported schema values.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If ``type`` is not one of the supported schema names.
        """

        if self.type not in ["number", "integer", "string", "boolean"]:
            raise ValueError(
                "Invalid type. Must be one of:"
                "number, integer, string, boolean"
            )
        return self


class FunctionDefinition(BaseModel):
    """Function metadata consumed by the generator.

    Attributes:
        name: The function name.
        description: The function description.
        parameters: The parameter schema keyed by parameter name.
        returns: The return type schema.
    """

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: Dict[str, Type] = Field(default_factory=dict)
    returns: Type
