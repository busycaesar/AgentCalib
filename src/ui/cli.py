import time
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import ANSI
from rich.console import Console
from rich.markup import escape
from core import parse_user_input, messages
from config import BANNER, WELCOME_MESSAGE, GOODBYE_MESSAGE

console = Console()

PROMPT = ANSI("\033[1m\033[38;2;250;104;0m❯\033[0m ")
history = InMemoryHistory()

def run_cli_chat():
    console.print(BANNER, style="bold #fa6800")
    console.print(WELCOME_MESSAGE)

    while True:
        try:
            console.print()
            user_input = prompt(PROMPT, history=history)
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n{GOODBYE_MESSAGE}")
            break

        user_input = user_input.strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            console.print()
            console.print(GOODBYE_MESSAGE)
            break

        start_time = time.monotonic()

        try:
            with console.status("[dim]Biasing the gate...[/dim]", spinner="dots"):
                response = parse_user_input(messages, user_input)
        except Exception as error:
            console.print(f"[red]Error:[/red] {escape(str(error))}. Please try again.")
            continue

        elapsed = time.monotonic() - start_time

        console.print()
        console.print(f"[bold #fa6800]●[/bold #fa6800] {escape(response)}")
        console.print(f"[dim]✻ Threshold reached in {elapsed:.0f}s[/dim]")
