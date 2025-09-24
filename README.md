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

| Command Group | Description | Credentials Used |
|---------------|-------------|------------------|
| `things` | Manage things (digital twins) | Standard (`ditto:ditto`) |
| `policies` | Manage access policies | Standard (`ditto:ditto`) |
| `search` | Search for things | Standard (`ditto:ditto`) |
| `connections` | Manage connections | DevOps (`devops:foobar`) |
| `config` | View service configuration | DevOps (`devops:foobar`) |
| `logging` | Manage logging configuration | DevOps (`devops:foobar`) |
| `permission` | Check permissions | DevOps (`ditto:ditto`) |
| `devops` | DevOps operations | Standard (`ditto:ditto`) |

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

### Create Policy

#### `ditto-client policy create <policy_id> <policy_file>`
Create a new policy.

```bash
# Create a new policy
ditto-client policy create "my.namespace:new-policy" examples/cli-examples/policy.json
```

#### `ditto-client policy get <policy_id>`
Retrieve a specific policy by ID.

```bash
# Get a policy
ditto-client policy get "my.namespace:my-policy"
```

#### `ditto-client policy entries <policy_id>`
List policy entries.

```bash
# List all policy entries
ditto-client policy entries "my.namespace:my-policy"
```

---

### Things Management

#### `ditto-client things create <thing_id> <data_file>`
Create a new thing.

```bash
# Create a new thing
ditto-client things create "my.namespace:new-thing" examples/cli-examples/thing.json
```

#### `ditto-client things list`
List all things with optional filtering.

```bash
# List all things
ditto-client things list

# List things with specific fields
ditto-client things list --fields "thingId,attributes"

# List specific things by ID
ditto-client things list --ids "my.namespace:new-thing"
```

#### `ditto-client things get <thing_id>`
Retrieve a specific thing by ID.

```bash
# Get a specific thing
ditto-client things get "my.namespace:my-thing"
```

#### `ditto-client things update <thing_id> <patch_file>`
Update a thing using JSON patch.

```bash
# Update a thing
ditto-client things update "my.namespace:my-thing" examples/cli-examples/thing.json
```

---

### Search Operations

#### `ditto-client search query`
Search for things using RQL (Resource Query Language).

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

#### `ditto-client search count`
Count things matching search criteria.

```bash
# Count all things
ditto-client search count

# Count things with filter
ditto-client search count --filter 'eq(attributes/location,"Kitchen")'
```

---

### Connection Management (DevOps)

#### `ditto-client connection create <connection_id>`
Create a new connection.

```bash
# Create a connection
ditto-client connection create "new-connection" --definition "connection-config"
```

#### `ditto-client connection list`
List all connections.

```bash
# List all connections
ditto-client connection list

# List with specific fields
ditto-client connection list --fields "id,connectionStatus"
```

#### `ditto-client connection get <connection_id>`
Retrieve a specific connection by ID.

```bash
# Get a connection
ditto-client connection get "my-connection"

# Get with specific fields
ditto-client connection get "my-connection" --fields "id,status"
```

---

### **CLEAN UP**

#### `ditto-client policy delete <policy_id>`
Delete policy.

```bash
# Delete a policy
ditto-client policy delete "my.namespace:my-policy"
```

#### `ditto-client things delete <thing_id>`
Delete a thing.

```bash
# Delete a thing
ditto-client things delete "my.namespace:my-thing"
```

#### `ditto-client connection delete <connection_id>`
Delete a connection.

```bash
# Delete a connection
ditto-client connection delete "my-connection"
```

---

### Configuration Management (DevOps)

#### `ditto-client config get`
Retrieve service configuration.

```bash
# Get all configuration
ditto-client config get
```

---

### Logging Management (DevOps)

#### `ditto-client logging get`
Retrieve logging configuration.

```bash
# Get logging configuration
ditto-client logging get

# Get module-specific config
ditto-client logging get --module "gateway"
```

#### `ditto-client logging update <update_file>`
Update logging configuration.

```bash
# Update logging configuration
ditto-client logging update examples/cli-examples/logging.json
```

---

### Permission Management (DevOps)

#### `ditto-client permission check <request_file>`
Check permissions on specified resources.

```bash
# Check permissions
ditto-client permission check examples/cli-examples/permission.json
```

---

### DevOps Operations

#### `ditto-client devops whoami`
Get current user information.

```bash
# Get current user info
ditto-client devops whoami
```
