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

"""
Test module for verifying cleanup behavior of the multicast hearing mechanism.

This module contains test suites that verify proper resource cleanup and process
termination when the multicast hearing process receives shutdown signals.
"""

__module__ = "tests"

try:
	"""Handle imports with CWE-758 mitigation.

	This implementation uses a nested try-except pattern to:
	1. Attempt direct context import
	2. Fallback to relative import
	3. Validate context module integrity
	4. Import required dependencies

	References:
	- CWE-758: Reliance on Undefined, Unspecified, or Implementation-Defined Behavior
	"""
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
		from context import Process
		from unittest.mock import MagicMock
		import socket
except ImportError as baton:
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("mat", "hear")
class HearCleanupTestSuite(context.BasicUsageTestSuite):
	"""
	Test suite for verifying the cleanup behavior of the multicast hearing mechanism.

	This suite tests that the `McastHEAR` class correctly releases resources
	and terminates gracefully when the hearing process receives a "STOP Test"
	message. It ensures that sockets are properly closed and no lingering
	processes remain after execution, adhering to the expected cleanup
	protocols.
	"""

	__module__ = "tests.test_hear_cleanup"

	__name__ = "tests.test_hear_cleanup.HearCleanupTestSuite"

	# Constants for test configuration
	STOP_DELAY_SECONDS: int = 1
	"""
	Time to wait for server cleanup after sending `STOP`.

	Must be > 0 to ensure server has an opportunity to handle messages.
	"""

	KILL_DELAY_SECONDS: int = 3
	"""
	Average time to wait for process completion after sending `STOP` before sending `SIGKILL`.

	Should be sufficient for handling `STOP` messages but not too long.
	"""

	PROCESS_TIMEOUT_SECONDS: int = 15
	"""
	Maximum time to wait for process completion after sending `STOP`.

	Should be sufficient for cleanup but not too long.
	"""

	EXPECTED_STOP_EXIT_CODE: int = 0
	"""
	Expected exit code when process receives `STOP` messages.

	`0` = `success` as per POSIX convention.
	"""

	TEST_MULTICAST_GROUP: str = "224.0.0.1"
	"""Standard multicast group address for testing."""

	def test_cleanup_on_exit(self) -> None:
		"""Test proper cleanup of McastHEAR when receiving STOP message.

		Prerequisites:
			- Available test port (self._the_test_port)
			- Multicast group 224.0.0.1 accessible

		Expected behavior:
			1. Start McastHEAR process in daemon mode
			2. Send "STOP Test" message
			3. Verify process terminates cleanly
			4. Ensure all resources are released

		Success criteria:
			- Process exits with code 0
			- No lingering processes or sockets
		"""
		theResult: bool = False
		fail_fixture: str = "STOP --> HEAR == error"
		_fixture_port_num: int = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_HEAR_kwargs = {
				"port": _fixture_port_num,
				"group": self.TEST_MULTICAST_GROUP,
			}
			self.assertIsNotNone(_fixture_HEAR_kwargs)
			p = Process(
				target=multicast.hear.McastHEAR().doStep, name="HEAR", kwargs=_fixture_HEAR_kwargs
			)
			p.daemon = True
			p.start()
			self.assertIsNotNone(p)
			self.assertTrue(p.is_alive())
			try:
				sender = multicast.send.McastSAY()
				self.assertIsNotNone(sender)
				p_tick: int = 0
				while p.is_alive() and (p_tick <= self.PROCESS_TIMEOUT_SECONDS):
					(didSend, _) = sender(
						group=self.TEST_MULTICAST_GROUP, port=_fixture_port_num,
						ttl=1, data="STOP Test",
					)
					if not didSend:  # pragma: no branch
						raise unittest.SkipTest("Can't test without transmitting") from None
					p.join(self.STOP_DELAY_SECONDS)
					p_tick += 1
				self.assertFalse(p.is_alive())
			except Exception as _root_cause:
				p.join(self.KILL_DELAY_SECONDS)
				if p.is_alive():
					p.terminate()
					p.join(self.STOP_DELAY_SECONDS)
					p.close()
				raise unittest.SkipTest(fail_fixture) from _root_cause
			p.join(self.PROCESS_TIMEOUT_SECONDS)
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(
				int(p.exitcode),
				int(self.EXPECTED_STOP_EXIT_CODE),
				"CEP-8 VIOLATION.",
			)
			theResult = (int(p.exitcode) <= int(self.EXPECTED_STOP_EXIT_CODE))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	@staticmethod
	def get_default_ip() -> str:
		"""Get the default IP address of the machine.

		Determines the machine's default IP address by creating a UDP socket connection
		to a reserved test IP address and retrieving the local socket address.

		Uses 203.0.113.1 (TEST-NET-3) for RFC 5737 compliance. Port 59095 is chosen as an
		arbitrary high port number.

		Args:
			None

		Returns:
			str: The IP address of the default network interface.

		Raises:
			CommandExecutionError: If the IP address cannot be determined.

		Meta Testing:

			>>> ip = HearCleanupTestSuite.get_default_ip()
			>>> isinstance(ip, str)
			True
			>>> len(ip.split('.'))
			4

		"""
		s = None
		try:
			# Create a socket connection to an external address
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			# Connect to a public non-routable IP
			s.connect(("203.0.113.1", 59095))
			# Get the IP address of the default interface
			ip = s.getsockname()[0]
		except OSError as _cause:  # pragma: no branch
			raise multicast.exceptions.CommandExecutionError("Failed to determine IP", 69) from _cause
		finally:
			if s is not None:
				s.close()
		return ip

	def test_should_not_invoke_kill_func_when_handle_error_not_called(self) -> None:
		"""Test that handle_error only conditionally calls kill_func on stop keyword.

		Verifies that the server properly handles mocked requests without
		the STOP command and never calls the kill_func to free up server resources early.

		Args:
			None (self is implicit)

		Returns:
			None

		Raises:
			AssertionError: If the test conditions are not met.
		"""
		theResult = False
		fail_fixture = "Mock(MSG) --> Handler-HEAR --> early shutdown"
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			# Create an instance of McastServer
			server_address = (self.TEST_MULTICAST_GROUP, _fixture_port_num)
			self.server = multicast.hear.McastServer(server_address, None, False)
			self.server.shutdown = MagicMock()  # Mock the shutdown method
			client_address = (self.get_default_ip(), _fixture_port_num)
			# Mock a request not containing "STOP"
			request = ("Any other message with O, P, S, T", multicast.genSocket())
			# Add assertions for initial state
			self.assertIsNotNone(request[1], "Socket should be created")
			self.assertIsInstance(request[0], str, "Request should be a string")
			try:
				self.server.handle_error(request, client_address)
				# Assert that the shutdown method was called
				self.server.shutdown.assert_not_called()
				theResult = True
			finally:
				# Clean up
				self.server.server_close()
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
		self.assertTrue(theResult, fail_fixture)

	def test_should_invoke_kill_func_when_handle_error_called(self) -> None:
		"""Test that kill_func calls shutdown on the server instance.

		Verifies that the server properly handles mocked requests with
		the STOP command and calls the kill_func to free up server resources.

		Args:
			None (self is implicit)

		Returns:
			None

		Raises:
			AssertionError: If the test conditions are not met.
		"""
		theResult = False
		fail_fixture = "Mock(STOP) --> Handler-HEAR --X shutdown"
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			# Create an instance of McastServer
			server_address = (self.TEST_MULTICAST_GROUP, _fixture_port_num)
			self.server = multicast.hear.McastServer(server_address, None, False)
			self.server.shutdown = MagicMock()  # Mock the shutdown method
			client_address = (self.get_default_ip(), _fixture_port_num)
			# Mock a request containing "STOP"
			request = ("STOP message", multicast.genSocket())
			# Add assertions for initial state
			self.assertIsNotNone(request[1], "Socket should be created")
			self.assertIsInstance(request[0], str, "Request should be a string")
			try:
				self.server.handle_error(request, client_address)
				# Assert that the shutdown method was called
				self.server.shutdown.assert_called_once()
				theResult = True
			finally:
				# Clean up
				self.server.server_close()
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
		self.assertTrue(theResult, fail_fixture)


if __name__ == "__main__":
	unittest.main()
