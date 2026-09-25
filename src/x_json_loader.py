from src import *


class XLoader:
    function_definitions: List[FunctionDefinition]
    prompts: List[Prompt]

    def __init__(
        self,
        path_functions_definition: str,
        path_prompts: str,
    ) -> None:
        self._load_functions_definitions(path_functions_definition)
        self._load_prompts(path_prompts)

    def _load_json(self, path: str) -> List:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            raise ValueError("Invalid JSON format: expected array")
        return raw

    def _load_functions_definitions(self, path: str) -> None:
        items = self._load_json(path)
        self.function_definitions = [
            FunctionDefinition.model_validate(item) for item in items
        ]

    def _load_prompts(self, path: str) -> None:
        items = self._load_json(path)
        self.prompts = [Prompt.model_validate(item) for item in items]