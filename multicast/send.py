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

# Third-party Acknowledgement:
# ..........................................
# Some code (less than 10%) was modified/derived from:
# https://stackoverflow.com/a/52791404
# Copyright (c) 2019, "pterodragon" (https://stackoverflow.com/users/5256940/pterodragon)
# which was under CC-by-sa-4 license.
# see https://creativecommons.org/licenses/by-sa/4.0/ for details
# The Code in McastSAY.setupArgs (previously parseArgs), and McastSAY.doStep (previously main)
# are thus also under
# CC-by-sa-4 https://creativecommons.org/licenses/by-sa/4.0/
# ..........................................
# NO ASSOCIATION

"""Provides multicast broadcast features.

Caution: See details regarding dynamic imports [documented](../__init__.py) in this module.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automatically imported.
		A: Test that the send component is initialized.
		B: Test that the send.__MAGIC__ components are initialized.

		>>> multicast.send is not None
		True
		>>>

		>>> multicast.send.__doc__ is not None
		True
		>>>

		>>> multicast.send.__module__ is not None
		True
		>>>

		>>> multicast.send.McastSAY is not None
		True
		>>>


"""

__package__ = "multicast"  # skipcq: PYL-W0622
"""The package of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automatically imported.

		>>> multicast.send.__package__ is not None
		True
		>>>
		>>> multicast.send.__package__ == multicast.__package__
		True
		>>>

"""

__module__ = "multicast"
"""The module of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automatically imported.

		>>> multicast.send.__module__ is not None
		True
		>>>

"""

__file__ = "multicast/send.py"
"""The file of this component."""

__name__ = "multicast.send"  # skipcq: PYL-W0622 - Ensures the correct name value.
"""The name of this component.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automatically imported.

		>>> multicast.send.__name__ is not None
		True
		>>>

"""

try:
	import sys
	if "multicast" not in sys.modules:
		# skipcq
		from . import multicast as multicast  # pylint: disable=cyclic-import - skipcq: PYL-C0414
	else:  # pragma: no branch
		multicast = sys.modules["multicast"]
	_BLANK = multicast._BLANK  # skipcq: PYL-W0212 - module ok
except Exception as _cause:
	del _cause  # skipcq - cleanup any error leaks early
	# skipcq
	import multicast as multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414

try:
	import logging
	from multicast import argparse as _argparse  # skipcq: PYL-C0414
	from multicast import unicodedata as _unicodedata  # skipcq: PYL-C0414
	from multicast import socket as _socket  # skipcq: PYL-C0414
	from multicast import struct as _struct  # skipcq: PYL-C0414
	depends = [_unicodedata, _socket, _struct, _argparse]
	for unit in depends:
		try:
			if unit.__name__ is None:  # pragma: no branch
				raise ImportError(
					f"[CWE-440] module failed to import {str(unit)}."
				) from None
		except Exception as _cause:  # pragma: no branch
			raise ImportError("[CWE-758] Module failed completely.") from _cause
except Exception as baton:  # pragma: no branch
	raise ImportError(baton) from baton


module_logger = logging.getLogger(__name__)
module_logger.debug(
	"Loading %s",  # lazy formatting to avoid PYL-W1203
	__name__,
)


class McastSAY(multicast.mtool):
	"""
	Multicast Broacaster tool.

		Testing:

		Testcase 0: First set up test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.send is not None
			True
			>>> multicast._MCAST_DEFAULT_PORT is not None
			True
			>>> multicast._MCAST_DEFAULT_GROUP is not None
			True
			>>> multicast._MCAST_DEFAULT_TTL is not None
			True
			>>>

		Testcase 1: Recv should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> multicast.send is not None
			True
			>>> multicast.send.McastSAY is not None
			True
			>>> multicast.send.McastSAY.__module__ is not None
			True
			>>> multicast.send.McastSAY.__proc__ is not None
			True
			>>> multicast.send.McastSAY.__prologue__ is not None
			True
			>>>

	"""

	__module__ = "multicast.send"

	__name__ = "multicast.send.McastSAY"

	__proc__ = "SAY"

	__prologue__ = "Python Multicast Broadcaster."

	@classmethod
	def setupArgs(cls, parser):
		"""
		Will attempt add send args.

			Testing:

			Testcase 0: First set up test fixtures by importing multicast.

				>>> import multicast
				>>> multicast.send is not None
				True
				>>> multicast.send.McastSAY is not None
				True
				>>>

			Testcase 1: main should return an int.
				A: Test that the multicast component is initialized.
				B: Test that the send component is initialized.
				C: Test that the main(say) function is initialized.
				D: Test that the main(say) function returns an int 0-3.

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

			Testcase 2: setupArgs should return None untouched.
				A: Test that the multicast component is initialized.
				B: Test that the send component is initialized.
				C: Test that the McastSAY.setupArgs() function is initialized.
				D: Test that the McastSAY.setupArgs() function yields None.

				>>> multicast.send is not None
				True
				>>> multicast.send.McastSAY is not None
				True
				>>> multicast.send.McastSAY.setupArgs is not None
				True
				>>> tst_fxtr_null_args = None
				>>> test_fixture = multicast.send.McastSAY.setupArgs(tst_fxtr_null_args)
				>>> test_fixture is not None
				False
				>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
				<...None...>
				>>> tst_fxtr_null_args == test_fixture
				True
				>>> tst_fxtr_null_args is None
				True
				>>>
				>>> test_fixture is None
				True
				>>>


		"""
		if parser is not None:  # pragma: no branch
			if __debug__:
				module_logger.debug(
					"Adding %s arguments.",  # lazy formatting to avoid PYL-W1203
					__name__,
				)
			parser.add_argument(
				"--port",
				type=int,
				default=multicast._MCAST_DEFAULT_PORT  # skipcq: PYL-W0212 - module ok
			)
			parser.add_argument(
				"--group",
				default=multicast._MCAST_DEFAULT_GROUP  # skipcq: PYL-W0212 - module ok
			)
			parser.add_argument(
				"--groups",
				required=False,
				nargs="*",
				dest="groups",
				help="multicast groups (ip addrs) to listen to join."
			)
			msgGrp = parser.add_argument_group()
			msgGrp.add_argument(
				"-m",
				"--message",
				nargs="+",
				dest="data",
				default="PING from {name}: group: {group}, port: {port}",
			)
			# v2.0.9: Added the --pipe option
			msgGrp.add_argument(
				"--pipe",
				action="store_const",
				const=["-"],
				dest="data",
				help="read message from stdin (equivalent to --message -)"
			)

	@staticmethod
	def _sayStep(group, port, data):
		"""
		Internal method to send a message via multicast.

		Will send the given data over the given port to the given group.
		The actual magic is handled here.

		Args:
			group (str): Multicast group address to send the message to.
			port (int): Port number to use for sending.
			data (str): Message data to be sent.

		Returns:
			bool: True if the message was sent successfully, False otherwise.
		"""
		_success = False
		sock = multicast.genSocket()
		if __debug__:
			module_logger.info(
				"Preparing to send %d",  # lazy formatting to avoid PYL-W1203
				len(data),
			)
		try:
			if __debug__ and module_logger.isEnabledFor(logging.DEBUG):  # pragma: no branch
				module_logger.debug("Encoding.")
				_payload = data.encode('utf8')
				module_logger.debug(
					"Encoded %d.",  # lazy formatting to avoid PYL-W1203
					len(_payload),
				)
				module_logger.debug(
					"Sending %s to (%s, %d).",  # lazy formatting to avoid PYL-W1203
					_payload, group, port,
				)
				sock.sendto(_payload, (group, port))
				module_logger.debug(
					"Sent %d.",  # lazy formatting to avoid PYL-W1203
					len(_payload),
				)
			else:
				sock.sendto(data.encode('utf8'), (group, port))
			_success = True
		finally:
			multicast.endSocket(sock)
		if __debug__:  # pragma: no branch
			if _success:
				module_logger.info("Finished sending. Reporting success.")
			else:  # pragma: no branch
				module_logger.warning("Failed to send. Reporting failure.")
		return _success

	def doStep(self, *args, **kwargs):
		"""
		Execute the SAY operation to send multicast messages.

		Overrides the `doStep` method from `mtool` to send messages based on
		provided arguments.

		Args:
			*args: Variable length argument list containing command-line arguments.
			**kwargs: Arbitrary keyword arguments.
			- group (str): Multicast group address (default: multicast._MCAST_DEFAULT_GROUP)
			- port (int): Port number (default: multicast._MCAST_DEFAULT_PORT)
			- data (str, list, or bytes): Message to be sent. If set to ['-'], reads from stdin.

		Returns:
			tuple: A tuple containing a status indicator and optional error message.
		"""
		_logger = logging.getLogger(McastSAY.__name__)
		_logger.debug(McastSAY.__proc__)
		group = kwargs.get(
			"group",
			multicast._MCAST_DEFAULT_GROUP  # skipcq: PYL-W0212 - module ok
		)
		port = kwargs.get("port", multicast._MCAST_DEFAULT_PORT)  # skipcq: PYL-W0212 - module ok
		data = kwargs.get("data")
		_result = False
		if data == ["-"]:
			_logger.debug("Reading from stdin")
			_result = True
			# Read from stdin in chunks
			while True:
				try:
					# Read configured amount of bytes at a time - matches read size by default
					# skipcq: PYL-W0212
					chunk = sys.stdin.read(
						multicast._MCAST_DEFAULT_BUFFER_SIZE,  # skipcq: PYL-W0212 - module ok
					)
				except OSError:
					_logger.exception("[CWE-228] Error reading from stdin.")
					break
				if not chunk:
					break
				_result = _result and self._sayStep(group, port, chunk)
			_logger.debug("Finished reading stdin.")
		elif isinstance(data, list):
			# Join multiple arguments into a single string
			message = " ".join(data)
			_result = self._sayStep(group, port, message)
		else:
			message = data.decode('utf8') if isinstance(data, bytes) else str(data)
			_result = self._sayStep(group, port, message)
		if __debug__:  # pragma: no branch
			if _result:
				module_logger.debug(
					"SEND result was %s. Reporting success.",  # lazy formatting to avoid PYL-W1203
					_result,
				)
			else:
				module_logger.debug(
					"SEND result was %s. Reporting failure.",  # lazy formatting to avoid PYL-W1203
					_result,
				)
		return (_result, None)  # skipcq: PTC-W0020  - intended
