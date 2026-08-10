from src import *

JsonType = Literal["number", "string"]


class ParameterSpec(BaseModel):
    type: JsonType


class ReturnSpec(BaseModel):
    type: JsonType


class FunctionDefinition(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: Dict[str, ParameterSpec] = Field(default_factory=Dict)
    returns: ReturnSpec


class ToolCall(BaseModel):
    name: str = Field(min_length=1)
    parameters: Dict[str, Any] = Field(default_factory=Dict)


class FunctionTests(BaseModel):
    prompt: str = Field(min_length=1)
