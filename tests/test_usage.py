#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Test Repo Template
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://github.com/reactive-firewall/python-repo/blob/HEAD/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tests of integration by usage.

	Caution: See details about Robust Imports documented in tests.context.

	Meta
	tests.test_usage.BasicIntegrationTestSuite

	Integration Tests - Fixtures:

		Test fixtures by importing test context.

		>>> import tests.test_usage as test_usage
		>>> import tests
		>>>

		>>> tests.test_usage.MulticastTestSuite #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<class...tests.test_usage.MulticastTestSuite...>
		>>>

		>>> tests.test_usage.BasicIntegrationTestSuite #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<class...tests.test_usage.BasicIntegrationTestSuite...>
		>>>

"""

__module__ = "tests"

try:
	try:
		import context
	except Exception as _root_cause:  # pragma: no branch
		del _root_cause  # skipcq - cleanup any error leaks early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from collections import namedtuple
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from multicast import __main__  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		import io
		from unittest.mock import patch
		from context import subprocess
		from context import Process
except Exception as _cause:
	raise ImportError("[CWE-758] Failed to import test context") from _cause


@context.markWithMetaTag("mat", "say", "hear")
class MulticastTestSuite(context.BasicUsageTestSuite):
	"""
	A test suite for special Multicast usage scenarios.

	This test suite extends the BasicUsageTestSuite and focuses on testing various
	aspects of the multicast functionality, including error handling, command-line
	interface behavior, and basic send/receive operations.

	Methods:
	--------
	test_aborts_WHEN_calling_multicast_GIVEN_invalid_tools():
		Tests the behavior of the CLI tools when given invalid tool names.

	test_say_is_stable_WHEN_calling_multicast_GIVEN_say_tool():
		Verifies the stability of the 'SAY' command with various message arguments.

	test_recv_aborts_WHEN_calling_multicast_GIVEN_invalid_args():
		Checks if the 'RECV' command properly aborts when given invalid arguments.

	test_hear_aborts_WHEN_calling_multicast_GIVEN_invalid_args():
		Ensures the 'HEAR' command aborts correctly when provided with invalid arguments.

	test_hear_is_stable_WHEN_calling_multicast_GIVEN_invalid_tool():
		Tests the stability of the 'HEAR' command when given an invalid tool (--hex).

	test_noop_stable_WHEN_calling_multicast_GIVEN_noop_args():
		Verifies the stability of the 'NOOP' command.

	test_help_works_WHEN_calling_multicast_GIVEN_help_tool():
		Checks if the 'HELP' command functions correctly.

	test_hear_works_WHEN_say_works():
		Tests the basic send and receive functionality using 'SAY' and 'HEAR' commands.

	test_recv_Errors_WHEN_say_not_used():
		Verifies that 'RECV' command produces an error when 'SAY' is not used.

	Notes:
	------
	- This test suite uses subprocess calls to test the multicast CLI interface.
	- Some tests involve multiprocessing to simulate concurrent operations.
	- Ensure proper network configuration for multicast tests to function correctly.

	Warnings:
	---------
	- Some tests may require specific network conditions to pass successfully.
	- Failure in these tests may indicate issues with the multicast implementation
		or the testing environment rather than actual bugs in the code.
	"""

	__module__ = "tests.test_usage"

	__name__ = "tests.test_usage.MulticastTestSuite"

	def test_aborts_WHEN_calling_multicast_GIVEN_invalid_tools(self):
		"""Tests the impossible state for CLI tools given bad tools"""
		theResult = False
		fail_fixture = str("multicast.__main__.McastDispatch().useTool(JUNK) == error")
		tst_dispatch = multicast.__main__.McastDispatch()
		test_junk_values = ["", "NoSuchTool", None]
		try:
			for tst_in in test_junk_values:
				(test_code, test_fixture) = tst_dispatch.useTool(tst_in)
				self.assertEqual(type(test_code), type(True))
				self.assertIsNone(test_fixture)
				self.assertTupleEqual(
					tst_dispatch.useTool(tst_in),
					(False, None),  # skipcq: PTC-W0020  - This is test-code.
					fail_fixture
				)
			theResult = True
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_say_is_stable_WHEN_calling_multicast_GIVEN_say_tool(self):
		"""
		Tests the message argument for expected syntax given simple args.

		First check that the --message argument requires a message value, or exits(2) as per CEP-8.
		Second check that providing the message value "test" is sufficient to succeed with exit(0).

		Rational of these tests are simple enough, the mis-use of the SAY sub-command should result
		in an argument error value of 2, due to misuse of shell/CLI builtin as per CEP-8, while a
		value of 0 should indicate success.
		"""
		theResult = False
		fail_fixture = str(
			"multicast.__main__.McastDispatch().useTool(SAY, message) != valid exit(0..3)"
		)
		try:
			with self.assertRaises(SystemExit) as rtn_val_a:
				_ = multicast.__main__.McastDispatch().doStep(["SAY", "--message"])
			(tst_err_rslt_b, rtn_val_b) = multicast.__main__.McastDispatch().doStep(
				["SAY", "--message", "test"]
			)
			tst_err_rslt_a = rtn_val_a.exception.code
			self.assertIsNotNone(rtn_val_a)
			self.assertIsNotNone(rtn_val_b)
			self.assertIsNotNone(tst_err_rslt_a)
			self.assertIsNotNone(tst_err_rslt_b)
			self.assertNotEqual(int(tst_err_rslt_a), int(0), str(rtn_val_a))
			self.assertNotEqual(int(tst_err_rslt_a), int(1), str(rtn_val_a))
			self.assertNotEqual(int(tst_err_rslt_b), int(1), str(rtn_val_b))
			self.assertNotEqual(int(tst_err_rslt_b), int(2), str(rtn_val_b))
			self.assertNotEqual(rtn_val_a, rtn_val_b)
			self.assertNotEqual(tst_err_rslt_a, tst_err_rslt_b)
			self.assertNotEqual(int(tst_err_rslt_b), int(tst_err_rslt_a))
			self.assertNotEqual(int(tst_err_rslt_a), int(tst_err_rslt_b))
			self.assertNotEqual(int(tst_err_rslt_b), int(3))
			self.assertNotEqual(int(tst_err_rslt_a), int(3))
			self.assertEqual(int(tst_err_rslt_a), int(2), str(rtn_val_a))
			self.assertEqual(int(tst_err_rslt_b), int(0), str(rtn_val_b))
			theResult = (int(tst_err_rslt_b) < int(tst_err_rslt_a))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_recv_aborts_WHEN_calling_multicast_GIVEN_invalid_args(self):
		"""Tests the message argument for failure given invalid input"""
		theResult = False
		fail_fixture = str("multicast.__main__.McastDispatch().useTool(RECV, junk) != exit(1)")
		try:
			with self.assertRaises(SystemExit) as rtn_val_c:
				_ = multicast.__main__.McastDispatch().doStep(["RECV", "--port", "test"])
			with self.assertRaises(SystemExit) as rtn_val_d:
				_ = multicast.__main__.McastDispatch().doStep(
					["RECV", "--port=test", "group=None"]
				)
			self.assertIsNotNone(rtn_val_c)
			self.assertIsNotNone(rtn_val_d)
			tst_err_rslt_c = rtn_val_c.exception.code
			tst_err_rslt_d = rtn_val_d.exception.code
			self.assertIsNotNone(tst_err_rslt_c)
			self.assertIsNotNone(tst_err_rslt_d)
			self.assertNotEqual(int(tst_err_rslt_c), int(0))
			self.assertNotEqual(int(tst_err_rslt_c), int(1))
			self.assertNotEqual(int(tst_err_rslt_d), int(1))
			self.assertEqual(int(tst_err_rslt_c), int(2))
			self.assertEqual(int(tst_err_rslt_d), int(2))
			self.assertEqual(int(tst_err_rslt_d), int(tst_err_rslt_c))
			self.assertEqual(int(tst_err_rslt_c), int(tst_err_rslt_d))
			self.assertNotEqual(int(tst_err_rslt_d), int(3))
			theResult = (int(tst_err_rslt_d) == int(tst_err_rslt_c))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_aborts_WHEN_calling_multicast_GIVEN_invalid_args(self):
		"""Tests the message argument for failure given invalid input"""
		theResult = False
		fail_fixture = str("multicast.__main__.McastDispatch().useTool(HEAR, junk) != exit(2)")
		try:
			with self.assertRaises(SystemExit) as rtn_val_e:
				_ = __main__.main(["HEAR", "--port", "test"])
			with self.assertRaises(SystemExit) as rtn_val_f:
				_ = __main__.main(["RECV", "--port", "test"])
			self.assertIsNotNone(rtn_val_e)
			self.assertIsNotNone(rtn_val_f)
			tst_err_rslt_e = rtn_val_e.exception.code
			tst_err_rslt_f = rtn_val_f.exception.code
			self.assertIsNotNone(tst_err_rslt_e)
			self.assertIsNotNone(tst_err_rslt_f)
			self.assertNotEqual(int(tst_err_rslt_e), int(0))
			self.assertNotEqual(int(tst_err_rslt_f), int(0))
			self.assertNotEqual(int(tst_err_rslt_e), int(1))
			self.assertNotEqual(int(tst_err_rslt_f), int(1))
			self.assertEqual(int(tst_err_rslt_e), int(2), "CEP-8 Violation. REGRESSION in HEAR")
			self.assertEqual(int(tst_err_rslt_f), int(2), "CEP-8 Violation. REGRESSION in RECV")
			self.assertNotEqual(rtn_val_e, rtn_val_f)
			self.assertNotEqual(int(tst_err_rslt_e), int(3), "Regression. 3 != 64")
			self.assertNotEqual(int(tst_err_rslt_f), int(3), "Regression. 3 != 64")
			self.assertEqual(int(tst_err_rslt_f), int(tst_err_rslt_e))
			theResult = (int(tst_err_rslt_f) == int(tst_err_rslt_e))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_ignores_WHEN_calling_multicast_GIVEN_invalid_args(self):
		"""Tests the group argument for new auto-default behavior given None."""
		theResult = False
		fail_fixture = str("multicast.__main__.main(HEAR, group=None) == ERROR")
		try:
			(rtn_val_f, tst_err_rslt_f) = __main__.main(
				["HEAR", "--group", "None", "--iface=None"]
			)
			self.assertIsNotNone(rtn_val_f)
			self.assertIsNotNone(tst_err_rslt_f)
			self.assertNotEqual(int(tst_err_rslt_f[0]), int(1), "REGRESSION in JOIN")
			self.assertNotEqual(int(tst_err_rslt_f[0]), int(70), "CEP-8 Violation.")
			self.assertNotEqual(int(tst_err_rslt_f[0]), int(2), "CEP-8 Violation.")
			self.assertNotEqual(int(tst_err_rslt_f[0]), int(3), "CEP-8 Violation.")
			self.assertEqual(int(tst_err_rslt_f[0]), int(0), fail_fixture)
			theResult = (int(tst_err_rslt_f[0]) == int(0))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_is_stable_WHEN_calling_multicast_GIVEN_invalid_tool(self):
		"""Tests the hexdump argument for failure given future tools"""
		theResult = False
		fail_fixture = str("multicast.__main__.McastDispatch().useTool(HEAR, hex) == error")
		try:
			self.assertTupleEqual(
				multicast.__main__.main(["HEAR", "--hex"]),
				(70, (False, None))  # skipcq: PTC-W0020  - This is test-code.
			)
			theResult = True
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_noop_stable_WHEN_calling_multicast_GIVEN_noop_args(self):
		"""Tests the NOOP state for multicast given bad input"""
		theResult = False
		fail_fixture = str("multicast.__main__.main(NOOP) == Error")
		try:
			self.assertIsNotNone(multicast.__main__.main(["NOOP"]), fail_fixture)
			self.assertIsNotNone(multicast.__main__.main(["NOOP"])[0])  # skipcq: PTC-W0020
			self.assertTupleEqual(
				multicast.__main__.main(["NOOP"]),
				(0, (True, None)),  # skipcq: PTC-W0020  - This is test-code.
			)
			theResult = True
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_help_works_WHEN_calling_multicast_GIVEN_help_tool(self):
		"""Tests the HELP argument for help usage"""
		theResult = False
		fail_fixture = str("multicast.__main__.McastDispatch().useTool(HELP, []) == Empty")
		try:
			with self.assertRaises(SystemExit) as rtn_val_h:
				multicast.__main__.McastDispatch().doStep(["HELP"])
			self.assertIsNotNone(rtn_val_h)
			theResult = True
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_works_WHEN_say_works(self):
		"""Tests the basic send and recv test"""
		theResult = False
		fail_fixture = str("SAY --> HEAR == error")
		sub_fail_fixture = str("SAY X-> HEAR == Error X-> HEAR :: (Error in SAY)")
		try:
			_fixture_SAY_args = [
				"--port",
				"59991",
				"--group",
				"'224.0.0.1'",
				"--message",
				"'test message'"
			]
			_fixture_HEAR_args = [
				"--port",
				"59991",
				"--groups",
				"'224.0.0.1'""",
				"--group",
				"'224.0.0.1'"
			]
			p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="HEAR",
				args=(["HEAR", _fixture_HEAR_args])
			)
			p.start()
			try:
				tst_fixture_sendDispatch = multicast.__main__.McastDispatch()
				self.assertIsNotNone(
					tst_fixture_sendDispatch.doStep(["SAY", _fixture_SAY_args])
				)
				self.assertIsNotNone(
					tst_fixture_sendDispatch.doStep(["SAY", _fixture_SAY_args])
				)
				self.assertIsNotNone(
					tst_fixture_sendDispatch.doStep(["SAY", _fixture_SAY_args])
				)
			except Exception as _root_cause:
				p.join()
				raise unittest.SkipTest(sub_fail_fixture) from _root_cause
			p.join()
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0), f"Unexpected Exit-Code: {p.exitcode}.")
			theResult = (int(p.exitcode) <= int(0))
		except unittest.SkipTest as baton:
			raise unittest.SkipTest(sub_fail_fixture) from baton
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_works_WHEN_fuzzed_and_say_works(self):
		"""Tests the basic send and recv test. Skips if fuzzing broke SAY fixture."""
		theResult = False
		fail_fixture = str("SAY --> HEAR == error")
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_SAY_args = [
				"--port",
				str(_fixture_port_num),
				"--group",
				"'224.0.0.1'",
				"--message",
				"'test message'"
			]
			_fixture_HEAR_args = [
				"HEAR",
				"--port",
				str(_fixture_port_num),
				"--groups",
				"'224.0.0.1'",
				"--group",
				"'224.0.0.1'"
			]
			p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="HEAR",
				args=(["HEAR", _fixture_HEAR_args])
			)
			p.start()
			try:
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep(["SAY", _fixture_SAY_args])
				)
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep(["SAY", _fixture_SAY_args])
				)
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep(["SAY", _fixture_SAY_args])
				)
			except Exception as _root_cause:
				p.join()
				raise unittest.SkipTest(fail_fixture) from _root_cause
			p.join()
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) <= int(0))
		except unittest.SkipTest as baton:
			raise unittest.SkipTest("Fuzzing broke SAY fixture.") from baton
		except Exception as _cause:
			context.debugtestError(_cause)
			self.skipTest(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_say_works_WHEN_using_stdin(self):
		"""Tests the basic send with streamed input test case."""
		theResult = False
		fail_fixture = str("STDIN --> SAY == error")
		_fixture_port_num = self._the_test_port
		try:
			say = multicast.send.McastSAY()
			self.assertIsNotNone(say)
			self.assertIsNotNone(_fixture_port_num)
			test_cases = [
				"",  # Empty input
				"Test message from stdin",  # Basic case
				"A" * 1024,  # Large input
				"Special chars: !@#$%^&*()",  # Special characters
				"Unicode: 你好世界",  # Unicode
				"HEAR\x00"  # Null byte injection
			]
			for test_input in test_cases:
				self.assertIsNotNone(test_input)
				with patch('sys.stdin', io.StringIO(test_input)):
					result = say.doStep(data=["-"], group="224.0.0.1", port=_fixture_port_num)
					self.assertIsNotNone(result)
					# Verify the message was actually sent
					theResult = result[0] or False
					self.assertTrue(theResult)  # Assuming there's a success indicator
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_recv_Errors_WHEN_say_not_used(self):
		"""Tests the basic noop recv test"""
		theResult = False
		fail_fixture = str("NOOP --> RECV != error")
		sub_fail_fixture = str("NOOP X-> RECV == Error X-> RECV :: (Error in NOOP)")
		try:
			_fixture_RECV_args = [
				"--port",
				"59992",
				"--groups",
				"'224.0.0.1'",
				"--group",
				"'224.0.0.1'"
			]
			p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="NOHEAR",
				args=(["RECV", _fixture_RECV_args])
			)
			p.start()
			try:
				test_cls = multicast.__main__.McastDispatch()
				self.assertTupleEqual(
					test_cls.doStep(["NOOP", []]),
					(int(0), (True, None)),  # skipcq: PTC-W0020  - This is test-code.
					sub_fail_fixture
				)
			except Exception as _root_cause:
				p.join()
				raise unittest.SkipTest(sub_fail_fixture) from _root_cause
			p.join()
			self.assertIsNotNone(p.exitcode, fail_fixture)
			self.assertEqual(int(p.exitcode), int(0), f"Unexpected Exit-Code: {p.exitcode}.")
			theResult = (int(p.exitcode) <= int(0))
		except unittest.SkipTest as baton:
			raise unittest.SkipTest(sub_fail_fixture) from baton
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


@context.markWithMetaTag("mat", "usage")
class BasicIntegrationTestSuite(context.BasicUsageTestSuite):
	"""
	A test suite for basic functional integration tests of the multicast module.

	This class inherits from context.BasicUsageTestSuite and provides a set of
	test cases to verify the functionality of the multicast module's command-line
	interface and core features.

	The suite includes tests for:
	- Printing usage information when called with the help argument
	- Verifying command-specific help output
	- Comparing responses between absolute and implicit module calls
	- Checking version information output
	- Validating error handling for invalid inputs
	- Profiling and stability checks for the NOOP command

	Attributes:
		_thepython (str): Path to the Python interpreter used for testing.

	Methods:
		setUp(): Prepares the test environment before each test method is run.
		test_prints_usage_WHEN_called_GIVEN_help_argument(): Verifies help output.
		test_prints_usage_WHEN_called_GIVEN_cmd_and_help_argument(): Checks command-specific help.
		test_equivilant_response_WHEN_absolute_vs_implicit(): Compares module call methods.
		test_prints_version_WHEN_called_GIVEN_version_argument(): Validates version output.
		test_Usage_Error_WHEN_the_help_command_is_called(): Ensures correct help output.
		test_profile_WHEN_the_noop_command_is_called(): Profiles the NOOP command.
		test_stable_WHEN_the_noop_command_is_called(): Checks NOOP command stability.
		test_invalid_Error_WHEN_cli_called_GIVEN_bad_input(): Verifies error handling.

	Note:
		This test suite relies on the context module for utility functions and
		the subprocess module for executing Python commands. It uses various
		assertion methods to validate the expected behavior of the multicast module.

	Example:
		To run this test suite, use the unittest module's test runner:

		```
		python -m unittest tests.test_usage.BasicIntegrationTestSuite
		```
	"""

	__module__ = "tests.test_usage"

	__name__ = "tests.test_usage.BasicIntegrationTestSuite"

	def setUp(self) -> None:
		"""
		Set up the test environment before each test method is run.

		This method calls the superclass's setUp method to ensure that any
		necessary initialization is performed. It also checks if the
		`_thepython` attribute is None, and if so, it skips the test with
		a message indicating that there is no Python command to test with.

		Args:
			None

		Returns:
			None

		Raises:
			unittest.SkipTest: If there is no Python command available for testing.
		"""
		super(self.__class__, self).setUp()  # skipcq: PYL-E1003 - this is more polymorphic
		if (self._thepython is None):
			self.skipTest(str("No python cmd to test with!"))

	def test_prints_usage_WHEN_called_GIVEN_help_argument(self):
		"""Test case for multicast.__main__ help."""
		theResult = False
		fail_fixture = str("multicast.__main__(--help) == not helpful")
		try:
			if (self._thepython is not None):
				theOutputtxt = context.checkPythonCommand(
					[str(self._thepython), str("-m"), str("multicast"), str("--help")],
					stderr=subprocess.STDOUT
				)
				self.assertIn(str("usage:"), str(theOutputtxt))
				if (str("usage:") in str(theOutputtxt)):
					theResult = True
				else:
					theResult = False
					context.debugUnexpectedOutput(
						str("usage:"), str(theOutputtxt), self._thepython
					)
		except Exception as _cause:
			context.debugtestError(_cause)
			del _cause  # skipcq - cleanup any error leaks early
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("Could Not find usage from multicast --help"))

	def test_prints_usage_WHEN_called_GIVEN_cmd_and_help_argument(self):
		"""Test case for multicast HEAR|RECV|SAY help."""
		theResult = None
		fail_fixture = str("multicast.__main__(--help) == not helpful")
		try:
			if (self._thepython is not None):
				for test_case in [".__main__", ""]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast{}").format(str(test_case)),
						str("--help")
					]
					theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					self.assertIn(str("usage:"), str(theOutputtxt))
					if (str("usage:") in str(theOutputtxt)):
						theResult = ((theResult is None) or (theResult is True))
					else:
						theResult = False
						context.debugUnexpectedOutput(
							str("usage:"), str(theOutputtxt), self._thepython
						)
		except Exception as _cause:
			context.debugtestError(_cause)
			del _cause  # skipcq - cleanup any error leaks early
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("Could Not find usage from multicast CMD --help"))

	def test_equivilant_response_WHEN_absolute_vs_implicit(self):
		"""Test case for multicast vs multicast.__main__"""
		theResult = False
		try:
			theExpectedText = context.checkPythonCommand(
				[str(self._thepython), str("-m"), str("multicast.__main__")],
				stderr=subprocess.STDOUT
			)
			self.assertIsNotNone(theExpectedText)
			theOutputtxt = context.checkPythonCommand(
				[str(self._thepython), str("-m"), str("multicast")], stderr=subprocess.STDOUT
			)
			self.assertIn(str(theExpectedText), str(theOutputtxt))
			if (str(theExpectedText) in str(theOutputtxt)):
				theResult = True
			else:
				theResult = False
				context.debugUnexpectedOutput(
					str(theExpectedText), str(theOutputtxt), self._thepython
				)
		except BaseException as _cause:
			context.debugtestError(_cause)
			del _cause  # skipcq - cleanup any error leaks early
			theResult = False
		self.assertTrue(theResult, str("Could Not swap multicast for multicast.__main__"))

	def test_prints_version_WHEN_called_GIVEN_version_argument(self):
		"""Test for result from --version argument: python -m multicast.* --version """
		theResult = False
		if (self._thepython is not None):
			try:
				for test_case in [".__main__", ""]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast{}").format(str(test_case)),
						str("--version")
					]
					theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					context.check_exec_command_has_output(self, args)
					theResult = (theOutputtxt is not None)
			except Exception as _cause:
				context.debugtestError(_cause)
				del _cause  # skipcq - cleanup any error leaks early
				theResult = False
		self.assertTrue(theResult, str("Could Not find version from multicast --version"))

	def _validate_help_output(self, args: list) -> bool:
		"""
		Helper method to validate help command output.

		Args:
			args (list) -- List of command arguments to execute

		Returns:
			bool: True if validation passes, False otherwise
		"""
		usageText = "usage:"
		theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
		subResult = False
		try:
			if isinstance(theOutputtxt, bytes):
				theOutputtxt = theOutputtxt.decode('utf8')
		except UnicodeDecodeError:
			theOutputtxt = str(repr(bytes(theOutputtxt)))
		self.assertIsNotNone(theOutputtxt)
		self.assertIn(str(usageText), str(theOutputtxt))
		if str(usageText) in str(theOutputtxt):
			subResult = True
		else:
			context.debugUnexpectedOutput(
				str(usageText), str(theOutputtxt), self._thepython
			)
		return subResult

	def test_Usage_Error_WHEN_the_help_command_is_called(self):
		"""Test case for multicast* --help."""
		theResult = False
		fail_fixture = str("multicast --help == not helpful")
		try:
			if (self._thepython is not None):
				for test_case in [".__main__", ""]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast{}").format(str(test_case)),
						str("--help")
					]
					with self.subTest(args=args):
						if self._validate_help_output(args):
							theResult = True
		except Exception as _cause:
			context.debugtestError(_cause)
			del _cause  # skipcq - cleanup any error leaks early
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("Could Not find usage from multicast --help"))

	def test_Usage_Error_WHEN_the_help_sub_command_is_called(self):
		"""
		Test case for validating help output of multicast sub-commands.

		This test ensures that the help output is correct for various sub-commands
		(HEAR, RECV, SAY) in both daemon and non-daemon modes. It validates that
		each command combination provides appropriate usage information.

		Test fixtures use named tuples to organize:
		- mode: daemon/non-daemon mode
		- command: the sub-command being tested
		"""
		theResult = False
		fail_fixture = str("multicast [HEAR|RECV] --help == not helpful")
		try:
			TestCase = namedtuple("TestCase", ["mode", "command"])
			inner_fixtures = [
				TestCase(mode="--daemon {}", command="HEAR"),
				TestCase(mode="{}", command="HEAR"),
				TestCase(mode="--daemon {}", command="RECV"),
				TestCase(mode="{}", command="RECV"),
				TestCase(mode="{}", command="SAY"),
				TestCase(mode="{}", command="NOOP")
			]
			if (self._thepython is not None):
				theResult = True
				for test_case_o in [".__main__", ""]:
					for test_case_i in inner_fixtures:
						self.assertIsInstance(test_case_i, TestCase)
						args = [
							str(self._thepython),
							str("-m"),
							str("multicast{}").format(str(test_case_o)),
							str(test_case_i.mode).format(str(test_case_i.command)),
							str("--help")
						]
						with self.subTest(args=args):
							if not self._validate_help_output(args):
								theResult = False
		except Exception as _cause:
			context.debugtestError(_cause)
			del _cause  # skipcq - cleanup any error leaks early
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("Could Not find usage from multicast --help"))

	def test_profile_WHEN_the_noop_command_is_called(self):
		"""Test case template for profiling"""
		theResult = False
		if (self._thepython is not None):
			try:
				for test_case in ["NOOP"]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(str(test_case))
					]
					theOutputtxt = context.timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtxt, bytes):
							theOutputtxt = theOutputtxt.decode('utf8')
					except UnicodeDecodeError:
						theOutputtxt = str(repr(bytes(theOutputtxt)))
					# or simply:
					self.assertIsNotNone(theOutputtxt)
					theResult = True
			except Exception as _cause:
				context.debugtestError(_cause)
				del _cause  # skipcq - cleanup any error leaks early
				theResult = False
		assert theResult

	def test_stable_WHEN_the_noop_command_is_called(self):
		"""Test case template for profiling"""
		theResult = False
		if (self._thepython is not None):
			try:
				for test_case in ["NOOP"]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(str(test_case))
					]
					context.checkPythonFuzzing(args, stderr=None)
					# now test it
					theResult = True
			except Exception as _cause:
				context.debugtestError(_cause)
				del _cause  # skipcq - cleanup any error leaks early
				theResult = False
		self.assertTrue(theResult, str("Could Not handle multicast NOOP"))

	def test_invalid_Error_WHEN_cli_called_GIVEN_bad_input(self):
		"""Test case template for invalid input to multicast CLI."""
		theResult = False
		if (self._thepython is not None):
			try:
				test_cases = [
					"BAdInPut",  # Basic invalid input
					int(1),  # Non-string input
					"exit",  # Reserved word
					"",  # Empty string
					" ",  # Whitespace
					"\t",  # Tab character
					"你好",  # Unicode
					"HEAR\x00",  # Null byte injection
					"SAY;ls"  # Command injection attempt
				]
				for test_case in test_cases:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(str(test_case))
					]
					theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					# or simply:
					if theOutputtxt:
						self.assertIsNotNone(theOutputtxt, f"Error with {str(test_case)}")
						self.assertIn(str("invalid choice:"), str(theOutputtxt))
						self.assertIn(repr(str(test_case)), str(theOutputtxt))
						theResult = True
			except Exception as _cause:
				context.debugtestError(_cause)
				del _cause  # skipcq - cleanup any error leaks early
				theResult = False
		self.assertTrue(theResult, str("Could Not handle negative inputs"))


if __name__ == '__main__':
	unittest.main()
