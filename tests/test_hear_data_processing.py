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
	except ImportError as _cause:  # pragma: no branch
		del _cause  # skipcq - cleanup any error vars early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from unittest.mock import MagicMock
		from context import Process
except Exception as baton:
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("mat", "hear")
class RecvDataProcessingTestSuite(context.BasicUsageTestSuite):
	"""
	A test suite that validates the multicast sender and receiver's handling of empty data.

	Test cases:
		- Sending empty binary data.
		- Sending empty data followed by a stop command.
	"""

	__module__ = "tests.test_hear_data_processing"

	__name__ = "tests.test_hear_data_processing.RecvDataProcessingTestSuite"

	def test_multicast_sender_with_no_data(self) -> None:
		"""
		Tests the multicast sender and receiver with Empty binary data.

		"""
		theResult = False
		fail_fixture = "SAY -X] RECV? != error"
		_fixture_port_num = self._always_generate_random_port_WHEN_called()
		_fixture_mcast_addr = "224.0.0.1"
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			self.assertIsNotNone(_fixture_mcast_addr)
			_fixture_HEAR_args = [
				"--port",
				str(_fixture_port_num),
				"--groups",
				f"'{_fixture_mcast_addr}'",
				"--group",
				f"'{_fixture_mcast_addr}'",
			]
			p = Process(
				target=multicast.__main__.main, name="RECV", args=(
					"RECV",
					_fixture_HEAR_args,
				)
			)
			p.start()
			self.assertIsNotNone(p)
			try:
				sender = multicast.send.McastSAY()
				self.assertIsNotNone(sender)
				sender(group=_fixture_mcast_addr, port=_fixture_port_num, ttl=1, data=b'')
				self.assertIsNotNone(p)
				self.assertTrue(p.is_alive(), fail_fixture)
			except Exception as _root_cause:
				p.join(3)
				if p.is_alive():
					p.terminate()
					p.close()
				raise unittest.SkipTest(fail_fixture) from _root_cause
			p.join(5)
			self.assertFalse(p.is_alive(), "RESOURCE LEAK.")
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) == int(0))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_multicast_sender_with_no_data_before_follow_by_stop(self) -> None:
		"""
		Tests the multicast sender and receiver with Empty binary data, followed by a stop.

		"""
		theResult = False
		fail_fixture = "SAY -X] HEAR? != error"
		_fixture_port_num = self._always_generate_random_port_WHEN_called()
		_fixture_mcast_addr = "224.0.0.1"
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			_fixture_HEAR_args = [
				"--port",
				str(_fixture_port_num),
				"--groups",
				f"'{_fixture_mcast_addr}'",
				"--group",
				f"'{_fixture_mcast_addr}'",
			]
			p = Process(
				target=multicast.__main__.main,
				name="HEAR",
				args=(
					"--daemon",
					"HEAR",
					_fixture_HEAR_args,
				)
			)
			p.start()
			self.assertIsNotNone(p)
			try:
				sender = multicast.send.McastSAY()
				self.assertIsNotNone(sender)
				sender(group=_fixture_mcast_addr, port=_fixture_port_num, ttl=1, data=b'')
				self.assertIsNotNone(p)
				self.assertTrue(p.is_alive(), fail_fixture)
				while p.is_alive():
					sender(group=_fixture_mcast_addr, port=_fixture_port_num, data=["STOP"])
					p.join(1)
				self.assertFalse(p.is_alive(), "HEAR ignored STOP")
			except Exception as _root_cause:
				p.join(3)
				if p.is_alive():
					p.terminate()
					p.close()
				raise unittest.SkipTest(fail_fixture) from _root_cause
			p.join(5)
			self.assertFalse(p.is_alive(), "RESOURCE LEAK.")
			self.assertIsNotNone(p.exitcode, "Unexpected None == Exit-Code.")
			self.assertEqual(int(p.exitcode), int(0), f"Unexpected Exit-Code: {p.exitcode}.")
			theResult = (int(p.exitcode) >= int(0))
		except unittest.SkipTest as baton:
			raise unittest.SkipTest() from baton
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


class HearHandleNoneDataTestSuite(context.BasicUsageTestSuite):
	"""
	A test suite that uses MagicMock to perform light testing of the default handler for HEAR.

	"""

	__module__ = "tests.test_hear_data_processing"

	__name__ = "tests.test_hear_data_processing.HearHandleNoneDataTestSuite"

	def test_handle_none_data(self) -> None:
		"""Test that HearUDPHandler properly handles None data without raising exceptions.

		This test verifies that:
			1. The handler initializes correctly with None request data
			2. The handle() method executes without errors
			3. The handler properly processes the None data case
		"""
		_fixture_port_num = self._always_generate_random_port_WHEN_called()
		self.assertIsNotNone(_fixture_port_num)
		self.assertIsInstance(_fixture_port_num, int)
		handler = multicast.hear.HearUDPHandler(
			request=(None, None), client_address=('224.0.0.1', _fixture_port_num), server=None
		)
		# Mock the socket to prevent actual network calls
		handler.request = (None, MagicMock())
		mock_socket = handler.request[1]
		handler.handle()
		# Verify that the handler processed the None data case correctly
		self.assertEqual(
			mock_socket.method_calls, [], "Socket should not be used when data is None"
		)

	def test_handle_with_invalid_utf8_data(self) -> None:
		"""Test that HearUDPHandler silently ignores invalid UTF-8 data.

		This test verifies that:
			1. The handler continues processing when receiving invalid UTF-8 data
			2. No exception is raised
			3. The handler silently ignores the decoding error
		"""
		_fixture_port_num = self._always_generate_random_port_WHEN_called()
		self.assertIsNotNone(_fixture_port_num)
		self.assertIsInstance(_fixture_port_num, int)
		_fixture_client_addr = ("224.0.0.1", _fixture_port_num)
		data = b'\xff\xfe\xfd\xfc'  # Invalid UTF-8 bytes
		sock = multicast.genSocket()
		handler = multicast.hear.HearUDPHandler(
			request=(data, sock), client_address=_fixture_client_addr, server=None
		)
		try:
			# Mock the processing method
			handler._process = MagicMock()
			# Should silently ignore invalid UTF-8 data
			handler.handle()  # If no exception is raised, the test passes
			# Verify handler state after processing invalid data
			self.assertIsNone(handler.server)  # Server should remain None
			self.assertEqual(handler.client_address, _fixture_client_addr)
			# Verify no data was processed
			handler._process.assert_not_called()
			# Test with different invalid UTF-8 sequences
			for invalid_data in [b'\xff', b'\xfe\xff', b'\xff\xff\xff']:
				handler.request = (invalid_data, sock)
				handler.handle()
				handler._process.assert_not_called()
		except Exception as _cause:
			self.fail(f"Handler raised an unexpected exception: {_cause}")
		finally:
			# Clean up socket
			multicast.endSocket(sock)


if __name__ == '__main__':
	unittest.main()
