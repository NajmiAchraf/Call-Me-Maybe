from __future__ import annotations

import json
from typing import Any, List

from .models import FunctionDefinition, Prompt


class XLoader:
    """Load and validate function definitions and prompts from JSON files.

    Attributes:
        function_definitions: The validated function definitions.
        prompts: The validated prompts.
    """

    function_definitions: List[FunctionDefinition]
    prompts: List[Prompt]

    def __init__(
        self,
        path_functions_definition: str,
        path_prompts: str,
    ) -> None:
        """Load both input files and expose them as validated models.

        Args:
            path_functions_definition: The JSON file containing function
                definitions.
            path_prompts: The JSON file containing prompts.

        Returns:
            None.
        """

        self.function_definitions = self._load_functions_definitions(
            path_functions_definition
        )
        self.prompts = self._load_prompts(path_prompts)

    def _load_json(self, path: str) -> List[Any]:
        """Read a JSON array from disk and return it as raw Python values.

        Args:
            path: The JSON file path.

        Returns:
            The parsed JSON array.

        Raises:
            ValueError: If the file does not contain a JSON array.
        """

        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            raise ValueError("Invalid JSON format: expected array")
        return raw

    def _load_functions_definitions(
        self, path: str
    ) -> List[FunctionDefinition]:
        """Convert raw function definition objects into validated models.

        Args:
            path: The JSON file path containing function definitions.

        Returns:
            A list of validated function definitions.
        """

        items = self._load_json(path)
        return [FunctionDefinition.model_validate(item) for item in items]

    def _load_prompts(self, path: str) -> List[Prompt]:
        """Convert raw prompt objects into validated models.

        Args:
            path: The JSON file path containing prompts.

        Returns:
            A list of validated prompts.
        """

        items = self._load_json(path)
        return [Prompt.model_validate(item) for item in items]
