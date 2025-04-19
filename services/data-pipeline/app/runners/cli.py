import asyncio
import typer
from app.run_pipeline import run_all, register_all

cli = typer.Typer(help="CLI tool for running data pipelines.")


@cli.command("register")
def register_pipelines(
    source: str = typer.Option(None, help="Source name (e.g., krakenexchange)"),
    pipeline: str = typer.Option(None, help="Pipeline name (e.g., ohlcpipeline)"),
):
    """
    Register all pipelines without executing them.
    """

    async def _run():
        await register_all(source, pipeline)

    asyncio.run(_run())


@cli.command("run")
def run_pipelines(
    source: str = typer.Option(None, help="Source name (e.g., krakenexchange)"),
    pipeline: str = typer.Option(None, help="Pipeline name (e.g., ohlcpipeline)"),
):
    """
    Register and run all pipelines.
    """
    asyncio.run(run_all(source, pipeline))


@cli.command("say-hello")
def say_hello(name: str = "world"):
    """
    Simple hello command for testing CLI.
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    cli()
