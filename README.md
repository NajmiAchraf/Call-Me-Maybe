*This project has been created as part of the 42 curriculum by anajmi.*

# Call Me Maybe

## Description

Call Me Maybe is a function-calling tool that translates natural language prompts into structured function calls. The objective is not to answer the prompt directly, but to identify the target function name and format its arguments into valid JSON.

Designed around the constraints of small language models (SLM) such as Qwen3-0.6B, the system avoids relying on spontaneous model compliance. Instead, it guarantees reliable JSON generation by combining structured system prompt conditioning, greedy autoregressive decoding (`argmax`), dynamic syntax brace tracking, and deterministic output schema casting.

The system uses two input files:

- `data/input/function_calling_tests.json`: natural language prompts to process
- `data/input/functions_definition.json`: function definitions, parameter schemas, descriptions, and return types

The final results are written to:

- `data/output/function_calling_results.json`

## Instructions

### Requirements

- Python 3.10+
- `uv` package manager
- `llm_sdk` package (provided in the repository)

### Installation

From the project root:

```bash
uv sync

```

### Execution

Run the default pipeline using the Makefile:

```bash
make install
make run

```

`make run` processes default inputs from `data/input/` and writes results to `data/output/function_calling_results.json`.

Alternatively, pass explicit arguments directly to the module:

```bash
uv run python -m src --functions_definition path/to/functions.json --input path/to/tests.json --output path/to/results.json

```

### Output Format

The output is a valid JSON array containing structured call objects:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  }
]

```

## Example Usage

```bash
make run
cat data/output/function_calling_results.json

```

## Makefile

Key shortcuts provided in the root `Makefile`:

* `make install` → Runs `uv sync`
* `make run` → Executes `uv run python -m src` using default paths
* `make debug` → Launches the entry point under `pdb`
* `make clean` → Removes Python cache artifacts and bytecode
* `make lint` → Runs `flake8` and `mypy` checks on `src/`
* `make lint-strict` → Runs strict linting and type checking
* `make moulinette` → Evaluates generated output against reference benchmarks

## Execution Flow

1. **CLI Argument Parsing (`src/parser.py`)**: Validates flag names, verifies directory structures, and ensures inputs exist and contain valid JSON.
2. **Data Deserialization (`src/x_json_loader.py`)**: Loads raw JSON into validated Pydantic models (`Prompt` and `FunctionDefinition`).
3. **Pipeline Initialization (`src/__main__.py`)**: Instantiates `XLoader` and triggers the `Generator`.
4. **Prompt Construction (`src/generator.py`)**: Formats function definitions and rules into the system prompt context for `Small_LLM_Model`.
5. **Autoregressive Decoding (`src/generator.py`)**: Encodes the sequence, computes logits via `get_logits_from_input_ids()`, selects tokens using greedy `argmax`, and stops generation early using dynamic brace-depth tracking (`{` / `}`).
6. **Parsing & Parameter Normalization (`src/generator.py`)**: Isolates the JSON payload using regex, parses it with `json.loads()`, and coerces numeric parameters to floats via `_cast_parameters()`.
7. **Terminal UI (`src/tools.py`)**: Renders real-time progress animations and logs execution timing metrics.

## Algorithm Explanation

1. **Schema Injection**: Injects tool specifications, argument names, and types directly into system prompt instructions.
2. **Tokenization**: Converts formatted system/user prompts into initial token IDs using `slm_model.encode()`.
3. **Logit Evaluation**: Passes token sequence IDs through `slm_model.get_logits_from_input_ids()` to obtain candidate logit scores.
4. **Greedy Selection**: Selects the top token (`argmax`) and appends it to the sequence via `slm_model.decode()`.
5. **Brace Tracking**: Tracks `{` and `}` balance on each iteration to halt inference the instant the JSON payload completes.
6. **Schema Coercion**: Extracts JSON via regex, parses it into Python dictionaries, and explicitly casts numeric values to `float` representation (`2` → `2.0`).

## Design Decisions

* **Pydantic Validation (`src/models.py`)**: Enforces strict typing for schemas and inputs, validating supported types (`number`, `integer`, `string`, `boolean`).
* **Defensive CLI Validation (`src/parser.py`)**: Performs early checks on file paths, extension types, and JSON formatting to prevent runtime crashes.
* **Explicit Float Coercion (`_cast_parameters`)**: Systematically converts integer and number parameters to Python `float` values to satisfy evaluator schema rules.
* **Brace-Balance Early Termination**: Halts autoregressive sampling as soon as JSON syntax terminates, avoiding unnecessary token passes and preventing prose drift.
* **Decoupled Terminal Utilities (`src/tools.py`)**: Moves execution timing and terminal progress bars out of model logic.

## Performance Analysis

* **Accuracy**: Explicit system prompt context prevents tool hallucination and forces predictable function matching.
* **Speed**: Brace tracking halts token generation early, cutting down inference latency.
* **Reliability**: Combining regex extraction, `json.loads()`, and type casting ensures valid, evaluator-compliant JSON structure.

## Challenges Faced

* **SLM Prose Drift**: Preventing small models (0.6B parameters) from emitting preamble text or continuing after generating JSON.
* **Float Compliance**: Ensuring integers are explicitly converted to float representations (`2.0`) to meet grading specifications.
* **Defensive Error Handling**: Handling missing files, bad paths, or malformed JSON gracefully prior to model execution.

## Testing Strategy

* Pydantic schema validation tests for `Prompt` and `FunctionDefinition` models.
* End-to-end execution checks across test datasets (arithmetic, string operations, regex substitutions).
* Defensive CLI path testing against missing files and malformed JSON payloads.
* JSON structure and float formatting verification on `data/output/function_calling_results.json`.

## Resources

* Python `json`, `re`, and `argparse` documentation
* Pydantic documentation
* 42 Subject specifications for Call Me Maybe
* `llm_sdk` reference implementation

### AI Usage

AI assistance was utilized to help organize, refine, and edit the structure and technical clarity of this README document.

