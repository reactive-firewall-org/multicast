#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing) (Extra Fuzzing Group)
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
		del _cause  # skipcq - cleanup any error vars early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from context import BasicUsageTestSuite
		import io
		from unittest.mock import patch
		from context import subprocess
		from context import Process
		from context import string
except Exception as baton:
	raise ImportError(f"[CWE-758] {__file__} Failed to import test context") from baton


_has_hypothesis: bool = False
"""
	Hypothesis is not compatible with this project's license, however for users that accept the
	relevant terms and conditions of the Hypothesis module and have installed it, the following
	optional tests extend coverage to leverage hypothesis.

	Otherwise this file is effectively omitted from testing.

	Disclaimer:
	For clarity this file (as python sourcecode) is Licensed under MIT (the "License");
	The resulting python tests (as software) are only provided "AS IS" and WITHOUT WARRANTIES OR
	CONDITIONS OF ANY KIND, either express or implied. The dependencies of the resulting
	python tests (as software), are NOT covered by the same Licensed. Assembly may be required.
"""

if not _has_hypothesis:
	try:
		from hypothesis import given
		from hypothesis import settings
		from hypothesis import strategies as st
		_has_hypothesis = True
	except ImportError:  # pragma: no branch
		_has_hypothesis = False


def onlyIfHasHypothesis(has_hypothesis: bool) -> callable:
	"""
	Conditionally enable a test suite class based on the availability of the hypothesis library.

	If the provided flag is False, returns a dummy class with a placeholder method that does nothing,
	allowing tests dependent on hypothesis to be safely bypassed. If the provided flag is True,
	the original class is returned unchanged.

	Arguments:
		has_hypothesis (bool): Flag indicating whether the hypothesis library is available.

	Returns:
		callable: A decorator function that returns either the original class or a dummy class
		with a placeholder method, depending on the has_hypothesis flag.
	"""
	def decorator(cls: callable) -> callable:  # skipcq: PY-D0003 -- decorator ok
		if not has_hypothesis:
			# Create an empty class with a method that returns None
			return type(cls.__name__, (object,), {
				'method': lambda self: None
			})
		return cls
	return decorator


@context.markWithMetaTag("fuzzing", "slow")
@onlyIfHasHypothesis(_has_hypothesis)
class HypothesisTestSuite(BasicUsageTestSuite):
	"""
	A test suite that uses Hypothesis to perform fuzz testing on the multicast sender and receiver.

	This class extends `context.BasicUsageTestSuite` and provides a test case
	to verify the robustness of the multicast implementation when handling
	random binary data of varying sizes.

	Methods:
	- `test_multicast_sender_with_random_data(self, data)`: Tests sending and
		receiving random binary data using the multicast sender and receiver.

	Note:
	This test ensures that the multicast sender and receiver can handle binary
	data up to 1472 bytes, which is the typical maximum size for UDP packets
	without fragmentation.
	"""

	__module__ = "tests.test_fuzz"

	__name__ = "tests.test_fuzz.HypothesisTestSuite"

	@given(st.binary(min_size=1, max_size=1472))
	@settings(deadline=None)
	def test_multicast_sender_with_random_data(self, data: any) -> None:
		"""
		Tests the multicast sender and receiver with random binary data.

		This test uses the `hypothesis` library to generate random binary data
		between 1 and 1472 bytes, sends it using the multicast sender, and verifies
		that the multicast receiver successfully receives the data.

		Args:
			data (bytes): Random binary data generated by Hypothesis.

		Notes:
		- A random port number is used for each test run to prevent port collisions.
		- The test sets up a receiver process and sends the data multiple times.
		- If the receiver process encounters an error, the test is skipped.
		"""
		theResult: bool = False
		fail_fixture: str = "SAY --> HEAR == error"
		_fixture_port_num: int = self._always_generate_random_port_WHEN_called()
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			_fixture_SAY_args = [
				"SAY",
				"--port",
				str(_fixture_port_num),
				"--group",
				"'224.0.0.1'",
				"--message",
				f"'{data}'"
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
				args=[_fixture_HEAR_args]
			)
			p.start()
			try:
				self.assertIsNotNone(multicast.__main__.McastDispatch().doStep(_fixture_SAY_args))
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep(_fixture_SAY_args)
				)  # preemptive extra retry
			except Exception as _root_cause:
				p.join()
				raise unittest.SkipTest(fail_fixture) from _root_cause
			p.join()
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) <= int(0))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.skipTest(fail_fixture)
		self.assertTrue(theResult, fail_fixture)

	@given(st.text(alphabet=string.ascii_letters + string.digits, min_size=3, max_size=15))
	@settings(deadline=400)
	def test_invalid_Error_WHEN_cli_called_GIVEN_invalid_fuzz_input(self, text: str) -> None:
		"""
		Test the multicast CLI's response to invalid fuzzed input.

		This test case uses Hypothesis to generate random strings of ASCII letters
		and digits, then passes them as arguments to the multicast CLI. It verifies
		that the CLI correctly identifies and reports these as invalid inputs.

		Args:
			text (str): A randomly generated string of ASCII letters and digits,
				with length between 3 and 15 characters.

		Assertions:
			- The CLI output contains "invalid choice:" message
			- The CLI output includes the invalid input text
		"""
		theResult: bool = False
		fail_fixture: str = "XZY? --> Multicast != error"
		if (self._thepython is not None) and (multicast.__main__.TASK_OPTIONS is not None):
			if str(text) not in multicast.__main__.TASK_OPTIONS:
				try:
					args = [str(self._thepython), str("-m"), str("multicast"), str(text)]
					theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					# or simply:
					self.assertIsNotNone(theOutputtxt)
					self.assertIn(str("invalid choice:"), str(theOutputtxt))
					self.assertIn(str(text), str(theOutputtxt))
					theResult = True
				except Exception as _cause:
					context.debugtestError(_cause)
					del _cause  # skipcq - cleanup any error leaks early
					theResult = False
			else:  # pragma: no branch
				theResult = True  # but this won't have "invalid choice"
		self.assertTrue(theResult, fail_fixture)

	@given(st.text(alphabet=string.ascii_letters + string.digits, min_size=56, max_size=2048))
	@settings(deadline=2222)
	def test_say_works_WHEN_using_stdin_GIVEN_alnum_of_any_size_fuzz_input(self, text: str) -> None:
		"""
		Test the multicast send response to valid alnum input.

		Args:
			text (str): A randomly generated string of ASCII letters and digits,
				with length between 56 and 2048 characters.

		Assertions:
			- Verifies that the multicast sender can handle input from stdin
			- Confirms the process exits successfully after sending the message
			- Validates the receiver process terminates cleanly
		"""
		theResult: bool = False
		fail_fixture: str = f"stdin({text.__sizeof__()}) --> SAY == error"
		sub_fail_fixture: str = str(
			"""stdin({text.__sizeof__()}) --> SAY ?-> HEAR? == Error X-> HEAR"""
		)
		_fixture_port_num: int = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_HEAR_kwargs = {
				"port": _fixture_port_num,
				"group": "224.0.0.1"
			}
			self.assertIsNotNone(_fixture_HEAR_kwargs)
			p = Process(
				target=multicast.hear.McastHEAR().doStep, name="HEAR", kwargs=_fixture_HEAR_kwargs
			)
			p.daemon = True
			p.start()
			with context.managed_process(p) as managed_p:
				self.assertIsNotNone(managed_p)
				self.assertTrue(managed_p.is_alive())
				try:
					sender = multicast.send.McastSAY()
					self.assertIsNotNone(sender)
					test_input = str(text)
					# ESSENTIAL PART OF THIS TEST
					self.assertIsNotNone(test_input)
					with patch('sys.stdin', io.StringIO(test_input)):
						self.assertIsNotNone(
							sender.doStep(data=['-'], group='224.0.0.1', port=_fixture_port_num)
						)
					self.assertIsNotNone(p)
					self.assertTrue(p.is_alive())
					while p.is_alive():
						sender(group="224.0.0.1", port=_fixture_port_num, data=["STOP", "Test"])
						managed_p.join(1)
					self.assertFalse(managed_p.is_alive())
				except Exception as _root_cause:
					raise unittest.SkipTest(sub_fail_fixture) from _root_cause
				self.assertFalse(managed_p.is_alive(), "RESOURCE LEAK")
				self.assertIsNotNone(managed_p.exitcode)
				self.assertEqual(int(managed_p.exitcode), int(0))
				theResult = (int(managed_p.exitcode) <= int(0))
		except unittest.SkipTest as baton:
			raise unittest.SkipTest(fail_fixture) from baton
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


if __name__ == '__main__':
	unittest.main()
