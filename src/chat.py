import time
from rich.console import Console
from rich.markup import escape
from core import parse_user_input, messages
from config import BANNER, WELCOME_MESSAGE

GOODBYE = "Entering cutoff. Goodbye!"

console = Console()

def run_chat():
    console.print(BANNER, style="bold #fa6800")
    console.print(WELCOME_MESSAGE)

    while True:
        try:
            console.print()
            user_input = console.input("[bold #fa6800]❯[/bold #fa6800] ")
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n{GOODBYE}")
            break

        user_input = user_input.strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            console.print()
            console.print(GOODBYE)
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
