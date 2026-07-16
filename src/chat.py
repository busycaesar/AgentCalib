import time

from rich.console import Console
from rich.panel import Panel
from rich.markup import escape

from core import parse_user_input, messages
from config import BANNER, WELCOME_MESSAGE

GOODBYE = "Goodbye!"
INPUT_HINT = 'Try "refactor __init__.py"'

console = Console()

def run_chat():
    console.print(BANNER, style="bold cyan")
    console.print(WELCOME_MESSAGE)
    console.print(Panel(INPUT_HINT, border_style="dim", expand=False))

    while True:
        try:
            user_input = console.input("[bold cyan]❯[/bold cyan] ")
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n{GOODBYE}")
            break

        user_input = user_input.strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            console.print(GOODBYE)
            break

        start_time = time.monotonic()

        try:
            with console.status("[dim]Thinking...[/dim]", spinner="dots"):
                response = parse_user_input(messages, user_input)
        except Exception as error:
            console.print(f"[red]Error:[/red] {escape(str(error))}. Please try again.")
            continue

        elapsed = time.monotonic() - start_time

        console.print(f"[bold cyan]●[/bold cyan] {escape(response)}")
        console.print(f"[dim]✻ Brewed for {elapsed:.0f}s[/dim]")
        console.print()
