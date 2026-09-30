import sys
import time
from datetime import timedelta


begin: float = 0.0


def elapsed_time(start: float) -> str:
    """
    Format the elapsed time from the start time to the current time.

    Args:
        start (float): The start time in seconds.

    Returns:
        str: The formatted elapsed time.
    """
    elapsed_time = time.time() - start
    delta = timedelta(seconds=elapsed_time)

    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000

    if hours > 0:
        return f"{hours}h {minutes}min {seconds}s {milliseconds}ms"
    elif minutes > 0:
        return f"{minutes}min {seconds}s {milliseconds}ms"
    elif seconds > 0:
        return f"{seconds}s {milliseconds}ms"
    else:
        return f"{milliseconds}ms"


def print_start(total: int) -> None:
    global begin
    begin = time.time()
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
    status_line = f'\r🤖 [{current}/{total}] '
    status_line += f'[{bar}] {percent:3d}% | Processing: "{short_prompt}"'
    sys.stdout.write(status_line.ljust(80))
    sys.stdout.flush()


def print_finish() -> None:
    # Finalize status bar line and output completed state
    sys.stdout.write(f"\n\n✨ Done! All prompts processed successfully."
                     f" Elapsed time: {elapsed_time(begin)}\n")
    sys.stdout.flush()


def print_output_path(output_path: str) -> None:
    print(f"\n📄 Output written to: {output_path}\n")
