try:

    from .parser import parse_args
    from .generator import Generator
    from .x_json_loader import XLoader

except ImportError as ie:
    print("Error: Failed to import required modules.")
    print(ie)
    exit(1)
except KeyboardInterrupt:
    print("\n\nInterrupted by user\n\n")
    exit(1)


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
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user\n\n")
        exit(1)
