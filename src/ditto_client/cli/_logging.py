# ruff: noqa: B008

import asyncio
import json
from pathlib import Path
from typing import Optional

import typer
from kiota_abstractions.base_request_configuration import RequestConfiguration
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typer import Typer

from ditto_client.generated.devops.logging.logging_request_builder import LoggingRequestBuilder
from ditto_client.generated.models.logging_update_fields import LoggingUpdateFields

from ._utils import create_devops_client

logging_app = Typer()


@logging_app.command()
def get(
    include_disabled: bool = typer.Option(False, "--include-disabled", help="Include disabled loggers"),
    module_name: Optional[str] = typer.Option(None, "--module", "-m", help="Module name to get logging config for"),
) -> None:
    """Get logging configuration from Ditto services."""

    async def _run() -> None:
        client = create_devops_client()

        if module_name:
            # Get module-specific logging config
            response = await client.devops.logging.by_module_name(module_name).get()
        else:
            # Get general logging config
            query_params = LoggingRequestBuilder.LoggingRequestBuilderGetQueryParameters()
            query_params.include_disabled_loggers = include_disabled
            request_config = RequestConfiguration(query_parameters=query_params)
            response = await client.devops.logging.get(request_configuration=request_config)

        if not response:
            rprint("[yellow]No logging configuration found[/yellow]")
            return
        rprint(response)

    asyncio.run(_run())


@logging_app.command()
def update(
    update_file: Path = typer.Argument(..., help="Path to JSON file containing logging updates"),
) -> None:
    """Update logging configuration for Ditto services."""

    async def _run() -> None:
        client = create_devops_client()

        # Read the logging update data
        update_data = json.loads(update_file.read_text())

        # Create the logging update
        logging_update = LoggingUpdateFields(additional_data=update_data)

        response = await client.devops.logging.put(body=logging_update)

        if response:
            rprint("[green]Logging configuration updated successfully[/green]")
            # Display update results
            table = Table(title="Update Results")
            table.add_column("Service", justify="left", style="cyan")
            table.add_column("Status", justify="center", style="green")
            table.add_column("Message", justify="left", style="yellow")

            for result in response:
                status = "Success" if hasattr(result, "success") and result.success else "Failed"
                message = getattr(result, "message", "N/A") if hasattr(result, "message") else "N/A"
                service = getattr(result, "service", "Unknown") if hasattr(result, "service") else "Unknown"

                table.add_row(service, status, message)

            console = Console()
            console.print(table)
        else:
            rprint("[red]Failed to update logging configuration[/red]")

    asyncio.run(_run())
