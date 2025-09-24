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

## Usage - CLI

The Ditto client includes a comprehensive CLI for interacting with Eclipse Ditto services. The CLI provides the following commands:

| Command Group | Description |
|---------------|-------------|
| `policy` | Manage access policies |
| `thing` | Manage things (digital twins) |
| `search` | Search for things |
| `connection` | Manage connections |
| `devops` | DevOps operations |
| `permission` | Check permissions |
| `config` | View service configuration |
| `logging` | Manage logging configuration |


### Global Configuration

The CLI uses the following environment variables, you can set it as per your environment:

```bash
export DITTO_BASE_URL="http://host.docker.internal:8080"
export DITTO_USERNAME="ditto"
export DITTO_PASSWORD="ditto"
export DITTO_DEVOPS_USERNAME="devops"
export DITTO_DEVOPS_PASSWORD="foobar"
```

---

### Policy Management

#### Create a new policy.

`ditto-client policy create <policy_id> <policy_file>`

```bash
# Create a new policy
ditto-client policy create "my.namespace:new-policy" examples/cli-examples/policy.json
```

#### Retrieve a specific policy by ID.

`ditto-client policy get <policy_id>`

```bash
# Get a policy
ditto-client policy get "my.namespace:my-policy"
```

#### List policy entries.

`ditto-client policy entries <policy_id>`

```bash
# List all policy entries
ditto-client policy entries "my.namespace:my-policy"
```

#### Delete policy.

`ditto-client policy delete <policy_id>`

```bash
# Delete a policy
ditto-client policy delete "my.namespace:my-policy"
```

---

### Things Management

#### Create a new thing.

`ditto-client thing create <thing_id> <data_file>`

```bash
# Create a new thing
ditto-client thing create "my.namespace:new-thing" examples/cli-examples/thing.json
```

#### List all things with optional filtering.

`ditto-client thing list`

```bash
# List all things
ditto-client thing list

# List things with specific fields
ditto-client thing list --fields "thingId,attributes"

# List specific things by ID
ditto-client thing list --ids "my.namespace:new-thing"
```

#### Retrieve a specific thing by ID.

`ditto-client thing get <thing_id> [--revision <revision>]`

```bash
# Get a specific thing
ditto-client thing get "my.namespace:my-thing"

# Get a specific revision of a thing
ditto-client thing get "my.namespace:my-thing" --revision 1
```

#### Update a thing using JSON file.

`ditto-client thing update <thing_id> <patch_file>`

```bash
# Update a thing
ditto-client thing update "my.namespace:my-thing" examples/cli-examples/thing.json
```

#### Compare current thing with historical revision.

`ditto-client thing diff <thing_id> <revision>`

```bash
# Compare current state with revision 1
ditto-client thing diff "my.namespace:my-thing" 1
```

#### Delete a thing.

`ditto-client thing delete <thing_id>`

```bash
# Delete a thing
ditto-client thing delete "my.namespace:my-thing"
```

---

### Search Operations

#### Search for things using RQL (Resource Query Language).

`ditto-client search query`

```bash
# Search all things
ditto-client search query

# Search with filter
ditto-client search query --filter 'eq(attributes/location,"Kitchen")'

# Search with size limit and sorting
ditto-client search query --option "size(3),sort(+thingId)"

# Search in specific namespaces
ditto-client search query --namespaces "my.namespace"
```

#### Count things matching search criteria.

`ditto-client search count`

```bash
# Count all things
ditto-client search count

# Count things with filter
ditto-client search count --filter 'eq(attributes/location,"Kitchen")'
```

---

### Connection Management (DevOps)

#### Create a new connection.

`ditto-client connection create <connection_id>`

```bash
# Create a connection
ditto-client connection create "new-connection" --definition "connection-config"
```

#### List all connections.

`ditto-client connection list`

```bash
# List all connections
ditto-client connection list

# List with specific fields
ditto-client connection list --fields "id,connectionStatus"
```

#### Retrieve a specific connection by ID.

`ditto-client connection get <connection_id>`

```bash
# Get a connection
ditto-client connection get "my-connection"

# Get with specific fields
ditto-client connection get "my-connection" --fields "id,status"
```

#### Delete a connection.

`ditto-client connection delete <connection_id>`

```bash
# Delete a connection
ditto-client connection delete "my-connection"
```

---

### Configuration Management (DevOps)

#### Retrieve service configuration.

```bash
# Get all configuration
ditto-client config get
```

---

### Logging Management (DevOps)

#### Retrieve logging configuration.

`ditto-client logging get`

```bash
# Get logging configuration
ditto-client logging get

# Get module-specific config
ditto-client logging get --module "gateway"
```

#### Update logging configuration.

`ditto-client logging update <update_file>`

```bash
# Update logging configuration
ditto-client logging update examples/cli-examples/logging.json
```

---

### Permission Management (DevOps)

#### Check permissions on specified resources.

`ditto-client permission check <request_file>`

```bash
# Check permissions
ditto-client permission check examples/cli-examples/permission.json
```

---

### DevOps Operations

#### Get current user information.

```bash
# Get current user info
ditto-client devops whoami
```
