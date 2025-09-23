# Eclipse Ditto Client

Eclipse Ditto Project - https://eclipse.dev/ditto/index.html

This repository is the python client generated using Microsoft Kiota ([https://github.com/microsoft/kiota-python](https://github.com/microsoft/kiota-python))

## Install

```bash
uv add ditto-client
```

## Usage

```python
auth_provider = BasicAuthProvider(user_name=_USERNAME, password=_PASSWORD)

request_adapter = HttpxRequestAdapter(auth_provider)
request_adapter.base_url = "http://localhost:8080"

ditto_client = DittoClient(request_adapter)

response = await ditto_client.api.two.things.get()
```

Default setup for Ditto uses Ngix with basic authentication. A custom authentication provider has been included
in the library to support it. See [BasicAuth Provider](src/ditto_client/basic_auth.py).

[See examples/basic.py for the full usage](examples/basic.py)
