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

import sys
import abc
import argparse
import logging
import socket
import struct
import unicodedata

# skipcq
__all__ = [
	"""__package__""",
	"""__module__""",
	"""__name__""",
	"""__version__""",
	"""__prologue__""",
	"""__doc__""",
	"""exceptions""",
	"""exceptions.CommandExecutionError""",  # skipcq: PYL-E0603 -- imports ok
	"""exceptions.ShutdownCommandReceived""",  # skipcq: PYL-E0603 -- imports ok
	"""exceptions.get_exit_code_from_exception""",  # skipcq: PYL-E0603 -- imports ok
	"""exceptions.exit_on_exception""",  # skipcq: PYL-E0603 -- imports ok
	"""get_exit_code_from_exception""",
	"""exit_on_exception""",
	"""env""",
	"""skt""",
	"""skt.__package__""",  # skipcq: PYL-E0603 -- shadow imports ok
	"""skt.__module__""",  # skipcq: PYL-E0603 -- shadow imports ok
	"""skt.__name__""",  # skipcq: PYL-E0603 -- shadow imports ok
	"""skt.__file__""",  # skipcq: PYL-E0603 -- shadow imports ok
	"""skt.genSocket""",  # skipcq: PYL-E0603 -- shadow imports ok
	"""skt.genSocket.__func__""",  # skipcq: PYL-E0603 -- shadow imports ok
	"""genSocket""",  # skipcq: PYL-E0603 -- imports ok
	"""skt.endSocket""",  # skipcq: PYL-E0603 -- imports ok
	"""skt.endSocket.__func__""",  # skipcq: PYL-E0603 -- shadow imports ok
	"""endSocket""",  # skipcq: PYL-E0603 -- imports ok
	"""EXIT_CODES""",
	"""EXCEPTION_EXIT_CODES""",
	"""_BLANK""",
	"""_MCAST_DEFAULT_BUFFER_SIZE""",  # added in version 2.0.6
	"""_MCAST_DEFAULT_PORT""",
	"""_MCAST_DEFAULT_GROUP""",
	"""_MCAST_DEFAULT_TTL""",
	"""mtool""",
	"""recv""",
	"""send""",
	"""hear""",
	"""recv.McastRECV""",  # skipcq: PYL-E0603 -- imports ok
	"""send.McastSAY""",  # skipcq: PYL-E0603 -- imports ok
	"""hear.McastHEAR""",  # skipcq: PYL-E0603 -- imports ok
]

__path__ = [__file__[0:-12]]
"""The sequence of strings enumerating the locations where the package’s submodules will be found.

	The `__path__` attribute, like many dunder attributes, is associated with the implementation
	of Python language features. When utilizing this module as an imported module or a
	command-line interface (CLI) tool, the `__path__` attribute can be safely disregarded.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__path__ is not None
		True
		>>>

	Testcase 0: multicast.__path__ should be a list.
		A: Test that the __path__ attribute is initialized.
		B: Test that the __path__ attribute has contents.
		C: Test that the __path__ attribute has a value of "multicast" somewhere in the first item.

		>>> _multicast.__path__ is not None
		True
		>>> type(_multicast.__path__)
		<class 'list'>
		>>> _multicast.__name__ in _multicast.__path__[0]
		True
		>>>

"""

__package__ = "multicast"  # skipcq: PYL-W0622
"""The package of this program.

	The `__package__` attribute, like many dunder attributes, was associated with the implementation
	of Python language features. When utilizing this module as an imported module or a
	command-line interface (CLI) tool, the `__package__` attribute can be safely disregarded.
	Within the context of this module, `__package__` serves as a convenient constant that holds
	the name of the package.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__package__ is not None
		True
		>>>

	Testcase 0: multicast.__package__ should be the string "multicast".
		A: Test that the __package__ attribute is initialized.
		B: Test that the __package__ attribute is a string.
		C: Test that the __package__ attribute has a value of "multicast".

		>>> _multicast.__package__ is not None
		True
		>>> type(_multicast.__package__) == type(str())
		True
		>>> type(_multicast.__package__)
		<class 'str'>
		>>> _multicast.__package__
		"multicast"
		>>>

"""

__module__ = "multicast"
"""The module of this program.

	The `__module__` attribute, like many dunder attributes, is associated with the implementation
	of Python language features. When utilizing this module as an imported module or a
	command-line interface (CLI) tool, the `__module__` attribute can be safely disregarded.
	Within the context of this module, `__module__` serves as a convenient constant that holds
	the name of the module.

	Out of the three attributes: __package__, __module__, and __name__, it is recommended that
	__module__ be used to programmatically obtain the value for comparative purposes, as it is
	specifically suited for that function.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__module__ is not None
		True
		>>>

	Testcase 0: multicast.__module__ should be the string "multicast".
		A: Test that the __module__ attribute is initialized.
		B: Test that the __module__ attribute is a string.
		C: Test that the __module__ attribute has a value of "multicast".

		>>> _multicast.__module__ is not None
		True
		>>> type(_multicast.__module__) == type(str())
		True
		>>> type(_multicast.__module__)
		<class 'str'>
		>>> _multicast.__module__
		"multicast"
		>>>

"""

__name__ = "multicast"  # skipcq: PYL-W0622
"""The name of this program.

	The `__name__` attribute, like many dunder attributes, is associated with the implementation
	of Python language features. When utilizing this module as an imported module or a
	command-line interface (CLI) tool, the `__name__` attribute can be safely disregarded.
	Within the context of this module, `__name__` serves as a convenient constant that holds
	the human-readable name of the module.

	Out of the three attributes: __package__, __module__, and __name__, it is recommended that
	__name__ be used to programmatically obtain the value for formatting purposes, as it is
	specifically suited for that function.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__name__ is not None
		True
		>>>

	Testcase 0: multicast.__name__ should be the string "multicast".
		A: Test that the __name__ attribute is initialized.
		B: Test that the __name__ attribute is a string.
		C: Test that the __name__ attribute has a value of "multicast".

		>>> _multicast.__name__ is not None
		True
		>>> type(_multicast.__name__) == type(str())
		True
		>>> type(_multicast.__name__)
		<class 'str'>
		>>> _multicast.__name__
		"multicast"
		>>>

"""

global __version__  # skipcq: PYL-W0604

__version__ = "2.1.0-alpha-1"
"""The version of this program.

	The `__version__` attribute, like many dunder attributes, is associated with the implementation
	of Python language features. Within the context of this module, `__version__` serves as a
	convenient constant that holds the version of the package.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__version__ is not None
		True
		>>>

	Testcase 0: multicast.__version__ should be the version string.
		A: Test that the __version__ attribute is initialized.
		B: Test that the __version__ attribute is a string.
		C: Test that the __version__ attribute has a value with "." dot(s).

		>>> _multicast.__version__ is not None
		True
		>>> type(_multicast.__version__) == type(str())
		True
		>>> type(_multicast.__version__)
		<class 'str'>
		>>> "." in _multicast.__version__
		True
		>>> "x" in _multicast.__version__
		False
		>>>

"""

__prologue__ = f"Python Multicast library version {__version__}."
"""The one-line description or summary of this program."""

__doc__ = __prologue__ + """

The `multicast` package simplifies multicast communication in Python applications.

A comprehensive package for multicast communication in Python applications.
Provides tools for sending, receiving, and listening to multicast messages over UDP.
The package includes command-line utilities and is designed to work with multiple Python
versions. It supports IPv4 multicast addresses and is compliant with dynamic/private port
ranges as per RFC-6335.

Key Features:
	- Easy-to-use python interfaces for multicast communication.
		- transmission via multicast.send
		- high-level receiving via multicast.hear for building custom multicast services.
		- low-level receiving via multicast.recv for advanced non-blocking use-cases.
	- Command-line tools for quick multicast prototyping.
	- Support for UDP multicast (currently IPv4 Only) via Python's built-in socket module.
	- Compliance with RFC-6335 for dynamic/private port ranges.

Security Considerations:
	- Ensure proper data sanitization and validation to prevent injection attacks.
	- Be mindful of TTL settings to limit message propagation to the intended network segment.

Attributes:
	__version__ (str): The version of this package.
	_MCAST_DEFAULT_BUFFER_SIZE (int): Default buffer size for multicast communication (1316).
	_MCAST_DEFAULT_PORT (int): Default port for multicast communication (59259).
	_MCAST_DEFAULT_GROUP (str): Default multicast group address ('224.0.0.1').
	_MCAST_DEFAULT_TTL (int): Default TTL for multicast packets (1).

Dynamic Imports:
	The sub-modules within "multicast" are interdependent, requiring access to each other's
	functionalities. These statements import sub-modules of "multicast" and assign them to
	aliases that match their sub-module names, facilitating organized access to these
	components.
	While the multicast alias is the same as the multicast module name, this pattern should
	serve to reinforce the Multicast module's namespace, especially when dealing with dynamic
	imports and to maintain consistency across different parts of the code.
	Roughly speaking, the following diagram describes the interdependentcies:
	```mermaid
		graph TD;
			Client-Code-->multicast/__init__.py;
			multicast/__init__.py-->sys;
			multicast/__init__.py-->argparse;
			multicast/__init__.py-->logging;
			multicast/exceptions.py-->multicast/__init__.py;
			multicast/exceptions.py-->functools;
			multicast/__init__.py-->multicast/exceptions.py;
			multicast/__init__.py-->struct;
			multicast/__init__.py-->socket;
			multicast/env.py-->multicast/__init__.py;
			multicast/env.py-->os;
			multicast/env.py-->warnings;
			multicast/env.py-->ipaddress;
			multicast/__init__.py-->multicast/env.py;
			multicast/skt.py-->multicast/__init__.py;
			multicast/__init__.py-->multicast/skt.py;
			multicast/recv.py-->sys;
			multicast/recv.py-->warnings;
			multicast/recv.py-->multicast/__init__.py;
			multicast/__init__.py-->multicast/recv.py;
			multicast/send.py-->sys;
			multicast/send.py-->multicast/__init__.py;
			multicast/send.py-->logging;
			multicast/__init__.py-->multicast/send.py;
			multicast/hear.py-->sys;
			multicast/hear.py-->multicast/__init__.py;
			multicast/hear.py-->multicast/recv.py;
			multicast/hear.py-->multicast/send.py;
			multicast/hear.py-->threading;
			multicast/hear.py-->socketserver;
			multicast/hear.py-->warnings;
			multicast/__init__.py-->multicast/hear.py;
			multicast/__main__.py-->multicast/__init__.py;
			multicast/__main__.py-->multicast/exceptions.py;
			multicast/__main__.py-->multicast/recv.py;
			multicast/__main__.py-->multicast/send.py;
			multicast/__main__.py-->multicast/hear.py;
			multicast/__init__.py-->multicast/__main__.py;
	```


Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>>

		>>> multicast.__doc__ is not None
		True
		>>>

		>>> multicast.__version__ is not None
		True
		>>>

	Testcase 0: multicast.recv should have a doctest.

		>>> import multicast.recv
		>>>

		>>> multicast.recv.__module__ is not None
		True
		>>>

	Testcase 1: multicast.send should have a doctest.

		>>> import multicast.send
		>>>

		>>> multicast.send.__module__ is not None
		True
		>>>

	Testcase 2: multicast.__main__ should have a doctest.

		>>> import multicast.__main__ as _main
		>>>

		>>> _main.__module__ is not None
		True
		>>> _main.__doc__ is not None
		True
		>>>


"""

global _MCAST_DEFAULT_BUFFER_SIZE  # skipcq: PYL-W0604

_MCAST_DEFAULT_BUFFER_SIZE = 1316
"""
	Arbitrary buffer size to use by default, though any value below 65507 should work.

	> [!CAUTION]
	> This value is NOT related to the actual packet size, the python socket module, and
	> underlying OS, firmware and even some hardware will handle all of that. If you need
	> to change buffers you are better off focusing on changing the underlying MTU of the
	> entire network infrastructure instead (albeit that may not be possible for most users).

	The value of this buffer is related to how **this** module 'packetizes' streams when
	encoding to, and decoding from, socket bytes and Python's UTF-8 interpretation. There
	is no impact on how a python implementation will actually buffer network data in
	regards to the value of _MCAST_DEFAULT_BUFFER_SIZE at runtime.

	Minimal Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default buffer size.
		A: Test that the _MCAST_DEFAULT_BUFFER_SIZE attribute is initialized.
		B: Test that the _MCAST_DEFAULT_BUFFER_SIZE attribute is an int.

		>>> multicast._MCAST_DEFAULT_BUFFER_SIZE is not None
		True
		>>> type(multicast._MCAST_DEFAULT_BUFFER_SIZE) is type(1)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_BUFFER_SIZE > int(1)
		True
		>>>

	Testcase 1: Multicast should validate buffer size constraints.
		A: Test that the _MCAST_DEFAULT_BUFFER_SIZE attribute is initialized.
		B: Test that the _MCAST_DEFAULT_BUFFER_SIZE attribute is an int.
		C: Test that the _MCAST_DEFAULT_BUFFER_SIZE attribute is RFC-791 & RFC-768 compliant.
		D: Test that the _MCAST_DEFAULT_BUFFER_SIZE attribute is a smaller than fragment thresholds
			for typical ethernet MTUs by default.

		>>> multicast._MCAST_DEFAULT_BUFFER_SIZE is not None
		True
		>>> type(multicast._MCAST_DEFAULT_BUFFER_SIZE) is type(1)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_BUFFER_SIZE >= int(56)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_BUFFER_SIZE <= int(65527)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_BUFFER_SIZE <= int(1500)
		True
		>>>


"""

global _MCAST_DEFAULT_PORT  # skipcq: PYL-W0604

_MCAST_DEFAULT_PORT = 59259
"""
	Arbitrary port to use by default, though any dynamic and free port would work.

	A Value of "59259" is chosen as a default multicast port as per RFC-6335
	on the rational that this memorable port will be treated as a user-allocated
	(caveat: senders should match the intended listener's port)

	> [!IMPORTANT]
	> Multicast is not actually port-aware, and port filtering is instead
	> handled at the protocol layer (e.g., UDP) instead, and may not behave
	> as expected for some real-world setups.

	Minimal Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default port.
		A: Test that the _MCAST_DEFAULT_PORT attribute is initialized.
		B: Test that the _MCAST_DEFAULT_PORT attribute is an int.

		>>> multicast._MCAST_DEFAULT_PORT is not None
		True
		>>> type(multicast._MCAST_DEFAULT_PORT) is type(1)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_PORT > int(1024)
		True
		>>>

	Testcase 1: Multicast should have a default port.
		A: Test that the _MCAST_DEFAULT_PORT attribute is initialized.
		B: Test that the _MCAST_DEFAULT_PORT attribute is an int.
		C: Test that the _MCAST_DEFAULT_PORT attribute is RFC-6335 compliant.

		>>> multicast._MCAST_DEFAULT_PORT is not None
		True
		>>> type(multicast._MCAST_DEFAULT_PORT) is type(1)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_PORT >= int(49152)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_PORT <= int(65535)
		True
		>>>


"""

global _MCAST_DEFAULT_GROUP  # skipcq: PYL-W0604

_MCAST_DEFAULT_GROUP = "224.0.0.1"
"""Arbitrary group to use by default, though any mcst grp would work.

	A Value of "224.0.0.1" is chosen as a default multicast group as per RFC-5771
	on the rational that this group address will be treated as a local-net multicast
	(caveat: one should use link-local for ipv6)

	Minimal Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default port.
		A: Test that the _MCAST_DEFAULT_GROUP attribute is initialized.
		B: Test that the _MCAST_DEFAULT_GROUP attribute is an IP string.

		>>> multicast._MCAST_DEFAULT_GROUP is not None
		True
		>>> type(multicast._MCAST_DEFAULT_GROUP) is type(str)
		True
		>>>

"""

global _MCAST_DEFAULT_TTL  # skipcq: PYL-W0604

_MCAST_DEFAULT_TTL = int(1)
"""Arbitrary TTL time to live to use by default, though any small (1-126) TTL would work.

	A Value of 1 (one TTL) is chosen as per RFC1112 Sec 6.1 on the rational that an
	explicit value that could traverse byond the local connected network should be
	chosen by the caller rather than the default value. This is inline with the principle
	of none, one or many.

	Minimal Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default TTL.
		A: Test that the _MCAST_DEFAULT_TTL attribute is initialized.
		B: Test that the _MCAST_DEFAULT_TTL attribute is an int.
		c: Test that the _MCAST_DEFAULT_TTL attribute is default of 1.

		>>> multicast._MCAST_DEFAULT_TTL is not None
		True
		>>> type(multicast._MCAST_DEFAULT_TTL) is type(1)
		True
		>>> (int(multicast._MCAST_DEFAULT_TTL) >= int(0))
		True
		>>> (int(multicast._MCAST_DEFAULT_TTL) <= int(2))
		True
		>>>

"""

global _BLANK  # skipcq: PYL-W0604

_BLANK = str("""""")
"""Arbitrary blank string.

	Minimal Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>> _BLANK = multicast._BLANK

	Testcase 0: Multicast should have a default port.
		A: Test that the _BLANK attribute is initialized.
		B: Test that the _BLANK attribute is an empty string.

		>>> _BLANK is not None
		True
		>>> type(_BLANK) is type(str)
		True
		>>>
		>>> len(_BLANK) <= 0
		True
		>>>

"""

if hasattr(logging, "getLogger"):  # pragma: no branch
	logging.getLogger(__module__).addHandler(logging.NullHandler())
	logging.getLogger(__module__).debug(
		"Loading %s",  # lazy formatting to avoid PYL-W1203
		__module__,
	)

if not hasattr(sys, "modules"):  # pragma: no branch
	raise ModuleNotFoundError(
		"[CWE-684]: we could not import sys. ABORT."  # also is a CWE-440 if ever reached
	) from None

if not hasattr(argparse, "ArgumentParser"):
	raise ModuleNotFoundError("[CWE-440]: we could not import argparse. ABORT.") from None

if not hasattr(unicodedata, "normalize"):
	raise ModuleNotFoundError("[CWE-440]: we could not import unicodedata. ABORT.") from None

if not hasattr(socket, "setdefaulttimeout"):
	raise ModuleNotFoundError("[CWE-440]: we could not import socket. ABORT.") from None

try:
	_tmp_mcast_value: int = int(_MCAST_DEFAULT_TTL)
	logging.getLogger(__module__).debug(
		"Setting default socket timeout to %d",  # lazy formatting to avoid PYL-W1203
		_tmp_mcast_value,
	)
	socket.setdefaulttimeout(_tmp_mcast_value)
finally:
	del _tmp_mcast_value  # skipcq - cleanup any bootstrap/setup leaks early

if not hasattr(struct, "pack"):
	raise ModuleNotFoundError("[CWE-440]: we could not import struct. ABORT.") from None

if not hasattr(abc, "ABC"):
	raise ModuleNotFoundError("[CWE-440]: we could not import Abstract base class. ABORT.") from None

if "multicast.exceptions" not in sys.modules:
	# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
	from . import exceptions  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
else:  # pragma: no branch
	global exceptions  # skipcq: PYL-W0604
	exceptions = sys.modules["multicast.exceptions"]

EXIT_CODES = exceptions.EXIT_CODES
"""See multicast.exceptions.EXIT_CODES."""

EXCEPTION_EXIT_CODES = exceptions.EXCEPTION_EXIT_CODES
"""See multicast.exceptions.EXCEPTION_EXIT_CODES."""

CommandExecutionError = exceptions.CommandExecutionError
"""See multicast.exceptions.CommandExecutionError Class."""

ShutdownCommandReceived = exceptions.ShutdownCommandReceived
"""See multicast.exceptions.ShutdownCommandReceived Class."""

get_exit_code_from_exception = exceptions.get_exit_code_from_exception
"""See multicast.exceptions.get_exit_code_from_exception function."""

exit_on_exception = exceptions.exit_on_exception
"""See multicast.exceptions.exit_on_exception function."""

if "multicast.env" not in sys.modules:
	# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
	from . import env  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
else:  # pragma: no branch
	global env  # skipcq: PYL-W0604
	env = sys.modules["multicast.env"]

try:
	_config = env.load_config()

	if _config is None:  # pragma: no branch
		raise ImportError("[CWE-440]: we could not import environment (multicast.env). ABORT.") from None

	logging.getLogger(__module__).debug("Configuring overrides and defaults.")
	_MCAST_DEFAULT_PORT = _config["port"]
	_MCAST_DEFAULT_GROUP = _config["group"]
	_MCAST_DEFAULT_TTL = _config["ttl"]
	_MCAST_DEFAULT_BUFFER_SIZE = _config["buffer_size"]
	global _MCAST_DEFAULT_BIND_IP  # skipcq: PYL-W0604
	_MCAST_DEFAULT_BIND_IP = _config["bind_addr"]
	global _MCAST_DEFAULT_GROUPS  # skipcq: PYL-W0604
	_MCAST_DEFAULT_GROUPS = _config["groups"]
	if __debug__:  # pragma: no branch
		logging.getLogger(__module__).info("Overrides and defaults are configured.")
		logging.getLogger(__module__).debug("Defaults:")
		for key, value in _config.items():
			logging.getLogger(__module__).debug(
				"\t%s=%s",  # lazy formatting to avoid PYL-W1203
				key, value,
			)
finally:
	del _config  # skipcq - cleanup any bootstrap/setup leaks early


class mtool(abc.ABC):
	"""
	Class for Multicast tools.

	Utility class for CLI tools of the Multicast package. setupArgs() and doStep() are
	abstract and need to be implemented by subclasses.

	Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>> _multicast.mtool is not None
		True
		>>>

	Testcase 0: multicast.mtool should be the abstract class "multicast.mtool".
		A: Test that the mtool abstract class is partially implemented.
		B: Test that the mtool abstract class has abstract methods.

		>>> _multicast.mtool is not None
		True
		>>> type(_multicast.mtool) #doctest: +ELLIPSIS
		<...abc.ABC...>
		>>> hasattr(_multicast.mtool, "__abstractmethods__")
		True
		>>>

	Testcase 1: multicast.mtool should have two key abstract methods.
		A: Test that the mtool abstract class has at-least two (2) abstract methods.
		B: Test that the mtool abstract class has the abstract method "dostep".
		C: Test that the mtool abstract class has the abstract method "setupArgs".

		>>> hasattr(_multicast.mtool, "__abstractmethods__")
		True
		>>> len(_multicast.mtool.__abstractmethods__) >= int(2)
		True
		>>> "doStep" in _multicast.mtool.__abstractmethods__
		True
		>>> "setupArgs" in _multicast.mtool.__abstractmethods__
		True
		>>>

	Testcase 2: multicast.mtool should allow sub-classes to be callable.
		A: Test that the mtool abstract class can be sub-classes.
		B: Test that the mtool abstract class has the implemented method "buildArgs".
		B: Test that the mtool abstract class has the implemented method "parseArgs".

		>>> hasattr(_multicast.mtool, "__abstractmethods__")
		True
		>>> len(_multicast.mtool.__abstractmethods__) >= int(2)
		True
		>>> "doStep" in _multicast.mtool.__abstractmethods__
		True
		>>> "setupArgs" in _multicast.mtool.__abstractmethods__
		True
		>>> _test_dir_fixture = dir(_multicast.mtool)
		>>> _test_dir_fixture is not None
		True
		>>> "buildArgs" in _test_dir_fixture
		True
		>>> "parseArgs" in _test_dir_fixture
		True
		>>> class test_class_fixture(_multicast.mtool):
		...	def doStep(self, *args):
		...		return (True, 42)
		...
		...	@classmethod
		...	def setupArgs(cls, parser):
		...		parser.add_parser("NOOP", help="Does Nothing.")
		...		return parser
		...
		>>>
		>>> tst_fxtr_args = ['''NOOP''']
		>>> test_fixture = test_class_fixture.parseArgs(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> test_fixture_inst = test_class_fixture()
		>>> test_fixture_inst is not None
		True
		>>> test_fixture_inst(False) #doctest: +ELLIPSIS
		(...42...)
		>>> del test_fixture_inst
		>>>

	"""

	__module__ = "multicast"

	__proc__ = None

	__prologue__ = "Add a prologue here."

	__epilogue__ = "Add an epilogue here."

	@classmethod
	def buildArgs(cls, calling_parser_group: argparse.ArgumentParser) -> argparse.ArgumentParser:
		"""
		Will build the argparse parser.

		Utility Function to build the argparse parser; see argparse.ArgumentParser for more.
		returns argparse.ArgumentParser - the ArgumentParser to use.

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.mtool is not None
			True
			>>>

		Testcase 0: buildArgs should return an ArgumentParser.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the mtool.buildArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> type(multicast.mtool) #doctest: +ELLIPSIS
			<...abc.ABCMeta...>
			>>> multicast.mtool.buildArgs is not None
			True
			>>> class test_tool_fixture(multicast.mtool):
			...	def doStep(self, *args):
			...		pass
			...
			...	@classmethod
			...	def setupArgs(cls, parser):
			...		return parser
			...
			>>>
			>>> type(test_tool_fixture.buildArgs(None)) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...ArgumentParser...>
			>>>
			>>>


		"""
		if calling_parser_group is None:  # pragma: no branch
			logging.getLogger(__module__).debug(
				"Building %s arguments.",  # lazy formatting to avoid PYL-W1203
				__name__,
			)
			calling_parser_group = argparse.ArgumentParser(
				prog=str(cls.__name__ if cls.__proc__ is None else cls.__proc__),
				description=cls.__prologue__,
				epilog=cls.__epilogue__,
				add_help=False
			)
			group = calling_parser_group.add_mutually_exclusive_group(required=False)
			group.add_argument("-h", "--help", action="help")
			group.add_argument(
				"-v",
				"--version",
				action="version",
				version=f"%(prog)s {__version__}"
			)
			calling_parser_group.add_argument(
				"--use-std", dest="is_std", default=False, action="store_true",
				help="Use interactive command mode. Disabled by default."
			)
			calling_parser_group.add_argument(
				"--daemon", dest="is_daemon", default=False, action="store_true",
			)
		subparsers = calling_parser_group.add_subparsers(
			title="Tools", dest="cmd_tool", help="Sub-Commands.", metavar="CMD"
		)
		if mtool.__class__.__subclasscheck__(mtool, cls):  # pragma: no branch
			cls.setupArgs(subparsers)
		return calling_parser_group

	@classmethod
	def parseArgs(cls, arguments) -> tuple:
		"""
		Will attempt to parse the given CLI arguments.

		See argparse.ArgumentParser for more.
		param str - arguments - the array of arguments to parse. Usually sys.argv[1:]
		returns argparse.Namespace - the Namespace parsed with the key-value pairs.

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.mtool is not None
			True
			>>>

		Testcase 0: parseArgs should return a namespace.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the multicast.mtool.parseArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> multicast.mtool.parseArgs is not None
			True
			>>> class test_tool_fixture(multicast.mtool):
			...	def doStep(self, *args):
			...		pass
			...
			...	@classmethod
			...	def setupArgs(cls, parser):
			...		parser.add_parser("NOOP", help="Does Nothing.")
			...		return parser
			...
			>>>
			>>> tst_fxtr_args = ['''NOOP''', '''--port=1234''', '''--iface=127.0.0.1''']
			>>> test_fixture = test_tool_fixture.parseArgs(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...tuple...>
			>>> tst_fxtr_args_2 = ['''NOOP''', '''--junk''', '''--more-trash=stuff''']
			>>> (test_fixture_2, test_ignore_extras) = test_tool_fixture.parseArgs(tst_fxtr_args_2)
			>>> test_fixture_2 is not None
			True
			>>> type(test_fixture_2) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...Namespace...>
			>>>


		"""
		arguments = cls.checkToolArgs(arguments)
		return cls.buildArgs(None).parse_known_args(arguments)

	@classmethod
	def checkToolArgs(cls, args) -> list:
		"""
		Will handle the None case for arguments.

		Used as a helper function.

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast
			>>>

		Testcase 0: multicast.mtool should have a doctests.

			>>> import multicast
			>>> multicast.mtool is not None
			True
			>>> multicast.mtool.__class__ is not None
			True
			>>>
			>>> multicast.mtool.__doc__ is not None
			True
			>>>

		Testcase 1: multicast.checkToolArgs should return an array.

			>>> import multicast
			>>> multicast.mtool.checkToolArgs(None) is not None
			True
			>>> type(multicast.mtool.checkToolArgs(None)) is type([None])
			True
			>>>

		Testcase 2: multicast.checkToolArgs should return an array.

			>>> import multicast
			>>> type(multicast.mtool.checkToolArgs(["arg1", "arg2"])) is type(["strings"])
			True
			>>> type(multicast.mtool.checkToolArgs([0, 42])) is type([int(1)])
			True
			>>>


		"""
		return [None] if args is None else args

	def __call__(self, *args, **kwargs):
		"""
		Call self as a function.

			Default implementation simply calls the abstract function doStep
			and passes the given positional arguments, thus key-word arguments
			will be silently ignored.

			Subclasses should not reimplement __call__ directly and instead
			should implement necessary logic in the abstract doStep() function.
		"""
		return self.doStep(*args, **kwargs)

	@classmethod
	@abc.abstractmethod
	def setupArgs(cls, parser) -> None:  # pragma: no cover
		"""Abstract hook for setting up the tool's arguments."""
		pass  # skipcq - abstract method

	@abc.abstractmethod
	def doStep(self, *args, **kwargs) -> tuple:  # pragma: no cover
		"""
		Abstracts the __call__ behavior for sub-classing the tool.

		This method should be overridden by subclasses to implement the specific functionality
		of each multicast tool. It accepts variable positional and keyword arguments as needed
		by the specific implementation.

		Args:
			*args: Variable length argument list.
			**kwargs: Arbitrary keyword arguments.

		Returns:
			tuple: A tuple containing a status indicator and a result message.

		Raises:
			NotImplementedError: If the subclass does not implement this method.
		"""
		raise NotImplementedError("Subclasses must implement this method.")


if "multicast.skt" not in sys.modules:
	# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
	from . import skt  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
else:  # pragma: no branch
	global skt  # skipcq: PYL-W0604
	skt = sys.modules["multicast.skt"]

genSocket = skt.genSocket
"""See multicast.skt.genSocket."""

endSocket = skt.endSocket
"""See multicast.skt.endSocket."""

if "multicast.recv" not in sys.modules:
	# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
	from . import recv  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
else:  # pragma: no branch
	global recv  # skipcq: PYL-W0604
	recv = sys.modules["multicast.recv"]

if "multicast.send" not in sys.modules:
	# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
	from . import send  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
else:  # pragma: no branch
	global send  # skipcq: PYL-W0604
	send = sys.modules["multicast.send"]

if "multicast.hear" not in sys.modules:
	# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
	from . import hear  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
else:  # pragma: no branch
	global hear  # skipcq: PYL-W0604
	hear = sys.modules["multicast.hear"]

try:
	if "multicast.__main__" in sys.modules:  # pragma: no cover
		global __main__  # skipcq: PYL-W0604
		__main__ = sys.modules["multicast.__main__"]
except Exception:
	import multicast.__main__ as __main__  # pylint: disable=cyclic-import - skipcq: PYL-R0401

if __name__ in "__main__":
	__EXIT_CODE = 2
	if __main__.cli is not None:
		__EXIT_CODE = __main__.cli()
	exit(__EXIT_CODE)  # skipcq: PYL-R1722 - intentionally allow coverage and testing to catch exit
