# ruff: noqa: B008

import asyncio
import os

import typer
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typer import Typer

from ditto_client.basic_auth import BasicAuthProvider
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


devops_app = Typer()


@devops_app.command()
def whoami() -> None:
    """Get current user information."""

    async def _run() -> None:
        client = _create_client()

        response = await client.api.two.whoami.get()

        if not response:
            rprint("[red]Failed to get user information[/red]")
            return

        # Create a table for better display
        table = Table(title="Current User Information")
        table.add_column("Property", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", justify="left", style="green")

        table.add_row("Default Subject", response.default_subject or "N/A")
        table.add_row("Subjects", ", ".join(response.subjects) if response.subjects else "None")

        console = Console()
        console.print(table)

    asyncio.run(_run())
