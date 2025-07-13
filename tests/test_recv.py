#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
# ..................................
# Copyright (c) 2025, Mr. Walls
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

"""Test module for multicast.recv functionality.

This module provides test cases for the recv module, focusing on the
McastRECV.doStep method's branching logic for success/failure logging.
"""


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
		from context import sys
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from unittest import mock
		import io
except ImportError as baton:
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("extra", "coverage")
class McastRECVTestSuite(context.BasicUsageTestSuite):
	"""Test cases for McastRECV class doStep method."""

	__module__ = "tests.test_recv"

	def setUp(self) -> None:
		"""Set up test fixtures."""
		super(McastRECVTestSuite, self).setUp()
		self.recv_tool = multicast.recv.McastRECV()
		# Store original stdout for later restoration
		self.original_stdout = sys.stdout

	def tearDown(self) -> None:
		"""Tear down test fixtures."""
		# Restore original stdout
		sys.stdout = self.original_stdout
		super(McastRECVTestSuite, self).tearDown()

	@mock.patch('multicast.recv.module_logger')
	def test_doStep_with_response(self, mock_logger: mock.MagicMock) -> None:
		"""Test case 1: Test doStep with successful response."""
		# Mock _hearstep to return a non-empty response
		with mock.patch.object(
			multicast.recv.McastRECV, '_hearstep', return_value='Test response',
		) as mock_hear:
			result, response = self.recv_tool.doStep(is_std=False)
			# Verify results
			self.assertTrue(result)
			self.assertEqual(response, 'Test response')
			# Verify logger called with success message
			mock_logger.info.assert_called_once_with("Success")
			# Verify _hearstep was called with expected defaults
			mock_hear.assert_called_once()

	@mock.patch('multicast.recv.module_logger')
	def test_doStep_with_empty_response(self, mock_logger: mock.MagicMock) -> None:
		"""Test case 2: Test doStep with empty response."""
		# Mock _hearstep to return an empty response
		with mock.patch.object(
			multicast.recv.McastRECV, '_hearstep', return_value='',
		) as mock_hear:
			result, response = self.recv_tool.doStep(is_std=False)
			# Verify results: expect a failure (False) and no response (None)
			self.assertFalse(result)
			self.assertIsNone(response)
			# Verify logger called with nothing received message
			mock_logger.debug.assert_any_call("Nothing Received.")
			# Verify _hearstep was called with expected defaults
			mock_hear.assert_called_once()

	@mock.patch('multicast.recv.module_logger')
	def test_doStep_logging_sequence_success(self, mock_logger: mock.MagicMock) -> None:
		"""Test case 3: Verify logging sequence for successful response."""
		# Mock _hearstep to return a non-empty response
		with mock.patch.object(
			multicast.recv.McastRECV, '_hearstep', return_value='Test response',
		):
			self.recv_tool.doStep(is_std=False)
			# Verify initial debug log and success log
			mock_logger.debug.assert_any_call("RECV")
			mock_logger.info.assert_called_once_with("Success")
			# Ensure that "Nothing Received" is not logged
			for call in mock_logger.debug.call_args_list:
				self.assertNotEqual(call[0][0], "Nothing Received.")

	@mock.patch('multicast.recv.module_logger')
	def test_doStep_logging_sequence_empty(self, mock_logger: mock.MagicMock) -> None:
		"""Test case 4: Verify logging sequence for empty response."""
		# Mock _hearstep to return an empty response
		with mock.patch.object(
			multicast.recv.McastRECV, '_hearstep', return_value='',
		):
			self.recv_tool.doStep(is_std=False)
			# Verify initial debug log and nothing received log
			mock_logger.debug.assert_any_call("RECV")
			mock_logger.debug.assert_any_call("Nothing Received.")
			# Verify that no success log was called
			mock_logger.info.assert_not_called()

	@mock.patch('multicast.recv.module_logger')
	def test_doStep_console_output(self, mock_logger: mock.MagicMock) -> None:
		"""Test case 5: Test console output when is_std is True with data."""
		# Capture printed output by redirecting stdout
		mock_stdout = io.StringIO()
		sys.stdout = mock_stdout
		# Mock _hearstep to return a non-empty response
		with mock.patch.object(
			multicast.recv.McastRECV, '_hearstep', return_value='Test response',
		):
			self.recv_tool.doStep(is_std=True)
			# Verify that the response is printed to console
			output = mock_stdout.getvalue()
			self.assertIn('Test response', output)
			# Verify that the logger recorded the intended debug message
			mock_logger.debug.assert_any_call("Will Print to Console.")

	@mock.patch('multicast.recv.module_logger')
	def test_doStep_with_custom_parameters(self, mock_logger: mock.MagicMock) -> None:
		"""Test case 6: Test doStep with custom parameters."""
		# Mock _hearstep to capture and return custom test output
		with mock.patch.object(
			multicast.recv.McastRECV, '_hearstep', return_value='Custom test',
		) as mock_hear:
			custom_group: str = "224.0.0.2"
			custom_port: int = self._the_test_port
			custom_iface: str = "lo"
			self.recv_tool.doStep(
				groups=[custom_group],
				port=custom_port,
				iface=custom_iface,
				group=custom_group,
				is_std=False,
			)
			# Verify _hearstep is called with custom parameters
			mock_hear.assert_called_once_with(
				[custom_group], custom_port, custom_iface, custom_group,
			)
			# Verify that a success log is recorded for the custom parameters
			mock_logger.info.assert_called_once_with("Success")


if __name__ == '__main__':
	unittest.main()
