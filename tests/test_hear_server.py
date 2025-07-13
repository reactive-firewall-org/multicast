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
		import socket
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
except Exception as baton:
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("mat", "hear")
class McastHearTestSuite(context.BasicUsageTestSuite):  # skipcq: PTC-W0046 -- intermediate class

	__module__ = "tests.test_hear_server"

	__name__ = "tests.test_hear_server.McastHearTestSuite"

	@staticmethod
	def get_default_ip():
		"""Get the default IP address of the machine.

		Returns:
			str: The IP address of the default network interface.

		Note:
			Uses 203.0.113.1 (TEST-NET-3) for RFC 5737 compliance.
			Port 59095 is chosen as an arbitrary high port number.
		"""
		s = None
		try:
			# Create a socket connection to an external address
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			# Connect to a public non-routable IP
			s.connect(("203.0.113.1", 59095))
			# Get the IP address of the default interface
			ip = s.getsockname()[0]
		except OSError as _cause:
			raise multicast.exceptions.CommandExecutionError("Failed to determine IP", 69) from _cause
		finally:
			if s is not None:
				s.close()
		return ip


class McastServerTestSuite(McastHearTestSuite):
	"""Test suite for McastServer functionality.

	This suite verifies the server's behavior in handling various types of requests,
	error conditions, and resource management.

	Attributes:
		__module__ (str): Module identifier
		__name__ (str): Full class name
	"""

	__module__ = "tests.test_hear_server"

	__name__ = "tests.test_hear_server.McastServerTestSuite"

	def test_handle_error_without_stop_in_request(self) -> None:
		"""
		Test McastServer.handle_error with a non-STOP request.

		Verifies that the server properly handles requests without
		the STOP command and cleans up resources.
		"""
		theResult = False
		fail_fixture = "Mock(BLAH) --> Handler-HEAR == error"
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			# Create an instance of McastServer
			server_address = ('224.0.0.1', _fixture_port_num)
			server = multicast.hear.McastServer(server_address, multicast.hear.HearUDPHandler)
			client_address = (self.get_default_ip(), _fixture_port_num)
			# Mock a request not containing "STOP"
			request = ("Regular message", multicast.genSocket())
			# Add assertions for initial state
			self.assertIsNotNone(request[1], "Socket should be created")
			self.assertIsInstance(request[0], str, "Request should be a string")
			try:
				server.handle_error(request, client_address)
			finally:
				# Clean up
				server.server_close()
			theResult = (multicast.endSocket(request[1]) is None)
			self.assertTrue(theResult, "RESOURCE LEAK")
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
		self.assertTrue(theResult, fail_fixture)

	def test_handle_error_with_none_request(self) -> None:
		"""
		Test the behavior of the handle_error method when provided with a None request.

		This test verifies that when the handle_error method is called with None as the request,
		the method should handle the error gracefully without raising exceptions. The test checks
		that the request remains None after the error handling.

		Verifies that:
			1. The random port number is not None and is an integer.
			2. The McastServer initializes correctly with the specified server address and handler.
			3. The handle_error method can process a None request without raising an error.

		Fail Fixture:
			The test will fail if the handle_error method does not handle the None request correctly
			or if any unexpected exceptions are raised during the process.

		Raises:
			AssertionError: If the port number is None or not an integer.
			Exception: If any unexpected error occurs during processing.
		"""
		theResult: bool = False
		fail_fixtures: list = [
			"Server fixture was NOT initialized.",
			"Mock(EMPTY) --X Handler-HEAR != Safe",
		]
		_fixture_port_num: int = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			# Create an instance of McastServer
			server_address = ('224.0.0.1', _fixture_port_num)
			server = multicast.hear.McastServer(server_address, multicast.hear.HearUDPHandler)
			client_address = (self.get_default_ip(), _fixture_port_num)
			# check the server is
			self.assertIsNotNone(server, fail_fixtures[0])
			# Mock None as a request
			request = None
			self.assertIsNone(request, "RESOURCE LEAK")
			try:
				server.handle_error(request, client_address)
			finally:
				# Clean up
				server.server_close()
			theResult = (request is None)
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixtures[1])
		self.assertTrue(theResult, fail_fixtures[1])


class HearUDPHandlerTestSuite(McastHearTestSuite):
	"""
	Test suite for validating HearUDPHandler functionality.

	This suite tests the behavior of the UDP handler with various
	input combinations, including edge cases with None data and sockets.

	Attributes:
		__module__ (str): Module identifier
		__name__ (str): Full class name
	"""

	__module__ = "tests.test_hear_server"

	__name__ = "tests.test_hear_server.HearUDPHandlerTestSuite"

	def test_handle_with_none_data_and_sock(self) -> None:
		"""
		Test the behavior of the HearUDPHandler when provided with None data and socket.

		This test verifies that when the handler is initialized with None
		for both the request and the socket, it should return early without
		processing. The test checks that the handler's return value is
		None, indicating that no further action was taken.

		Verifies that:
			1. The random port number is not None and is an integer.
			2. The handler initializes correctly with None request and None socket.
			3. The resulting handler returns None when handling with None request and None socket.

		Fail Fixture:
			The test will fail if the handler does not return None when
			initialized with the specified parameters.

		Raises:
			AssertionError: If the port number is None or not an integer.
		"""
		fail_fixture = "Handler(None, None) --> HEAR == error"
		_fixture_port_num = self._the_test_port
		self.assertIsNotNone(_fixture_port_num)
		self.assertIsInstance(_fixture_port_num, int)
		handler = multicast.hear.HearUDPHandler(
			request=(None, None),
			client_address=(self.get_default_ip(), _fixture_port_num),
			server=None
		)
		self.assertIsNotNone(handler)
		# Should return early without processing
		result = handler.handle()
		self.assertIsNone(result, fail_fixture)

	def test_handle_with_data_none_sock(self) -> None:
		"""
		Test the behavior of the HearUDPHandler when provided with a None inputs.

		This test verifies that when the handler is initialized with a
		No-Op request and None socket, it should return early without
		processing. The test checks that the handler's return value is
		None, indicating that no further action was taken.

		Verifies that:
			1. That the random port number is not None and is an integer.
			2. The handler initializes at all with a request and a None socket.
			3. The resulting handler returns None when handling with None request and None socket.

		Fail Fixture:
			The test will fail if the handler does not return None when
			initialized with the specified parameters.

		Raises:
			AssertionError: If the port number is None or not an integer.
		"""
		fail_fixture = """Handler(None, None) --> HEAR == error"""
		_fixture_port_num = self._the_test_port
		self.assertIsNotNone(_fixture_port_num)
		self.assertIsInstance(_fixture_port_num, int)
		handler = multicast.hear.HearUDPHandler(
			request=(b"No-Op", None),
			client_address=(self.get_default_ip(), _fixture_port_num),
			server=None
		)
		self.assertIsNotNone(handler)
		# Should return early without processing
		result = handler.handle()
		self.assertIsNone(result, fail_fixture)

	def test_handle_with_valid_data_and_sock(self) -> None:
		"""
		Test the behavior of the HearUDPHandler when provided with valid data and socket.

		This test verifies that when the handler is initialized with a valid
		request and a valid socket, it should process the message correctly.
		The test checks that the handler's return value is None, indicating
		successful processing.

		Verifies that:
			1. The random port number is not None and is an integer.
			2. The handler initializes correctly with a valid request and socket.
			3. The resulting handler processes the message without errors.

		Fail Fixture:
			The test will fail if the handler does not return None when
			handling the valid request and socket.

		Raises:
			AssertionError: If the port number is None or not an integer.
			Exception: If any unexpected error occurs during processing.
		"""
		sock = multicast.genSocket()
		fail_fixture = """Handler("The Test", sock) --> HEAR == error"""
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			handler = multicast.hear.HearUDPHandler(
				request=(b"The Test", sock),
				client_address=(self.get_default_ip(), _fixture_port_num),
				server=None
			)
			self.assertIsNotNone(handler)
			# Should process the message
			result = handler.handle()
			# Clean up socket
			self.assertIsNone(multicast.endSocket(sock), "RESOURCE LEAK")
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
		self.assertIsNone(result, fail_fixture)


if __name__ == '__main__':
	unittest.main()
