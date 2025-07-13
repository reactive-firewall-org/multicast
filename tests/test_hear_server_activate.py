#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
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


if __name__ == '__main__':
	unittest.main()
