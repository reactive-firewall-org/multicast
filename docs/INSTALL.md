# Installation

Install the package using `pip`:

```bash
pip install multicast
```

## Alternative Methods

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
git clone https://github.com/reactive-firewall-org/multicast.git multicast && cd ./multicast
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
pip install -e "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
```

***

If all went well, `multicast` is now installed and working :tada:

***

#### Copyright (c) 2021-2025, Mr. Walls

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md)
