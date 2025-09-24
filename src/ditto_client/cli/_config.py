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

from ditto_client.basic_auth import BasicAuthProvider
from ditto_client.generated.devops.config.config_request_builder import ConfigRequestBuilder
from ditto_client.generated.ditto_client import DittoClient


def _create_client() -> DittoClient:
    """Create and configure a DittoClient instance."""
    username = os.getenv("DITTO_USERNAME", "devops")
    password = os.getenv("DITTO_PASSWORD", "foobar")
    base_url = os.getenv("DITTO_BASE_URL", "http://host.docker.internal:8080")

    auth_provider = BasicAuthProvider(user_name=username, password=password)
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = base_url

    return DittoClient(request_adapter)


config_app = Typer()


@config_app.command()
def get(
    module_name: str = typer.Argument(..., help="Module name to retrieve config for"),
    pod_name: str = typer.Argument(..., help="Pod name (requires module)"),
) -> None:
    """Get configuration from Ditto services."""

    async def _run() -> None:
        try:
            client = _create_client()

            if module_name and pod_name:
                # Get specific pod config
                response = await client.devops.config.by_module_name(module_name).by_pod_name(pod_name).get()
                if not response:
                    rprint("[yellow]No configuration found[/yellow]")
                    return
                rprint(response)

        except Exception as e:
            if "connection" in str(e).lower() or "connect" in str(e).lower():
                rprint("[red]Connection failed![/red]")
                rprint("[yellow]Make sure Ditto is running and accessible.[/yellow]")
                return
            else:
                rprint(f"[red]Error: {e}[/red]")
                return

    asyncio.run(_run())
