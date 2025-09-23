# Eclipse Ditto Client

Eclipse Ditto Project - https://eclipse.dev/ditto/index.html

This repository is the python client generated using Microsoft Kiota ([https://github.com/microsoft/kiota-python](https://github.com/microsoft/kiota-python))

## Install

```bash
uv add ditto-client
```

## Running Ditto

A sample docker compose is provided as part of this repository.

You must run the ditto services outside the devcontainer as they consume lot of resources.

```bash
# outside your devcontainer (i.e. on your host)
# at <your_path>/ditto-client dir
docker compose -f assets/ditto/docker-compose.yaml up
```

## Usage

```python
auth_provider = BasicAuthProvider(user_name=_USERNAME, password=_PASSWORD)

request_adapter = HttpxRequestAdapter(auth_provider)
request_adapter.base_url = "http://host.docker.internal:8080"

ditto_client = DittoClient(request_adapter)

response = await ditto_client.api.two.things.get()
```

Default setup for Ditto uses Ngix with basic authentication. A custom authentication provider has been included
in the library to support it. See [BasicAuth Provider](src/ditto_client/basic_auth.py).

[See examples/basic.py for the full usage](examples/basic.py)
