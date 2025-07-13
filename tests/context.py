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

__name__ = "tests.context"  # skipcq: PYL-W0622

__doc__ = """Test context and environment setup module.

This module provides the testing environment setup and utilities for the multicast
package tests. It handles imports, path configurations, and provides helper functions
for test execution.

Functions:
	getCoverageCommand: Get appropriate coverage command for test execution.
	getPythonCommand: Get appropriate Python command, with coverage wrapping, for test execution.
	checkPythonCommand: Execute Python commands with proper error handling.
	timePythonCommand: Time profile wraps checkPythonCommand transparently.
	checkStrOrByte: Validate Python console results with proper error handling.
	debugBlob: Debug helper for unexpected outputs.
	managed_process(process): Context manager for safely handling multiprocessing processes.

Classes:
	BasicUsageTestSuite: Base test suite with common test functionality.

Robust imports: These statements import the entire "multicast" module,
	allowing access to all its functionalities within the test environment.
	This can be flagged as an intentional
	[cyclic-import](https://pylint.pycqa.org/en/latest/user_guide/messages/refactor/cyclic-import.html)
	warning.

Meta Tests - Fixtures:

	Context for Testing.

		Test fixtures by importing test context.

		>>> import tests.context as context
		>>>

		>>> from context import unittest as _unittest
		>>>

		>>> from context import subprocess as _subprocess
		>>>

		>>> from context import multicast as _multicast
		>>>

		>>> from context import profiling as _profiling
		>>>

	Testcase 1: Subclassing BasicUsageTestSuite should be simple.

		>>> from tests.context import BasicUsageTestSuite
		>>> class MyTests(BasicUsageTestSuite):
		...     def test_example(self):
		...         self.assertTrue(True)
		>>>

"""

try:
	import sys
	if not hasattr(sys, 'modules') or not sys.modules:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-440] sys.modules is not available or empty.") from None
except ImportError as _cause:
	raise ImportError("[CWE-440] Unable to import sys module.") from _cause

try:
	import os
	if not hasattr(os, 'sep') or not os.sep:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-440] OS support is not available.") from None
	import string
	if not hasattr(string, 'digits') or not string.digits:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-440] string support is not available.") from None
	import secrets
	import unittest
	import warnings
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] Module Failed to import.") from _cause

try:
	from contextlib import contextmanager
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] contextlib.contextmanager Failed to import.") from _cause

try:
	if 'Process' not in sys.modules:
		from multiprocessing import Process as Process  # skipcq: PYL-C0414
	else:  # pragma: no branch
		Process = sys.modules["Process"]
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] Process Failed to import.") from _cause

try:
	import subprocess
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] subprocess Failed to import.") from _cause

try:
	if 'packaging' not in sys.modules:
		import packaging
	else:  # pragma: no branch
		packaging = sys.modules["packaging"]
	from packaging import version
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] packaging.version Failed to import.") from _cause

try:
	if 'multicast' not in sys.modules:
		import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
	else:  # pragma: no branch
		multicast = sys.modules["multicast"]  # pylint: disable=cyclic-import
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] Multicast Python Module Failed to import.") from _cause

try:
	if 'tests.profiling' not in sys.modules:
		import tests.profiling as profiling
	else:  # pragma: no branch
		profiling = sys.modules["tests.profiling"]
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] profiling Failed to import.") from _cause

try:
	if 'multicast.exceptions' not in sys.modules:
		import multicast.exceptions
	else:  # pragma: no branch
		multicast.exceptions = sys.modules["multicast.exceptions"]
	from multicast.exceptions import CommandExecutionError
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] Test Exceptions Failed to import.") from _cause

__BLANK = str("""""")
"""
	A literally named variable to improve readability of code when using a blank string.

	Meta Testing:

	First set up test fixtures by importing test context.

		>>> import tests.context as _context
		>>>

	Testcase 1: __BLANK should be a blank string.

		>>> import tests.context as _context
		>>> _context.__BLANK is None
		False
		>>> isinstance(_context.__BLANK, type(str()))
		True
		>>> len(_context.__BLANK) == int(0)
		True
		>>>


"""


def markWithMetaTag(*marks: str) -> callable:
	"""Decorator to apply pytest marks if pytest is available."""
	try:
		import pytest
		pytest_available = True
	except ImportError:
		pytest_available = False

	def decorator(cls) -> any:  # skipcq: PY-D0003 -- decorator ok
		if pytest_available:
			for mark in marks:
				cls = pytest.mark.__getattr__(mark)(cls)
		return cls

	return decorator


def getCoverageCommand() -> str:
	"""
		Function for backend coverage command.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool to allow coverage testing to continue beyond
		the process fork of typical cli testing.

		Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: function should have a output.

			>>> _context.getCoverageCommand() is None
			False
			>>>


	"""
	thecov = "exit 1 ; #"
	try:
		thecov = checkPythonCommand(["command", "-v", "coverage"])
		_unsafe_cov = checkPythonCommand(["which", "coverage"])
		if (str("/coverage") in str(thecov) or str("/coverage") in str(_unsafe_cov)):
			thecov = str("coverage")  # skipcq: TCV-002
		elif str("/coverage3") in str(checkPythonCommand(["command", "-v", "coverage3"])):
			thecov = str("coverage3")  # skipcq: TCV-002
		else:  # pragma: no branch
			thecov = "exit 1 ; #"  # skipcq: TCV-002
	except Exception:  # pragma: no branch
		thecov = "exit 1 ; #"  # handled error by suppressing it and indicating caller should abort.
	return str(thecov)


def __check_cov_before_py():
	"""
		Utility Function to check for coverage availability before just using plain python.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool before falling back on just plain python.

		Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: function should have a output.

			>>> _context.__check_cov_before_py() is not None
			True
			>>>

		Testcase 2: function should have a string output of python or coverage.

			>>> _test_fixture = _context.__check_cov_before_py()
			>>> isinstance(_test_fixture, type(str("")))
			True
			>>> (str("python") in _test_fixture) or (str("coverage") in _test_fixture)
			True
			>>>


	"""
	thepython = str(sys.executable)
	thecov = getCoverageCommand()
	if (str("coverage") in str(thecov)) and (sys.version_info >= (3, 7)):
		thepython = str(f"{str(thecov)} run -p")  # skipcq: TCV-002
	else:  # pragma: no branch
		try:
			# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
			import coverage as coverage  # skipcq: PYL-C0414
			if coverage.__name__ is not None:
				thepython = str("{} -m coverage run -p").format(str(sys.executable))
		except Exception:
			thepython = str(sys.executable)  # handled error by falling back on faile-safe value.
	return thepython


def getPythonCommand() -> str:
	"""
		Function for backend python command.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool with getCoverageCommand() first.

		Meta Testing:

		First set up test fixtures by importing test context.

		>>> import tests.context as _context
		>>>

		Testcase 1: function should have a output.

		>>> _context.getPythonCommand() is not None
		True
		>>>

	"""
	thepython = "python"
	try:
		thepython = __check_cov_before_py()
	except Exception:  # pragma: no branch
		thepython = "exit 1 ; #"
		try:
			thepython = str(sys.executable)
		except Exception:
			thepython = "exit 1 ; #"  # handled error by suppressing it and indicating exit.
	return str(thepython)


def checkCovCommand(*args):  # skipcq: PYL-W0102  - [] != [None]
	"""
	Modifies the input command arguments to include coverage-related options when applicable.

	This utility function checks if the first argument contains "coverage" and, if so,
	modifies the argument list to include additional coverage run options. It's primarily
	used internally by other functions in the testing framework.
	Not intended to be run directly.

	Args:
		*args (list): A list of command arguments; should not be pass None.

	Returns:
		list: The modified list of arguments with 'coverage run' options added as applicable.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: Function should return unmodified arguments if 'coverage' is missing.

			>>> _context.checkCovCommand("python", "script.py")
			['python', 'script.py']

		Testcase 2: Function should modify arguments when 'coverage' is the first argument.
			A.) Missing 'run'

			>>> _context.checkCovCommand("coverage", "script.py")  #doctest: +ELLIPSIS
			['...', 'run', '-p', '--context=Integration', '--source=multicast', 'script.py']

		Testcase 3: Function should modify arguments when 'coverage run' is in the first argument.
			A.) NOT missing 'run'

			>>> _context.checkCovCommand("coverage run", "script.py")  #doctest: +ELLIPSIS
			['...', 'run', '-p', '--context=Integration', '--source=multicast', 'script.py']

		Testcase 4: Function should handle coverage command with full path.

			>>> _context.checkCovCommand("/usr/bin/coverage", "test.py")  #doctest: +ELLIPSIS
			['...', 'run', '-p', '--context=Integration', '--source=multicast', 'test.py']

		Testcase 5: Function should handle coverage invoked via sys.executable.

			>>> import sys as _sys
			>>> test_fixture = [str("{} -m coverage run").format(_sys.executable), "test.py"]
			>>> _context.checkCovCommand(*test_fixture)  #doctest: +ELLIPSIS
			[..., '-m', 'coverage', 'run', '-p', '...', '--source=multicast', 'test.py']


	"""
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import system.") from None
	if not args or args[0] is None:
		# skipcq: TCV-002
		raise ValueError("[CWE-1286] args must be an array of positional arguments") from None
	else:
		args = [*args]  # convert to an array
	if str("coverage") in args[0]:
		i = 1
		if str(f"{str(sys.executable)} -m coverage") in str(args[0]):  # pragma: no branch
			args[0] = str(sys.executable)
			args.insert(1, str("-m"))
			args.insert(2, str("coverage"))
			i += 2
		else:  # pragma: no branch
			args[0] = str(getCoverageCommand())
		extra_args = ["run", "-p", "--context=Integration", "--source=multicast"]
		# PEP-279 - see https://www.python.org/dev/peps/pep-0279/
		for k, ktem in enumerate(extra_args):
			offset = i + k
			args.insert(offset, ktem)
	return [*args]


def taint_command_args(args: (list, tuple)) -> list:
	"""Validate and sanitize command arguments for security.

	This function validates the command (first argument) against a whitelist
	and sanitizes all arguments to prevent command injection attacks.

	Args:
		args (list): Command arguments to validate

	Returns:
		list: Sanitized command arguments

	Raises:
		CommandExecutionError: If validation fails

	Meta Testing:

		>>> import tests.context as _context
		>>> import sys as _sys
		>>>

		Testcase 1: Function should validate and return unmodified Python command.

			>>> test_fixture = ['python', '-m', 'pytest']
			>>> _context.taint_command_args(test_fixture)
			['python', '-m', 'pytest']
			>>>

		Testcase 2: Function should handle sys.executable path.

			>>> test_fixture = [str(_sys.executable), '-m', 'coverage', 'run']
			>>> result = _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			>>> str('python') in str(result[0]) or str('coverage') in str(result[0])
			True
			>>> result[1:] == ['-m', 'coverage', 'run']
			True
			>>>

		Testcase 3: Function should reject disallowed commands.

			>>> test_fixture = ['rm', '-rf', '/']
			>>> _context.taint_command_args(test_fixture)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			multicast.exceptions.CommandExecutionError: Command 'rm' is not allowed...
			>>>

		Testcase 4: Function should validate input types.

			>>> test_fixture = None
			>>> _context.taint_command_args(test_fixture)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			multicast.exceptions.CommandExecutionError: Invalid command arguments
			>>>
			>>> test_fixture = "python -m pytest"  # String instead of list
			>>> _context.taint_command_args(test_fixture)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			multicast.exceptions.CommandExecutionError: Invalid command arguments
			>>>

		Testcase 5: Function should handle coverage command variations.

			>>> test_fixture = [str(_sys.executable), 'coverage', 'run', '--source=multicast']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			[...'coverage', 'run', '--source=multicast']
			>>>
			>>> test_fixture = ['coverage', 'run', '--source=multicast']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			['exit 1 ; #', 'run',...'run', '--source=multicast']
			>>>
			>>> test_fixture = ['coverage3', 'run', '--source=.']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			['exit 1 ; #', 'run',...'--source=.']
			>>>

		Testcase 6: Function should handle case-insensitive command validation.

			>>> test_fixture = ['Python3', '-m', 'pytest']
			>>> _context.taint_command_args(test_fixture)
			['Python3', '-m', 'pytest']
			>>>
			>>> test_fixture = ['COVERAGE', 'run']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			[...'COVERAGE', 'run'...]
			>>>
	"""
	if not args or not isinstance(args, (list, tuple)):
		raise CommandExecutionError("Invalid command arguments", exit_code=66)
	# Validate the command (first argument)
	allowed_commands = {
		"python", "python3", "coverage", "coverage3",
		sys.executable,  # Allow the current Python interpreter
	}
	command = str(args[0]).lower()
	# Extract base command name for exact matching
	# Handle both path separators (/ for Unix, \ for Windows)
	command_base = command.split("/")[-1].split("\\")[-1]
	# Check if command is allowed (exact match on base name or full path match with sys.executable)
	if command_base not in allowed_commands and command != str(sys.executable).lower():
		raise CommandExecutionError(
			f"Command '{command}' is not allowed. Allowed commands: {allowed_commands}",
			exit_code=77
		)
	# Sanitize all arguments to prevent injection
	tainted_args = [str(arg) for arg in args]
	# Special handling for coverage commands
	if "coverage" in command:
		tainted_args = checkCovCommand(*tainted_args)
	# Sanitize all arguments to prevent injection
	return tainted_args


def validateCommandArgs(args: list) -> None:
	"""
	Validates command arguments to ensure they do not contain null characters.

	Args:
		args (list): A list of command arguments to be validated.

	Raises:
		ValueError: If any argument contains a null character.
	"""
	if (args is None) or (args == [None]) or (len(args) <= 0):  # pragma: no branch
		# skipcq: TCV-002
		raise ValueError("[CWE-1286] args must be an array of positional arguments") from None
	for arg in args:
		if isinstance(arg, str) and "\x00" in arg:
			raise ValueError("[CWE-20] Null characters are not allowed in command arguments.")


def checkStrOrByte(theInput):
	"""
	Converts the input to a string if possible, otherwise returns it as bytes.

	This utility function is designed to handle both string and byte inputs,
	ensuring consistent output type. It attempts to decode byte inputs to UTF-8
	strings, falling back to bytes if decoding fails.

	Args:
		theInput: The input to be checked and potentially converted.
					Can be None, str, bytes, or any other type.

	Returns:
		str: If the input is already a string or can be decoded to UTF-8.
		bytes: If the input is bytes and cannot be decoded to UTF-8.
		None: If the input is None.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: Input is a string.

			>>> _context.checkStrOrByte("Hello")
			'Hello'
			>>>

		Testcase 2: Input is UTF-8 decodable bytes.

			>>> _context.checkStrOrByte(b"Hello")
			'Hello'
			>>>

		Testcase 3: Input is bytes that are not UTF-8 decodable.

			>>> _context.checkStrOrByte(b'\\xff\\xfe')
			b'\xff\xfe'
			>>>

		Testcase 4: Input is None.

			>>> _context.checkStrOrByte(None) is None
			True
			>>>

		Testcase 5: Input is an empty string.

			>>> _context.checkStrOrByte("")
			''
			>>>

		Testcase 6: Input is empty bytes.

			>>> _context.checkStrOrByte(b"")
			''
			>>>


	"""
	theOutput = None
	if theInput is not None:  # pragma: no branch
		theOutput = theInput
	try:
		if isinstance(theInput, bytes):
			theOutput = theInput.decode("UTF-8")
	except UnicodeDecodeError:  # pragma: no branch
		theOutput = bytes(theInput)
	return theOutput


def checkPythonCommand(args, stderr=None):
	"""
	Execute a Python command and return its output.

	This function is a wrapper around subprocess.check_output with additional
	error handling and output processing. It's designed to execute Python
	commands or coverage commands, making it useful for running tests and
	collecting coverage data.

	Args:
		args (list): A list of command arguments to be executed.
		stderr (Optional[int]): File descriptor for stderr redirection.
			Defaults to None.

	Returns:
		str: The command output as a string, with any byte output decoded to UTF-8.

	Raises:
		subprocess.CalledProcessError: If the command returns a non-zero exit status.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import sys as _sys
			>>> import tests.context as _context
			>>>

		Testcase 1: Function should have an output when provided valid arguments.

			>>> test_fixture_1 = [str(_sys.executable), '-c', 'print("Hello, World!")']
			>>> _context.checkPythonCommand(test_fixture_1)
			'Hello, World!\\n'

		Testcase 2: Function should capture stderr when specified.

			>>> import subprocess as _subprocess
			>>> test_args_2 = [
			... 	str(_sys.executable), '-c', 'import sys; print("Error", file=sys.stderr)'
			... ]
			>>>
			>>> _context.checkPythonCommand(test_args_2, stderr=_subprocess.STDOUT)
			'Error\\n'

		Testcase 3: Function should handle exceptions and return output.

			>>> test_fixture_e = [str(_sys.executable), '-c', 'raise ValueError("Test error")']
			>>> _context.checkPythonCommand(
			... 	test_fixture_e, stderr=_subprocess.STDOUT
			... ) #doctest: +ELLIPSIS
			'Traceback (most recent call last):\\n...ValueError...'

		Testcase 4: Function should return the output as a string.

			>>> test_fixture_s = [str(_sys.executable), '-c', 'print(b"Bytes output")']
			>>> isinstance(_context.checkPythonCommand(
			... 	test_fixture_s, stderr=_subprocess.STDOUT
			... ), str)
			True


	"""
	theOutput = None
	try:
		if (args is None) or (args == [None]) or (len(args) <= 0):  # pragma: no branch
			theOutput = None  # None is safer than subprocess.check_output(["exit 1 ; #"])
		else:
			validateCommandArgs(args)
			if str("coverage") in args[0]:
				args = checkCovCommand(*args)
			# Validate and sanitize command arguments
			safe_args = taint_command_args(args)
			theOutput = subprocess.check_output(safe_args, stderr=stderr)
	except Exception as _cause:  # pragma: no branch
		theOutput = None
		try:
			if _cause.output is not None:
				theOutput = _cause.output
		except Exception:
			theOutput = None  # suppress all errors
	theOutput = checkStrOrByte(theOutput)
	return theOutput


@profiling.do_cprofile
def timePythonCommand(args, stderr=None):  # skipcq: PYL-W0102  - [] != [None]
	"""
	Function for backend subprocess check_output command.

	Args:
		args (array): An array of positional command arguments to be executed.
		stderr (Optional[int]): File descriptor for stderr redirection.
		Defaults to None.

		Returns:
			The output of checkPythonCommand.
	"""
	return checkPythonCommand(args, stderr=stderr)


def checkPythonFuzzing(args, stderr=None):  # skipcq: PYL-W0102  - [] != [None]
	"""
	Function for backend subprocess check_output command with improved error handling.

	Args:
		args (list): A list of command arguments to be executed.
		stderr (Optional[int]): File descriptor for stderr redirection.
		Defaults to None.

	Returns:
		str: The command output as a string.

	Raises:
		RuntimeError: If an error occurs during command execution.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: Function should raise RuntimeError when args is None.

			>>> _context.checkPythonFuzzing(None)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			multicast.exceptions.CommandExecutionError: ...

		Testcase 2: Function should raise RuntimeError when args is an empty list.

			>>> _context.checkPythonFuzzing([])  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			multicast.exceptions.CommandExecutionError: ...

		Testcase 3: Function should return output when valid arguments are provided.

			>>> import sys as _sys
			>>> test_fixture_3 = [str(_sys.executable), '-c', 'print("Hello, Fuzzing!")']
			>>> _context.checkPythonFuzzing(test_fixture_3)
			'Hello, Fuzzing!\\n'

		Testcase 4: Function should handle coverage command and return output. Coverage will fail.

			>>> test_fixture_4 = [
			...     'coverage run', '-c', 'print("Coverage Fuzzing!")'
			... ]
			>>> _context.checkPythonFuzzing(test_fixture_4)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			multicast.exceptions.CommandExecutionError: ...Command...
			'['coverage', 'run',...'-c'...]' returned...exit status 1...
			>>>

		Testcase 5: Function should capture stderr when specified.

			>>> import subprocess as _subprocess
			>>> test_fixture_5 = [
			...     str(_sys.executable), '-c', 'import sys; print("Error", file=sys.stderr)'
			... ]
			>>> _context.checkPythonFuzzing(test_fixture_5, stderr=_subprocess.STDOUT)
			'Error\\n'


	"""
	theOutput = None
	try:
		if (args is None) or (args == [None]) or (len(args) <= 0):  # pragma: no branch
			theOutput = None
			_exc_msg = "No command arguments provided to execute."
			raise CommandExecutionError(str(_exc_msg), exit_code=66) from None
		else:
			if str("coverage") in args[0]:
				args = checkCovCommand(*args)
			# Validate and sanitize command arguments
			safe_args = taint_command_args(args)
			theOutput = subprocess.check_output(safe_args, stderr=stderr)
	except BaseException as _cause:  # pragma: no branch
		theOutput = None
		raise CommandExecutionError(str(_cause), exit_code=2) from _cause  # do not suppress errors
	theOutput = checkStrOrByte(theOutput)
	return theOutput


def debugBlob(blob=None):
	"""Helper function to debug unexpected outputs.

		Especially useful for cross-python testing where output may differ
		yet may be from the same logical data.

		Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

			>>> norm_fixture = "Example Sample"
			>>> othr_fixture = \"""'Example Sample'\"""
			>>>

		Testcase 1: function should have a output.

			>>> debugBlob(norm_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<BLANKLINE>
			String:
			"
			Example Sample
			"
			<BLANKLINE>
			Data:
			"
			'Example Sample'
			"
			<BLANKLINE>
			True
			>>>

		Testcase 2: function should have a output even with bad input.

			>>> debugBlob(othr_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<BLANKLINE>
			String:
			"
			...Example Sample...
			"
			<BLANKLINE>
			Data:
			"
			...'Example Sample'...
			"
			<BLANKLINE>
			True
			>>>

	"""
	try:
		print(__BLANK)
		print(str("String:"))
		print(str("""\""""))
		print(str(blob))
		print(str("""\""""))
		print(__BLANK)
		print(str("Data:"))
		print(str("""\""""))
		print(repr(blob))
		print(str("""\""""))
		print(__BLANK)
	except Exception:
		print(__BLANK)
	return True


def debugtestError(someError):
	"""Helper function to debug unexpected outputs.

		Meta Testing:

		First set up test fixtures by importing test context.

		>>> import tests.context as _context
		>>>

		>>> err_fixture = RuntimeError(\"Example Error\")
		>>> bad_fixture = BaseException()
		>>>

		Testcase 1: function should have a output.

		>>> debugtestError(err_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<BLANKLINE>
		ERROR:
		<... \'...RuntimeError\'>
		Example Error
		('Example Error',)
		<BLANKLINE>
		>>>

		Testcase 2: function should have a output even with bad input.

		>>> debugtestError(bad_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<BLANKLINE>
		ERROR:
		<... \'...BaseException\'>
		<BLANKLINE>
		<No Args>
		<BLANKLINE>
		>>>

	"""
	print(__BLANK)
	print(str("ERROR:"))
	if someError is not None:
		print(str(type(someError)))
		print(str(someError))
		if str((someError.args)) not in str(()):
			print(str((someError.args)))
		else:
			print(str("<No Args>"))
		print(__BLANK)


def check_exec_command_has_output(test_case, someArgs):
	"""Test case for command output != None.

		returns True if has output and False otherwise.
	"""
	theResult = False
	fail_msg_fixture = "Expecting output: CLI test had no output."
	try:
		if (test_case._thepython is not None):
			try:
				theArgs = [test_case._thepython] + someArgs
				test_case.assertIsNotNone(
					checkPythonCommand(theArgs, stderr=subprocess.STDOUT), fail_msg_fixture
				)
				theResult = True
			except BaseException as _root_cause:
				debugtestError(_root_cause)
				theResult = False
	except Exception as _cause:
		debugtestError(_cause)
		theResult = False
	test_case.assertTrue(theResult, fail_msg_fixture)
	return theResult


def debugUnexpectedOutput(expectedOutput, actualOutput, thepython):
	"""Helper function to debug unexpected outputs.

		Meta Testing:

		First set up test fixtures by importing test context.

		>>> import tests.context as _context
		>>>

		>>> expected_fixture = "<EXPECTED OUTPUT>"
		>>> unexpected_fixture = "<ACTUAL OUTPUT>"
		>>> python_fixture = "<PYTHON USED>"
		>>>

		Testcase 1: function should have a output.

		>>> _context.debugUnexpectedOutput(
		... 	expected_fixture, unexpected_fixture, python_fixture
		... ) #doctest: -DONT_ACCEPT_BLANKLINE
		<BLANKLINE>
		python cmd used: <PYTHON USED>
		<BLANKLINE>
		The expected output is...
		<BLANKLINE>
		<EXPECTED OUTPUT>
		<BLANKLINE>
		The actual output was...
		<BLANKLINE>
		<ACTUAL OUTPUT>
		<BLANKLINE>
		>>>

		Testcase 2: function should have a output even with bad input.

		>>> _context.debugUnexpectedOutput(
		... 	expected_fixture, unexpected_fixture, None
		... ) #doctest: -DONT_ACCEPT_BLANKLINE
		<BLANKLINE>
		Warning: Unexpected output!
		<BLANKLINE>
		The expected output is...
		<BLANKLINE>
		<EXPECTED OUTPUT>
		<BLANKLINE>
		The actual output was...
		<BLANKLINE>
		<ACTUAL OUTPUT>
		<BLANKLINE>
		>>>

	"""
	print(__BLANK)
	if (thepython is not None):
		print(f"python cmd used: {str(thepython)}")
	else:
		print("Warning: Unexpected output!")
	print(__BLANK)
	if (expectedOutput is not None):
		print(str("The expected output is..."))
		print(__BLANK)
		print(f"{str(expectedOutput)}")
		print(__BLANK)
	print(str("The actual output was..."))
	print(__BLANK)
	print(str(f"{str(actualOutput)}"))
	print(__BLANK)


@contextmanager
def managed_process(process):
	"""
	Context manager for safely handling multiprocessing processes.

	Ensures that the given process is properly terminated and cleaned up,
	even if exceptions occur during execution. This includes terminating,
	joining, and closing the process to prevent resource leaks.

	Args:
		process (multiprocessing.Process): The process to manage.

	Yields:
		multiprocessing.Process: The managed process within the context.
	"""
	try:
		yield process
	finally:
		try:
			if process.is_alive():
				process.terminate()
				process.join(timeout=3)
				if process.is_alive():
					process.kill()
		except Exception as _cause:
			if (__debug__ and sys.stderr.isatty()):
				# Log the error but don't re-raise as this is cleanup code
				warnings.warn(
					f"Error during process cleanup: {_cause}", stacklevel=2,
				)


class BasicUsageTestSuite(unittest.TestCase):
	"""
		Basic functional test cases.

		Meta Tests - Creation:

		First set up test fixtures by importing test context.

		>>> import tests.context as _context
		>>>

		>>> class TestCaseFixture(_context.BasicUsageTestSuite):
		... 	pass
		>>>
		>>> TestCaseFixture
		<class 'tests.context.TestCaseFixture'>
		>>>

		Testcase 1: BasicUsageTestSuite are unittest.TestCase

		>>> isinstance(BasicUsageTestSuite("skipTest"), unittest.TestCase)
		True
		>>>

	"""

	__module__ = "tests.context"

	__name__ = "tests.context.BasicUsageTestSuite"

	NO_PYTHON_ERROR: str = "No python cmd to test with!"  # skipcq: TCV-002
	"""Error message used when Python command is not available for testing.

	This constant is used across multiple test methods to maintain consistency
	in error reporting when Python command execution is not possible.
	"""

	@classmethod
	def setUpClass(cls) -> None:
		"""Overrides unittest.TestCase.setUpClass(cls) to set up thepython test fixture."""
		cls._thepython = getPythonCommand()

	@staticmethod
	def _always_generate_random_port_WHEN_called() -> int:
		"""
		Generates a pseudo-random port number within the dynamic/private port range.

		This method returns a random port number between 49152 and 65535,
		compliant with RFC 6335, suitable for temporary testing purposes to
		avoid port conflicts.

		Returns:
			int: A random port number between 49152 and 65535.
		"""
		return secrets.randbelow(65535 - 49152 + 1) + 49152

	def setUp(self) -> None:
		"""Overrides unittest.TestCase.setUp(unittest.TestCase).
			Defaults is to skip test if class is missing thepython test fixture.
		"""
		if not self._thepython:
			self.skipTest(self.NO_PYTHON_ERROR)  # skipcq: TCV-002
		self._the_test_port = self._always_generate_random_port_WHEN_called()

	def _should_get_package_version_WHEN_valid(self) -> packaging.version.Version:
		"""
		Retrieve the current version of the package.

		This helper method imports the package and extracts the __version__ attribute.

		Returns:
			packaging.version.Version -- A validated version object from the __version__ attribute.
		Raises:
			AssertionError -- If the version string is invalid or cannot be retrieved.
			ImportError -- If the multicast package cannot be imported.

		"""
		parsed_version: packaging.version.Version = None
		try:
			self.assertIsNotNone(multicast.__module__, "Version will be effectively None.")
			self.assertIsNotNone(multicast.__version__, "Version is not valid.")
			_raw_version_fixture = multicast.__version__
			self.assertIsInstance(_raw_version_fixture, str, "Version is not a string.")
			# Strip custom tags
			# stuff like: mcast_version = mcast_version.replace("-hotfix", "").replace("-hf", "")
			# Refactor alpha/beta tags
			parsed_version = version.parse(_raw_version_fixture)
			self.assertIsNotNone(parsed_version, "Version is not valid.")
			self.assertIsInstance(parsed_version, version.Version, "Version is not valid.")
			self.assertTrue(
				len(parsed_version.release) >= 2,
				"Version must have at least major.minor components."
			)
		except Exception:
			self.fail("Failed to import the multicast package to retrieve version.")
		return parsed_version

	@unittest.skipUnless(True, "Insanity Test. Good luck debugging.")
	def test_absolute_truth_and_meaning(self) -> None:
		"""Test case 0: Insanity Test."""
		assert True
		self.assertTrue(True, "Insanity Test Failed")  # skipcq: PYL-W1503

	def test_finds_python_WHEN_testing(self) -> None:
		"""Test case 1: Class Test-Fixture Meta Test."""
		if (self._thepython is not None) and (len(self._thepython) <= 0):
			self.fail(self.NO_PYTHON_ERROR)  # skipcq: TCV-002
		self.test_absolute_truth_and_meaning()

	def tearDown(self) -> None:
		"""Overrides unittest.TestCase.tearDown(unittest.TestCase).
			Defaults is to reset the random port test fixture.
		"""
		if self._the_test_port:
			self._the_test_port = None

	@classmethod
	def tearDownClass(cls) -> None:
		"""Overrides unittest.TestCase.tearDownClass(cls) to clean up thepython test fixture."""
		cls._thepython = None
