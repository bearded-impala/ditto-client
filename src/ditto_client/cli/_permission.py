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

from ditto_client.basic_auth import BasicAuthProvider
from ditto_client.generated.ditto_client import DittoClient
from ditto_client.generated.models.permission_check_request import PermissionCheckRequest


def _create_client() -> DittoClient:
    """Create and configure a DittoClient instance."""
    username = os.getenv("DITTO_USERNAME", "devops")
    password = os.getenv("DITTO_PASSWORD", "foobar")
    base_url = os.getenv("DITTO_BASE_URL", "http://host.docker.internal:8080")

    auth_provider = BasicAuthProvider(user_name=username, password=password)
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = base_url

    return DittoClient(request_adapter)


permission_app = Typer()


@permission_app.command()
def check(
    request_file: Path = typer.Argument(..., help="Path to JSON file containing permission check request"),
) -> None:
    """Check permissions on specified resources."""

    async def _run() -> None:
        try:
            client = _create_client()

            # Read the permission check request data
            request_data = json.loads(request_file.read_text())

            # Create the permission check request
            permission_request = PermissionCheckRequest(additional_data=request_data)

            response = await client.api.two.check_permissions.post(body=permission_request)

            if not response:
                rprint("[red]Permission check failed[/red]")
                return
        except Exception as e:
            if "connection" in str(e).lower() or "connect" in str(e).lower():
                rprint("[red]Connection failed![/red]")
                rprint("[yellow]Make sure Ditto is running and accessible.[/yellow]")
                return
            else:
                rprint(f"[red]Error: {e}[/red]")
                return

        # Display the permission check results
        if response.additional_data:
            rprint("[green]Permission Check Results:[/green]")
            rprint(json.dumps(response.additional_data, indent=2, default=str))
        else:
            rprint("[yellow]No permission check results returned[/yellow]")

    asyncio.run(_run())
