#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
# ..................................
# Copyright (c) 2017-2026, Mr. Walls
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

__module__ = "tests"

try:
	try:
		import context
	except Exception as _cause:  # pragma: no branch
		del _cause  # skipcq - cleanup any error vars early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		import threading
		import socket
		import socketserver
except Exception as baton:
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("mat", "hear")
class McastServerActivateTestSuite(context.BasicUsageTestSuite):
	"""Test suite for verifying multicast server activation functionality.

	This test suite focuses on the proper initialization and activation
	of the multicast server, including socket setup and cleanup procedures.
	"""

	__module__ = "tests.test_hear_server_activate"

	__name__ = "tests.test_hear_server_activate.McastServerActivateTestSuite"

	def test_server_activate(self):
		"""
		Test multicast server activation and socket initialization.

		Verifies that:
			1. Server socket is properly initialized
			2. Socket type is set to SOCK_DGRAM
			3. Server thread starts successfully
			4. Cleanup is performed correctly
		"""
		# Define multicast constants
		MCAST_GROUP = '224.0.0.2'
		THREAD_JOIN_TIMEOUT = 5.0
		final_result = False

		# Define a simple request handler
		class SimpleHandler:
			"""
			A simple request handler for processing incoming requests.

			This class serves as a placeholder for handling requests. The
			actual handling logic is not implemented in this fixture, as
			the focus is on the server activation.
			"""
			def handle(self):
				"""
				Handle an incoming request.

				This method is intended to contain the logic for processing
				a request. In this case, it is just a test fixture and does not
				perform any actions.
				"""
				pass  # Handler logic is not the focus here

		# Create an instance of McastServer
		server_address = (MCAST_GROUP, 0)  # Bind to any available port
		server = multicast.hear.McastServer(server_address, SimpleHandler)

		# Start the server in a separate thread

		def run_server() -> None:
			"""
			Start the server and run it indefinitely.

			This function activates the server and begins serving requests
			in a blocking manner. It is intended to be run in a separate
			thread to allow other operations to continue concurrently.

			Note:
				This function will not return until the server is stopped.
			"""
			server.server_activate()
			server.serve_forever()

		server_thread = threading.Thread(target=run_server)
		server_thread.daemon = True
		server_thread.start()
		try:
			# Check that the socket is properly initialized
			self.assertIsNotNone(server.socket)
			self.assertEqual(server.socket.type, socket.SOCK_DGRAM)
			# Since we're not sending actual data, just ensure the server is running
			final_result = server_thread.is_alive()
		finally:
			# Clean up the server
			server.shutdown()
			server.server_close()
			server_thread.join(timeout=THREAD_JOIN_TIMEOUT)
			self.assertFalse(server_thread.is_alive(), "Server thread did not terminate")
		self.assertTrue(final_result)


@context.markWithMetaTag("mat", "hear")
class HearServerInitTestSuite(context.BasicUsageTestSuite):

	def test_initialization_with_valid_address(self):
		"""
		Test multicast server initialization with a valid address.

		Verifies that:
			1. The server instance is of the correct type (McastServer).
			2. The server instance is also recognized as a UDPServer.
			3. Cleanup is performed correctly after initialization.
		"""
		server = multicast.hear.McastServer(('224.0.0.1', 12345), None)
		self.assertIsInstance(server, multicast.hear.McastServer)
		self.assertIsInstance(server, socketserver.UDPServer)
		server.server_close()  # Clean up

	def test_initialization_with_logger_name(self):
		"""
		Test multicast server initialization with a specific logger name.

		Verifies that:
			1. The logger is properly initialized.
			2. The logger's name ends with the expected multicast address.
			3. Cleanup is performed correctly after initialization.
		"""
		test_addr = ('239.0.0.9', 23456)
		server = multicast.hear.McastServer(test_addr, None)
		self.assertIsNotNone(server.logger)
		self.assertTrue(server.logger.name.endswith('239.0.0.9'))
		server.server_close()  # Clean up

	def test_initialization_without_address(self):
		"""
		Test multicast server initialization without a valid address.

		Verifies that:
			1. The logger is initialized with the default name when server_address is None.
			2. The logger is initialized with the default name when server_address is an empty tuple.
			3. Cleanup is performed correctly after initialization.
		"""
		server = multicast.hear.McastServer(None, None)
		self.assertIsNotNone(server.logger)
		self.assertEqual(
			server.logger.name,
			f"multicast.hear.McastServer.{multicast._MCAST_DEFAULT_GROUP}"
		)
		server.server_close()  # Clean up

		server = multicast.hear.McastServer((), None)
		self.assertIsNotNone(server.logger)
		self.assertEqual(
			server.logger.name,
			f"multicast.hear.McastServer.{multicast._MCAST_DEFAULT_GROUP}"
		)
		server.server_close()  # Clean up


if __name__ == '__main__':
	unittest.main()
