# ruff: noqa: B008

import asyncio
import json
import os
from pathlib import Path
from typing import Optional

import typer
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typer import Typer

from ditto_client.cli.utils.create_client import create_client
from ditto_client.generated.models.policy import Policy

policy_app = Typer()


@policy_app.command()
def get(
    policy_id: str = typer.Argument(..., help="The ID of the policy to retrieve"),
) -> None:
    """Get a specific policy by ID."""

    async def _run() -> None:
        client = create_client()

        response = await client.api.two.policies.by_policy_id(policy_id).get()

        if not response:
            rprint(f"[red]Policy '{policy_id}' not found[/red]")
            return

        rprint(response)

    asyncio.run(_run())


@policy_app.command()
def create(
    policy_id: str = typer.Argument(..., help="The ID of the policy to create"),
    policy_file: Path = typer.Argument(..., help="Path to JSON file containing policy definition"),
) -> None:
    """Create a new policy."""

    async def _run() -> None:
        client = create_client()

        # Read the policy data
        policy_data = json.loads(policy_file.read_text())

        # Create the new policy
        new_policy = Policy(**policy_data)

        response = await client.api.two.policies.by_policy_id(policy_id).put(body=new_policy)

        if response:
            rprint(f"[green]Successfully created policy '{policy_id}'[/green]")
            rprint(response)
        else:
            rprint(f"[red]Failed to create policy '{policy_id}'[/red]")

    asyncio.run(_run())


@policy_app.command()
def delete(
    policy_id: str = typer.Argument(..., help="The ID of the policy to delete"),
    confirm: bool = typer.Option(False, "--confirm", help="Skip confirmation prompt"),
) -> None:
    """Delete a policy."""

    if not confirm:
        if not typer.confirm(f"Are you sure you want to delete policy '{policy_id}'?"):
            rprint("[yellow]Operation cancelled[/yellow]")
            return

    async def _run() -> None:
        client = create_client()

        await client.api.two.policies.by_policy_id(policy_id).delete()
        rprint(f"[green]Successfully deleted policy '{policy_id}'[/green]")

    asyncio.run(_run())


@policy_app.command()
def entries(
    policy_id: str = typer.Argument(..., help="The ID of the policy"),
    subject_id: Optional[str] = typer.Option(None, "--subject-id", help="Filter by subject ID"),
) -> None:
    """List policy entries."""

    async def _run() -> None:
        client = create_client()

        response = await client.api.two.policies.by_policy_id(policy_id).entries.get()

        if not response:
            rprint("[yellow]No policy entries found[/yellow]")
            return

        rprint(response)

    asyncio.run(_run())
