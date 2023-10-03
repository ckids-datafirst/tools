# type: ignore[attr-defined]
from typing import Optional

from enum import Enum
from random import choice

import typer
from rich.console import Console

from datafirst_tools import github_subcommand, version

app = typer.Typer(
    name="datafirst-tools",
    help="Tools to handle the DataFirst program",
    add_completion=False,
)
app.add_typer(
    github_subcommand.app,
    name="github",
    help="Tools to handle the GitHub organization",
)


console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]datafirst-tools[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


if __name__ == "__main__":
    app()
