# Usage

## Basic Library Usage

> [!NOTE]
> The API is in a continuous state of improvement, so version pinning is recommended for now.

### Listening to Multicast

The preferred way to receive multicast messages is to allow the `multicast.hear.McastServer`
template class to handle the ephemeral multicast receivers as a kind of multicast server, allowing
a handler to focus on processing the data.

Here is an example of multicast socket server usage (circa v2.1)

```python3
# imports
import multicast
from multiprocessing import Process
import random  # for random port

# Multicast group address and port
MCAST_GRP = "224.0.0.1"  # Replace with your multicast group address (use IPv4 dotted notation)
MCAST_PORT = int(random.SystemRandom().randint(49152, 65535))  # Replace with your multicast port

# Other important settings (Non-Multicast)
# Multicast does not care about the host IP, but the UDP protocol layer of the Python socket does
# There are 3 logical choices for the vast majority of users:
# 1. '0.0.0.0' for Promiscuous mode (Usually needs privileges to use on most Operating Systems)
# 2. The actual interface IPv4 dot notation address for unprivileged mode
# 3. MCAST_GRP value, Linux and MacOS implementations can let the system choose by passing the
#    MCAST_GRP to the Python socket.bind operation (handled by multicast.skt when missing Host IP)
#    Windows users must use option 1 or 2 for now.
# This address is per socket (e.g., can be chosen per socket even if on a single interface)
# HOST_BIND_IP = "0.0.0.0"

# Options for multicast listener
listener_options = {
    "is_daemon": True,  # bool: enable daemon mode
    "port": MCAST_PORT,  # int: UDP port for multicast
    "group": MCAST_GRP  # str: multicast group address (use IPv4 dotted notation)
}

# Create a multicast listener
listener = multicast.hear.McastHEAR()

# create a separate process for the listener
p = Process(
    target=listener,
    name="HEAR", kwargs=listener_options
)
p.daemon = listener_options["is_daemon"]
p.start()

# ... use CTL+C (or signal 2) to shutdown the server 'p'
```

> [!IMPORTANT]
> The above example probably will return with nothing outside a handler function in a loop,
> unless you enable the default logging beforehand with:
>
> ```python3
> # setup console logging as example
> import logging
> multicast_logging_sink = logging.getLogger()
> multicast_logging_sink.setLevel(logging.INFO)  # increase default logging from multicast module
> handler = logging.StreamHandler()  # example trivial log handler
> multicast_logging_sink.addHandler(handler)
> 
> # import multicast
> from multicast import hear
>
> # Create a multicast listener
> listener = hear.McastHEAR()
>
> # Listen for messages indefinitely (use control+C to stop)
> listener(group='224.0.0.1', port=59595, ttl=1)
> ```

### Sending Multicast Transmissions

```python3
# imports
import multicast
from multiprocessing import Process

# Multicast group address and port
MCAST_GRP = "224.0.0.1"  # Replace with your multicast group address (use IPv4 dotted notation)
MCAST_PORT = 59595  # Replace with your multicast port (use the same port as the listeners)

# Other important settings (Non-Multicast)
# Multicast does not care about the host IP, but the UDP protocol layer of the Python socket does
# The sender will default to letting the system choose
# HOST_BIND_IP = "0.0.0.0"

# Options for multicast sender
sender_options = {
    "port": MCAST_PORT,  # int: UDP port for multicast
    "group": MCAST_GRP,  # str: multicast group address (use IPv4 dotted notation)
    "data": "Default listener only knows: STOP"  # str: message content to try to _transmit_
}

# Create an ephemeral multicast sender
sender = multicast.send.McastSAY()

# create a separate process for the sender
p = Process(
    target=sender,
    name="SAY", kwargs=sender_options
)
p.daemon = False  # sender should not be a daemon

try:
    p.start()
except Exception as baton:
    p.join()  # good practice to handle clean up
    raise RuntimeError("multicast seems to have failed.") from baton  # re-raise
finally:
    # clean up some stuff
    if p:
        p.join() # if not already handled don't forget to join the process and other overhead
    # hint: if you use a loop and need to know the exit code
    didWork = (p is not None and p.exitcode <= 0)  # e.g. check for success

```

## Advanced Library Usage

### Custom handlers

> [!TIP]
> The API for custom handlers currently requires implementing a subclass
> `multicast.hear.HearUDPHandler` and handling the listener's `multicast.hear.McastServer` server
> directly with something like this:
>
> ```python3
> from multicast.hear import McastServer, HearUDPHandler
> with McastServer((MCAST_GRP, MCAST_PORT), HearUDPHandler) as server:
>     server_initialized = True
>     server.serve_forever()  # ... use CTL+C (or signal 2) to shutdown the server
> ```
>
> This is essentially what the
> [default listener does under-the-hood](https://github.com/reactive-firewall-org/multicast/blob/v2.0.9a5/multicast/hear.py#L830C4-L832C27)
> automatically.

### Direct ephemeral receiver with an ad-hoc handler

In the unusual case where the `multicast.hear.McastServer` provides insufficient control, there is
still the option of directly handling the ephemeral receiver, before resorting to low-level raw
sockets. The complication is that developers will need to provide some kind of ad-hoc handler.

```python3
# imports
import multicast
import random  # for random port

# Multicast group address and port
MCAST_GRP = "224.0.0.1"  # Replace with your multicast group address (use IPv4 dotted notation)
MCAST_PORT = int(random.SystemRandom().randint(49152, 65535))  # Replace with your multicast port

# Note
# Multicast does not care about the host IP, but the UDP protocol layer of the Python socket does
# There are 3 logical choices for the vast majority of users:
# 1. '0.0.0.0' for Promiscuous mode (Usually needs privileges to use on most Operating Systems)
# 2. The actual interface IPv4 dot notation address for unprivileged mode
# 3. None, Linux and MacOS implementations can let the system choose by passing the
#    MCAST_GRP to the Python socket.bind operation (handled by multicast.skt when missing Host IP)
#    Windows users must use option 1 or 2 for now.
# This address is per socket (e.g., can be chosen per socket even if on a single interface)
# The module will by default choose option 1 unless a valid interface name is passed in.

# Options for multicast listener
listener_options = {
    "is_daemon": False,  # bool: enable/disable daemon mode
    "groups": [MCAST_GRP],  # list[str]: multicast group addresses (use IPv4 dotted notation list)
    "port": MCAST_PORT,  # int: UDP port for multicast
    "iface": None,  # str: System specific interface name, or None to let system choose
    "group": MCAST_GRP  # str: primary multicast group address (use IPv4 dotted notation)
}

# Example setup for Low-Level use-case
# Define a decorator to loop until able to print a string result of enough length
import functools


def printLoopStub(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            # cache function result
            cache = func(*args, **kwargs)
            if cache and len(cache) > 1:
                print( str( cache ) )
                break
            elif not cache:
                continue
            else:
                print("Result is too short.")
    return wrapper


# Example low-level handler
# Define a decorated handler to only return successfully received messages


@printLoopStub
def inputHandler():
    # Create an ephemeral multicast receiver
    receiver = multicast.recv.McastRECV()
    # create an empty default string
    out_string = str()
    # try to receive some multicast messages
    (didWork, buffer_string) = receiver(
        **listener_options
    )
    # check the result and "handle" if successful
    if didWork:
        out_string += buffer_string
    del receiver  # optionally cleanup receiver beforehand
    return out_string


# create the actual handler instance
inputHandler()

```

***

## CLI Usage

The CLI is actually not the best way to use this kind of library, so it should not be considered
the full implementation. For testing and prototyping, though, it is quite convenient; therefore,
I begin with it.

CLI should work like so:

```plain
multicast [[-h|--help]|[--version] [--use-std] [--daemon] (SAY|RECV|HEAR)
    [-h|--help]
    [--port PORT]
    [--iface IFACE]
    [-m MESSAGE|--message MESSAGE|--pipe]
    [--group BIND_GROUP]
    [--groups [JOIN_MCAST_GROUPS ...]]
```

The commands are `SAY`, `RECV`, and `HEAR` for the CLI and are analogous to `send` listen/accept
and echo functions of a 1-to-1 connection.

### `SAY`

The `SAY` command is used to send data messages via multicast datagrams.

* Note: the `--message` flag is expected with the `SAY` command;
  if neither `--pipe` nor `--messages` are provided, `SAY` behaves like `NOOP`.
* Note: the `--daemon` flag has no effect on the `SAY` command.
* Note: the `--pipe` option reads message from stdin (added in v2.1.0, equivalent to `--message -`).

### `RECV`

The `RECV` command is used to receive multicast datagrams by listening or "joining" a multicast
group.

* If the `--use-std` flag is set, the output is printed to the standard-output.
* This command is purely for testing or interfacing with external components and not intended as a
  first-class API
* Note: If the `--daemon` flag is used the process will loop after reporting each datagrams until
  canceled, it has no effect on the `RECV` command.

### `HEAR`

The `HEAR` command is used to send data acknowledged messages via "HEAR" messages echoing select
received multicast datagrams.

* While mostly a testing function, it is possible to use `HEAR` as a proxy for other send/recv
  instances by using the `--daemon` flag
* Note: this will use the same port for sends and receives and can lead to data loss if less than
  two groups are used.
* If more than one group is used via the `--groups` flag, then all but the bind group
  (via `--group`) will be echoed to the bind group.

***

#### Copyright (c) 2021-2025, Mr. Walls

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md)
