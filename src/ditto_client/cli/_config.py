# ruff: noqa: B008

import asyncio
import json
import os
from typing import Optional

import typer
from click import Argument
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typer import Typer

from ditto_client.cli.utils.create_client import create_client
from ditto_client.generated.devops.config.config_request_builder import ConfigRequestBuilder

config_app = Typer()


@config_app.command()
def get(
    module_name: Optional[str] = typer.Option(None, help="Module name to retrieve config for"),
    pod_name: Optional[str] = typer.Option(None, help="Pod name (requires module)"),
) -> None:
    """Get configuration from Ditto services."""

    async def _run() -> None:
        client = create_client("devops")

        if module_name and pod_name:
            response = await client.devops.config.by_module_name(module_name).by_pod_name(pod_name).get()
        else:
            response = await client.devops.config.get()

        if not response:
            rprint("[yellow]No configuration found[/yellow]")
            return
        rprint(response)

    asyncio.run(_run())
