from llm_sdk import Small_LLM_Model
from src import *


class Generator:
    def __init__(
        self,
        prompts: List[Prompt],
        function_definitions: str,
    ) -> None:

        self.slm_model = Small_LLM_Model()
        self.prompts = prompts
        self.function_definitions = function_definitions

        self._run()

    def _run(self):
        for prompt in self.prompts:
            print(f"\n\nProcessing prompt: {prompt.prompt}")
            function_name = self._generate_function_name(prompt.prompt)
            print(f"Generated answer: {function_name}")
            break

    def _generate_function_name(self, user_prompt: str) -> str:
        prompt = (
            f"User prompt: {user_prompt}\n"
            f"Function definitions: {self.function_definitions}"
        )
        return self._generate_function(prompt)

    def _generate_function(self, prompt: str) -> str:

        # Encode the prompt using the model's tokenizer
        input_ids = self.slm_model.encode(prompt)
        # Convert the input IDs to a list of integers
        ids: List[int] = input_ids[0].tolist()
        generated_so_far = ""

        for _ in range(20):
            # Get the logits for the current input IDs
            logits = self.slm_model.get_logits_from_input_ids(ids)
            soft_max = logits.index(max(logits))
            ids.append(soft_max)

            # Decode the softmax token to get the corresponding string representation
            soft_max_token = self.slm_model.decode([soft_max])
            generated_so_far += soft_max_token

        return generated_so_far
