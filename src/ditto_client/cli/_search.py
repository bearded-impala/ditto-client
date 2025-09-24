# ruff: noqa: B008

import asyncio
import json
import os
from pathlib import Path
from typing import Optional

import typer
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typer import Typer

from ditto_client.basic_auth import BasicAuthProvider
from ditto_client.generated.api.two.search.things.count.count_request_builder import CountRequestBuilder
from ditto_client.generated.api.two.search.things.things_request_builder import ThingsRequestBuilder
from ditto_client.generated.ditto_client import DittoClient


def _create_client() -> DittoClient:
    """Create and configure a DittoClient instance."""
    username = os.getenv("DITTO_USERNAME", "ditto")
    password = os.getenv("DITTO_PASSWORD", "ditto")
    base_url = os.getenv("DITTO_BASE_URL", "http://host.docker.internal:8080")

    auth_provider = BasicAuthProvider(user_name=username, password=password)
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = base_url

    return DittoClient(request_adapter)


search_app = Typer()


@search_app.command()
def list(
    filter: Optional[str] = typer.Option(
        None, "--filter", "-f", help="RQL filter expression (e.g., 'eq(attributes/location,\"kitchen\")')"
    ),
    fields: Optional[str] = typer.Option(None, "--fields", help="Comma-separated list of fields to include"),
    namespaces: Optional[str] = typer.Option(
        None, "--namespaces", "-n", help="Comma-separated list of namespaces to search"
    ),
    option: Optional[str] = typer.Option(
        None, "--option", "-o", help="Search options (e.g., 'size(10),sort(+thingId)')"
    ),
    timeout: Optional[str] = typer.Option(None, "--timeout", "-t", help="Request timeout (e.g., '30s', '1m')"),
) -> None:
    """Search for things in Ditto."""

    async def _run() -> None:
        try:
            client = _create_client()

            # Build query parameters if provided
            request_config = None
            if filter or fields or namespaces or option or timeout:
                query_params = ThingsRequestBuilder.ThingsRequestBuilderGetQueryParameters()
                if filter:
                    query_params.filter = filter
                if fields:
                    query_params.fields = fields
                if namespaces:
                    query_params.namespaces = namespaces
                if option:
                    query_params.option = option
                if timeout:
                    query_params.timeout = timeout

                request_config = RequestConfiguration(query_parameters=query_params)

            response = await client.api.two.search.things.get(request_configuration=request_config)

            if not response:
                rprint("[yellow]No things found[/yellow]")
                return
        except Exception as e:
            if "connection" in str(e).lower() or "connect" in str(e).lower():
                rprint("[red]Connection failed![/red]")
                rprint("[yellow]Make sure Ditto is running and accessible.[/yellow]")
                return
            else:
                rprint(f"[red]Error: {e}[/red]")
                return

        # Create a table for better display
        table = Table(title="Ditto Things")
        table.add_column("Thing ID", justify="left", style="cyan", no_wrap=True)
        table.add_column("Features", justify="center", style="yellow")

        for thing in response.items:
            # Features is a Features object, not a dict, so we need to check if it has any data
            features_count = (
                len(thing.features.additional_data) if thing.features and thing.features.additional_data else 0
            )
            table.add_row(thing.thing_id, str(features_count))

        console = Console()
        console.print(table)

    asyncio.run(_run())


@search_app.command()
def count(
    filter: Optional[str] = typer.Option(
        None, "--filter", "-f", help="RQL filter expression (e.g., 'eq(attributes/location,\"kitchen\")')"
    ),
    namespaces: Optional[str] = typer.Option(
        None, "--namespaces", "-n", help="Comma-separated list of namespaces to search"
    ),
) -> None:
    """List things from Ditto."""

    async def _run() -> None:
        try:
            client = _create_client()

            # Build query parameters if provided
            request_config = None
            if filter or namespaces:
                query_params = CountRequestBuilder.CountRequestBuilderGetQueryParameters()
                if filter:
                    query_params.filter = filter
                if namespaces:
                    query_params.namespaces = namespaces

                request_config = RequestConfiguration(query_parameters=query_params)

            response = await client.api.two.search.things.count.get(request_configuration=request_config)
            rprint(f"[green]Total things: {response}[/green]")
        except Exception as e:
            rprint(f"[red]Error: {e}[/red]")
            return

    asyncio.run(_run())
