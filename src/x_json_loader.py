from src import *


def load_json(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, list):
        raise ValueError("Invalid function calling format")

    return raw


def load_functions_definitions(path: str) -> List[FunctionDefinition]:
    items = load_json(path)

    return [FunctionDefinition.model_validate(item) for item in items]


def load_prompts(path: str) -> List[Prompt]:
    items = load_json(path)

    return [Prompt.model_validate(item) for item in items]
