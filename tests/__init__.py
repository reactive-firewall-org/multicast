# -*- coding: utf-8 -*-

# Python Test Template
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

"""Multicast Testing Module.

	Package containing test suites and utilities for the multicast module.

	This package provides comprehensive testing coverage for various multicast functionalities
	including server operations, data processing, cleanup routines, and exception handling.

	For specific test cases, see:
		- Server operations: test_hear_server.McastServerTestSuite
		- Data processing: test_hear_data_processing.RecvDataProcessingTestSuite
		- Cleanup routines: test_hear_cleanup.HearCleanupTestSuite
		- Exception handling: test_exceptions.ExceptionsTestSuite

	Robust imports: These statements import the entire "multicast" module,
		allowing access to all its functionalities within the test environment.
		This may be flagged as an intentional cyclic import by pylint.
		See warning about cyclic-imports
		[here](https://pylint.pycqa.org/en/latest/user_guide/messages/refactor/cyclic-import.html)

	Testing:

	Testcase 0: Load tests fixtures

		>>> import tests as _tests
		>>> _tests.__module__ is not None
		True
		>>> _tests.__package__ is not None
		True
		>>>

	Testcase 1: Load tests

		>>> import tests as _tests
		>>> _tests.__module__ is not None
		True
		>>> import unittest as _unittest
		>>> _tests.TEST_GROUPS is not None
		True
		>>> _tests.get_test_suite is not None
		True
		>>>
		>>> output = _tests.get_test_suite()
		>>> output is not None
		True
		>>> isinstance(output, _unittest.TestSuite)
		True
		>>>

"""

__package__ = "tests"  # skipcq: PYL-W0622

__module__ = "tests"

try:
	import sys
	import os
	import unittest
	import types
	from typing import Optional
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] Module failed to import.") from _cause

try:
	import logging
	try:
		class ANSIColors:
			"""
			A class that defines ANSI color codes for terminal output.

			This class contains ANSI escape sequences for various colors and a
			mapping of logging levels to their corresponding colors. It also
			includes a nested class for a colored stream handler that formats
			log messages with the appropriate colors based on their severity.

			Attributes:
				BLACK (str): ANSI code for black text.
				RED (str): ANSI code for red text.
				GREEN (str): ANSI code for green text.
				YELLOW (str): ANSI code for yellow text.
				BLUE (str): ANSI code for blue text.
				MAGENTA (str): ANSI code for magenta text.
				CYAN (str): ANSI code for cyan text.
				GREY (str): ANSI code for grey text.
				AMBER (str): ANSI code for amber text.
				REDBG (str): ANSI code for red background.
				ENDC (str): ANSI code to reset text formatting.

				logging_color (dict): A dictionary mapping logging levels to their
										corresponding ANSI color codes.
				logging_level (dict): A dictionary mapping logging levels to their
										corresponding logging module constants.
			"""
			# Define ANSI color codes
			BLACK = """\033[30m"""
			RED = """\033[31m"""
			GREEN = """\033[32m"""
			YELLOW = """\033[33m"""
			BLUE = """\033[34m"""
			MAGENTA = """\033[35m"""
			CYAN = """\033[36m"""
			GREY = """\033[37m"""
			AMBER = """\033[93m"""
			REDBG = """\033[41m"""  # Red background
			ENDC = """\033[0m"""

		logging_color = {
			'debug': ANSIColors.BLUE, 'info': ANSIColors.GREY,
			'warning': ANSIColors.AMBER,
			'error': ANSIColors.RED,
			'critical': str(str(ANSIColors.BLACK) + str(ANSIColors.REDBG)),
		}

		logging_level = {
			'debug': logging.DEBUG,
			'info': logging.INFO,
			'warning': logging.WARNING,
			'error': logging.ERROR,
			'critical': logging.CRITICAL,
		}

		class ColoredStreamHandler(logging.StreamHandler):
			"""
			A custom logging handler that outputs with color formatting based on the log level.

			This handler checks if the output stream is a terminal and applies
			the appropriate ANSI color codes to the log messages. If the output
			is not a terminal, it outputs plain text without color.

			Methods:
				emit(record: logging.LogRecord) -> None:
					Formats and writes the log message to the stream with
					appropriate color based on the log level.
			"""

			def emit(self, record: logging.LogRecord) -> None:
				"""
				Formats and writes the log message to the stream with color.

				Args:
					record (logging.LogRecord): The log record containing
												information about the log event.

				Raises:
					ValueError: If the log level is invalid or not recognized.
				"""
				# Get the log level as a string
				loglevel = record.levelname.lower()
				# Validate the log level
				if not isinstance(loglevel, str) or loglevel not in logging_color:
					raise ValueError("Invalid log level") from None  # pragma: no cover
				# Determine color based on whether the output is a terminal
				if sys.stdout.isatty():
					colorPrefix = logging_color[loglevel]  # skipcq: TCV-002
					endColor = ANSIColors.ENDC  # skipcq: TCV-002
				else:
					colorPrefix = ""
					endColor = ""
				# Format the message
				msg = self.format(record)
				formatted_msg = f"{colorPrefix}{msg}{endColor}"
				# Write the formatted message to the stream
				self.stream.write(formatted_msg + self.terminator)
				self.flush()

	except Exception as _root_cause:  # pragma: no branch
		raise ImportError("[CWE-909] Could Not Initialize Test Logger") from _root_cause
	# Setup logging for testing
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	handler = ColoredStreamHandler()
	root.addHandler(handler)
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] Logging failed to initialize.") from _cause

try:
	if 'multicast' not in sys.modules:
		import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
	else:  # pragma: no branch
		multicast = sys.modules["multicast"]
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] multicast Failed to import.") from _cause

try:
	_LOGGER = logging.getLogger(__module__)
	_LOGGER.debug("Initializing tests.")
	_DIR_NAME = str(".")
	_PARENT_DIR_NAME = str("..")
	_BASE_NAME = os.path.dirname(__file__)
	if 'multicast' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(_BASE_NAME, _PARENT_DIR_NAME)))
	if 'tests' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(_BASE_NAME, _DIR_NAME)))
except ImportError as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] multicast tests Failed to import.") from _cause

try:
	from tests import profiling as profiling  # skipcq: PYL-C0414
	from tests import test_basic
	from tests import test_exceptions
	from tests import test_deps
	# removed test_install_requires, in v2.0.9a3
	from tests import test_manifest
	from tests import test_build
	from tests import test_usage
	from tests import test_hear_server
	from tests import test_hear_server_activate
	from tests import test_hear_cleanup
	from tests import test_hear_data_processing
	from tests import test_hear_keyboard_interrupt

	depends = [
		profiling,
		test_basic,
		test_deps,
		test_build,
		test_manifest,
		test_usage,
		test_hear_server_activate,
		test_hear_cleanup,
		test_hear_data_processing,
		test_exceptions,
		test_hear_keyboard_interrupt,
		test_hear_server
	]

	try:
		from tests import test_fuzz
		depends.insert(10, test_fuzz)
	except Exception:  # pragma: no branch
		_LOGGER.exception("Error loading optional Fuzzing tests")

	for unit_test in depends:
		try:
			if unit_test.__name__ is None:  # pragma: no branch
				raise ImportError(
					f"Test module failed to import even the {str(unit_test)} tests."
				) from None
		except Exception as _root_cause:  # pragma: no branch
			raise ImportError("[CWE-758] Test module failed completely.") from _root_cause
except Exception as _cause:  # pragma: no branch
	_LOGGER.debug(str(type(_cause)))
	_LOGGER.exception(str(_cause))
	_LOGGER.debug(str((_cause.args)))
	del _cause  # skipcq - cleanup any error leaks early
	exit(0)  # skipcq: PYL-R1722 - intentionally allow overwriteing exit for testing

try:
	if 'tests.context' not in sys.modules:
		from tests import context
	else:  # pragma: no branch
		context = sys.modules["tests.context"]
except ImportError as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] context Failed to import.") from _cause


def loadDocstringsFromModule(module: types.ModuleType) -> unittest.TestSuite:
	"""
	Load and return a test suite containing doctests from the specified module.

	This function attempts to import the `doctest` module and uses it to find
	and load all doctests defined in the provided module. If the module is
	valid and contains doctests, a `unittest.TestSuite` object is returned
	containing those tests. If no doctests are found or if an error occurs
	during the loading process, appropriate messages are printed to the
	console.

	Notes:
	- The function checks if the `doctest` module is already imported to
		avoid unnecessary imports.
	- The `DocTestFinder` is configured with the following options:
		- `verbose=False`: Disables verbose output for the test discovery. (changed in v2.0.9a3)
		- `recurse=True`: Allows the finder to search for doctests in
			nested functions and classes.
		- `exclude_empty=True`: Excludes empty doctests from the results.
	- If no doctests are found in the specified module, a message is printed
		indicating that no tests were found.
	- Any other exceptions encountered during the loading process are caught
		and printed to the console.

	See Also:
		- get_test_suite: Function that uses `loadDocstringsFromModule` to build test suites
		- load_tests: Function that loads both regular tests and doctests

	Args:
		module (module) -- The Python module from which to load doctests. This should be a
			valid module object that has been imported. If the module is None,
			the function will return None.

	Returns:
		(unittest.TestSuite or None) -- A `unittest.TestSuite` object containing the
			doctests found in the specified module. If the module is None,
			the function returns None.

	Raises:
		ImportError
			If the `doctest` module fails to import, an ImportError is raised
			with a message indicating the failure.

	Meta-Testing:

		>>> import multicast
		>>> suite = loadDocstringsFromModule(multicast)  #doctest: +ELLIPSIS
		>>> if suite:
		...     print(f"Loaded {len(suite._tests)} doctests from "
		...         f"{multicast.__name__}")  # doctest: +ELLIPSIS
		Loaded ... doctests from ...
		>>>

	"""
	if not module:  # pragma: no branch
		return None
	try:
		if 'doctest' not in sys.modules:
			import doctest
		else:  # pragma: no branch
			doctest = sys.modules["doctest"]
	except Exception as _cause:  # pragma: no branch
		raise ImportError("[CWE-440] doctest Failed to import.") from _cause
	finder = doctest.DocTestFinder(verbose=False, recurse=True, exclude_empty=True)
	doc_suite = unittest.TestSuite()
	try:
		doc_suite.addTests(doctest.DocTestSuite(module=module, test_finder=finder))
	except ValueError as _cause:  # pragma: no branch
		# ValueError is raised when no tests are found
		_LOGGER.warning(
			"No doctests found in %s: %s",  # lazy formatting to avoid PYL-W1203
			module.__name__,
			_cause,  # log as just warning level, instead of exception (error), but still detailed.
			exc_info=True,
		)
	except Exception:
		_LOGGER.exception(
			"Error loading doctests from %s",  # lazy formatting to avoid PYL-W1203
			module.__name__,
		)
	return doc_suite


# === Test Suite Groups ===
MINIMUM_ACCEPTANCE_TESTS = {
	"bootstrap": [
		# Init/exceptions/env/skt tests
		test_exceptions.ExceptionsTestSuite,  # Also in basic, but crucial for bootstrap
	],
	"basic": [
		test_basic.BasicTestSuite,
	],
	"build": [
		# Build and packaging tests
		test_build.BuildPEP517TestSuite,
		test_manifest.ManifestInclusionTestSuite,
		test_build.BuildPEP621TestSuite,  # added in v2.0.9a3
		# removed test_install_requires.ParseRequirementsTestSuite in v2.0.9a3
	],
	"doctests": [
		# These will be loaded dynamically via DocTestSuite
		loadDocstringsFromModule(multicast),
		loadDocstringsFromModule(multicast.exceptions),
		loadDocstringsFromModule(multicast.env),
		loadDocstringsFromModule(multicast.skt),
		loadDocstringsFromModule(multicast.recv),
		loadDocstringsFromModule(multicast.send),
		loadDocstringsFromModule(multicast.hear),
	],
	"say": [
		# Tests focused on multicast/send.py
		test_usage.MulticastTestSuite,  # send-related tests
	],
	"hear": [
		# Tests focused on multicast/recv.py and multicast/hear.py
		test_hear_server.McastServerTestSuite,
		test_hear_server.HearUDPHandlerTestSuite,
		test_hear_server_activate.McastServerActivateTestSuite,
		test_hear_data_processing.RecvDataProcessingTestSuite,
		test_hear_data_processing.HearHandleNoneDataTestSuite,
		test_hear_cleanup.HearCleanupTestSuite,
	],
	"usage": [
		# Tests focused on multicast/__main__.py and API use cases
		test_usage.BasicIntegrationTestSuite,
	],
}


EXTRA_TESTS = {
	"coverage": [
		test_deps.BuildRequirementsTxtTestSuite,
		test_hear_keyboard_interrupt.TestHearKeyboardInterrupt,
		# Add other coverage-focused tests here
	],
	"linting": [],  # To be implemented
	"security": [],  # To be implemented
}

try:
	from tests import test_recv  # added in v2.0.7
	depends.insert(11, test_recv)
	EXTRA_TESTS["coverage"].append(test_recv.McastRECVTestSuite)
except Exception:  # pragma: no branch
	_LOGGER.warning("Error loading optional debug tests", exc_info=True)

try:
	EXTRA_TESTS["coverage"].append(loadDocstringsFromModule(__module__))
	EXTRA_TESTS["coverage"].append(loadDocstringsFromModule(context))
	EXTRA_TESTS["coverage"].append(loadDocstringsFromModule("tests.MulticastUDPClient"))
except Exception:  # pragma: no branch
	_LOGGER.warning("Error loading optional doctests", exc_info=True)
	# reported, so now just continue with testing

try:
	from tests import test_extra  # added in v2.0.7
	depends.insert(11, test_extra)
	EXTRA_TESTS["security"].append(test_extra.ExtraDocsUtilsTestSuite)
	import docs.utils
	EXTRA_TESTS["security"].append(loadDocstringsFromModule(docs.utils))
except Exception:  # pragma: no branch
	_LOGGER.warning("Error loading optional extra tests", exc_info=True)

try:
	FUZZING_TESTS = {
		"slow": [
			test_fuzz.HypothesisTestSuite,  # Assuming this exists
		],
		# Future fuzzing test categories to be added
	}
except Exception:
	FUZZING_TESTS = {"slow": []}

PERFORMANCE_TESTS = {
	"scalability": [],  # Future implementation
	"multi_sender": [],  # Future implementation
	"multi_receiver": [],  # Future implementation
}

# Load specific group/category
TEST_GROUPS = {
	"mat": MINIMUM_ACCEPTANCE_TESTS,
	"extra": EXTRA_TESTS,
	"fuzzing": FUZZING_TESTS,
	"performance": PERFORMANCE_TESTS,
}


def get_test_suite(
	group: Optional[str] = None,
	category: Optional[str] = None,
) -> unittest.TestSuite:
	"""Get a test suite based on group and category.

	Args:
		group (str): Test group ('mat', 'extra', 'fuzzing', 'performance')
		category (str): Specific category within the group

	Returns:
		unittest.TestSuite: The configured test suite
	"""
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()

	# Helper function to add test cases to suite
	def add_test_cases(test_cases: list) -> None:
		"""
		Adds a list of test cases to the test suite.

		This function iterates over the provided list of test cases. If a test case
		is an instance of unittest.TestSuite, it adds the entire suite to the
		main suite. If the test case is a class, it loads the tests from that
		class and adds them to the main suite.

		Args:
			test_cases (list): A list of test cases or test suites to be added
								to the main test suite.

		Returns:
			None: This function does not return a value.
		"""
		for test_case in test_cases:
			if isinstance(test_case, unittest.TestSuite):
				# Handle doctests
				suite.addTests(test_case)
			else:
				suite.addTests(loader.loadTestsFromTestCase(test_case))

	# Load all MATs if no group specified
	if not group:
		for category_tests in MINIMUM_ACCEPTANCE_TESTS.values():
			add_test_cases(category_tests)
		# and for coverage targets:
		add_test_cases(EXTRA_TESTS["coverage"])
		return suite
	if group not in TEST_GROUPS:  # pragma: no branch
		raise ValueError(f"Unknown test group: {group}")
	selected_group = TEST_GROUPS[group]
	if category:  # pragma: no branch
		if category not in selected_group:  # pragma: no branch
			raise ValueError(f"Unknown category '{category}' in group '{group}'")
		add_test_cases(selected_group[category])
	else:  # pragma: no branch
		# Load all categories in the group
		for category_tests in selected_group.values():
			add_test_cases(category_tests)
	return suite


def load_tests(loader, tests, pattern) -> unittest.TestSuite:
	"""Will Load the tests from the project and then attempts to load the doctests too.

	Meta Testing:

	Testcase 0: Load test fixtures

		>>> import tests as _tests
		>>>

	Testcase 1: Load test fixtures

		>>> import tests as _tests
		>>> _tests.load_tests is not None
		True

	"""
	return get_test_suite()
