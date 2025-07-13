# Environment Configuration Module

## Overview

The `multicast.env` module provides environment-based configuration for the multicast package,
allowing runtime customization of network settings through environment variables.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MULTICAST_PORT` | 59259 | Port number for multicast communication (49152-65535) |
| `MULTICAST_GROUP` | "224.0.0.1" | Primary multicast group address (224.0.0.0/4) |
| `MULTICAST_GROUPS` | - | Space-separated list of additional multicast addresses |
| `MULTICAST_TTL` | 1 | Time-to-live value (1-126) |
| `MULTICAST_BIND_ADDR` | "0.0.0.0" | Address to bind to |
| `MULTICAST_BUFFER_SIZE` | 1316 | Receive buffer size in bytes |

## Usage

### Basic Configuration

```python
import os  # used to set environment

# Set custom configuration
os.environ['MULTICAST_PORT'] = '50000'
os.environ['MULTICAST_GROUP'] = '224.0.0.2'

# see os.environ['MULTICAST_GROUPS'] for multi-group config

# Uncommonly there is need to increase TTL and BUFFER size,
# however users probably want raw sockets in those cases.
# os.environ['MULTICAST_TTL'] = '2'  # May harm your own bandwidth when increasing
# os.environ['MULTICAST_BUFFER_SIZE'] = '2048'  # Expect increased data loss when increasing

# Configuration loads on import
import multicast
```

### Multiple Group Configuration

```python
# Join multiple multicast groups
os.environ['MULTICAST_GROUPS'] = '224.0.0.1 224.0.0.2 224.0.0.3'
# Configuration loads on import
import multicast

# load config
from multicast.env import load_config
config = load_config()

# you can now access the configuration
# e.g.
print(config['groups'])  # ['224.0.0.1', '224.0.0.2', '224.0.0.3']
```

_(changing the resulting config values only causes the setting to lose its special value,
and does not actually update Multicast after import)_

## Configuration Details

### Port Configuration

- Valid range: 49152-65535 (dynamic/private ports)
- Invalid values trigger a warning and fall back to default
- Example:

  ```python
  os.environ['MULTICAST_PORT'] = '50000'
  ```

### Group Configuration

- Must be valid multicast addresses (224.0.0.0/4)
- Invalid addresses trigger a warning and fall back to default
- Example:

  ```python
  os.environ['MULTICAST_GROUP'] = '224.0.0.2'
  ```

### TTL Configuration

- Valid range: 1-126 (as per RFC-1112)
- Also sets socket default timeout
- Example:

  ```python
  os.environ['MULTICAST_TTL'] = '2'
  ```

### Buffer Size Configuration

- Must be positive integer
- Invalid values trigger a warning and fall back to default
- Example:

  ```python
  os.environ['MULTICAST_BUFFER_SIZE'] = '2048'
  ```

## Caveat

- Environment variables must be set before importing the module
- Invalid values trigger a warnings but won't cause failures
- Changes to configuration affect all subsequent operations

## References

- [RFC-1112: Host Extensions for IP Multicasting](https://datatracker.ietf.org/doc/html/rfc1112)
- [RFC-6335: IANA Port Number Registry](https://datatracker.ietf.org/doc/html/rfc6335)

---

### Copyright (c) 2024-2025, Mr. Walls

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md)
