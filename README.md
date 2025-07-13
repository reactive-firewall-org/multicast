# Multicast Python Module

![Mcast Logo](https://github.com/reactive-firewall-org/multicast/blob/stable/Logo.svg)

## Introduction

The `multicast` package is a Python library that simplifies sending and receiving multicast network
messages. It provides classes and tools for implementing multicast communication in Python
applications, making it straightforward to work with multicast sockets.

## Features

* **Easy Multicast Communication**: Send and receive messages over multicast networks with
  simple `Python` interfaces.
* **Command-Line Tools**: Includes command-line utilities for quick multicast prototyping.
* **Cross-Python Compatibility**: Designed to work with multiple Python versions.
* **Support for UDP**: Works with UDP via IPv4 multicast addresses.

## Status

### Master (Development)

[![CircleCI](https://circleci.com/gh/reactive-firewall-org/multicast/tree/master.svg?style=svg)](https://circleci.com/gh/reactive-firewall-org/multicast/tree/master)
[![Minimal Acceptance Tests](https://github.com/reactive-firewall-org/multicast/actions/workflows/CI-MATs.yml/badge.svg?branch=master)](https://github.com/reactive-firewall-org/multicast/actions/workflows/CI-MATs.yml)
[![CI](https://github.com/reactive-firewall-org/multicast/actions/workflows/Tests.yml/badge.svg?branch=master)](https://github.com/reactive-firewall-org/multicast/actions/workflows/Tests.yml)
[![Appveyor](https://ci.appveyor.com/api/projects/status/0h5vuexyty9lbl81/branch/master?svg=true)](https://ci.appveyor.com/project/reactive-firewall-org/multicast/branch/master)
[![Documentation Status](https://readthedocs.org/projects/reactive-firewallmulticast/badge/?version=master)](https://reactive-firewallmulticast.readthedocs.io/en/latest/?badge=master)
[![Code Coverage](https://codecov.io/gh/reactive-firewall-org/multicast/branch/master/graph/badge.svg)](https://codecov.io/gh/reactive-firewall-org/multicast/branch/master/)
[![Coverage Status](https://coveralls.io/repos/github/reactive-firewall-org/multicast/badge.svg)](https://coveralls.io/github/reactive-firewall-org/multicast)
[![Bandit](https://github.com/reactive-firewall-org/multicast/actions/workflows/bandit.yml/badge.svg?branch=master)](https://github.com/reactive-firewall-org/multicast/actions/workflows/bandit.yml)
[![Style Status](https://github.com/reactive-firewall-org/multicast/actions/workflows/flake8.yml/badge.svg?branch=master&event=push)](https://github.com/reactive-firewall-org/multicast/actions/workflows/flake8.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/reactive-firewall-org/multicast/badge)](https://www.codefactor.io/repository/github/reactive-firewall-org/multicast)
![Size](https://img.shields.io/github/languages/code-size/reactive-firewall-org/multicast.svg)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall-org/multicast/?category=code)](https://github.com/reactive-firewall-org/multicast/)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall-org/multicast/?category=blanks)](https://github.com/reactive-firewall-org/multicast/)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall-org/multicast/?category=lines)](https://github.com/reactive-firewall-org/multicast/)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall-org/multicast/?category=comments)](https://github.com/reactive-firewall-org/multicast/)
![Commits-since](https://img.shields.io/github/commits-since/reactive-firewall-org/multicast/stable.svg?maxAge=9000)

### Stable (Mainstream)

[![Stable CI](https://github.com/reactive-firewall-org/multicast/actions/workflows/Tests.yml/badge.svg?branch=stable)](https://github.com/reactive-firewall-org/multicast/actions/workflows/Tests.yml)
[![Stable Appveyor](https://ci.appveyor.com/api/projects/status/0h5vuexyty9lbl81/branch/stable?svg=true)](https://ci.appveyor.com/project/reactive-firewall-org/multicast/branch/stable)
[![Stable Code Coverage](https://codecov.io/gh/reactive-firewall-org/multicast/branch/stable/graph/badge.svg)](https://codecov.io/gh/reactive-firewall-org/multicast/branch/stable/)
[![CodeQL](https://github.com/reactive-firewall-org/multicast/actions/workflows/codeql-analysis.yml/badge.svg?branch=stable)](https://github.com/reactive-firewall-org/multicast/actions/workflows/codeql-analysis.yml)

## Installation

Install the package using `pip`:

```bash
pip install multicast
```

<details><summary>Alternative Methods</summary>

There are many ways to install the module besides using `pip`, but unless you have a specific need,
using `pip` is recommended for most users.

### PEP-668 and externally-managed-environment installs

Users using Homebrew may require additional flags to use `pip`:

```bash
python3 -m pip install --use-pep517 --break-system-packages --user 'multicast>=2.0.8'
```

### Install from Source

*Source builds require development tools including (but not limited to): `git`, and `make`*

#### Stable builds (Release Candidates)

```bash
# clone the multicast source repository
git clone "https://github.com/reactive-firewall-org/multicast.git" multicast
cd multicast
# switch to the stable branch
git checkout stable
# build the multicast module
make -f Makefile build
# install the build
make user-install
# Optionally check the install
python3 -m multicast --version
```

#### Developer builds

> [!WARNING]
> **Development Builds** *(e.g., Cutting-Edge)* are not intended as full-fledged releases, however
> updates to the Development Builds are more frequent than releases.

```bash
# clone the multicast source repository
git clone "https://github.com/reactive-firewall-org/multicast.git" multicast
cd multicast
# switch to the default "master" branch
git checkout master
# build the multicast module
make -f Makefile build
# install the build
make user-install
# Optionally check the install
python3 -m multicast --version
```

### Legacy egg style install

> [!WARNING]
> **Egg Style Builds** *(Deprecated)* are not supported since version `2.1` :shrug:

```bash
pip install -e "git+https://github.com/reactive-firewall-org/multicast.git#egg=multicast"
```

</details>

## Getting Started

Below are basic examples to help you start using the `multicast` package.

### Sending Multicast Messages

```python3
from multicast import send

# Create a multicast sender
sender = send.McastSAY()

# Send a message
sender(group='224.0.0.1', port=59259, ttl=1, data='Hello, Multicast!')
```

### Receiving Multicast Messages

```python3
from multicast import recv

# Create a multicast receiver
receiver = recv.McastRECV()

# Receive a message
message = receiver(group='224.0.0.1', port=59259, ttl=1)
print('Received:', message)
```

### Listening for Multicast Messages

* Depending on what needs to be done with received data, each case will be a bit different.

```python3
# setup console logging as example
import logging
multicast_logging_sink = logging.getLogger()
handler = logging.StreamHandler()  # example trivial log handler
multicast_logging_sink.setLevel(logging.INFO)  # increase default logging from multicast module
multicast_logging_sink.addHandler(handler)

# import multicast
from multicast import hear

# Create a multicast listener
listener = hear.McastHEAR()

# Listen for messages indefinitely (use control+C to stop)
listener(group='224.0.0.1', port=59259, ttl=1)
```

> [!TIP]
> While this trivial example just scratches the surface, the `multicast.hear` module provides an
> extendable implementation of the default handler for customizing the listening behavior well
> beyond just logging.

## Command-Line Usage

The `multicast` package provides command-line tools for multicast communication prototyping.

* Read the [Usage](docs/USAGE.md) for details.

## FAQ

* Read the [FAQ](docs/FAQ.md) for common answers.

## Default Settings

* **Multicast Group Address**: `224.0.0.1` (link-local multicast as per
  [RFC 5771](https://tools.ietf.org/html/rfc5771))
* **Default Port**: `59259` (within the dynamic/private port range defined by
  [RFC 6335](https://tools.ietf.org/html/rfc6335))
* **Time-to-Live (TTL)**: `1` (as recommended by
  [RFC 1112 Section 6.1](https://tools.ietf.org/html/rfc1112#section-6.1)
  ; messages do not leave the local network)

## Security Considerations

In the realm of network communication, security is paramount. When using multicast communication,
be vigilant about potential vulnerabilities:

* **Data Sanitization**: Always sanitize incoming data to prevent injection attacks
  ([CWE-20](https://cwe.mitre.org/data/definitions/20.html),
  [CWE-74](https://cwe.mitre.org/data/definitions/74.html)).

* **Network Scope**: Be mindful of the TTL settings to limit message propagation to the intended
  network segment. Inappropriate TTL values might expose your multicast traffic beyond the local
  network, potentially leading to information disclosure
  ([CWE-200](https://cwe.mitre.org/data/definitions/200.html)).

* **Validation and Error Handling**: Implement robust validation and error handling to prevent
  misuse or disruption of multicast services.
  ([CWE-351](https://cwe.mitre.org/data/definitions/351.html)).

As Bruce Schneier aptly puts it, "Security is a process, not a product." Always be proactive in
assessing and mitigating risks in your implementations and use of `multicast`.

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9458/badge)](https://www.bestpractices.dev/projects/9458)

## Documentation

For more detailed documentation and advanced usage, please refer to the
[documentation](https://reactive-firewallmulticast.readthedocs.io/en/master/).

## Contributing

Contributions are welcome! Please read the
[contributing guidelines](https://github.com/reactive-firewall-org/multicast/tree/stable/.github/CONTRIBUTING)
for more information.

### Next steps

Next steps and bug fixes are tracked by the
[Multicast Project Board](https://github.com/users/reactive-firewall/projects/1).

## License

### Copyright (c) 2021-2025, Mr. Walls

The Multicast Python Module is licensed under the MIT License. See the
[LICENSE.md](https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md) file for
details.

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md)
