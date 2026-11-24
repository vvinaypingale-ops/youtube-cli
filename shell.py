from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.panel import Panel
import shlex
from main import app

console = Console()

COMMANDS = [
    "ai",
    "voice",
    "play",
    "pause",
    "artist-info",
    "playlists",
    "add",
    "play-playlist",
    "help",
    "exit"
]

completer = WordCompleter(COMMANDS, ignore_case=True)


def banner():
    console.print(
        Panel.fit(
            """[bold cyan]░█▀▄▀█░█░█░█▀▀░▀█▀░█▀▀░░░█▀▀░█░░░▀█▀
░█░▀░█░█░█░▀▀█░░█░░█░░░░░█░░░█░░░░█░
░▀░░░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀[/bold cyan]
[dim]Powered by YouTube Music (Free & No API Key Required)[/dim]""",
            title="Music CLI Shell"
        )
    )


def run_shell():
    banner()
    session = PromptSession(
        history=FileHistory(".music_history")
    )

    while True:
        try:
            text = session.prompt(
                "music> ",
                completer=completer
            ).strip()

            if not text:
                continue

            if text.lower() in ["exit", "quit"]:
                console.print("[red]Goodbye![/red]")
                break

            if text.lower() == "help":
                app(["--help"])
                continue

            args = shlex.split(text)

            try:
                app(args, standalone_mode=False)
            except Exception as e:
                console.print(f"[red]{e}[/red]")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    run_shell()
