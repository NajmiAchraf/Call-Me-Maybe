from src import *

FUNCTIONS: dict[str, Callable[..., Any]] = {
    "fn_add_numbers": fn_add_numbers,
    "fn_get_square_root": fn_get_square_root,
    "fn_greet": fn_greet,
    "fn_reverse_string": fn_reverse_string,
    "fn_substitute_string_with_regex": fn_substitute_string_with_regex,
}


class ToolRouter:
    def __init__(self, definitions: list[FunctionDefinition]) -> None:
        self._defs = {d.name: d for d in definitions}
        self._json = definitions

    def __str__(self) -> str:
        prompt: list[str] = ["ToolRouter with functions:"]
        for fn in self._json:
            params = ", ".join(
                f"{k}: {v.type}" for k, v in fn.parameters.items()
            )
            prompt.append(f"  {fn.name}({params}): {fn.description}")
        prompt.append(
            f"Output valid ONLY JSON as: {{'name': {{'<fn_function_name>'}}, 'args': {{<arguments_dict>}}}}"
        )
        return "\n".join(prompt)

    def execute(self, call: ToolCall) -> Any:
        if call.name not in self._defs:
            raise ValueError(f"Unknown function in schema: {call.name}")
        if call.name not in FUNCTIONS:
            raise ValueError(f"Function not implemented: {call.name}")

        self._validate_params(self._defs[call.name], call.parameters)
        return FUNCTIONS[call.name](**call.parameters)

    def _validate_params(
        self, definition: FunctionDefinition, params: dict[str, Any]
    ) -> None:
        expected = definition.parameters

        for key in expected:
            if key not in params:
                raise ValueError(f"Missing required parameter: {key}")

        for key, value in params.items():
            if key not in expected:
                raise ValueError(f"Unexpected parameter: {key}")
            self._check_type(key, value, expected[key].type)

    @staticmethod
    def _check_type(name: str, value: Any, expected_type: str) -> None:
        if expected_type == "number":
            ok = isinstance(value, (int, float)) and not isinstance(
                value, bool
            )
        elif expected_type == "string":
            ok = isinstance(value, str)
        else:
            ok = False

        if not ok:
            raise TypeError(
                f"Parameter '{name}' must be {expected_type}, got {type(value).__name__}"
            )
