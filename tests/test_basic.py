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

__module__ = "tests"

try:
	try:
		import context
	except Exception as _root_cause:  # pragma: no branch
		del _root_cause  # skipcq - cleanup any error leaks early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import sys
		from context import unittest
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause


@context.markWithMetaTag("mat", "basic")
class BasicTestSuite(context.BasicUsageTestSuite):
	"""
	A test suite containing basic test cases for the multicast module.

	This class inherits from context.BasicUsageTestSuite and provides a set of
	unit tests to verify the fundamental functionality and error handling of
	the multicast module.

	Test Methods:
	- test_absolute_truth_and_meaning: An insanity test that always passes.
	- test_Does_Pass_WHEN_Meta_Test: Verifies basic assertion methods.
	- test_Does_Pass_WHEN_Using_Import_From_Syntax: Tests importing the multicast module.
	- test_Error_WHEN_the_help_command_is_called: Checks if the --help option raises an exception.
	- test_IsNone_WHEN_given_corner_case_input: Tests handling of invalid inputs.
	- test_None_WHEN_Nothing: A placeholder for additional tests.
	- test_Skip_UNLESS_linux_only: A test that only runs on Linux platforms.
	- test_Skip_UNLESS_darwin_only: A test that only runs on macOS platforms.

	Note:
	Some tests are conditionally skipped based on the operating system.
	The test methods use various assertion techniques to verify expected behaviors.

	This test suite is designed to catch basic issues and ensure the core
	functionality of the multicast module works as expected across different
	platforms.
	"""

	__module__ = "tests.test_basic"

	@unittest.skipUnless(__debug__, "Insanity Test. Good luck debugging.")
	def test_absolute_truth_and_meaning(self):
		"""Insanity Test 1: Because it only matters if we're not mad as hatters."""
		assert True

	@unittest.skipUnless(__debug__, "Insanity Test. Good luck debugging.")
	def test_Does_Pass_WHEN_Meta_Test(self):
		"""Insanity Test 2: for unittests assertion."""
		self.assertTrue(True)  # skipcq: PYL-W1503 - obviously this is an Insanity Test!
		self.assertFalse(False)  # skipcq: PYL-W1503 - obviously this is an Insanity Test!
		self.assertIsNone(None)  # skipcq: PYL-W1503 - obviously this is an Insanity Test!
		self.test_absolute_truth_and_meaning()
		self.test_None_WHEN_Nothing()

	@unittest.skipUnless(__debug__, "Insanity Test. Good luck debugging.")
	def test_None_WHEN_Nothing(self):
		"""Insanity Test 3: indirect call for unittests assertion."""
		self.assertIsNone(None)  # skipcq: PYL-W1503 - obviously this is an Insanity Test!
		# define new tests below

	def test_Does_Pass_WHEN_Using_Import_From_Syntax(self):
		"""Test case 0: importing multicast."""
		theResult = False
		try:
			from .context import multicast
			self.assertIsNotNone(multicast.__name__)
			self.assertIsNotNone(multicast.__module__)
			self.assertIsNotNone(multicast.__doc__)
			theResult = True
		except Exception as _cause:
			context.debugtestError(_cause)
			theResult = False
		self.assertTrue(theResult)

	def test_Error_WHEN_the_help_command_is_called(self):
		"""Test case 1: the --help options should error when called."""
		theResult = False
		try:
			from .context import multicast
			self.assertIsNotNone(multicast.__name__)
			theResult = (multicast.__name__ is not None)
			with self.assertRaises(Exception):
				raise RuntimeError("This is a test")
			with self.assertRaises(Exception):
				multicast.main(["--help"])
			theResult = True
		except Exception:
			theResult = False  # suppress non-testing errors
		self.assertTrue(theResult)

	def test_IsNone_WHEN_given_corner_case_input(self):
		"""Test case 2: Example for bad input directly into function."""
		theResult = False
		try:
			from .context import multicast
			theResult = (multicast.__name__ is not None)
			from multicast import __main__ as multicast
			tst_dispatch = multicast.McastDispatch()
			test_junk_values = [None, "JunkInput", "--Junk"]
			for tst_in in test_junk_values:
				(_ignored_code, test_fixture) = tst_dispatch.useTool(tst_in)
				self.assertIsNone(
					test_fixture,
					f"multicast.McastDispatch().useTool({str(tst_in)}) == ERROR"
				)
			theResult = True
		except Exception:
			theResult = False
		self.assertTrue(theResult)

	@unittest.skipUnless(sys.platform.startswith("linux"), "This test example requires linux")
	def test_Skip_UNLESS_linux_only(self):
		"""Linux is the test."""
		self.assertTrue(sys.platform.startswith("linux"))

	@unittest.skipUnless(sys.platform.startswith("darwin"), "This test example requires macOS")
	def test_Skip_UNLESS_darwin_only(self):
		"""MacOS is the test."""
		self.assertTrue(sys.platform.startswith("darwin"))


# leave this part
if __name__ == '__main__':
	unittest.main()
