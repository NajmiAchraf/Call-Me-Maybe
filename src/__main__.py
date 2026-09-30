from .parser import parse_args
from .generator import Generator
from .x_json_loader import XLoader


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
