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

    definitions = load_functions_definitions(args.functions_definition)
    prompt = load_prompts(args.input)

    router = ToolRouter(definitions)
    print(router)

    # Manual test call (Step 1+2+3 baseline)
    call = ToolCall.model_validate(
        {"name": "fn_add_numbers", "parameters": {"a": 40, "b": 2}}
    )
    result = router.execute(call)

    print(
        json.dumps({"name": call.name, "result": result}, ensure_ascii=False)
    )


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)
