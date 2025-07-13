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

"""Provides multicast HEAR Features.

Provides server-side functionality for listening to multicast messages. It implements a
UDP server that can receive and process multicast messages continuously.

Classes:
	McastServer: UDP server implementation for multicast communication.
	HearUDPHandler: Request handler for processing multicast messages.
	McastHEAR: Main tool class for HEAR operations.

Caution: See details regarding dynamic imports [documented](../__init__.py) in this module.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.hear is not None
		True
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 1: Recv should be automatically imported.
		A: Test that the multicast component is initialized.
		B: Test that the hear component is initialized.
		C: Test that the hear component has __doc__

		>>> multicast is not None
		True
		>>> multicast.hear is not None
		True
		>>> multicast.hear.__doc__ is not None
		True
		>>> type(multicast.hear.__doc__) == type(str(''''''))
		True
		>>>

	Testcase 2: Recv should be detailed with some metadata.
		A: Test that the __MAGIC__ variables are initialized.
		B: Test that the __MAGIC__ variables are strings.

		>>> multicast.hear is not None
		True
		>>> multicast.hear.__module__ is not None
		True
		>>> multicast.hear.__package__ is not None
		True
		>>> type(multicast.hear.__doc__) == type(multicast.recv.__module__)
		True
		>>>

	Testcase 3: main should return an int.
		A: Test that the multicast component is initialized.
		B: Test that the hear component is initialized.
		C: Test that the main(HEAR) function-flow is initialized.
		D: Test that the main(HEAR) function-flow returns an int 0-256.

		>>> multicast.__main__ is not None
		True
		>>> multicast.__main__.main is not None
		True
		>>> tst_fxtr_args = ['''HEAR''', '''--port=1234''']
		>>> (test_fixture, ignored_value) = multicast.__main__.main(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...int...>
		>>> int(test_fixture) >= int(0)
		True
		>>> type(test_fixture) is type(0)
		True
		>>> int(test_fixture) < int(256)
		True
		>>> (int(test_fixture) >= int(0)) and (int(test_fixture) < int(256))
		True
		>>>

	Testcase 3: Class McastHEAR should be stable.
		A: Test that the hear component is initialized.
		B: Tests that McastHEAR instantiates without error, as in trivial use-case.

		>>> multicast.hear is not None
		True
		>>> hear = multicast.hear.McastHEAR()
		>>> isinstance(hear, multicast.hear.McastHEAR)
		True
		>>>

"""

__package__ = "multicast"  # skipcq: PYL-W0622
"""Names the package of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Hear should be automatically imported.

		>>> multicast.hear.__package__ is not None
		True
		>>>
		>>> multicast.hear.__package__ == multicast.__package__
		True
		>>>


"""

__module__ = "multicast"
"""Names the module of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Hear should be automatically imported.

		>>> multicast.hear.__module__ is not None
		True
		>>>


"""

__file__ = "multicast/hear.py"
"""Names the file of this component."""

__name__ = "multicast.hear"  # skipcq: PYL-W0622
"""Names this component.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Hear should be automatically imported.

		>>> multicast.hear.__name__ is not None
		True
		>>>


"""

try:
	import sys
	if 'multicast' not in sys.modules:
		# skipcq
		from . import multicast as multicast  # pylint: disable=cyclic-import - skipcq: PYL-C0414
	else:  # pragma: no branch
		multicast = sys.modules["multicast"]
	_BLANK = multicast._BLANK  # skipcq: PYL-W0212 - module ok
	# skipcq
	from . import recv as recv  # pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
	# skipcq
	from . import send as send  # pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
except Exception as _cause:
	del _cause  # skipcq - cleanup any error leaks early
	# skipcq
	import multicast as multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414

try:
	import logging
	import threading
	import socketserver
	import warnings
	from multicast import argparse as _argparse
	from multicast import unicodedata as _unicodedata
	from multicast import socket as _socket
	from multicast import struct as _struct
	depends = [_unicodedata, _socket, _struct, _argparse]
	for unit in depends:
		try:
			if unit.__name__ is None:  # pragma: no branch
				raise ModuleNotFoundError(
					f"[CWE-440] module failed to import {str(unit)}."
				) from None
		except Exception as _root_cause:  # pragma: no branch
			raise ModuleNotFoundError("[CWE-758] Module failed completely.") from _root_cause
except Exception as _cause:  # pragma: no branch
	raise ImportError(_cause) from _cause


module_logger = logging.getLogger(__name__)
module_logger.debug(
	"Loading %s",  # lazy formatting to avoid PYL-W1203
	__name__,
)


class McastServer(socketserver.UDPServer):
	"""
	Generic Subclasses socketserver.UDPServer for handling '--daemon' function.

	Basically simplifies testing by allowing a trivial echo back (case-insensitive) of string
	data, after printing the sender's ip out.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.hear is not None
		True
		>>> from multicast.hear import McastServer as McastServer
		>>>

	Testcase 1: McastServer should be automatically imported.

		>>> McastServer.__name__ is not None
		True
		>>>


	"""

	__log_handle__ = """multicast.hear.McastServer"""  # skipcq: PYL-W0622
	"""Names this server's Logger.

	Basically just the prefix of the logger's name. Subclasses should override.

	Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

		Testcase 0: Multicast should be importable.

			>>> import multicast
			>>>

		Testcase 1: McastServer should be automatically imported.

			>>> multicast.hear.McastServer.__name__ is not None
			True
			>>> multicast.hear.McastServer.__log_handle__ is not None
			True
			>>>

	"""

	def __init__(
		self, server_address: tuple, RequestHandlerClass: type, bind_and_activate: bool = True
	) -> None:
		"""
		Initialize a new instance of the McastServer.

		Creates a new UDP server for multicast communication and sets up an appropriate logger
		based on the server address provided. May be extended, do not override.

		Returns:
			None

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

		Testcase 0: Multicast should be importable.

			>>> import socketserver
			>>> import multicast
			>>>

		Testcase 0: Basic initialization of McastServer.
			A: Test that McastServer can be initialized with minimal arguments.
			B: Test that the resulting instance is of the correct type.

			>>> server = multicast.hear.McastServer(('224.0.0.1', 12345), None)
			>>> isinstance(server, multicast.hear.McastServer)
			True
			>>> isinstance(server, socketserver.UDPServer)
			True
			>>> server.server_close()  # Clean up
			>>>

		Testcase 1: Server initialization with logger name extraction.
			A: Test that the server extracts the logger name from server_address.
			B: Test that the logger is properly initialized.

			>>> test_addr = ('239.0.0.9', 23456)
			>>> server = multicast.hear.McastServer(test_addr, None)
			>>> server.logger is not None
			True
			>>> server.logger.name.endswith('239.0.0.9')
			True
			>>> server.server_close()  # Clean up
			>>>

		"""
		logger_name = server_address[0] if server_address and len(server_address) > 0 else None
		if logger_name:  # pragma: no branch
			self.__logger = logging.getLogger(f"{self.__log_handle__}.{logger_name}")
		else:
			self.__logger = logging.getLogger(f"{self.__log_handle__}")
		super().__init__(server_address, RequestHandlerClass, bind_and_activate)

	def _sync_logger(self) -> None:
		"""Synchronize the logger instance with the bound socket address.

		This internal method updates the instance's logger attribute based on the current
		socket address. It extracts the address component from the socket's bound address
		and uses it to create a hierarchical logger name in the format
		'multicast.hear.McastServer.[address]'.

		If no valid address is found, it falls back to the base McastServer logger.
		This method is typically called after server_bind() to ensure the logger
		reflects the actual bound socket address.

		Note:
			This is an internal method and should not be called directly from outside
			the class.

		Args:
			None

		Returns:
			None

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

		Testcase 0: Multicast should be importable.

			>>> import types
			>>> import logging
			>>> import multicast
			>>>

		Testcase 1: Method exists and takes expected arguments.
			A: Test method exists in McastServer class.
			B: Test method signature does not accept arguments.

			>>> from multicast.hear import McastServer
			>>> hasattr(McastServer, '_sync_logger')
			True
			>>> import inspect
			>>> len(inspect.signature(McastServer._sync_logger).parameters) - 1  # Remove 'self'
			0
			>>>

		Testcase 2: Method handles case where socket has a valid address.
			A: Use a mock socket with a valid address.
			B: Verify logger name is properly formatted.

			>>> # Setup a server instance with mock socket
			>>> server = multicast.hear.McastServer(('239.0.0.9', 51234), None)
			>>> # Create mock socket with valid address
			>>> mock_socket = types.SimpleNamespace()
			>>> mock_socket.getsockname = lambda: ('239.0.0.9', 51234)
			>>> server.socket = mock_socket
			>>> # Call method and verify logger name
			>>> server._sync_logger()
			>>> server.logger.name
			'multicast.hear.McastServer.239.0.0.9'
			>>>

		Testcase 3: Method handles case where socket address name component is None.
			A: Use a mock socket with None as the address component.
			B: Verify logger falls back to base logger name.

			>>> # Setup a server instance
			>>> server = multicast.hear.McastServer(('239.0.0.9', 51234), None)
			>>> # Create mock socket with None as the address
			>>> mock_socket = types.SimpleNamespace()
			>>> mock_socket.getsockname = lambda: (None, 5678)
			>>> server.socket = mock_socket
			>>> # Call method and verify logger name
			>>> server._sync_logger()
			>>> server.logger.name
			'multicast.hear.McastServer'
			>>>

		Testcase 4: Method handles case where socket address has special formatting.
			A: Use a mock socket with an IPv6 address.
			B: Verify logger name incorporates the address correctly.

			>>> import multicast
			>>> from multicast.hear import McastServer
			>>> import types
			>>> import logging
			>>> # Setup a server instance
			>>> server = McastServer(('239.0.0.9', 51234), None)
			>>> # Create mock socket with IPv6 address format
			>>> mock_socket = types.SimpleNamespace()
			>>> mock_socket.getsockname = lambda: ('2001:db8::1', 5678)
			>>> server.socket = mock_socket
			>>> # Call method and verify logger name
			>>> server._sync_logger()
			>>> server.logger.name
			'multicast.hear.McastServer.2001:db8::1'
			>>>
		"""
		(logger_name, _) = self.socket.getsockname()
		if logger_name:
			self.__logger = logging.getLogger(f"{self.__log_handle__}.{logger_name}")
		else:  # pragma: no branch
			self.__logger = logging.getLogger(f"{self.__log_handle__}")

	@property
	def logger(self) -> logging.Logger:
		"""Getter for the logger attribute of McastServer.

		This property provides access to the server's internal logger instance. The logger name
		is determined during initialization and may be updated by calling _sync_logger when the
		server's socket address changes.

		Returns:
			logging.Logger -- The logger instance associated with this server.

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast
			>>> import logging
			>>>

		Testcase 0: Verify logger accessibility.
			A: Test that the logger property exists.
			B: Test that it's accessible from an McastServer instance.

			>>> server = multicast.hear.McastServer(("239.0.0.9", 0), multicast.hear.HearUDPHandler)
			>>> hasattr(server, 'logger')
			True
			>>> server.server_close()  # Clean up
			>>>

		Testcase 1: Verify logger type.
			A: Test that the logger property returns a logging.Logger instance.

			>>> server = multicast.hear.McastServer(("239.0.0.9", 0), multicast.hear.HearUDPHandler)
			>>> isinstance(server.logger, logging.Logger)
			True
			>>> server.server_close()  # Clean up
			>>>

		Testcase 2: Verify logger name.
			A: Test that the logger name includes the server class name.
			B: Test that it's properly formatted.

			>>> server = multicast.hear.McastServer(("239.0.0.9", 0), multicast.hear.HearUDPHandler)
			>>> server.logger.name.startswith('multicast.hear.McastServer')
			True
			>>> server.server_close()  # Clean up
			>>>
		"""
		return self.__logger

	def server_activate(self):
		"""
		Activate the server to begin handling requests.

		Overrides the base class method to set up the server after binding.

		Returns:
			None
		"""
		self.logger.info("server_activate")
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", category=ResourceWarning)
			self.open_for_request()
		super(McastServer, self).server_activate()

	def open_for_request(self):
		"""
		Prepare the server to accept requests.

		Overrides the base class method to set up a new listening UDP socket before the
		server starts processing requests.

		UDP Sockets are considered ephemeral.
		Sequentially, the old socket is recycled, or replaced, yielding a fungable socket, with the
		same port and bound ip, which is then used to join the same multicast group(s), at which
		point the new socket has transparently replaced the old socket.

		Returns:
			None
		"""
		self.logger.info("open_request")
		# enter critical section
		old_socket = self.socket
		(tmp_addr, tmp_prt) = old_socket.getsockname()
		multicast.endSocket(old_socket)
		self.socket = recv.joinstep([tmp_addr], tmp_prt, None, tmp_addr, multicast.genSocket())
		old_socket = None  # release for GC
		# exit critical section

	def server_bind(self):
		"""
		Bind the server to the specified address.

		Overrides the base class method to handle multicast group binding.

		Returns:
			None
		"""
		self.logger.info("server_bind")
		super(McastServer, self).server_bind()
		self._sync_logger()
		# enter critical section
		self.logger.info(
			"bound on: %s",  # lazy formatting to avoid PYL-W1203
			str(self.socket.getsockname()),
		)
		# exit critical section

	def close_request(self, request):
		"""
		Clean up after handling a request.

		Overrides the base class method to call open_for_request to close and regenerate the
		UDP socket, in addition to closing the request as normal.

		Args:
			request: The request object to close.

		Returns:
			None
		"""
		self.logger.info("close_request")
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", category=ResourceWarning)
			self.open_for_request()
		super(McastServer, self).close_request(request)

	def handle_error(self, request, client_address):
		"""
		Handle errors that occur during request processing.

		Overrides the base class method to handle requests with STOP in them,
		resulting in a graceful server shutdown. Otherwise forwards the call to super.

		Args:
			request: The request being handled when the error occurred.
			client_address: The client address associated with the request.

		Returns:
			None
		"""
		self.logger.info("handle_error")
		if request is not None and request[0] is not None and "STOP" in str(request[0]):
			def kill_func(a_server):
				"""
				Terminate the server.

				Args:
					a_server: The server instance to terminate.

				Returns:
					None
				"""
				if a_server is not None:
					a_server.shutdown()
			end_thread = threading.Thread(name="Kill_Thread", target=kill_func, args=[self])
			end_thread.start()
		else:
			super(McastServer, self).handle_error(request, client_address)


class HearUDPHandler(socketserver.BaseRequestHandler):
	"""
	Subclass of socketserver.BaseRequestHandler for handling the HEAR function.

	Basically simplifies testing by allowing a simple HEAR back (case-insensitive) of string
	data, after printing the sender's ip out.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.hear is not None
		True
		>>> from multicast.hear import HearUDPHandler as HearUDPHandler
		>>>

	Testcase 1: HearUDPHandler should be automatically imported.

		>>> HearUDPHandler.__name__ is not None
		True
		>>>


	"""

	__name__ = "multicast.hear.HearUDPHandler"  # skipcq: PYL-W0622
	"""Names this handler type.

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

		Testcase 0: Multicast should be importable.

			>>> import multicast
			>>>

		Testcase 1: HearUDPHandler should be automatically imported.

			>>> multicast.hear.HearUDPHandler.__name__ is not None
			True
			>>>


	"""

	def handle(self) -> None:
		"""
		Handles incoming UDP requests in the HEAR functionality.

		Overrides the base class method to define how incoming data is handled.

		By default:
			Processes the incoming data from the client, logs the messages,
			and sends a response back. If the data contains the
			keyword "STOP", it raises a `ShutdownCommandReceived` to
			initiate server shutdown.
			Silently ignores any UnicodeDecodeError when decoding data.
			Returns early if data or socket is None.

		Args:
			None

		Returns:
			None

		Raises:
			multicast.exceptions.ShutdownCommandReceived: When "STOP" is detected in incoming data.

		Minimal Acceptance Testing:

			First set up test fixtures by importing multicast.

			>>> import multicast
			>>>

			Testcase 0: Ensure `HearUDPHandler` can be imported.

			>>> import multicast
			>>> from multicast.hear import HearUDPHandler
			>>> HearUDPHandler.__name__ is not None
			True
			>>>

			Testcase 1: Verify the `handle` method exists.

			>>> handler = HearUDPHandler(
			...     request=('Test data', None), client_address=('192.0.2.1', 51111), server=None
			... )
			>>> hasattr(handler, 'handle')
			True
			>>>

			Testcase 2: `handle` requires valid requests or ignores input.

			>>> handler.request = ("No-Op", None)
			>>> handler.client_address = ("192.0.2.2", 51234)
			>>> handler.handle() is None
			True
			>>>

			Testcase 3: `handle` requires valid requests or ignores input.

			>>> tst_fixture_sock = multicast.genSocket()
			>>> handler.request = ("The Test", tst_fixture_sock)
			>>> handler.client_address = ("224.0.1.2", 51234)
			>>> handler.handle() is None
			True
			>>>
			>>> multicast.endSocket(tst_fixture_sock)
			>>>

			Testcase 4: `handle` raises on valid STOP requests.

			>>> tst_fixture_sock = multicast.genSocket()
			>>> handler.request = ("The Test is STOP", tst_fixture_sock)
			>>> handler.client_address = ("224.0.1.3", 54321)
			>>> try:
			...     handler.handle()
			... except multicast.exceptions.ShutdownCommandReceived:
			...     print("ShutdownCommandReceived raised")
			ShutdownCommandReceived raised
			>>>
			>>> multicast.endSocket(tst_fixture_sock)
			>>>
		"""
		(data, sock) = self.request
		if data is None or not sock:  # pragma: no branch
			return  # nothing to do -- fail fast.
		# skipcq: PYL-R1705 -- otherwise can try to decode
		try:
			data = data.decode('utf8') if isinstance(data, bytes) else str(data)
		except UnicodeDecodeError:  # pragma: no cover -- defensive code branch
			if __debug__:
				module_logger.debug(
					"Received invalid UTF-8 data from %s",  # lazy formatting to avoid PYL-W1203
					self.client_address[0],
				)
			return  # silently ignore invalid UTF-8 data -- fail quickly.
		_logger = logging.getLogger(f"{type(self).__module__}.{type(self).__qualname__}")
		if __debug__:
			_logger.info(
				"%s SAYS: %s to ALL",  # lazy formatting to avoid PYL-W1203
				str(self.client_address[0]), data.strip(),
			)
		me = str(sock.getsockname()[0])
		_sender: multicast.send.McastSAY = None
		_sender = send.McastSAY()
		if __debug__:  # pragma: no cover -- defensive code branch
			_what = data.strip().replace("""\r""", str()).replace("""%""", """%%""")
			_logger.info(
				"%s HEAR: [%s SAID %s]",  # lazy formatting to avoid PYL-W1203
				str(me), str(self.client_address), str(_what),
			)
			_logger.info(
				"%s SAYS [ HEAR [ {%s SAID %s ] from %s ]",  # lazy formatting to avoid PYL-W1203
				str(me), str(_what), str(self.client_address), str(me),
			)
		_sender._sayStep(  # skipcq: PYL-W0212 - module ok
			self.client_address[0], self.client_address[1],
			f"HEAR [ {data.upper()} SAID {self.client_address} ] from {me}"  # noqa
		)
		if "STOP" in str(data):
			raise multicast.exceptions.ShutdownCommandReceived("SHUTDOWN") from None


class McastHEAR(multicast.mtool):
	"""
	Provides the HEAR tooling by subclassing multicast.mtool.

	This class sets up a multicast server that listens for messages and processes them accordingly.

		Testing:

		Testcase 0: First set up test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.hear is not None
			True
			>>> multicast._MCAST_DEFAULT_PORT is not None
			True
			>>> multicast._MCAST_DEFAULT_GROUP is not None
			True
			>>> multicast._MCAST_DEFAULT_TTL is not None
			True
			>>> multicast.hear.McastHEAR is not None
			True
			>>>

		Testcase 2: Recv should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> multicast.hear is not None
			True
			>>> multicast.hear.McastHEAR is not None
			True
			>>> multicast.hear.McastHEAR.__module__ is not None
			True
			>>> multicast.hear.McastHEAR.__proc__ is not None
			True
			>>> multicast.hear.McastHEAR.__epilogue__ is not None
			True
			>>> multicast.hear.McastHEAR.__prologue__ is not None
			True
			>>>


	"""

	__module__ = "multicast.hear"

	__name__ = "multicast.hear.McastHEAR"

	__proc__ = "HEAR"

	__epilogue__ = """Generally speaking you want to bind to one of the groups you joined in
		this module/instance, but it is also possible to bind to group which
		is added by some other programs (like another python program instance of this)
	"""

	__prologue__ = "Python Multicast Server for multicast input."

	@classmethod
	def setupArgs(cls, parser):
		"""
		Ignored for this subclass of mtool.

		See multicast.__main__.McastRecvHearDispatch.setupArgs instead.

		Args:
			parser (argparse.ArgumentParser): ignored.

		Returns:
			None: This method does not return a value.

		Note:
			This is trivial implementation make this an optional abstract method.
		"""
		pass  # skipcq - Optional abstract method

	def doStep(self, *args, **kwargs):
		"""
		Execute the HEAR operation for multicast communication.

		Overrides the `doStep` method from `mtool` to set up a server that listens for
		multicast messages and processes them accordingly.

		Args:
			*args: Variable length argument list containing command-line arguments.
			**kwargs: Arbitrary keyword arguments.

		Returns:
			tuple: A tuple containing a status indicator and an optional result message.
		"""
		_logger = logging.getLogger(f"{type(self).__module__}.{type(self).__qualname__}")
		_logger.debug(McastHEAR.__proc__)
		HOST = kwargs.get("group", multicast._MCAST_DEFAULT_GROUP)  # skipcq: PYL-W0212 - module ok
		PORT = kwargs.get("port", multicast._MCAST_DEFAULT_PORT)  # skipcq: PYL-W0212 - module ok
		server_initialized = False
		server = None
		try:
			_logger.debug(
				"Initializing server on port %d as %s.",  # lazy formatting to avoid PYL-W1203
				PORT, HOST,
			)
			with McastServer((HOST, PORT), HearUDPHandler) as server:
				server_initialized = True
				server.serve_forever()
		except KeyboardInterrupt as _cause:
			try:
				if server and server.socket:  # pragma: no cover
					old_sock = server.socket
					multicast.endSocket(old_sock)
			finally:
				raise KeyboardInterrupt(
					f"HEAR has stopped due to interruption signal, was previously listening on ({HOST}, {PORT}).",
				) from _cause
		finally:
			_logger.debug(
				"Finalizing server with port %d from %s.",  # lazy formatting to avoid PYL-W1203
				PORT, HOST,
			)
			if server:  # pragma: no cover
				# deadlocks if not called by other thread
				end_it = threading.Thread(name="Kill_Thread", target=server.shutdown, args=[])
				end_it.start()
				end_it.join(1)
		if __debug__:
			if server_initialized:
				module_logger.debug(
					"HEAR result was %s. Reporting success.",  # lazy formatting to avoid PYL-W1203
					server_initialized,
				)
			else:
				module_logger.debug(
					"HEAR result was %s. Reporting failure.",  # lazy formatting to avoid PYL-W1203
					server_initialized,
				)
		return (server_initialized, None)
