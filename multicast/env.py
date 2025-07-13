#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__package__ = "multicast"  # skipcq: PYL-W0622
"""
The package of this component.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Env should be automatically imported.

		>>> multicast.env.__package__ is not None
		True
		>>>
		>>> multicast.env.__package__ == multicast.__package__
		True
		>>>

"""

__module__ = "multicast.env"
"""
The module of this component.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Env should be automatically imported.

		>>> multicast.env.__module__ is not None
		True
		>>>

"""

__file__ = "multicast/env.py"
"""The file of this component."""

__name__ = "multicast.env"  # skipcq: PYL-W0622
"""The name of this component.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Env should be automatically imported.

		>>> multicast.env.__name__ is not None
		True
		>>>

"""

try:
	import os
	import warnings
	from . import logging  # skipcq: PLY-C0414
	from . import socket  # skipcq: PYL-C0414
	import ipaddress
except ImportError as _cause:
	baton = ImportError(_cause, "[CWE-758] Module failed completely.")
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = _cause
	raise baton from _cause


module_logger = logging.getLogger(__module__)
module_logger.debug(
	"Loading %s",  # lazy formatting to avoid PYL-W1203
	__module__,
)
module_logger.debug(
	"Initializing %s environment.",  # lazy formatting to avoid PYL-W1203
	__package__,
)


def validate_buffer_size(size: int) -> bool:
	"""
	Validate if the buffer size is a positive integer.

	Arguments:
		size (int) -- The buffer size to validate.

	Returns:
		bool: True if the buffer size is valid ( > 0), False otherwise.

	Raises:
		ValueError: If the size cannot be converted to an integer.

	Minimum Acceptance Testing:
		>>> validate_buffer_size(1316)  # Default value
		True
		>>> validate_buffer_size(1)  # Minimum valid value
		True
		>>> validate_buffer_size(0)  # Zero is invalid
		False
		>>> validate_buffer_size(-1)  # Negative is invalid
		False
		>>> validate_buffer_size(65507)  # Maximum UDP payload size 65,535 -8 -20 (RFC-791 & RFC-768)
		True
		>>> validate_buffer_size("1316")  # String that can be converted
		True
		>>> try:
		...     validate_buffer_size('invalid')
		... except ValueError:
		...     print('ValueError raised')
		ValueError raised

	"""
	try:
		size_num = int(size)
		return 0 < size_num <= 65507
	except (ValueError, TypeError) as _cause:
		raise ValueError(f"Invalid buffer size value: {size}. Must be a positive integer.") from _cause


def validate_port(port: int) -> bool:
	"""
	Validate if the port number is within the dynamic/private port range.

	Rational for requiring within the dynamic/private port range: This is only setting the default,
	and can be overridden by the client code on a case-by-case basis. By requiring **default**
	port values to be within the dynamic/private port range, the design is following the principle
	of "secure by default" and the open/closed principle.

	Arguments:
		port (int) -- The port number to validate.

	Returns:
		bool: True if the port is valid (49152-65535), False otherwise.

	Raises:
		ValueError: If the port cannot be converted to an integer.

	Minimum Acceptance Testing:
		>>> validate_port(49152)
		True
		>>> validate_port(65535)
		True
		>>> validate_port(1024)
		False
		>>> validate_port(70000)
		False
		>>> try:
		...     validate_port('invalid')
		... except ValueError:
		...     print('ValueError raised')
		ValueError raised
	"""
	try:
		port_num = int(port)
		return 49152 <= port_num <= 65535
	except (ValueError, TypeError) as _cause:  # pragma: no branch
		raise ValueError(f"Invalid port value: {port}. Must be an integer.") from _cause


def validate_multicast_address(addr: str) -> bool:
	"""
	Validate if the address is a valid multicast address.

	Arguments:
		addr (str) -- The IP address to validate.

	Returns:
		bool: True if the address is a valid multicast address (224.0.0.0/4), False otherwise.

	Minimum Acceptance Testing:
		>>> validate_multicast_address('224.0.0.1')
		True
		>>> validate_multicast_address('239.255.255.255')
		True
		>>> validate_multicast_address('192.168.1.1')
		False
		>>> validate_multicast_address('invalid')
		False
	"""
	try:
		ip = ipaddress.IPv4Address(addr)
		return ip.is_multicast
	except (ValueError, AttributeError):  # pragma: no branch
		return False


def validate_ttl(ttl: int) -> bool:
	"""
	Validate if the TTL value is within the valid range as per RFC-1112.

	Arguments:
		ttl (int) -- The TTL value to validate.

	Returns:
		bool: True if the TTL is valid (1-126), False otherwise.

	Raises:
		ValueError: If the TTL cannot be converted to an integer.

	Minimum Acceptance Testing:
		>>> validate_ttl(1)
		True
		>>> validate_ttl(126)
		True
		>>> validate_ttl(0)
		False
		>>> validate_ttl(127)
		False
		>>> try:
		...     validate_ttl('invalid')
		... except ValueError:
		...     print('ValueError raised')
		ValueError raised
	"""
	try:
		ttl_num = int(ttl)
		return 1 <= ttl_num <= 126
	except (ValueError, TypeError) as _cause:  # pragma: no branch
		raise ValueError(
			f"Invalid TTL value: {ttl}. Must be a positive integer below 127.",
		) from _cause


def load_buffer_size() -> int:
	"""
	Load and validate the multicast buffer size from environment variable.

	This function attempts to load the buffer size from the MULTICAST_BUFFER_SIZE
	environment variable. If the value is valid, it returns the buffer size.
	Invalid values trigger warnings and fall back to the default.

	MTU Considerations for Buffer Size:
		When setting a buffer size, consider the MTU of the underlying network:
		- Ethernet: 1500 bytes MTU → 1472 bytes max payload (1500 - 28 bytes overhead)
		- PPP: 296 bytes MTU → 268 bytes max payload
		- Wi-Fi (802.11): 2304 bytes MTU → 2276 bytes max payload
		- Frame Relay: 128 bytes MTU → 100 bytes max payload

		The overhead consists of:
		- UDP header: 8 bytes
		- IP header: 20 bytes (without options)

		Setting buffer sizes larger than the network's max payload may cause IP
		fragmentation, which can lead to performance issues and increased complexity.

	Returns:
		int: The validated buffer size, or the default value if not set/invalid.

	Environment:
		MULTICAST_BUFFER_SIZE -- The buffer size in bytes.

	Raises:
		ImportError: If the multicast module cannot be imported.

	Minimum Acceptance Testing:

	Testcase 0: Setup test fixtures.
		>>> import os
		>>> from multicast import _MCAST_DEFAULT_BUFFER_SIZE
		>>> original_buffer = _MCAST_DEFAULT_BUFFER_SIZE

	Testcase 1: Test with valid environment variable
		>>> os.environ["MULTICAST_BUFFER_SIZE"] = "2048"
		>>> buffer_size = load_buffer_size()
		>>> buffer_size
		2048
		>>> # The function updates the global in the module's namespace, but this doesn't affect
		>>> # the imported value in the test namespace
		>>> _MCAST_DEFAULT_BUFFER_SIZE != 2048  # Global in test namespace is not updated
		True

	Testcase 2: Test with invalid (negative) environment variable
		>>> os.environ["MULTICAST_BUFFER_SIZE"] = "-100"
		>>> import warnings
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     buffer_size = load_buffer_size()
		...     len(w) == 1  # One warning was issued
		True
		>>> buffer_size == 1316  # Falls back to default
		True

	Testcase 3: Test with invalid (zero) environment variable
		>>> os.environ["MULTICAST_BUFFER_SIZE"] = "0"
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     buffer_size = load_buffer_size()
		...     len(w) == 1  # One warning was issued
		True
		>>> buffer_size == 1316  # Falls back to default
		True

	Testcase 4: Test with invalid (non-integer) environment variable
		>>> os.environ["MULTICAST_BUFFER_SIZE"] = 'not_an_integer'
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     buffer_size = load_buffer_size()
		...     len(w) == 1  # One warning was issued
		True
		>>> buffer_size == 1316  # Falls back to default
		True

	Testcase 5: Test with no environment variable
		>>> if "MULTICAST_BUFFER_SIZE" in os.environ: os.environ.pop("MULTICAST_BUFFER_SIZE")
		'not_an_integer'
		>>> buffer_size = load_buffer_size()
		>>> buffer_size == 1316  # Uses default
		True

		# Cleanup
		>>> globals()['_MCAST_DEFAULT_BUFFER_SIZE'] = original_buffer

	"""
	# Import globals that we'll potentially update
	from multicast import _MCAST_DEFAULT_BUFFER_SIZE
	module_logger.debug("Looking for MULTICAST_BUFFER_SIZE in environment.")
	try:
		buffer_size = int(os.getenv(
			"MULTICAST_BUFFER_SIZE",
			_MCAST_DEFAULT_BUFFER_SIZE  # skipcq: PYL-W1508
		))
		module_logger.debug("Done.")
	except (ValueError, TypeError):  # pragma: no branch
		warnings.warn(
			f"Invalid MULTICAST_BUFFER_SIZE value, using default {_MCAST_DEFAULT_BUFFER_SIZE}",
			stacklevel=2,
		)
		buffer_size = _MCAST_DEFAULT_BUFFER_SIZE  # skipcq: PYL-W1508
	# Validate and potentially update buffer-size
	module_logger.debug("Validating MULTICAST_BUFFER_SIZE.")
	if validate_buffer_size(buffer_size):
		globals()["_MCAST_DEFAULT_BUFFER_SIZE"] = buffer_size
		module_logger.debug("Valid.")
	else:
		warnings.warn(
			f"Invalid MULTICAST_BUFFER_SIZE {buffer_size}, using default {_MCAST_DEFAULT_BUFFER_SIZE}",
			stacklevel=2,
		)
		buffer_size = _MCAST_DEFAULT_BUFFER_SIZE
	module_logger.debug(
		"Loaded %s as internal multicast buffer size.",  # lazy formatting to avoid PYL-W1203
		str(buffer_size),
	)
	return buffer_size


def load_port() -> int:
	"""
	Load and validate the multicast port from environment variable.

	This function attempts to load the port number from the MULTICAST_PORT
	environment variable. If the value is valid, it updates the global
	_MCAST_DEFAULT_PORT. Invalid values trigger warnings and fall back to
	the default.

	Returns:
		int: The validated port number to use for multicast operations.
			Returns the default port if the environment value is invalid.

	Raises:
		ImportError: If the multicast module cannot be imported.

	Minimum Acceptance Testing:

	Testcase 0: Setup test fixtures.

		>>> import os
		>>> from multicast import _MCAST_DEFAULT_PORT
		>>> original_port = _MCAST_DEFAULT_PORT

	Testcase 1: Test with valid port.

		>>> os.environ['MULTICAST_PORT'] = '50000'
		>>> port = load_port()
		>>> type(port) == type(int(0))
		True
		>>> port
		50000
		>>> type(_MCAST_DEFAULT_PORT) == type(int(0))  # Global is an int
		True
		>>> _MCAST_DEFAULT_PORT != 50000  # Global was Not updated
		True

	Testcase 2: Test with invalid numeric port

		>>> os.environ['MULTICAST_PORT'] = '1024'
		>>> import warnings
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     port = load_port()
		...     len(w) == 1  # One warning was issued
		True
		>>> port == original_port  # Falls back to original default
		True
		>>> os.environ.pop('MULTICAST_PORT', None)
		'1024'
		>>>

	Testcase 3: Test with non-numeric port.

		>>> os.environ['MULTICAST_PORT'] = 'invalid'
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     port = load_port()
		...     len(w) == 1  # One warning was issued
		True
		>>> port == original_port  # Falls back to original default
		True
		>>> os.environ.pop('MULTICAST_PORT', None)
		'invalid'
		>>>

	Testcase 4: Test with unset environment variable.

		>>> os.environ.pop('MULTICAST_PORT', None)
		>>> port = load_port()
		>>> port == original_port  # Uses default
		True

		# Cleanup
		>>> globals()['_MCAST_DEFAULT_PORT'] = original_port
	"""
	# Import globals that we'll potentially update
	from multicast import _MCAST_DEFAULT_PORT
	module_logger.debug("Looking for MULTICAST_PORT in environment.")
	try:
		port = int(os.getenv("MULTICAST_PORT", _MCAST_DEFAULT_PORT))
		module_logger.debug("Done.")
	except (ValueError, TypeError):  # pragma: no branch
		warnings.warn(
			f"Invalid MULTICAST_PORT value, using default {_MCAST_DEFAULT_PORT}", stacklevel=2,
		)
		port = _MCAST_DEFAULT_PORT
	# Validate and potentially update port
	module_logger.debug("Validating MULTICAST_PORT.")
	if validate_port(port):
		globals()["_MCAST_DEFAULT_PORT"] = port
		module_logger.debug("Valid.")
	else:
		warnings.warn(
			f"Port {port} is outside valid range (49152-65535), using default {_MCAST_DEFAULT_PORT}",
			stacklevel=2,
		)
		port = _MCAST_DEFAULT_PORT
	module_logger.debug(
		"Loaded %s as default multicast port.",  # lazy formatting to avoid PYL-W1203
		str(port),
	)
	return port


def load_group() -> ipaddress.IPv4Address:
	"""
	Load and validate the multicast group from environment variable.

	This function attempts to load the multicast group address from the
	MULTICAST_GROUP environment variable. If the value is valid, it updates
	the global _MCAST_DEFAULT_GROUP. Invalid values trigger warnings and
	fall back to the default.

	Returns:
		ipaddress.IPv4Address: The validated IPv4 multicast address.
			Returns the default group if the environment value is invalid.

	Raises:
		ImportError: If the multicast module cannot be imported.
		ValueError: If the default group is not a valid IPv4 address.

	Minimum Acceptance Testing:

	Testcase 0: Setup test fixtures.

		>>> import os
		>>> from multicast import _MCAST_DEFAULT_GROUP
		>>> original_group = _MCAST_DEFAULT_GROUP

	Testcase 1: Test with valid multicast group

		>>> os.environ['MULTICAST_GROUP'] = '224.0.0.2'
		>>> group = load_group()
		>>> str(group)
		'224.0.0.2'
		>>> group
		IPv4Address('224.0.0.2')
		>>> _MCAST_DEFAULT_GROUP != '224.0.0.2'  # Global was NOT updated
		True

		# reset global after test.
		>>> globals()['_MCAST_DEFAULT_GROUP'] = original_group
		>>> os.environ.pop('MULTICAST_GROUP', None)
		'224.0.0.2'
		>>>

	Testcase 2: Test with invalid multicast group
		A. Start with empty MULTICAST_GROUP
		B. Set an invalid MULTICAST_GROUP ip value.
		C. Use `load_group()` to load the builtin default.
		D. Verify builtin default was loaded and a warning was issued.
		E. Verify MULTICAST_GROUP is still the same IP.

		>>> os.environ.pop('MULTICAST_GROUP', None)
		>>> os.environ['MULTICAST_GROUP'] = '192.168.1.1'
		>>> import warnings
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     group = load_group()
		...     len(w) == 1  # One warning was issued
		True
		>>> str(group) == original_group  # Falls back to original default
		True
		>>> os.environ.pop('MULTICAST_GROUP', None)
		'192.168.1.1'
		>>>

	Testcase 3: Test with invalid IP format.
		A. Start with empty MULTICAST_GROUP
		B. Set an invalid MULTICAST_GROUP value.
		C. Use `load_group()` to load the builtin default.
		D. Verify builtin default was loaded and a warning was issued.
		E. Verify MULTICAST_GROUP is still invalid.

		>>> os.environ.pop('MULTICAST_GROUP', None)
		>>> os.environ['MULTICAST_GROUP'] = 'invalid'
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     group = load_group()
		...     len(w) == 1  # One warning was issued
		True
		>>> str(group) == original_group  # Falls back to original default
		True
		>>> os.environ.pop('MULTICAST_GROUP', None)
		'invalid'
		>>>

	Testcase 4: Test with unset environment variable.
		A. Start with empty MULTICAST_GROUP
		B. Use `load_group()` to load the builtin default.
		C. Verify builtin default was loaded.
		D. Verify MULTICAST_GROUP is still empty (None).

		>>> os.environ.pop('MULTICAST_GROUP', None)
		>>> group = load_group()
		>>> str(group) == original_group  # Uses default
		True
		>>> os.environ.pop('MULTICAST_GROUP', None)  # still None
		>>>

		# Cleanup
		>>> globals()['_MCAST_DEFAULT_GROUP'] = original_group
	"""
	# Import globals that we'll potentially update
	from multicast import _MCAST_DEFAULT_GROUP
	module_logger.debug("Looking for any MULTICAST_GROUP in environment.")
	group = os.getenv("MULTICAST_GROUP", _MCAST_DEFAULT_GROUP)
	# Validate and potentially update group
	module_logger.debug("Validating either MULTICAST_GROUP or default.")
	if validate_multicast_address(group):
		globals()["_MCAST_DEFAULT_GROUP"] = group
		module_logger.debug("Valid.")
	else:
		warnings.warn(
			f"Invalid multicast group {group}, using default {_MCAST_DEFAULT_GROUP}", stacklevel=2,
		)
		group = _MCAST_DEFAULT_GROUP
	module_logger.debug(
		"Loaded %s as default multicast group.",  # lazy formatting to avoid PYL-W1203
		group,
	)
	return ipaddress.IPv4Address(group)


def load_TTL() -> int:
	"""
	Load and validate the TTL value from environment variable.

	This function attempts to load the Time-To-Live value from the
	MULTICAST_TTL environment variable. If the value is valid, it updates
	the global _MCAST_DEFAULT_TTL and the socket default timeout. Invalid
	values trigger warnings and fall back to the default.

	Returns:
		int: The validated TTL value (1-126).
			Returns the default TTL if the environment value is invalid.

	Raises:
		ImportError: If the multicast module cannot be imported.

	Minimum Acceptance Testing:

	Testcase 0: Setup
		>>> import os
		>>> import socket
		>>> from multicast import _MCAST_DEFAULT_TTL
		>>> original_ttl = _MCAST_DEFAULT_TTL
		>>> original_timeout = socket.getdefaulttimeout()

	Testcase 1: Test with valid TTL
		>>> os.environ['MULTICAST_TTL'] = '2'
		>>> ttl = load_TTL()
		>>> ttl
		2
		>>> _MCAST_DEFAULT_TTL != 2  # Global was NOT updated
		True
		>>> socket.getdefaulttimeout() == 2  # Socket timeout was updated
		True

	Testcase 2: Test with invalid numeric TTL
		>>> os.environ['MULTICAST_TTL'] = '127'
		>>> import warnings
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     ttl = load_TTL()
		...     len(w) == 1  # One warning was issued
		True
		>>> ttl == original_ttl  # Falls back to original default
		True

	Testcase 3: Test with non-numeric TTL
		>>> os.environ['MULTICAST_TTL'] = 'invalid'
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     ttl = load_TTL()
		...     len(w) == 1  # One warning was issued
		True
		>>> ttl == original_ttl  # Falls back to original default
		True
		>>> os.environ.pop('MULTICAST_TTL', None)
		'invalid'
		>>>

	Testcase 4: Test with unset environment variable
		>>> os.environ.pop('MULTICAST_TTL', None)
		>>> ttl = load_TTL()
		>>> ttl == original_ttl  # Uses default
		True

		# Cleanup
		>>> globals()['_MCAST_DEFAULT_TTL'] = original_ttl
		>>> socket.setdefaulttimeout(original_timeout)
	"""
	# Import globals that we'll potentially update
	from multicast import _MCAST_DEFAULT_TTL
	module_logger.debug("Looking for MULTICAST_TTL in environment.")
	try:
		ttl = int(os.getenv("MULTICAST_TTL", _MCAST_DEFAULT_TTL))
		module_logger.debug("Done.")
	except (ValueError, TypeError):  # pragma: no branch
		warnings.warn(
			f"Invalid MULTICAST_TTL value, using default {_MCAST_DEFAULT_TTL}", stacklevel=2,
		)
		ttl = _MCAST_DEFAULT_TTL
	# Validate and potentially update TTL
	module_logger.debug("Validating MULTICAST_TTL.")
	if validate_ttl(ttl):
		globals()["_MCAST_DEFAULT_TTL"] = ttl
		module_logger.debug("Valid.")
	else:
		warnings.warn(
			f"TTL {ttl} is outside valid range (1-126), using default {_MCAST_DEFAULT_TTL}",
			stacklevel=2,
		)
		ttl = _MCAST_DEFAULT_TTL
	module_logger.debug(
		"Loaded %d as default multicast time-to-live.",  # lazy formatting to avoid PYL-W1203
		ttl,
	)
	# Update socket default timeout
	module_logger.debug("Update socket default timeout.")
	socket.setdefaulttimeout(int(ttl))
	module_logger.debug("Updated.")
	return ttl


def load_config() -> dict:
	"""
	Load multicast configuration from environment variables.

	This function loads configuration settings from environment variables,
	validates them, and updates the global defaults if valid. Invalid values
	trigger warnings and fall back to defaults.

	Returns:
		dict: A dictionary containing the validated configuration with the following keys:
			- port (int): The port number (49152-65535)
			- group (str): The primary multicast group address
			- groups (list): List of multicast group addresses to join
			- ttl (int): Time-to-live value (1-126) used as the Socket timeout in seconds
			- bind_addr (str): Address to bind to
			- buffer_size (int): Receive buffer size

	Minimum Acceptance Testing:

	First set up test fixtures by importing os.

		>>> import os

	Testcase 0: Test with unset environment variables.
		A: Test with unset environment variables value falls back to defaults.

		>>> for key in ['MULTICAST_PORT', 'MULTICAST_GROUP', 'MULTICAST_GROUPS']:
		...     os.environ.pop(key, None)
		>>> config = load_config()
		>>> config['port'] == _MCAST_DEFAULT_PORT
		True
		>>> config['group'] == _MCAST_DEFAULT_GROUP
		True
		>>> _MCAST_DEFAULT_GROUP in config['groups']
		True
		>>>

	Testcase 1: Test with valid values

		>>> os.environ['MULTICAST_PORT'] = '50000'
		>>> os.environ['MULTICAST_GROUP'] = '224.0.0.2'
		>>> os.environ['MULTICAST_GROUPS'] = '224.0.0.1 224.0.0.2'
		>>> os.environ['MULTICAST_TTL'] = '2'
		>>> config = load_config()
		>>> config['port']
		50000
		>>> config['group']
		'224.0.0.2'
		>>> sorted(config['groups'])
		['224.0.0.1', '224.0.0.2']
		>>> config['ttl']
		2

	Testcase 2: Test with invalid group (falls back to default)

		>>> os.environ['MULTICAST_GROUP'] = '224.0.0.2'
		>>> os.environ['MULTICAST_GROUPS'] = '192.168.1.1 224.0.0.2'
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     config = load_config()
		...     len(w) > 0  # Warning was issued
		True
		>>> config['group'] in config['groups']  # Valid multicast group is included in groups
		True
		>>> '224.0.0.2' in config['groups']  # Valid multicast group address is included in groups
		True
		>>> '192.168.1.1' in config['groups']  # Invalid value omitted
		False
		>>> os.environ.pop('MULTICAST_GROUP', None)
		'224.0.0.2'
		>>>

		# Cleanup
		>>> os.environ.pop('MULTICAST_GROUPS', None)
		'192.168.1.1 224.0.0.2'
		>>>

	Testcase 3: Test with invalid port (falls back to default)

		>>> os.environ['MULTICAST_PORT'] = '1024'
		>>> import warnings
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     config = load_config()
		...     len(w) > 0  # Warning was issued
		True
		>>> config['port'] == _MCAST_DEFAULT_PORT  # Falls back to default
		True
		>>> os.environ.pop('MULTICAST_PORT', None)
		'1024'
		>>>

	Testcase 4: Test with invalid group (falls back to default)

		>>> os.environ['MULTICAST_GROUP'] = '192.168.1.1'
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     config = load_config()
		...     len(w) > 0  # Warning was issued
		True
		>>> config['group'] == _MCAST_DEFAULT_GROUP  # Falls back to default
		True
		>>> os.environ.pop('MULTICAST_GROUP', None)
		'192.168.1.1'
		>>>

	Testcase 5: Test with valid multicast bind address.

		>>> os.environ['MULTICAST_BIND_ADDR'] = '224.0.0.3'
		>>> config = load_config()
		>>> config['bind_addr']
		'224.0.0.3'
		>>> '224.0.0.3' in config['groups']  # Valid multicast bind address is included in groups
		True
		>>> len(config['groups']) >= 2  # Contains at least bind_addr and default group
		True

	Testcase 6: Test with invalid multicast bind address.

		>>> os.environ['MULTICAST_BIND_ADDR'] = '192.168.1.1'
		>>> config = load_config()
		>>> config['bind_addr']
		'192.168.1.1'
		>>> '192.168.1.1' not in config['groups']  # Invalid multicast address not in groups
		True
		>>> _MCAST_DEFAULT_GROUP in config['groups']  # Still contains default group
		True

	Testcase 7: Test with invalid IP format in bind address.

		>>> os.environ['MULTICAST_BIND_ADDR'] = 'invalid-ip'
		>>> config = load_config()
		>>> config['bind_addr']
		'invalid-ip'
		>>> len(config['groups']) == 1  # Only contains default group
		True
		>>> _MCAST_DEFAULT_GROUP in config['groups']
		True

		# Cleanup
		>>> os.environ.pop('MULTICAST_BIND_ADDR', None)
		'invalid-ip'
		>>>

	Testcase 8: Test with valid positive buffer size.

		>>> os.environ['MULTICAST_BUFFER_SIZE'] = '2048'
		>>> config = load_config()
		>>> config['buffer_size']
		2048
		>>> isinstance(config['buffer_size'], int)  # Ensures integer type
		True

	Testcase 9: Test with valid minimum buffer size.

		>>> os.environ['MULTICAST_BUFFER_SIZE'] = '1'
		>>> config = load_config()
		>>> config['buffer_size']
		1
		>>> isinstance(config['buffer_size'], int)
		True

	Testcase 10: Test with invalid negative buffer size.

		>>> os.environ['MULTICAST_BUFFER_SIZE'] = '-1024'
		>>> import warnings
		>>> with warnings.catch_warnings(record=True) as w:
		...     warnings.simplefilter("always")
		...     config = load_config()
		...     len(w) == 1  # expected warning was issued
		True
		>>> config['buffer_size'] == _MCAST_DEFAULT_BUFFER_SIZE  # Falls back to default
		True

		# Cleanup
		>>> os.environ.pop('MULTICAST_BUFFER_SIZE', None)
		'-1024'
		>>> config = None
		>>>

	Testcase 11: Test with non-numeric buffer size.

		>>> os.environ['MULTICAST_BUFFER_SIZE'] = 'invalid'
		>>> try:
		...     config = load_config()
		... except ValueError:
		...     print('ValueError raised')
		>>> # Verify config is not None (load_config should handle the error and use default)
		>>> config is not None
		True

		# Cleanup
		>>> os.environ.pop('MULTICAST_BUFFER_SIZE', None)
		'invalid'
		>>>

	"""
	# Load values from environment with defaults
	module_logger.info("Loading multicast overrides from environment.")
	port = load_port()
	group = load_group()
	ttl = load_TTL()
	buffer_size = load_buffer_size()
	module_logger.debug("Looking for MULTICAST_GROUPS in environment.")
	groups_str = os.getenv("MULTICAST_GROUPS", "")
	module_logger.debug("Done.")
	module_logger.debug("Looking for MULTICAST_BIND_ADDR in environment.")
	bind_addr = os.getenv("MULTICAST_BIND_ADDR", str(group))  # skipcq: PYL-W1508
	module_logger.debug("Done.")
	# Process and validate groups
	module_logger.debug("Processing and validating groups.")
	groups = set()
	if groups_str:
		for addr in groups_str.split():
			if validate_multicast_address(addr):
				groups.add(str(addr))
			else:
				warnings.warn(
					f"Invalid multicast group {addr} in MULTICAST_GROUPS, skipping", stacklevel=2,
				)
	# Always include the primary group
	groups.add(str(group))
	module_logger.debug("Processed groups.")
	# Include bind_addr if it's a valid multicast address
	module_logger.debug("Processing and validating bind-address.")
	if validate_multicast_address(bind_addr):
		module_logger.debug("Adding multicast bind-address to groups.")
		groups.add(str(bind_addr))
	module_logger.debug("Processed bind-address.")
	module_logger.debug("Overrides and defaults are ready to configure.")
	return {
		"port": port,
		"group": str(group),
		"groups": sorted(groups),  # Convert to sorted list for consistent ordering
		"ttl": ttl,
		"bind_addr": bind_addr,
		"buffer_size": buffer_size
	}


# skipcq
__all__ = [
	"""__package__""",
	"""__module__""",
	"""__name__""",
	"""__doc__""",  # skipcq: PYL-E0603
	"""validate_buffer_size""",
	"""validate_port""",
	"""validate_multicast_address""",
	"""validate_ttl""",
	"""load_config""",
]
