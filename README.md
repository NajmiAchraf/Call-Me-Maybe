*This project has been created as part of the 42 curriculum by anajmi.*

# Call Me Maybe

## Description

Call Me Maybe is a function-calling tool that translates natural language prompts into structured function calls. The goal is not to answer the user directly, but to identify the correct function name and produce the required arguments in valid JSON.

The project is designed around the constraints of small language models. Instead of relying on a model to spontaneously output correct JSON, the implementation uses constrained decoding to restrict token choices and keep the output schema-compliant. This makes the system reliable even with a small model such as Qwen3-0.6B.

The input comes from two JSON files:

- `data/input/function_calling_tests.json`: natural language prompts to process
- `data/input/functions_definition.json`: available functions, their parameter schemas, return types, and descriptions

The program writes its final results to:

- `data/output/function_calling_results.json`

## Instructions

### Requirements

- Python 3.10+
- `uv`
- The provided `llm_sdk` package available in the repository

### Install dependencies

From the project root:

```bash
uv sync
```

### Run the program

Use the Makefile shortcuts from the project root:

```bash
make install
make run
```

`make run` reads the default files from `data/input/` and writes the result to `data/output/function_calling_results.json`.

### Output

The program generates a valid JSON array where each object contains exactly:

- `prompt`
- `name`
- `parameters`

Example:

```json
[
	{
		"prompt": "What is the sum of 2 and 3?",
		"name": "fn_add_numbers",
		"parameters": {"a": 2.0, "b": 3.0}
	}
]
```

## Example Usage

```bash
make run
cat data/output/function_calling_results.json
```

The output file is regenerated from the current input prompts and function definitions.

## Makefile

The project is driven by the root `Makefile`:

- `make install` → runs `uv sync`
- `make run` → runs `uv run python -m src` with the default input and output files
- `make debug` → runs the same entry point under `pdb`
- `make clean` → removes caches and compiled Python files
- `make lint` → runs `flake8` and `mypy` on `src/`
- `make lint-strict` → runs the stricter lint and type checks
- `make moulinette` → grades the generated output with the provided moulinette tool

## Execution Flow

The project runs with a short and explicit pipeline starting from the Makefile:

1. `make run` calls `uv run python -m src` with the default input and output files.
2. `src/__main__.py` loads the CLI arguments, then creates the loader and generator.
3. `src/parser.py` validates the file paths and checks that the input files are valid JSON.
4. `src/x_json_loader.py` reads `functions_definition.json` and `function_calling_tests.json` into `FunctionDefinition` and `Prompt` objects.
5. `src/generator.py` loads `Small_LLM_Model`, reads the vocabulary, and uses constrained decoding to select a valid function name.
6. The generator extracts the arguments for that function and writes `data/output/function_calling_results.json`.

In short: Makefile starts the program, `__main__` wires the modules, the loader reads and validates the inputs, and the generator produces the final JSON output.

## Algorithm Explanation

The core algorithm is a short 6-step loop:

1. **Inject tool schemas** into the prompt so the model sees the available functions, parameters, and types.
2. **Tokenize the prompt** with `slm_model.encode()` to obtain input IDs.
3. **Run the model** with `slm_model.get_logits_from_input_ids()` to get next-token logits.
4. **Decode greedily** by choosing the best valid token and appending it back to the sequence.
5. **Track JSON state** with brace balance so generation stops as soon as the JSON object is complete.
6. **Extract and normalize** the final JSON with `json.loads()`, then cast the arguments to the expected types.

This keeps the output structured, valid, and aligned with the function schema instead of depending on free-form generation.

## Design Decisions

- **Shared data models with Pydantic**: function definitions, prompts, and tool calls are validated with typed models.
- **Thin package entry point**: `src/__main__.py` only wires the CLI, loader, and generator together.
- **Relative imports**: internal modules import each other explicitly to avoid circular imports and package-level side effects.
- **Constrained decoding over free generation**: the model is only allowed to choose from valid next tokens, reducing malformed output.
- **Deterministic parameter extraction**: arguments are derived with predictable rules instead of relying on free-form generation.
- **JSON-first workflow**: the program always reads and writes JSON, which keeps the pipeline stable and easy to validate.

## Performance Analysis

The design favors reliability over unconstrained creativity.

- **Accuracy**: the function selection step is highly reliable because it is constrained by the known function set.
- **Speed**: processing is lightweight because the final argument extraction is deterministic and does not require additional model passes for each prompt.
- **Reliability**: output is always serialized through Python JSON tools, which guarantees valid JSON formatting.
- **Scalability**: the approach remains practical for multiple prompts and changing function sets, because the function schema is loaded dynamically from the input file.

For the project requirements, the main objective is not raw model intelligence but structural correctness. This solution is optimized for that goal.

## Challenges Faced

- **Import order and circular dependencies**: the package originally needed a clearer separation between shared declarations and implementation modules.
- **Schema variability**: the function definitions can change during peer review, so the implementation must not depend on hardcoded function names only.
- **Constrained decoding logic**: mapping tokens to valid next choices required careful use of the vocabulary file and model logits.
- **JSON robustness**: the input files may be missing or malformed, so the loader and parser need defensive validation.
- **Small-model reliability**: a 0.6B model is not guaranteed to emit perfect structured output, so the pipeline had to control generation step by step.

## Testing Strategy

The implementation was validated with the following checks:

- loading and parsing of `functions_definition.json`
- loading and parsing of `function_calling_tests.json`
- validation of Pydantic models for prompts and function schemas
- end-to-end generation of `data/output/function_calling_results.json`
- JSON validity checks on the produced output
- manual tests with sample prompts such as sums, greetings, string reversal, square roots, and substitution tasks
- edge-case handling for malformed paths, missing files, and invalid JSON content

The output file is intended to be easy to verify during peer review with standard JSON tools.

## Resources

### Documentation and references

- Python `json` module documentation
- Pydantic documentation
- `argparse` documentation
- Hugging Face / tokenization references for understanding token-level generation
- The 42 subject for Call Me Maybe
- The `llm_sdk` package provided with the project

### AI usage

AI assistance was used to help structure the README, organize the implementation explanation, and refine the description of the constrained decoding pipeline. The actual project behavior, file layout, and validation logic were aligned with the source code and the 42 subject requirements.

## Additional Notes

- The repository should contain the `src/` implementation, the `llm_sdk/` package, and the `data/input/` files.
- The `data/output/` directory is generated when the program runs and should not be committed for submission.
- The solution is designed to adapt to changing prompts and function definitions during evaluation.
