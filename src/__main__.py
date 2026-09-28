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
    args = parse_args()

    x_loader = XLoader(
        path_functions_definition=args.functions_definition,
        path_prompts=args.input,
    )

    Generator(
        prompts=x_loader.prompts,
        fn_definitions=x_loader.function_definitions,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
