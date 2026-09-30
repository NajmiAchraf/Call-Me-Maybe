from __future__ import annotations

import json
from typing import Any, List

from .models import FunctionDefinition, Prompt


class XLoader:
    function_definitions: List[FunctionDefinition]
    prompts: List[Prompt]

    def __init__(
        self,
        path_functions_definition: str,
        path_prompts: str,
    ) -> None:
        self.function_definitions = self._load_functions_definitions(
            path_functions_definition
        )
        self.prompts = self._load_prompts(path_prompts)

    def _load_json(self, path: str) -> List[Any]:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            raise ValueError("Invalid JSON format: expected array")
        return raw

    def _load_functions_definitions(
        self, path: str
    ) -> List[FunctionDefinition]:
        items = self._load_json(path)
        return [FunctionDefinition.model_validate(item) for item in items]

    def _load_prompts(self, path: str) -> List[Prompt]:
        items = self._load_json(path)
        return [Prompt.model_validate(item) for item in items]
