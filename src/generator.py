from llm_sdk import Small_LLM_Model
from src import *


class Generator:
    def __init__(
        self,
        prompts: List[Prompt],
        fn_definitions: List[FunctionDefinition],
        output_path: str,
    ) -> None:
        # 1. Initialize the SLM Model instance
        self.slm_model = Small_LLM_Model()
        self.prompts = prompts
        self.fn_definitions = fn_definitions
        self.output_path = output_path

        self._run()


    def _run(self) -> None:
        results: List[Dict[str, Any]] = []
        total = len(self.prompts)
        print_start(total)

        for idx, prompt_obj in enumerate(self.prompts, start=1):
            user_prompt = prompt_obj.prompt

            # Update status animation
            render_progress(idx, total, user_prompt)

            # Build prompt instructed to output JSON
            full_prompt = self._build_slm_prompt(user_prompt)

            # Run autoregressive token generation using SLM
            raw_generated_json = self._generate_with_slm(full_prompt)

            # Parse generated SLM text into structured dict
            parsed_call = self._parse_slm_output(raw_generated_json)

            results.append(
                {
                    "prompt": user_prompt,
                    "name": parsed_call.get("name", "none"),
                    "parameters": parsed_call.get("parameters", {}),
                }
            )

        print_finish()

        # Save output file matching subject requirements (Section V.4)
        self._save_results(results)

    def _build_slm_prompt(self, user_prompt: str) -> str:
        """Formats available tools into a clear context for the SLM."""
        fn_docs = []
        for fn in self.fn_definitions:
            params = ", ".join(
                f'"{k}": <{v.type}>' for k, v in fn.parameters.items()
            )
            fn_docs.append(
                f"- Name: {fn.name}\n  Description: {fn.description}\n  Parameters: {{{params}}}"
            )

        tools_str = "\n".join(fn_docs)

        return (
            f"System: You are an API function calling bot.\n"
            f"Available tools:\n{tools_str}\n\n"
            f"User Request: \"{user_prompt}\"\n\n"
            f"Respond ONLY with a valid JSON object formatted as:\n"
            f'{{"name": "<function_name>", "parameters": {{<arguments>}}}}\n'
            f"JSON Output:"
        )

    def _generate_with_slm(self, prompt: str, max_new_tokens: int = 100) -> str:
        """
        Core SLM Token Generation Loop using:
        - slm_model.encode()
        - slm_model.get_logits_from_input_ids()
        - slm_model.decode()
        """
        # 1. Encode string prompt into initial token IDs
        input_ids = self.slm_model.encode(prompt)

        if hasattr(input_ids, "tolist"):
            ids: List[int] = (
                input_ids[0].tolist()
                if len(input_ids.shape) > 1
                else input_ids.tolist()
            )
        else:
            ids = List(input_ids)

        generated_text = ""
        open_braces = 0
        json_started = False

        # 2. Token-by-token loop
        for _ in range(max_new_tokens):
            # Retrieve logits vector from Qwen model for current sequence
            logits = self.slm_model.get_logits_from_input_ids(ids)

            # Argmax selection for greedy token decoding
            next_token_id = int(logits.index(max(logits)))
            ids.append(next_token_id)

            # Decode single token ID to text string
            token_str = self.slm_model.decode([next_token_id])
            generated_text += token_str

            # Stop condition: terminate generation once closing brace '}' completes JSON
            for char in token_str:
                if char == "{":
                    open_braces += 1
                    json_started = True
                elif char == "}":
                    open_braces -= 1

            if json_started and open_braces == 0:
                break

        return generated_text

    def _cast_parameters(self, fn_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures all numbers (int and float) are converted to float format (e.g., 2 -> 2.0)."""
        fn_def = next((f for f in self.fn_definitions if f.name == fn_name), None)
        if not fn_def:
            return params

        casted: Dict[str, Any] = {}
        for param_name, val in params.items():
            expected_type = fn_def.parameters.get(param_name)
            type_str = expected_type.type if expected_type else ""

            # Convert any integer/number parameter directly to float
            if type_str in ["number", "integer"] or isinstance(val, (int, float)):
                try:
                    casted[param_name] = float(val)
                except (ValueError, TypeError):
                    casted[param_name] = val
            elif type_str == "boolean":
                casted[param_name] = bool(val)
            elif type_str == "string":
                casted[param_name] = str(val)
            else:
                casted[param_name] = val

        return casted

    def _parse_slm_output(self, raw_text: str) -> Dict[str, Any]:
        try:
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                if isinstance(data, dict) and "name" in data and "parameters" in data:
                    fn_name = data["name"]
                    raw_params = data.get("parameters", {})

                    # Run parameter values through float conversion
                    data["parameters"] = self._cast_parameters(fn_name, raw_params)
                    return data
        except Exception:
            pass

        return {"name": "none", "parameters": {}}

    def _save_results(self, results: List[Dict[str, Any]]) -> None:
        out_path = Path(self.output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print_output_path(self.output_path)