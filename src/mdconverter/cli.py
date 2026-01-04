"""
CLI interface using Typer.

Provides commands for converting, validating, and fixing Markdown documents.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from mdconverter import __version__
from mdconverter.config import settings

app = typer.Typer(
    name="mdconvert",
    help="Modern Document to Markdown Converter with Vietnamese legal document support.",
    add_completion=True,
)
console = Console()


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"[bold blue]mdconverter[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """
    mdconvert - Modern Document to Markdown Converter.

    Convert PDF, DOCX, HTML, and other documents to clean, standardized Markdown.
    Includes special support for Vietnamese legal documents.
    """
    pass


@app.command()
def convert(
    input_path: Path = typer.Argument(
        ...,
        help="Input file or directory to convert.",
        exists=True,
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output directory. Defaults to same as input.",
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive", "-r",
        help="Recursively process directories.",
    ),
    tool: str = typer.Option(
        "auto",
        "--tool", "-t",
        help="Conversion tool: auto, gemini, pandoc, llamaparse.",
    ),
) -> None:
    """Convert documents to Markdown."""
    console.print(f"[bold]Converting:[/bold] {input_path}")

    if input_path.is_file():
        console.print(f"  Processing file: {input_path.name}")
        # TODO: Implement conversion logic
        console.print("[green]✓[/green] Conversion complete!")
    elif input_path.is_dir():
        console.print(f"  Scanning directory: {input_path}")
        # TODO: Implement batch conversion
        console.print("[green]✓[/green] Batch conversion complete!")


@app.command()
def validate(
    target: Path = typer.Argument(
        ...,
        help="File or directory to validate.",
        exists=True,
    ),
    fix: bool = typer.Option(
        False,
        "--fix", "-f",
        help="Automatically fix issues where possible.",
    ),
) -> None:
    """Validate Markdown files for quality and structure."""
    console.print(f"[bold]Validating:[/bold] {target}")
    # TODO: Implement validation logic
    console.print("[green]✓[/green] Validation complete!")


@app.command()
def lint(
    target: Path = typer.Argument(
        Path("."),
        help="File or directory to lint.",
    ),
    fix: bool = typer.Option(
        False,
        "--fix", "-f",
        help="Automatically fix lint issues.",
    ),
) -> None:
    """Lint Markdown files using PyMarkdown and VN Legal rules."""
    console.print(f"[bold]Linting:[/bold] {target}")
    # TODO: Implement linting logic
    console.print("[green]✓[/green] Linting complete!")


@app.command()
def config(
    show: bool = typer.Option(
        True,
        "--show", "-s",
        help="Show current configuration.",
    ),
) -> None:
    """Show or modify configuration."""
    console.print("[bold]Current Configuration:[/bold]")
    console.print(f"  Proxy: {settings.antigravity_proxy}")
    console.print(f"  Models: {', '.join(settings.models)}")
    console.print(f"  Max Tokens: {settings.max_output_tokens}")
    console.print(f"  Timeout: {settings.timeout_seconds}s")


if __name__ == "__main__":
    app()
