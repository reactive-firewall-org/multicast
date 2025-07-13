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
Test module for verifying keyboard interrupt handling in multicast operations.

This module contains test suites that verify proper handling of `SIGINT` signals,
ensuring clean shutdown and resource cleanup during keyboard interrupts.
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
	except ImportError as _cause:  # pragma: no branch
		del _cause  # skipcq - cleanup any error leaks early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import sys
		from context import unittest
		from context import subprocess
		import signal
		import time
		from context import BasicUsageTestSuite
except ImportError as baton:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("extra", "coverage")
class TestHearKeyboardInterrupt(BasicUsageTestSuite):
	"""
	Test suite for verifying keyboard interrupt (SIGINT) handling.

	This suite ensures that the multicast service properly handles
	SIGINT signals by cleaning up resources and exiting gracefully
	with the expected status code (130).
	"""
	__module__ = "tests.test_hear_keyboard_interrupt"

	# Constants for test configuration
	STARTUP_DELAY_SECONDS: int = 1
	"""
	Time to wait for server initialization before sending `SIGINT`.

	Must be > 0 to ensure server is ready.
	"""

	PROCESS_TIMEOUT_SECONDS: int = 5
	"""
	Maximum time to wait for process completion after `SIGINT`.

	Should be sufficient for cleanup but not too long.
	"""

	EXPECTED_SIGINT_EXIT_CODE: int = 130
	"""
	Expected exit code when process receives SIGINT.

	`130` = `128` + `SIGINT(2)` as per POSIX convention.
	"""

	INVALID_ARGS_EXIT_CODE: int = 2
	"""Exit code indicating invalid command-line arguments."""

	TEST_MULTICAST_GROUP: str = "224.0.0.1"
	"""Standard multicast group address for testing."""

	COVERAGE_CMD_TEMPLATE: str = f"{sys.executable} -m coverage run -p --context=Integration"
	"""Coverage command template for test execution."""

	def _build_hear_command(self, port: int, group: str = "224.0.0.1") -> list[str]:
		"""
		Build the command for running the multicast HEAR service.

		Args:
			port (int): The port number to use
			group (str, optional): The multicast group. Defaults to "224.0.0.1"

		Returns:
			list: The command arguments list
		"""
		return [
			self.COVERAGE_CMD_TEMPLATE, "--source=multicast",
			"-m", "multicast",
			"--daemon", "HEAR",
			"--port", str(port),
			"--group", group
		]

	def test_hear_keyboard_interrupt(self) -> None:
		"""
		Test proper handling of keyboard interrupts (SIGINT).

		This test:
			1. Starts a multicast server (with coverage tracking)
			2. Waits for server initialization
			3. Sends a SIGINT signal to simulate Ctrl+C
			4. Verifies that the server exits with the expected status code

		Success criteria:
			- Server must exit with status code 130 (standard SIGINT exit code)
			- Server must not exit with status code 2 (invalid arguments)
		"""
		theResult: bool = False
		fail_fixture: str = "C^INT --> HEAR == error"
		_fixture_port_num: int = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_HEAR_args: list[str] = self._build_hear_command(
				port=_fixture_port_num,
				group=self.TEST_MULTICAST_GROUP
			)
			self.assertIsNotNone(_fixture_HEAR_args)
			process: subprocess.Popen = subprocess.Popen(
				context.checkCovCommand(*_fixture_HEAR_args),
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True
			)
			try:
				time.sleep(self.STARTUP_DELAY_SECONDS)
				process.send_signal(signal.SIGINT)
				stdout, stderr = process.communicate(timeout=self.PROCESS_TIMEOUT_SECONDS)
				self.assertIsNotNone(stdout, "Incomplete Test.")
				self.assertIsNotNone(stderr, "Incomplete Test.")
				self.assertIsNotNone(process.returncode, "Incomplete Test.")
				self.assertNotEqual(
					int(process.returncode),
					int(self.INVALID_ARGS_EXIT_CODE),
					"Invalid Test Arguments."
				)
				self.assertEqual(
					int(process.returncode),
					int(self.EXPECTED_SIGINT_EXIT_CODE),
					"CEP-8 VIOLATION."
				)
				theResult = (int(process.returncode) >= int(1))
			finally:
				process.kill()
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


# leave this part
if __name__ == "__main__":
	unittest.main()
