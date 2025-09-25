# ruff: noqa: B008

import asyncio
from typing import Optional

import typer
from rich import print as rprint
from typer import Typer

from ditto_client.generated.models.retrieve_config import RetrieveConfig
from ditto_client.generated.models.retrieve_config_service import RetrieveConfigService

from ._utils import create_devops_client

config_app = Typer()


@config_app.command()
def get() -> None:
    """Get configuration from Ditto services."""

    async def _run() -> None:
        client = create_devops_client()

        response = await client.devops.config.get()

        if not response:
            rprint("[yellow]No configuration found[/yellow]")
            return

        rprint(response)

    asyncio.run(_run())
