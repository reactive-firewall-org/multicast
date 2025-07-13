# Welcome to Multicast's documentation

## Quickstart

**Welcome to the Multicast Python Library! Let's get you started quickly.**

### Step 1: Install Python 3

* Ensure Python 3 is installed on your system.

  ![Python version](https://gist.github.com/reactive-firewall/33d74d2233ecb4ffe5a3891134fa0328/raw/cb3eff82d38d9213b4f0a678285e62ec87ff2dea/quickstart_step_1_tty.gif)

### Step 2: Clone the Repository

* Open your terminal and run:

  ```shell
  git clone https://github.com/reactive-firewall-org/multicast.git
  cd multicast
  ```

  ![Git clone](https://gist.github.com/reactive-firewall/33d74d2233ecb4ffe5a3891134fa0328/raw/cb3eff82d38d9213b4f0a678285e62ec87ff2dea/quickstart_step_2_tty.gif)

### Step 3: Install the Package

* Run:

  ```shell
  make install
  ```

  ![Make install](https://gist.github.com/reactive-firewall/33d74d2233ecb4ffe5a3891134fa0328/raw/cb3eff82d38d9213b4f0a678285e62ec87ff2dea/quickstart_step_3_tty.gif)

### Step 4: Sending Messages

* Send a message using:

  ```shell
  python3 -m multicast SAY --group 224.1.1.2 --port 59595 --message "Hello, Multicast!"
  ```

### Step 5: Receiving Messages

* Receive messages by running:

  ```shell
  python3 -m multicast RECV --use-std --port 59595 --groups 224.1.1.2
  ```

**You're all set! Enjoy using Multicast for your projects.**

---

## Overview

Multicast is a Python module designed to simplify raw multicast communication in Python
applications. It offers intuitive interfaces for sending and receiving multicast messages,
enabling developers to implement efficient and robust multicast functionality with ease.

### Key Features

* **Simple API**: Easy-to-use functions for sending (`send`) and receiving (`recv`) multicast
  messages.
* **Command-Line Interface**: Convenient CLI commands (`SAY`, `RECV`, `HEAR`) for quick testing
  and debugging.
* **Cross-Platform Support**: Compatible with Linux, UNIX, and macOS.

### Getting Started

* **Installation**: Install the package using `make install` or via `pip`.
* **Quickstart**: Refer to the [Quickstart](#quickstart) section for immediate setup instructions.
* **Examples**: Explore detailed examples and API references in the [Usage Guide](./USAGE).

### Documentation Resources

* [README](./README): Introduction and installation instructions.
* [Usage Guide](./USAGE): Detailed usage examples and API documentation.
* [FAQ](./FAQ): Frequently asked questions and troubleshooting tips.
* [Release Notes](https://github.com/reactive-firewall-org/multicast/releases): Release information.
* [Environment Configuration](./Environment_Configuration): Environment Configuration Guide.
* [CI Processes](./CI): Information on continuous integration and testing strategies.
* [Exceptions in `multicast`](./Exception_Guide): Information on exceptions and their handling in
  the `multicast` module.
* [License](./LICENSE): Licensing information and acknowledgments.

## Contents

```{toctree}
:maxdepth: 2
:Name: Documentation
apidocs/index
/README
/USAGE
/FAQ
/Environment_Configuration
/CI
/Testing
/Exception_Guide
/LICENSE
```

---

### Copyright (c) 2021-2025, Mr. Walls

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md)
