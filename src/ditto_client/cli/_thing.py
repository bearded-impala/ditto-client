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

from ditto_client.cli._utils import create_client
from ditto_client.generated.api.two.things.things_request_builder import ThingsRequestBuilder
from ditto_client.generated.models.new_thing import NewThing
from ditto_client.generated.models.patch_thing import PatchThing

thing_app = Typer()


@thing_app.command()
def list(
    fields: Optional[str] = typer.Option(
        None, "--fields", "-f", help="Comma-separated list of fields to include (e.g., 'thingId,attributes,features')"
    ),
    ids: Optional[str] = typer.Option(None, "--ids", help="Comma-separated list of thing IDs to retrieve"),
    timeout: Optional[str] = typer.Option(None, "--timeout", "-t", help="Request timeout (e.g., '30s', '1m')"),
) -> None:
    """List things from Ditto."""

    async def _run() -> None:
        client = create_client()

        # Build query parameters if provided
        request_config = None
        if fields or ids or timeout:
            query_params = ThingsRequestBuilder.ThingsRequestBuilderGetQueryParameters()
            if fields:
                query_params.fields = fields
            if ids:
                query_params.ids = ids
            if timeout:
                query_params.timeout = timeout

            request_config = RequestConfiguration(query_parameters=query_params)

        response = await client.api.two.things.get(request_configuration=request_config)

        if not response:
            rprint("[yellow]No things found[/yellow]")
            return

        # Create a table for better display
        table = Table(title="Ditto Things")
        table.add_column("Thing ID", justify="left", style="cyan", no_wrap=True)
        table.add_column("Features", justify="center", style="yellow")

        for thing in response:
            # Features is a Features object, not a dict, so we need to check if it has any data
            features_count = (
                len(thing.features.additional_data) if thing.features and thing.features.additional_data else 0
            )
            table.add_row(thing.thing_id, str(features_count))

        console = Console()
        console.print(table)

    asyncio.run(_run())


@thing_app.command()
def get(
    thing_id: str = typer.Argument(..., help="The ID of the thing to retrieve"),
) -> None:
    """Get a specific thing by ID."""

    async def _run() -> None:
        client = create_client()

        response = await client.api.two.things.by_thing_id(thing_id).get()
        rprint(response)

        if not response:
            rprint(f"[red]Thing '{thing_id}' not found[/red]")
            return

    asyncio.run(_run())


@thing_app.command()
def create(
    thing_id: str = typer.Argument(..., help="The ID of the thing to create"),
    data_file: Path = typer.Argument(..., help="Path to JSON file containing thing additional data"),
) -> None:
    """Create a new thing."""

    async def _run() -> None:
        client = create_client()

        # Build the thing data
        thing_data = json.loads(data_file.read_text())

        # Create the new thing
        new_thing = NewThing(additional_data=thing_data)

        response = await client.api.two.things.by_thing_id(thing_id).put(body=new_thing)

        if response:
            rprint(f"[green]Successfully created thing '{thing_id}'[/green]")
        else:
            rprint(f"[red]Failed to create thing '{thing_id}'[/red]")

    asyncio.run(_run())


@thing_app.command()
def update(
    thing_id: str = typer.Argument(..., help="The ID of the thing to update"),
    patch_file: Path = typer.Argument(..., help="Path to JSON patch file"),
) -> None:
    """Update a thing using JSON patch."""

    async def _run() -> None:
        client = create_client()

        # Read the patch data
        patch_data = json.loads(patch_file.read_text())

        # Create the patch thing
        patch_thing = PatchThing(additional_data=patch_data)

        await client.api.two.things.by_thing_id(thing_id).patch(body=patch_thing)
        rprint(f"[green]Successfully updated thing '{thing_id}'[/green]")

    asyncio.run(_run())


@thing_app.command()
def delete(
    thing_id: str = typer.Argument(..., help="The ID of the thing to delete"),
    confirm: bool = typer.Option(False, "--confirm", help="Skip confirmation prompt"),
) -> None:
    """Delete a thing."""

    if not confirm:
        if not typer.confirm(f"Are you sure you want to delete thing '{thing_id}'?"):
            rprint("[yellow]Operation cancelled[/yellow]")
            return

    async def _run() -> None:
        client = create_client()

        await client.api.two.things.by_thing_id(thing_id).delete()
        rprint(f"[green]Successfully deleted thing '{thing_id}'[/green]")

    asyncio.run(_run())
