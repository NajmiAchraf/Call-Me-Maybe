import sys
from pathlib import Path

# Get the path of the folder you want to add
project_root = Path(__file__).resolve().parents[1]

# Inject it into Python's lookup path list
sys.path.append(str(project_root))

from src import *


def main() -> None:
    try:
        args = parse_args()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    function_definitions = load_functions_definitions(
        args.functions_definition
    )
    prompts = load_prompts(args.input)
    model = Small_LLM_Model()
    rt = Generator(model, prompts, function_definitions)


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)
