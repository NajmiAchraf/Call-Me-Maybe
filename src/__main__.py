import sys
from pathlib import Path

# Get the path of the folder you want to add
project_root = Path(__file__).resolve().parents[1]


# Inject it into Python's lookup path list
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))
sys.path.append(str(project_root / "llm_sdk"))


from src import *


def main() -> None:
    try:
        args = parse_args()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    x_loader = XLoader(
        path_functions_definition=args.functions_definition,
        path_prompts=args.input,
    )

    function_definitions = x_loader.fn_defs_as_prompt
    prompts = x_loader.prompts

    # print(function_definitions)
    # print(prompts)

    Generator(prompts, function_definitions)


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)
