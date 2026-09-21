from src import *


class XLoader:
    _function_definitions: List[FunctionDefinition]
    prompts: List[Prompt]
    fn_defs_as_prompt: str

    def __init__(
        self,
        path_functions_definition: str,
        path_prompts: str,
        # path_output: str | None = None,
    ) -> None:
        self._load_functions_definitions(path_functions_definition)
        self._load_prompts(path_prompts)

        self._fn_defs_to_prompt()

    def _fn_defs_to_prompt(self) -> None:
        prompt: List[str] = [
            "STRICT SYSTEM RULE: use ONLY the matching function from list below.\n"
            "if NO function matches the user's intent (even if types match), set name 'none.'\n"
            "Never use an unrelated function for different task.\n\n"
        ]
        for fn in self._function_definitions:
            params = ", ".join(
                f"{k}: {v.type}" for k, v in fn.parameters.items()
            )
            prompt.append(f"  {fn.name}({params}): {fn.description}")
        prompt.append(
            f"Output valid ONLY JSON as: {{'name': {{'<fn_name>'}}, 'args': {{<arguments_dict>}}}}"
        )

        self.fn_defs_as_prompt = "\n".join(prompt)

    def _load_json(self, path: str) -> List:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        if not isinstance(raw, List):
            raise ValueError("Invalid function calling format")

        return raw

    def _load_functions_definitions(self, path: str) -> None:
        items = self._load_json(path)

        self._function_definitions = [
            FunctionDefinition.model_validate(item) for item in items
        ]

    def _load_prompts(self, path: str) -> None:
        items = self._load_json(path)

        self.prompts = [Prompt.model_validate(item) for item in items]
