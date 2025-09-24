# ruff: noqa: B008

import asyncio
from typing import Optional

import typer
from kiota_abstractions.base_request_configuration import RequestConfiguration
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typer import Typer

from ditto_client.generated.api.two.search.things.count.count_request_builder import CountRequestBuilder
from ditto_client.generated.api.two.search.things.things_request_builder import ThingsRequestBuilder

from ._utils import create_ditto_client

search_app = Typer()


@search_app.command()
def query(
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
        client = create_ditto_client()

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

        # Create a table for better display
        table = Table(title="Ditto Things")
        table.add_column("Thing ID", justify="left", style="cyan", no_wrap=True)
        table.add_column("Features", justify="center", style="yellow")

        if response.items:
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
        client = create_ditto_client()

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

    asyncio.run(_run())
