from src import *


def print_start(total: int) -> None:
    print(f"\n🚀 Execution started: Processing {total} prompt(s)...\n")


def render_progress(current: int, total: int, current_prompt: str) -> None:
    """Renders an inline animated terminal progress bar."""
    percent = int((current / total) * 100)
    bar_length = 20
    filled = int(bar_length * current // total)
    bar = "█" * filled + "░" * (bar_length - filled)

    # Truncate prompt text if it's too long for the terminal line
    short_prompt = (
        (current_prompt[:25] + "...")
        if len(current_prompt) > 28
        else current_prompt
    )

    # \r resets the cursor to the beginning of the current terminal line
    status_line = f'\r🤖 [{current}/{total}] [{bar}] {percent:3d}% | Processing: "{short_prompt}"'
    sys.stdout.write(status_line.ljust(80))
    sys.stdout.flush()


def print_finish() -> None:
    # Finalize status bar line and output completed state
    sys.stdout.write("\n\n✨ Done! All prompts processed successfully.\n")
    sys.stdout.flush()


def print_output_path(output_path: str) -> None:
    print(f"\n📄 Output written to: {output_path}\n")
