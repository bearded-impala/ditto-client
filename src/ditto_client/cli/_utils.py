"""Centralized client creation utility for Ditto CLI."""

import os
from typing import Optional

from kiota_http.httpx_request_adapter import HttpxRequestAdapter

from ditto_client.basic_auth import BasicAuthProvider
from ditto_client.generated.ditto_client import DittoClient


def create_client(mode: Optional[str] = None) -> DittoClient:
    base_url = os.getenv("DITTO_BASE_URL", "http://host.docker.internal:8080")

    if mode == "devops":
        # Use devops credentials
        user_name = os.getenv("DITTO_USERNAME", "devops")
        password = os.getenv("DITTO_PASSWORD", "foobar")
    else:
        # Use default ditto credentials
        user_name = os.getenv("DITTO_USERNAME", "ditto")
        password = os.getenv("DITTO_PASSWORD", "ditto")

    auth_provider = BasicAuthProvider(user_name=user_name, password=password)
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = base_url

    return DittoClient(request_adapter)
