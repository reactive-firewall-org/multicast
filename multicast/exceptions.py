#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module
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

"""Provides multicast exception features.

Use for handling exit codes and exceptions from multicast. Contains classes and functions to
handle exceptions and errors for/from the multicast module.

> [!CAUTION]
> See details regarding dynamic imports [documented](../__init__.py) in this module.

Classes:
	CommandExecutionError: Exception for command execution failures.
	ShutdownCommandReceived: Exception for graceful server shutdown.

Attributes:
	EXIT_CODES (dict): Mapping of exit codes to exceptions and messages.
	EXCEPTION_EXIT_CODES (dict): Reverse mapping of exceptions to exit codes.

Error Handling Mechanisms:

	Exception Raising:

		- **Module Specific Exceptions**: Defined in `multicast/exceptions.py`, providing clear
			semantics for error conditions specific to the `multicast` module.
		- **Standard Exceptions**: Used where appropriate to leverage built-in exception types for
			common error scenarios.

	Exception Mapping:

		- The `exit_on_exception` decorator handles exceptions by mapping them to exit codes
			defined in `EXIT_CODES`.
		- Ensures that exceptions are caught and the program exits gracefully with standardized
			exit codes.

	Usage of `sys.exit()`:

		- Direct calls to `sys.exit()` are discouraged outside of centralized exception handling.
		- Prefer raising exceptions that are then handled by the exception management system.

Guidelines for Developers:

	- **Consistency**: Always raise exceptions using the predefined classes to maintain
		consistency in error handling.
	- **Clarity**: Provide informative error messages to aid in debugging and user feedback.
	- **Mapping**: Ensure any new exceptions are added to the `EXIT_CODES` dictionary with
		appropriate exit codes.
	- **Standards Compliance**: Adhere to CEP-8 guidelines for exit codes and exception handling
		protocols.

Conclusion:

	By following the error handling practices outlined in this guide, developers can create
	robust, maintainable code that handles error conditions gracefully and consistently. This
	contributes to a stable application and improves the overall developer experience.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.exceptions is not None
		True
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 1: Recv should be automatically imported.
		A: Test that the multicast component is initialized.
		B: Test that the exceptions component is initialized.
		C: Test that the exceptions component has __doc__

		>>> multicast is not None
		True
		>>> multicast.exceptions is not None
		True
		>>> multicast.exceptions.__doc__ is not None
		True
		>>> type(multicast.exceptions.__doc__) == type(str(''''''))
		True
		>>>

	Testcase 2: Exceptions should be detailed with some metadata.
		A: Test that the __MAGIC__ variables are initialized.
		B: Test that the __MAGIC__ variables are strings.

		>>> multicast.exceptions is not None
		True
		>>> multicast.exceptions.__module__ is not None
		True
		>>> multicast.exceptions.__package__ is not None
		True
		>>> type(multicast.exceptions.__doc__) == type(multicast.exceptions.__module__)
		True
		>>>

	Testcase 3: Custom exceptions should have exit-code details.

		>>> from multicast.exceptions import CommandExecutionError
		>>> try:
		...     raise CommandExecutionError("Failed", 1)
		... except CommandExecutionError as e:
		...     e.exit_code
		1
		>>>

"""

__package__ = "multicast"  # skipcq: PYL-W0622
"""
The package of this program.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: exceptions should be automatically imported.

		>>> multicast.exceptions.__package__ is not None
		True
		>>>
		>>> multicast.exceptions.__package__ == multicast.__package__
		True
		>>>

"""

__module__ = "multicast.exceptions"
"""
The module of this program.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Exceptions should be automatically imported.

		>>> multicast.exceptions.__module__ is not None
		True
		>>>

"""

__file__ = "multicast/exceptions.py"
"""The file of this component."""

__name__ = "multicast.exceptions"  # skipcq: PYL-W0622
"""The name of this component.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Exceptions should be automatically imported.

		>>> multicast.exceptions.__name__ is not None
		True
		>>>

"""

try:
	from . import argparse  # skipcq: PYL-C0414
	from . import logging  # skipcq: PYL-C0414
	import functools
except ImportError as _cause:
	baton = ImportError(_cause, "[CWE-758] Module failed completely.")
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = _cause
	raise baton from _cause


module_logger = logging.getLogger(__module__)
module_logger.debug(
	"Loading %s",  # lazy formatting to avoid PYL-W1203
	__module__,
)
module_logger.debug(
	"Initializing %s exceptions.",  # lazy formatting to avoid PYL-W1203
	__package__,
)


class CommandExecutionError(RuntimeError):
	"""
	Exception raised when a command execution fails.

	Attributes:
		message (str) -- Description of the error.
		exit_code (int) -- The exit code associated with the error.

	Raises:
		TypeError: If exit_code is not an integer.

	Meta-Testing:

		Testcase 1: Initialization with message and exit code.
			A. - Initializes the error.
			B. - checks inheritance.
			C. - checks each attribute.

			>>> error = CommandExecutionError("Failed to execute command", 1)
			>>> isinstance(error, RuntimeError)
			True
			>>> error.message
			'Failed to execute command'
			>>> error.exit_code
			1
	"""

	__module__ = "multicast.exceptions"

	__name__ = "multicast.exceptions.CommandExecutionError"

	def __init__(self, *args, **kwargs) -> None:
		"""
		Initialize CommandExecutionError with a message and exit code.

		Parameters:
			message (str) -- Description of the error.
			exit_code (int) -- The exit code associated with the error.
			*args: Variable length argument list.
			**kwargs: Arbitrary keyword arguments.

		Raises:
			TypeError: if the exit_code is not an int.

		Meta-Testing:

			Testcase 1: Initialization with different exit code:
				A. - Initializes a CommandExecutionError with a specific exit code.
				B. - Checks the message is still set, as super class would.
				C. - Checks the specific exit code is Misuse-Error (2).

				>>> error = CommandExecutionError("Error message", 2)
				>>> error.message
				'Error message'
				>>> error.exit_code
				2

			Testcase 2: Initialization with different call to init:
				A. - Initializes a CommandExecutionError with a specific exit code.
				B. - Checks the message is still set, as super class would.
				C. - Checks the specific exit code is Usage-Error (64).

				>>> pre_made_args = ["Usage Error", int(64)]
				>>> error = CommandExecutionError(*pre_made_args)
				>>> error.message
				'Usage Error'
				>>> error.exit_code
				64

			Testcase 3: Initialization with different call to init:
				A. - Initializes a CommandExecutionError with a specific exit code.
				B. - Checks the message is still set, as super class would.
				C. - Checks the cause is set, as super class would.
				D. - Checks the specific exit code is sixty-five (65).

				>>> pre_made_args = [ValueError("inner Cause"), "A Pre-made Error Message", int(65)]
				>>> error = CommandExecutionError(*pre_made_args)
				>>> error.message
				'A Pre-made Error Message'
				>>> error.__cause__  #doctest: +ELLIPSIS
				ValueError...inner Cause...
				>>> error.exit_code
				65
		"""
		if len(args) > 0 and isinstance(args[-1], int):
			exit_code = args[-1]
			args = args[:-1]
		else:
			exit_code = kwargs.pop("exit_code", 1)
		if len(args) > 0 and isinstance(args[0], BaseException):
			cause = args[0]
			args = args[1:]
		else:
			cause = kwargs.pop("__cause__", None)
		super().__init__(*args, **kwargs)
		if cause is not None:
			self.__cause__ = cause
		msg = args[0] if args else kwargs.get("message", "An error occurred")
		self.message = msg if msg else "An error occurred"
		del msg  # skipcq: PTC-W0043
		self.exit_code = exit_code


class ShutdownCommandReceived(RuntimeError):
	"""
	Exception raised when a 'STOP' command is received during the HEAR operation.

	This exception signals a graceful shutdown of the multicast server.

	Attributes:
		message (str): Description of the exception.

	Testing:

		Testcase 1: Initialization with default message.

			>>> exc = ShutdownCommandReceived()
			>>> isinstance(exc, RuntimeError)
			True
			>>> exc.message
			'SHUTDOWN'

		Testcase 2: Initialization with custom message.

			>>> exc = ShutdownCommandReceived("Custom shutdown message.")
			>>> exc.message
			'Custom shutdown message.'
	"""

	__module__ = "multicast.exceptions"

	__name__ = "multicast.exceptions.ShutdownCommandReceived"

	def __init__(self, *args, **kwargs) -> None:
		"""
		Initialize the ShutdownCommandReceived exception.

		The ShutdownCommandReceived exception is used by the default handler
		for the HEAR servers, to instruct the HEAR server to shutdown gracefully.

		Parameters:
			message (str): Optional custom message for the exception.
			*args: Additional positional arguments passed to RuntimeError.
			**kwargs: Additional keyword arguments passed to RuntimeError.

		Raises:
			TypeError: If message is not a string.

		Testing:

			Testcase 1: Default initialization.

				>>> exc = ShutdownCommandReceived()
				>>> isinstance(exc, ShutdownCommandReceived)
				True
				>>> exc.message
				'SHUTDOWN'

			Testcase 2: Initialization with custom message.

				>>> exc = ShutdownCommandReceived("Custom shutdown message.")
				>>> isinstance(exc, ShutdownCommandReceived)
				True
				>>> exc.message
				'Custom shutdown message.'

			Testcase 3: Invalid message type.

				>>> exc = ShutdownCommandReceived(message=123)  # doctest: +IGNORE_EXCEPTION_DETAIL
				Traceback (most recent call last):
				TypeError: message must be a string

			Testcase 4: Exit code verification.

				>>> exc = ShutdownCommandReceived()
				>>> exc.exit_code == 143  # Verify SIGTERM exit code
				True

			Testcase 5: Error propagation with exit_on_exception.

					>>> @exit_on_exception
					... def test_func():
					...     raise ShutdownCommandReceived()
					>>> test_func()  # doctest: +IGNORE_EXCEPTION_DETAIL
					Traceback (most recent call last):
					SystemExit: 143

			Testcase 6: Error message propagation.

				>>> try:
				...     raise ShutdownCommandReceived("Custom message")
				... except ShutdownCommandReceived as e:
				...     str(e) == "Custom message"
				True

			Testcase 7: Initialization with different call to init:
				A. - Initializes a ShutdownCommandReceived with a specific exit code.
				B. - Checks the message is still set, as normally would.
				C. - Checks the cause is set, as super class would.
				D. - Checks the specific exit code is NOT sixty-five (65) but rather still 143.

				>>> pre_made_args = [ValueError("inner Cause"), "A Pre-made SHUTDOWN", int(65)]
				>>> error = ShutdownCommandReceived(*pre_made_args)
				>>> error.message
				'A Pre-made SHUTDOWN'
				>>> error.__cause__  #doctest: +ELLIPSIS
				ValueError...inner Cause...
				>>> error.exit_code
				143
		"""
		if len(args) > 0 and isinstance(args[0], BaseException):
			cause = args[0]
			args = args[1:]
		else:
			cause = kwargs.pop("__cause__", None)
		if len(args) > 0 and isinstance(args[0], str):
			message = args[0]
			args = args[1:]
		else:
			message = kwargs.pop("message", "SHUTDOWN")
		if not isinstance(message, str):
			raise TypeError("[CWE-573] message must be a string")
		super().__init__(message, *args, **kwargs)
		if cause is not None:
			self.__cause__ = cause
		self.message = message
		self.exit_code = 143  # Use SIGTERM exit code for graceful shutdown


module_logger.debug("Initialized exceptions.")
module_logger.debug("Initializing error message strings.")
# Error message constants
EXIT_CODE_RANGE_ERROR = "Exit code must be an integer between 0 and 255"
module_logger.debug("Initialized message strings.")


def validate_exit_code(code) -> None:
	"""
	Validate that an exit code is within the valid range (0-255).

	This function ensures that exit codes provided to system functions
	are compliant with the POSIX standard range of 0-255. Values outside
	this range or non-integer values will cause an exception.

	Arguments:
		code: The exit code value to validate.

	Returns:
		None: If validation passes, no value is returned.

	Raises:
		ValueError: If the exit code is not an integer or outside the range 0-255.
		TypeError: If the provided argument is not a numeric type.

	Testing:
		Testcase 1: Valid exit codes.
			A. Test with minimum valid value.
			B. Test with maximum valid value.
			C. Test with typical success code.
			D. Test with typical error code.

			>>> validate_exit_code(0)  # Minimum valid value
			>>> validate_exit_code(255)  # Maximum valid value
			>>> validate_exit_code(1)  # Typical error code
			>>> validate_exit_code(70)  # Internal software error

		Testcase 2: Invalid type for exit code.
			A. Test with string value.
			B. Test with None value.
			C. Test with non-integer numeric value.

			>>> validate_exit_code("1")  # doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Exit code must be an integer between 0 and 255
			>>> validate_exit_code(None)  # doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Exit code must be an integer between 0 and 255
			>>> validate_exit_code(True)  # same as validate_exit_code(1)
			>>> validate_exit_code(1.5)  # doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Exit code must be an integer between 0 and 255

		Testcase 3: Out of range exit codes.
			A. Test with negative value.
			B. Test with value exceeding maximum.

			>>> validate_exit_code(-1)  # doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Exit code must be an integer between 0 and 255
			>>> validate_exit_code(256)  # doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Exit code must be an integer between 0 and 255

		Testcase 4: Integration with EXIT_CODES.
			A. Test with each key in EXIT_CODES.
			B. Verify all keys in EXIT_CODES are valid.

			>>> all(validate_exit_code(code) is None for code in EXIT_CODES.keys())
			True
			>>> # Verify boundary exceptions are properly handled
			>>> try:
			...     validate_exit_code(999)
			...     success = False
			... except ValueError:
			...     success = True
			>>> success
			True
	"""
	module_logger.debug("Validating possible exit code.")
	if not isinstance(code, int) or code < 0 or code > 255:
		raise ValueError(EXIT_CODE_RANGE_ERROR)
	module_logger.debug("Validated possible exit code.")


module_logger.debug("Initializing CEP-8 EXIT_CODES")


EXIT_CODES = {
	0: (None, 'Success'),
	1: (RuntimeError, 'General Error'),
	2: (OSError, 'Misuse of Shell Builtins'),
	64: (argparse.ArgumentError, 'Usage Error'),
	65: (ValueError, 'Data Error'),
	66: (FileNotFoundError, 'No Input'),
	69: (ConnectionError, 'Unavailable Service'),
	70: (Exception, 'Internal Software Error'),
	77: (PermissionError, 'Permission Denied'),
	125: (BaseException, 'Critical Failure'),
	126: (AssertionError, 'Command Invoked Cannot Execute'),
	127: (ModuleNotFoundError, 'Command Not Found'),
	129: (None, 'Hangup (SIGHUP)'),
	130: (KeyboardInterrupt, 'Interrupt (SIGINT)'),
	134: (None, 'Abort (SIGABRT)'),
	137: (None, 'Killed (SIGKILL)'),
	141: (BrokenPipeError, 'Broken Pipe (SIGPIPE)'),
	143: (SystemExit, 'Terminated (SIGTERM)'),
	255: (None, 'Exit Status Out of Range'),
}
"""
Provides a mapping between exit codes and their corresponding exception classes and messages.

The `EXIT_CODES` dictionary serves as a centralized mapping for standard exit codes used within
the multicast module. Each key represents an exit code (as an integer), and each value is a tuple
containing the associated exception class (or `None` if not applicable) and a human-readable
description of the exit condition.

CEP-8 Compliance:
	In accordance with
	[CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161)
	guidelines, this mapping facilitates consistent error handling and exit code management
	throughout the module. By associating specific exceptions with standard exit codes, the
	application adheres to predictable behavior in response to various error conditions, enhancing
	maintainability and debugging efficiency.

	Specific codes are detailed more in
	[CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161).

Usage Example:
	```python
		import sys
		from multicast.exceptions import EXIT_CODES
		from multicast.exceptions import get_exit_code_from_exception

		try:
			# Code that may raise an exception
			pass
		except Exception as _cause:
			exit_code = get_exit_code_from_exception(_cause)
			sys.exit(exit_code)
	```

Testing:

	Testcase 0: EXIT_CODES should be automatically imported.

		>>> import multicast
		>>> import multicast.exceptions
		>>> multicast.EXIT_CODES != None
		True
		>>> isInstance(multicast.EXIT_CODES, dict)
		True

"""


EXCEPTION_EXIT_CODES = {exc: code for code, (exc, _) in EXIT_CODES.items() if exc}
"""
	Dictionary mapping exception classes to their associated exit codes.

	Use this dictionary to retrieve the exit code corresponding to a given exception class.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.exceptions.

	>>> import multicast.exceptions as exceptions
	>>> exceptions.__name__
	'multicast.exceptions'

	Testcase 0: EXCEPTION_EXIT_CODES should be initializable.

		>>> from multicast.exceptions import EXCEPTION_EXIT_CODES
		>>> EXCEPTION_EXIT_CODES is not None
		True

	Testcase 1: EXCEPTION_EXIT_CODES should map exceptions to exit codes.
		A. - check `RuntimeError` is mapped to `1`.
		B. - check `FileNotFoundError` is mapped to `66`.

		>>> EXCEPTION_EXIT_CODES[RuntimeError]
		1
		>>> EXCEPTION_EXIT_CODES[FileNotFoundError]
		66

	Testcase 2: EXCEPTION_EXIT_CODES should not include None entries.
		A. - Test reverse map is not none.
		B. - Test reverse map contains only non-None.

		>>> None is EXCEPTION_EXIT_CODES
		False
		>>> None in EXCEPTION_EXIT_CODES
		False

"""


module_logger.debug("Initialized EXIT_CODES.")


def get_exit_code_from_exception(exc: BaseException) -> int:
	"""
	Retrieve the exit code associated with a specific exception.

	Arguments:
		exc (BaseException): The exception instance from which to retrieve the exit code.

	Returns:
		int: The exit code corresponding to the given exception.

	Raises:
		TypeError: If the provided argument is not an instance of BaseException.

	Testing:

		Testcase 1: Exception with a direct type match.
			A. Test with FileNotFoundError which has a specific exit code.
			B. Verify correct exit code is returned.

			>>> exc = FileNotFoundError('No such file or directory')
			>>> get_exit_code_from_exception(exc)
			66

		Testcase 2: Exception with an inherited type match.
			A. Test with a subclass of ValueError that doesn't have a direct mapping.
			B. Verify it returns the parent class's exit code.

			>>> class CustomValueError(ValueError): pass
			>>> exc = CustomValueError('Custom value error')
			>>> get_exit_code_from_exception(exc)
			65

		Testcase 3: Exception without any type match.
			A. Test with a custom exception that doesn't inherit from mapped types.
			B. Verify it returns the default error code.

			>>> exc = Exception('Generic error')
			>>> get_exit_code_from_exception(exc)
			70

		Testcase 4: Security boundary test with invalid input.
			A. Test with non-exception input.
			B. Verify type checking.

			>>> get_exit_code_from_exception("not an exception")
			70

	"""
	exc_type = type(exc)
	if exc_type in EXCEPTION_EXIT_CODES:
		return EXCEPTION_EXIT_CODES[exc_type]
	for exc_class in EXCEPTION_EXIT_CODES:
		if isinstance(exc, exc_class):
			return EXCEPTION_EXIT_CODES[exc_class]
	return 70  # Default to 'Internal Software Error'


def exit_on_exception(func: callable):
	"""
	Decorator that wraps a function to handle exceptions and exit with appropriate exit codes.

	This decorator captures exceptions raised by the wrapped function and handles them by mapping
	them to predefined exit codes specified in `EXIT_CODES`. It ensures that both `SystemExit`
	exceptions (which may be raised by modules like `argparse`) and other base exceptions result
	in the program exiting with meaningful exit codes and error messages.

	Arguments:
		func (callable): The function to be wrapped by the decorator.

	Returns:
		callable: The wrapped function with enhanced exception handling.

	Testing:

		Testcase 1: Successful execution without exceptions.
			A. Define a function that returns a value.
			B. Decorate it with `@exit_on_exception`.
			C. Call the function and confirm it returns the expected value.

			>>> @exit_on_exception
			... def sample_func():
			...     return "Success"
			>>> sample_func()
			'Success'

		Testcase 2: Function raises `SystemExit` exception.
			A. Define a function that raises `SystemExit`.
			B. Decorate it with `@exit_on_exception`.
			C. Call the function and verify it exits with the correct exit code.

			>>> @exit_on_exception
			... def system_exit_func():
			...     raise SystemExit(64)
			>>> system_exit_func()  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			SystemExit...64...

		Testcase 3: Function raises a general exception.
			A. Define a function that raises a `ValueError`.
			B. Decorate it with `@exit_on_exception`.
			C. Call the function and verify it exits with the mapped exit code.

			>>> @exit_on_exception
			... def error_func():
			...     raise ValueError("Invalid value")
			>>> error_func()  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			SystemExit...65...
	"""

	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		_func_logger = module_logger
		try:
			_func_logger = logging.getLogger(func.__name__)
			return func(*args, **kwargs)
		except SystemExit as baton:
			# Handle SystemExit exceptions, possibly from argparse
			exit_code = baton.code if isinstance(baton.code, int) else 2
			_func_logger.warning(
				"%s: %s",  # lazy formatting to avoid PYL-W1203
				EXIT_CODES[exit_code][1],
				baton,
			)
			raise SystemExit(exit_code) from baton
			# otherwise sys.exit(exit_code)
		except BaseException as _cause:
			exit_code = get_exit_code_from_exception(_cause)
			_func_logger.warning(
				"%s: %s",  # lazy formatting to avoid PYL-W1203
				EXIT_CODES[exit_code][1],
				_cause,
			)
			raise SystemExit(exit_code) from _cause
			# otherwise sys.exit(exit_code)

	return wrapper


module_logger.debug(
	"Loaded %s",  # lazy formatting to avoid PYL-W1203
	__module__,
)


# skipcq
__all__ = [
	"""__package__""",
	"""__module__""",
	"""__name__""",
	"""__doc__""",  # skipcq: PYL-E0603
	"""CommandExecutionError""",
	"""EXCEPTION_EXIT_CODES""",
	"""validate_exit_code""",
	"""EXIT_CODES""",
	"""get_exit_code_from_exception""",
	"""exit_on_exception""",
	"""ShutdownCommandReceived"""
]
