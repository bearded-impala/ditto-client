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
from ditto_client.generated.models.module import Module
from ditto_client.generated.models.module_updated_log_level import ModuleUpdatedLogLevel
from ditto_client.generated.models.result_update_request import ResultUpdateRequest
from ditto_client.generated.models.retrieve_logging_config import RetrieveLoggingConfig

from ._utils import create_devops_client

logging_app = Typer()


@logging_app.command()
def get(
    module_name: Optional[str] = typer.Option(None, help="Module name to get logging config for"),
) -> None:
    """Get logging configuration from Ditto services."""

    async def _run() -> None:
        client = create_devops_client()

        response: Module | RetrieveLoggingConfig | None

        if module_name:
            # Get module-specific logging config
            response = await client.devops.logging.by_module_name(module_name).get()
        else:
            # Get general logging config
            query_params = LoggingRequestBuilder.LoggingRequestBuilderGetQueryParameters()
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
    module_name: Optional[str] = typer.Option(None, help="Module name to update logging config for"),
) -> None:
    """Update logging configuration for Ditto services."""

    async def _run() -> None:
        client = create_devops_client()

        # Read the logging update data
        update_data = json.loads(update_file.read_text())

        # Create the logging update
        logging_update = LoggingUpdateFields(additional_data=update_data)

        response: ModuleUpdatedLogLevel | list[ResultUpdateRequest] | None

        if module_name:
            response = await client.devops.logging.by_module_name(module_name).put(body=logging_update)
        else:
            response = await client.devops.logging.put(body=logging_update)

        rprint(response)

    asyncio.run(_run())
