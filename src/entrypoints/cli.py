"""
Command Line Interface entrypoint for the Python Clean Architecture Boilerplate.
"""

import typer

from src.core.config.settings import get_settings
from src.core.config.logger import get_logger
from src.core.metadata import APP_NAME, DESCRIPTION

app = typer.Typer(
    name=APP_NAME,
    help=DESCRIPTION,
    add_completion=False,
)

logger = get_logger("boilerplate.cli")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable debug logging and local console output."
    ),
) -> None:
    """
    Python Clean Architecture Boilerplate CLI.
    """
    # Initialize settings and logger on startup
    settings = get_settings()

    if ctx.invoked_subcommand is None:
        typer.echo(f"Welcome to {APP_NAME} CLI. Use --help to see available commands.")

    logger.debug(
        "CLI context initialized",
        env=settings.APP_ENV,
        is_cloud=settings.IS_CLOUD,
        verbose=verbose,
    )


@app.command()
def verify_config() -> None:
    """
    Verifies that the core configuration and environment variables are loaded correctly.
    """
    settings = get_settings()
    logger.info("Verifying configuration...")

    typer.echo("Configuration loaded successfully:")
    typer.echo(f" - Environment: {settings.APP_ENV}")
    typer.echo(f" - Is Cloud: {settings.IS_CLOUD}")
    typer.echo(f" - Base Dir: {settings.BASE_DIR}")

    logger.info("Configuration check completed")


if __name__ == "__main__":
    app()
