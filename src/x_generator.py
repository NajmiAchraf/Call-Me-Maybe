from src import *


class Generator:
    def __init__(
        self,
        model: Small_LLM_Model,
        prompts: List[Prompt],
        function_definitions: List[FunctionDefinition],
    ) -> None:
        self.model = model
        self.prompts = prompts
        self.function_definitions = function_definitions

    def run(self):
        for prompt in self.prompts:
            function_name = self.generate_function_name(prompt.prompt)
            print(f"Generated function name: {function_name}")

    def generate_function_name(self, user_prompt: str) -> str:
        prompt = (
            f"User prompt: {user_prompt}"
            f"Function definitions: {self.function_definitions}"
        )

        input_ids = self.model.encode(prompt)
        ids: List[int] = input_ids[0].tolist()
        function_names = [
            function.name for function in self.function_definitions
        ]
        generated_so_far = ""
        for _ in range(20):
            logits = self.model.get_logits_from_input_ids(ids)
            soft_max = logits.index(max(logits))
            soft_max_token = self.model.decode([soft_max])
            if any(
                True
                for function_name in function_names
                if function_name.startswith(generated_so_far + soft_max_token)
            ):
                generated_so_far += soft_max_token
            ids.append(soft_max)
        return generated_so_far
