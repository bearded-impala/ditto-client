# Eclipse Ditto Client

Eclipse Ditto Project - https://eclipse.dev/ditto/index.html

This repository is the python client generated using Microsoft Kiota ([https://github.com/microsoft/kiota-python](https://github.com/microsoft/kiota-python))

## Install

```bash
uv add ditto-client
```

## Basic Authentication

Default setup for Ditto uses Ngix with basic authentication.

A custom authentication provider (src/ditto_client/basic_auth.py) has been included to support it.

[See examples/basic.py for the usage](examples/basic.py)
