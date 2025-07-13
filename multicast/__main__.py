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

"""Main entry point for the multicast package.

This module provides the command-line interface and core functionalities for multicast
communication. It handles command dispatching and execution of multicast operations.

Classes:
	McastNope: No-operation implementation for testing and validation.
	McastRecvHearDispatch: Handler for receiving multicast messages.
	McastDispatch: Main dispatcher for multicast operations.

Functions:
	main(*argv): Main entry point for CLI operations.

Example:
	>>> import multicast.__main__ as main
	>>> exit_code, _ = main.main(['NOOP'])
	>>> isinstance(exit_code, int)
	True

Caution: See details regarding dynamic imports [documented](../__init__.py) in this module.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>
		>>> import _multicast.__main__
		>>>

		>>> _multicast.__doc__ is not None
		True
		>>>

		>>> _multicast.__main__.__doc__ is not None
		True
		>>>

		>>> _multicast.__version__ is not None
		True
		>>>

	Testcase 0: multicast.__main__ should have a doctests.

		>>> import _multicast.__main__
		>>>

		>>> _multicast.__main__.__module__ is not None
		True
		>>>

		>>> _multicast.__main__.__doc__ is not None
		True
		>>>


"""

# skipcq
__all__ = [
	"""McastNope""",
	"""McastRecvHearDispatch""",
	"""McastDispatch""",
	"""main""",
	"""TASK_OPTIONS""",
]

__package__ = "multicast"  # skipcq: PYL-W0622
"""
The package of this component.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: __main__ should be automatically imported.

		>>> multicast.__main__.__package__ is not None
		True
		>>>
		>>> multicast.__main__.__package__ == multicast.__package__
		True
		>>>

"""

__module__ = "multicast.__main__"  # skipcq: PYL-W0622
"""
The module of this component.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: __main__ should be automatically imported.

		>>> multicast.__main__.__module__ is not None
		True
		>>>

"""

__file__ = "multicast/__main__.py"
"""The file of this component."""

try:
	from . import sys
except ImportError as baton:
	# Throw more relevant Error
	raise ImportError("[CWE-440] Error Importing Python") from baton

if "multicast.__version__" not in sys.modules:
	from . import __version__ as __version__  # skipcq: PYL-C0414
else:  # pragma: no branch
	__version__ = sys.modules["multicast.__version__"]

if "multicast._MCAST_DEFAULT_PORT" not in sys.modules:
	from . import _MCAST_DEFAULT_PORT as _MCAST_DEFAULT_PORT  # skipcq: PYL-C0414
else:  # pragma: no branch
	_MCAST_DEFAULT_PORT = sys.modules["multicast._MCAST_DEFAULT_PORT"]

if "multicast._MCAST_DEFAULT_GROUP" not in sys.modules:
	from . import _MCAST_DEFAULT_GROUP as _MCAST_DEFAULT_GROUP  # skipcq: PYL-C0414
else:  # pragma: no branch
	_MCAST_DEFAULT_GROUP = sys.modules["multicast._MCAST_DEFAULT_GROUP"]

if "multicast.exceptions" not in sys.modules:
	# pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
	from . import exceptions as exceptions  # skipcq: PYL-C0414
else:  # pragma: no branch
	exceptions = sys.modules["multicast.exceptions"]

if "multicast.mtool" not in sys.modules:
	from . import mtool as mtool  # skipcq: PYL-C0414
else:  # pragma: no branch
	mtool = sys.modules["multicast.mtool"]

if "multicast.recv" not in sys.modules:
	from . import recv as recv  # pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
else:  # pragma: no branch
	recv = sys.modules["multicast.recv"]

if "multicast.send" not in sys.modules:
	from . import send as send  # pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
else:  # pragma: no branch
	send = sys.modules["multicast.send"]

if "multicast.hear" not in sys.modules:
	from . import hear as hear  # pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
else:  # pragma: no branch
	hear = sys.modules["multicast.hear"]


class McastNope(mtool):
	"""
	The trivial implementation of mtool.

	Testing:

		Testcase 0: First set up test fixtures by importing multicast.

			>>> import multicast.__main__ as _multicast
			>>> _multicast.McastNope is not None
			True
			>>>

		Testcase 1: McastNope should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> _multicast.McastNope is not None
			True
			>>> _multicast.McastNope is not None
			True
			>>> _multicast.McastNope.__module__ is not None
			True
			>>> _multicast.McastNope.__proc__ is not None
			True
			>>> _multicast.McastNope.__prologue__ is not None
			True
			>>>


		Testcase 2: parseArgs should return a namespace.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the multicast.mtool.parseArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> _multicast.McastNope.parseArgs is not None
			True
			>>> tst_fxtr_args = ['''NOOP''', '''--port=1234''', '''--iface=127.0.0.1''']
			>>> test_fixture = _multicast.McastNope.parseArgs(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...tuple...>
			>>> tst_args_2 = ['''NOOP''', '''--junk''', '''--more-trash=stuff''']
			>>> (test_fixture_2, test_ignore_extras) = _multicast.McastNope.parseArgs(tst_args_2)
			>>> test_fixture_2 is not None
			True
			>>> type(test_fixture_2) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...Namespace...>
			>>>


	"""

	__module__ = "multicast.__main__"

	__name__ = "multicast.__main__.McastNope"

	__proc__ = "NOOP"  # NOT "Nope" rather "NoOp"

	__prologue__ = "No Operation."

	@classmethod
	def setupArgs(cls, parser):
		"""
		Sets up command-line arguments for the trivial subclass implementation of mtool.

		This method is intended to be overridden by subclasses to define
		specific command-line arguments. It takes a parser object as an
		argument, which is typically an instance of `argparse.ArgumentParser`.

		Args:
			parser (argparse.ArgumentParser): The argument parser to which
												the arguments should be added.

		Returns:
			None: This method does not return a value.

		Note:
			This is trivial implementation make this an optional abstract method. Subclasses may
			choose to implement it or leave it as a no-op.
		"""
		pass  # skipcq: PTC-W0049, PYL-W0107 - optional abstract method

	@staticmethod
	def NoOp(*args, **kwargs):
		"""
		Do Nothing.

		The meaning of Nothing. This function should be self-explanitory;
		it does 'no operation' i.e. nothing.

		This serves as a placeholder when no specific operation is required.

		Args:
			*args: Variable length argument list (unused).
			**kwargs: Arbitrary keyword arguments (unused).

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast.__main__
			>>>

		Testcase 0: multicast.__main__ should have a McastNope class.

			>>> import multicast.__main__
			>>> multicast.__main__.McastNope is not None
			True
			>>>

		Testcase 1: multicast.NoOp should return None.

			>>> import multicast.__main__
			>>> multicast.__main__.McastNope.NoOp() is None
			True
			>>> multicast.__main__.McastNope.NoOp() is not None
			False
			>>>
			>>> multicast.__main__.McastNope.NoOp("Junk")
			None
			>>>

		"""
		return None  # noqa

	def doStep(self, *args, **kwargs):
		"""
		Overrides the `doStep` method from `mtool` to perform no action.

		This method calls the `NoOp` function with the provided arguments and returns the result.
		This serves as a placeholder or default action when no specific operation is required.

		Args:
			*args: Positional arguments passed to `NoOp`.
			**kwargs: Keyword arguments passed to `NoOp`.

		Args:
			*args: Variable length argument list (unused).
			**kwargs: Arbitrary keyword arguments (unused).

		Returns:
			tuple: A "tuple" set to None.

		"""
		_None_from_NoOp = self.NoOp(*args, **kwargs)
		return (
			_None_from_NoOp is None,
			_None_from_NoOp  # noqa
		)


class McastRecvHearDispatch(mtool):
	"""
	The `McastRecvHearDispatch` class handles receiving and dispatching multicast messages.

	This class listens for multicast messages on a specified group and port, and dispatches them
	to the appropriate handler. It is designed to work with both command-line tools and
	programmatic interfaces.

	Testing:

		Testcase 0: First set up test fixtures by importing multicast.

			>>> import multicast.__main__ as _multicast
			>>> _multicast.McastNope is not None
			True
			>>>

		Testcase 1: Recv should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> multicast.__main__ is not None
			True
			>>> multicast.__main__.McastNope is not None
			True
			>>> multicast.recv.McastRECV.__module__ is not None
			True
			>>> multicast.recv.McastRECV.__proc__ is not None
			True
			>>> multicast.recv.McastRECV.__epilogue__ is not None
			True
			>>> multicast.recv.McastRECV.__prologue__ is not None
			True
			>>>


		Testcase 2: parseArgs should return a namespace.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the multicast.mtool.parseArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> _multicast.McastRecvHearDispatch.parseArgs is not None
			True
			>>> tst_fxtr_args = ['''NOOP''', '''--port=1234''', '''--iface=127.0.0.1''']
			>>> test_fixture = _multicast.McastRecvHearDispatch.parseArgs(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...tuple...>
			>>> tst_args_2 = ['''NOOP''', '''--junk''', '''--more-trash=stuff''']
			>>> (test_fixture_2, t_ig_ext) = _multicast.McastRecvHearDispatch.parseArgs(tst_args_2)
			>>> test_fixture_2 is not None
			True
			>>> type(test_fixture_2) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...Namespace...>
			>>>


	"""

	__module__ = "multicast.__main__"

	__name__ = "multicast.__main__.McastRecvHearDispatch"

	__proc__ = "HEAR"

	__epilogue__ = """Generally speaking you want to bind to one of the groups you joined in
		this module/instance, but it is also possible to bind to group which
		is added by some other programs (like another python program instance of this)
	"""

	__prologue__ = "Python Multicast Receiver. Primitives for a listener for multicast data."

	@classmethod
	def setupArgs(cls, parser):
		"""
		Will attempt to add hear args.

		Both HEAR and RECV use the same arguments, and are differentiated only by the global,
		'--daemon' argument during dispatch. The remaining arguments are:

			| Arguments | Notes |
			|-----------|------------------------------------------------------------|
			| --deamon  | Enable use of HEAR, otherwise use RECV if omitted          |
			| --group   | multicast group (ip address) to bind-to for the udp socket |
			| --groups  | multicast groups to join (should include the bind group)   |
			| --port    | The UDP port number to listen/filter on for the udp socket |

		Testing:

			Testcase 0: First set up test fixtures by importing multicast.

				>>> import multicast
				>>> multicast.hear is not None
				True
				>>> multicast.hear.McastHEAR is not None
				True
				>>>

			Testcase 1: main should return an int.
				A: Test that the multicast component is initialized.
				B: Test that the hear component is initialized.
				C: Test that the main(hear) function is initialized.
				D: Test that the main(hear) function returns an int 0-3.

				>>> multicast.hear is not None
				True
				>>> multicast.__main__.main is not None
				True
				>>> tst_fxtr_args = ['''HEAR''', '''--daemon''', '''--port=1234''']
				>>> (test_fixture, junk_ignore) = multicast.__main__.main(tst_fxtr_args)
				>>> test_fixture is not None
				True
				>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
				<...int...>
				>>> int(test_fixture) >= int(0)
				True
				>>> int(test_fixture) < int(4)
				True
				>>>

			Testcase 2: setupArgs should not error given valid input.
				A: Test that the multicast component is initialized.
				B: Test that the __main__ component is initialized.
				C: Test that the McastRecvHearDispatch class is initialized.
				D: Test that the setupArgs function returns without error.

				>>> multicast.__main__ is not None
				True
				>>> multicast.__main__.McastRecvHearDispatch is not None
				True
				>>> tst_fxtr_args = argparse.ArgumentParser(prog="testcase")
				>>> multicast.__main__.McastRecvHearDispatch.setupArgs(parser=tst_fxtr_args)
				>>>

			Testcase 3: setupArgs should return None untouched.
				A: Test that the multicast component is initialized.
				B: Test that the __main__ component is initialized.
				C: Test that the McastRecvHearDispatch class is initialized.
				D: Test that the McastRecvHearDispatch.setupArgs() function yields None.

				>>> multicast.__main__ is not None
				True
				>>> multicast.__main__.McastRecvHearDispatch is not None
				True
				>>> multicast.__main__.McastRecvHearDispatch.setupArgs is not None
				True
				>>> tst_fxtr_N = None
				>>> test_fixture = multicast.__main__.McastRecvHearDispatch.setupArgs(tst_fxtr_N)
				>>> test_fixture is not None
				False
				>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
				<...None...>
				>>> tst_fxtr_N == test_fixture
				True
				>>> tst_fxtr_N is None
				True
				>>>
				>>> test_fixture is None
				True
				>>>


		"""
		if parser is not None:  # pragma: no branch
			parser.add_argument(
				"--port",
				type=int,
				default=_MCAST_DEFAULT_PORT,  # skipcq: PYL-W0212 - module ok
			)
			__tmp_help = "local interface to use for listening to multicast data; "
			__tmp_help += "if unspecified, any one interface may be chosen."
			parser.add_argument("--iface", default=None, help=__tmp_help)
			__tmp_help = "multicast group (ip address) to bind-to for the udp socket; "
			__tmp_help += "should be one of the multicast groups joined globally "
			__tmp_help += "(not necessarily joined in this python program) "
			__tmp_help += "in the interface specified by --iface. "
			__tmp_help += f"If unspecified, bind-to {_MCAST_DEFAULT_GROUP} "
			__tmp_help += "(all addresses (all multicast addresses) of that interface)"
			parser.add_argument(
				"--group",
				default=_MCAST_DEFAULT_GROUP,  # skipcq: PYL-W0212 - module ok
				help=__tmp_help,
			)
			__tmp_help = "multicast groups (ip addresses) to join globally; "
			__tmp_help += "should be one of the multicast groups joined globally "
			__tmp_help += "by the interface specified by --iface. "
			__tmp_help += "If unspecified, or supplied an empty list, the default "
			__tmp_help += "implementation will join "
			__tmp_help += f"{_MCAST_DEFAULT_GROUP} (all addresses (all multicast addresses) "
			__tmp_help += "of that interface) instead of not joining. NOTE: If you really need "
			__tmp_help += "to NOT join the multicast group you should instead use the sockets "
			__tmp_help += "module directly, as this module does not support such a use-case."
			parser.add_argument("--groups", default=[], nargs="*", help=__tmp_help)

	@staticmethod
	def _help_daemon_dispatch(*args, **kwargs):
		"""
		Helps checking flags for daemon dispatching.

		Internal method to check the `--daemon` option
		and interpret how it affects the dispatching of sub-commands.

		Args:
			*args: Additional positional arguments.
			**kwargs: Parsed command-line arguments.

		Returns:
			boolean: True if daemon mode is to be used, otherwise False.

		"""
		_useHear = kwargs.get("is_daemon", False)
		return _useHear

	def doStep(self, *args, **kwargs):
		"""
		Executes a multicast step based on the daemon dispatch.

		Overrides the `doStep` method from `mtool` to determine and execute
		the correct sub-command based on provided arguments.

		This method selects either the `McastHEAR` or `McastRECV` class based on the daemon
		dispatch flag and executes the corresponding step.

		The RECV (via McastRECV) is the primitive sub-command to receive a single multicast hunk.
		The HEAR (via McastHEAR) is equivalent to running RECV in a loop to continually receive
		multiple hunks. Most use-case will probably want to use HEAR instead of RECV.

		Args:
			*args: Variable length argument list containing command-line arguments.
			**kwargs: Arbitrary keyword arguments.

		Returns:
			tuple: The result of the dispatched sub-command's `doStep` method.

		"""
		if self._help_daemon_dispatch(*args, **kwargs):
			__stub_class = hear.McastHEAR
		else:
			__stub_class = recv.McastRECV
		return __stub_class().doStep(*args, **kwargs)


# More boiler-plate-code

TASK_OPTIONS = {
	"NOOP": McastNope(),
	"RECV": McastRecvHearDispatch(),
	"SAY": send.McastSAY(),
	"HEAR": McastRecvHearDispatch(),
}
"""The callable function tasks of this program. will add."""


class McastDispatch(mtool):
	"""
	The `McastDispatch` class is the main entry point for dispatching multicast tasks.

	It provides a command-line interface for sending, receiving, and listening to multicast
	messages. The class handles argument parsing and dispatches the appropriate multicast
	tool based on the provided command.

	"""

	__proc__: str = "multicast"

	__prologue__: str = "The Main Entrypoint."

	__epilogue__: str = "Called from the command line, this main component handles the CLI dispatch."

	@classmethod
	def setupArgs(cls, parser) -> None:
		"""
		Will attempt to add each subcomponent's args.

		As the dispatch tool, this is more of a proxy implementation to call the sub-components
		own setupArgs.
		"""
		if parser is not None:  # pragma: no branch
			for sub_tool in sorted(TASK_OPTIONS.keys()):
				sub_parser = parser.add_parser(sub_tool, help="...")
				type(TASK_OPTIONS[sub_tool]).setupArgs(sub_parser)

	@staticmethod
	def useTool(tool, **kwargs) -> tuple:
		"""Will Handle launching the actual task functions."""
		theResult = None
		cached_list = sorted(TASK_OPTIONS.keys())
		_is_done = False
		if (tool is not None) and (tool in cached_list):
			try:
				(_is_done, theResult) = TASK_OPTIONS[tool].__call__([], **kwargs)
			except Exception as _cause:  # pragma: no branch
				theResult = f"CRITICAL - Attempted '[{tool}]: {kwargs}' just failed! :: {_cause}"  # noqa
				_is_done = False
		return (_is_done, theResult)  # noqa

	def doStep(self, *args, **kwargs) -> tuple:
		"""
		Executes the multicast tool based on parsed arguments.

		This method parses the command-line arguments, selects the appropriate multicast tool, and
		executes it. If an error occurs during argument handling, it prints a warning message.

		Args:
			*args: Command-line arguments for the multicast tool.

		Returns:
			A tuple containing the exit status and the result of the tool execution.
		"""
		_response: tuple = (64, exceptions.EXIT_CODES[64][1])
		try:
			(argz, _) = type(self).parseArgs(*args)
			service_cmd = argz.cmd_tool
			argz.__dict__.__delitem__("cmd_tool")
			_TOOL_MSG = (self.useTool(service_cmd, **argz.__dict__))  # skipcq: PYL-C0325
			if _TOOL_MSG[0]:
				_response = (0, _TOOL_MSG)
			else:
				_response = (70, _TOOL_MSG)
				if sys.stdout.isatty():  # pragma: no cover
					print(str(_TOOL_MSG))
		except Exception as _cause:  # pragma: no branch
			exit_code = exceptions.get_exit_code_from_exception(_cause)
			_response = (
				1,
				f"CRITICAL - Attempted '[{__name__}]: {args}' just failed! :: {exit_code} {_cause}" # noqa
			)
			if sys.stderr.isatty():
				print(
					"WARNING - An error occurred while handling the arguments. Refused.",
					file=sys.stderr,
				)
				print(f"{exceptions.EXIT_CODES[exit_code][1]}: {_cause}\n{_cause.args}", file=sys.stderr)
		return _response  # noqa


@exceptions.exit_on_exception
def main(*argv) -> tuple:
	"""
	Do main event stuff.

	Executes the multicast command-line interface, by parsing command-line arguments and dispatching
	the appropriate multicast operations.

	The main(*args) function in multicast is expected to return a POSIX compatible exit code and
	optional detail message. Regardless of errors the result as an 'exit code' (int) is returned,
	even if the optional details are not (e.g., `tuple(int(exit_code), None)`).
	The only exception is when the error results in exiting the process, which will exit the
	python runtime with the underlying return codes, instead of returning directly to the then
	unreachable caller. See `multicast.exceptions.exit_on_exception` for the mechanisms involved.
	The expected return codes are as follows:
		= 0:  Any nominal state (i.e. no errors and possibly success)
		≥ 1:  Any erroneous state (includes simple failure)
		> 2:  Any failed state
		< 0:  Implicitly erroneous and treated the same as abs(exit_code) would be.

	Args:
		*argv: the array of arguments. Usually sys.argv[1:]

	Returns:
		tuple: the underlying exit code int, and optional detail string.

	Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.send is not None
			True
			>>>

		Testcase 0: main should return an int.
			A: Test that the multicast component is initialized.
			B: Test that the send component is initialized.
			C: Test that the send.main function is initialized.
			D: Test that the send.main function returns an int 0-3.

			>>> multicast.send is not None
			True
			>>> multicast.__main__.main is not None
			True
			>>> tst_fxtr_args = ['''SAY''', '''--port=1234''', '''--message''', '''is required''']
			>>> (test_fixture, junk_ignore) = multicast.__main__.main(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...int...>
			>>> int(test_fixture) >= int(0)
			True
			>>> int(test_fixture) < int(4)
			True
			>>>


		Testcase 1: main should return an int.
			A: Test that the multicast component is initialized.
			B: Test that the recv component is initialized.
			C: Test that the main(recv) function is initialized.
			D: Test that the main(recv) function returns an int 0-3.

			>>> multicast.recv is not None
			True
			>>> multicast.__main__.main is not None
			True
			>>> tst_fxtr_args = ['''RECV''', '''--port=1234''', '''--group''', '''224.0.0.1''']
			>>> (test_fixture, junk_ignore) = multicast.__main__.main(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...int...>
			>>> int(test_fixture) >= int(0)
			True
			>>> int(test_fixture) < int(4)
			True
			>>>


		Testcase 2: main should error with usage.
			A: Test that the multicast component is initialized.
			B: Test that the recv component is initialized.
			C: Test that the main(recv) function is initialized.
			D: Test that the main(recv) function errors with a usage hint by default.

			>>> multicast.recv is not None
			True
			>>> multicast.__main__.main is not None
			True
			>>> (test_fixture, junk_ignore) = multicast.__main__.main() #doctest: +ELLIPSIS
			usage: multicast [-h | -V] [--use-std] [--daemon] CMD ...
			multicast...
			CRITICAL...
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...int...>
			>>> int(test_fixture) >= int(0)
			True
			>>> int(test_fixture) < int(4)
			True
			>>> type(junk_ignore)
			<...str...>
			>>> junk_ignore in "STOP"
			True
			>>>


	"""
	dispatch: McastDispatch = McastDispatch()
	return dispatch(*argv)


def cli() -> int:
	"""
	Do main console script stuff.

	Along with `main()`, `cli()` provides a main entrypoint for console usage of multicast.

	`cli()` just calls `main()` with arguments from `sys.argv` and returns only the exit-code.

	Through calling `multicast.__main__.main(sys.argv[1:])`, `cli()` ...
	> Executes the multicast command-line interface, by parsing command-line arguments and
	> dispatching the appropriate multicast operations.
	>
	> The main(*args) function in multicast is expected to return a POSIX compatible exit code...

	`cli()` versus `main(*args)`:
		- The primary difference is the return types, whereas `main(*args)` returns a `tuple`,
			`cli()` returns only the first element as an `int`.
		- The secondary difference between `cli()` and `main(*args)` is that `main(*args)` requires
			arguments to be passed, whereas `cli()` will use `sys.argv` instead.

	__Except__ in the case of errors, the result as an 'exit code' (int) is returned by `cli()`.
	The expected return codes are the same as those from `main(*args)`.

	Args:
		None: Uses `sys.argv` instead.

	Returns:
		int: the underlying exit code int

	Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.__main__.main is not None
			True
			>>>

		Testcase 0: calls to cli should return an int.
			A: Test that the call to the `cli` function returns an int 0-3.

			>>> tst_argv_args = ['''SAY''', '''--port=1234''', '''--message''', '''is required''']
			>>> sys.argv = tst_argv_args  # normally arguments are automatically already in argv
			>>> test_code = multicast.__main__.cli()
			>>> test_code is not None
			True
			>>> type(test_code) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...int...>
			>>> int(test_code) >= int(0)
			True
			>>> int(test_code) < int(4)
			True
			>>>

		Testcase 1: main should error with usage.
			A: Test that the multicast component is initialized.
			B: Test that the recv component is initialized.
			C: Test that the main(recv) function is initialized.
			D: Test that the main(recv) function errors with a usage hint by default.

			>>> multicast.__main__.main is not None
			True
			>>> test_code = multicast.__main__.cli() #doctest: +ELLIPSIS
			usage: multicast [-h | -V] [--use-std] [--daemon] CMD ...
			multicast...
			CRITICAL...
			>>> type(test_code) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...int...>
			>>> int(test_code) >= int(0)
			True
			>>> int(test_code) < int(4)
			True
			>>>
	"""
	__EXIT_CODE: tuple = (1, exceptions.EXIT_CODES[1][1])
	if sys.argv is not None:
		if len(sys.argv) > 1:
			__EXIT_CODE = main(sys.argv[1:])
		else:  # pragma: no branch
			__EXIT_CODE = main([__name__, "-h"])
	return __EXIT_CODE[0]


if __name__ in '__main__':
	exit(cli())  # skipcq: PYL-R1722 - intentionally allow overwriting exit for testing
