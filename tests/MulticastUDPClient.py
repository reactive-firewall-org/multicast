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

# THIS FILE IS A TEST FILE ONLY.

# Disclaimer of Warranties.
# A. YOU EXPRESSLY ACKNOWLEDGE AND AGREE THAT, TO THE EXTENT PERMITTED BY
#    APPLICABLE LAW, USE OF THIS SHELL SCRIPT AND ANY SERVICES PERFORMED
#    BY OR ACCESSED THROUGH THIS SHELL SCRIPT IS AT YOUR SOLE RISK AND
#    THAT THE ENTIRE RISK AS TO SATISFACTORY QUALITY, PERFORMANCE, ACCURACY AND
#    EFFORT IS WITH YOU.
#
# B. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THIS SHELL SCRIPT
#    AND SERVICES ARE PROVIDED "AS IS" AND "AS AVAILABLE", WITH ALL FAULTS AND
#    WITHOUT WARRANTY OF ANY KIND, AND THE AUTHOR OF THIS SHELL SCRIPT'S LICENSORS
#    (COLLECTIVELY REFERRED TO AS "THE AUTHOR" FOR THE PURPOSES OF THIS DISCLAIMER)
#    HEREBY DISCLAIM ALL WARRANTIES AND CONDITIONS WITH RESPECT TO THIS SHELL SCRIPT
#    SOFTWARE AND SERVICES, EITHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
#    NOT LIMITED TO, THE IMPLIED WARRANTIES AND/OR CONDITIONS OF
#    MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE,
#    ACCURACY, QUIET ENJOYMENT, AND NON-INFRINGEMENT OF THIRD PARTY RIGHTS.
#
# C. THE AUTHOR DOES NOT WARRANT AGAINST INTERFERENCE WITH YOUR ENJOYMENT OF THE
#    THE AUTHOR's SOFTWARE AND SERVICES, THAT THE FUNCTIONS CONTAINED IN, OR
#    SERVICES PERFORMED OR PROVIDED BY, THIS SHELL SCRIPT WILL MEET YOUR
#    REQUIREMENTS, THAT THE OPERATION OF THIS SHELL SCRIPT OR SERVICES WILL
#    BE UNINTERRUPTED OR ERROR-FREE, THAT ANY SERVICES WILL CONTINUE TO BE MADE
#    AVAILABLE, THAT THIS SHELL SCRIPT OR SERVICES WILL BE COMPATIBLE OR
#    WORK WITH ANY THIRD PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES,
#    OR THAT DEFECTS IN THIS SHELL SCRIPT OR SERVICES WILL BE CORRECTED.
#    INSTALLATION OF THIS THE AUTHOR SOFTWARE MAY AFFECT THE USABILITY OF THIRD
#    PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES.
#
# D. YOU FURTHER ACKNOWLEDGE THAT THIS SHELL SCRIPT AND SERVICES ARE NOT
#    INTENDED OR SUITABLE FOR USE IN SITUATIONS OR ENVIRONMENTS WHERE THE FAILURE
#    OR TIME DELAYS OF, OR ERRORS OR INACCURACIES IN, THE CONTENT, DATA OR
#    INFORMATION PROVIDED BY THIS SHELL SCRIPT OR SERVICES COULD LEAD TO
#    DEATH, PERSONAL INJURY, OR SEVERE PHYSICAL OR ENVIRONMENTAL DAMAGE,
#    INCLUDING WITHOUT LIMITATION THE OPERATION OF NUCLEAR FACILITIES, AIRCRAFT
#    NAVIGATION OR COMMUNICATION SYSTEMS, AIR TRAFFIC CONTROL, LIFE SUPPORT OR
#    WEAPONS SYSTEMS.
#
# E. NO ORAL OR WRITTEN INFORMATION OR ADVICE GIVEN BY THE AUTHOR
#    SHALL CREATE A WARRANTY. SHOULD THIS SHELL SCRIPT OR SERVICES PROVE DEFECTIVE,
#    YOU ASSUME THE ENTIRE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
#    Limitation of Liability.
# F. TO THE EXTENT NOT PROHIBITED BY APPLICABLE LAW, IN NO EVENT SHALL THE AUTHOR
#    BE LIABLE FOR PERSONAL INJURY, OR ANY INCIDENTAL, SPECIAL, INDIRECT OR
#    CONSEQUENTIAL DAMAGES WHATSOEVER, INCLUDING, WITHOUT LIMITATION, DAMAGES
#    FOR LOSS OF PROFITS, CORRUPTION OR LOSS OF DATA, FAILURE TO TRANSMIT OR
#    RECEIVE ANY DATA OR INFORMATION, BUSINESS INTERRUPTION OR ANY OTHER
#    COMMERCIAL DAMAGES OR LOSSES, ARISING OUT OF OR RELATED TO YOUR USE OR
#    INABILITY TO USE THIS SHELL SCRIPT OR SERVICES OR ANY THIRD PARTY
#    SOFTWARE OR APPLICATIONS IN CONJUNCTION WITH THIS SHELL SCRIPT OR
#    SERVICES, HOWEVER CAUSED, REGARDLESS OF THE THEORY OF LIABILITY (CONTRACT,
#    TORT OR OTHERWISE) AND EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE
#    POSSIBILITY OF SUCH DAMAGES. SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION
#    OR LIMITATION OF LIABILITY FOR PERSONAL INJURY, OR OF INCIDENTAL OR
#    CONSEQUENTIAL DAMAGES, SO THIS LIMITATION MAY NOT APPLY TO YOU. In no event
#    shall THE AUTHOR's total liability to you for all damages (other than as may
#    be required by applicable law in cases involving personal injury) exceed
#    the amount of five dollars ($5.00). The foregoing limitations will apply
#    even if the above stated remedy fails of its essential purpose.
################################################################################

__module__ = "tests"
"""This is a testing related stand-alone utilities module.

This module provides test fixtures and utilities for testing multicast communication.
It includes a basic UDP client implementation and handler for testing multicast
functionality.

Classes:
	MCastClient: Test fixture for multicast client operations.
	MyUDPHandler: UDP request handler for echo functionality.

Functions:
	main: Entry point for test operations.

Example:
	>>> from tests.MulticastUDPClient import MCastClient
	>>> client = MCastClient(grp_addr='224.0.0.1', src_port=59259)
	>>> isinstance(client._source_port, int)
	True
	>>>

"""

__name__ = "tests.MulticastUDPClient"  # skipcq: PYL-W0622

try:
	import sys
	if not hasattr(sys, 'modules') or not sys.modules:  # pragma: no branch
		raise ModuleNotFoundError(
			"[CWE-440] OMG! sys.modules is not available or empty."
		) from None
except ImportError as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] Unable to import sys module.") from _cause

try:
	import socket
	import socketserver
except ImportError as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Test module failed completely.") from _cause

try:
	import random
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-758] Test module failed to randomize.") from _cause


class MCastClient(object):  # skipcq: PYL-R0205
	"""
	For use as a test fixture.

	A trivial implementation of a socket-based object with a function
	named say. The say function of this class performs a send and recv on a given socket and
	then prints out simple diognostics about the content sent and any response received.

	Testing:

		First some test fixtures:

		>>> import socket as socket
		>>> import random as random
		>>>

	Testcase 0: test the class MCastClient is.
		A: Test that the MulticastUDPClient component is importable.
		B: Test that the MCastClient class is importable.

		>>> import tests.MulticastUDPClient
		>>> from MulticastUDPClient import MCastClient as MCastClient
		>>> MCastClient is not None
		True
		>>>

	Testcase 1: Test the class MCastClient has a say function.
		A: Test that the MulticastUDPClient component is importable.
		B: Test that the MCastClient class is importable.
		C: Test that the MCastClient class has the function named say.

		>>> import tests.MulticastUDPClient
		>>> from MulticastUDPClient import MCastClient as MCastClient
		>>> MCastClient is not None
		True
		>>> MCastClient.say is not None
		True
		>>> type(MCastClient.say)
		<class 'function'>
		>>>


	"""

	__module__ = "tests.MulticastUDPClient.MCastClient"

	_group_addr = None
	"""The multicast group address."""

	_source_port = None
	"""The source port for the client."""

	# skipcq: TCV-002
	def __init__(self, *args, **kwargs) -> None:  # pragma: no cover
		"""
		Initialize a MCastClient object with optional group address and source port.

		The client can be initialized with or without specifying a group address and source port.
		If no source port is provided, a random port between 50000 and 59999 is generated.

		Args:
			*args: Variable length argument list (Unused).
			**kwargs: Arbitrary keyword arguments.
				- grp_addr (str): The multicast group address.
				- src_port (int): The source port for the client.

		Meta Testing:

			First set up test fixtures by importing test context.

				>>> import tests.MulticastUDPClient as MulticastUDPClient
				>>> from MulticastUDPClient import MCastClient as MCastClient
				>>>

			Testcase 1: Initialization without any arguments.

				>>> client = MCastClient()
				>>> 50000 <= client._source_port <= 59999
				True
				>>> client._group_addr is None
				True
				>>>

			Testcase 2: Initialization with only group address.

				>>> tst_args = {}
				>>> client = MCastClient(grp_addr="224.0.0.1")
				>>> client._group_addr
				'224.0.0.1'
				>>> 50000 <= client._source_port <= 59999
				True
				>>>

			Testcase 3: Initialization with only source port.

				>>> client = MCastClient(src_port=55555)
				>>> client._source_port
				55555
				>>> client._group_addr is None
				True
				>>>

			Testcase 4: Initialization with both group address and source port.

				>>> client = MCastClient(grp_addr="224.0.0.2", src_port=55556)
				>>> client._group_addr
				'224.0.0.2'
				>>> client._source_port
				55556
				>>>


		"""
		# skipcq: TCV-002
		if "grp_addr" in kwargs:  # pragma: no branch
			self._group_addr = kwargs.get("grp_addr", None)  # skipcq: PTC-W0039 - ensure None
		if "src_port" in kwargs:  # pragma: no branch
			self._source_port = kwargs.get("src_port", 0)
		else:  # pragma: no branch
			self._source_port = int(
				50000 + (
					int(random.SystemRandom().randbytes(int(60000).__sizeof__()).hex(), 16) % 9999
				)
			)

	# skipcq: TCV-002
	@staticmethod
	def say(address: str, port: int, sock: socket.socket, msg: str) -> None:  # pragma: no cover
		"""
		Send a message to a specified multicast address and port, then receive and print it.

		This function sends a UTF-8 encoded message to the specified multicast address and port
		using the provided connection. It then waits for a response, decodes it, and prints both
		the sent and received messages.

		Args:
			address (str): The multicast group address to send the message to.
			port (int): The port number to send the message to.
			sock (socket.socket): The socket connection to use for sending and receiving.
			msg (str): The message to be sent.

		Returns:
			None

		Prints:
			The sent message and the received response.

		Meta Testing:

			First, set up test fixtures:

				>>> import unittest.mock
				>>> from MulticastUDPClient import MCastClient
				>>>

			Testcase 1: Test sending and receiving a message.

				>>> mock_socket = unittest.mock.Mock()
				>>> mock_socket.recv.return_value = b"Response received"
				>>> client = MCastClient()
				>>> client.say("224.0.0.1", 59991, mock_socket, "Test message")
				Sent:     Test message
				Received: Response received
				>>>

			Testcase 2: Test sending a 'STOP' message.

				>>> mock_socket.recv.return_value = b"Stopped"
				>>> client.say("224.0.0.1", 59991, mock_socket, "STOP")
				Sent:     STOP
				Received: Stopped
				>>>


		Note:
			This function assumes that the connection is already properly configured
			for multicast communication.

		"""
		# skipcq: TCV-002
		sock.sendto(bytes(msg + "\n", "utf-8"), (address, port))  # pragma: no cover
		received = str(sock.recv(1024), "utf-8")  # pragma: no cover
		sp = " " * 4  # pragma: no cover
		if sys.stdout.isatty():  # pragma: no cover
			print(f"Sent: {sp}{msg}")  # skipcq: PYL-C0209  -  must remain compatible
			print(f"Received: {received}")  # skipcq: PYL-C0209  -  must remain compatible


class MyUDPHandler(socketserver.BaseRequestHandler):
	"""
	Subclasses socketserver.BaseRequestHandler to handle echo functionality.

	Simplifies testing by echoing back the received string data in uppercase,
	after printing the sender's IP address.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.MulticastUDPClient as MulticastUDPClient
			>>> from MulticastUDPClient import MyUDPHandler as MyUDPHandler
			>>>

		Testcase 1: MyUDPHandler should be automatically imported.

			>>> MyUDPHandler.__name__ is not None
			True
			>>>

	"""

	__module__ = "tests.MulticastUDPClient.MyUDPHandler"

	# skipcq: TCV-002
	def handle(self) -> None:  # pragma: no cover
		"""
		Handle incoming UDP requests.

		This method overrides the `handle` method from `socketserver.BaseRequestHandler`
		to process incoming UDP messages. It receives a message from a client, echoes it
		back in uppercase, and prints diagnostic information.

		Meta Testing:

			First set up test fixtures by importing test context.

				>>> import socket
				>>> import threading
				>>> from tests.MulticastUDPClient import MyUDPHandler
				>>>

			Testcase 1: Test handling a simple message.

				>>> import socketserver
				>>> server = socketserver.UDPServer(('localhost', 0), MyUDPHandler)
				>>> threading.Thread(target=server.serve_forever, daemon=True).start()
				>>> client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				>>> client_socket.sendto("hello world\n", server.server_address)
				>>> data, _ = client_socket.recvfrom(1024)
				>>> data
				b'HELLO WORLD\n'
				>>> server.shutdown()
				>>>

			Testcase 2: Test handling an empty message.

				>>> import socketserver
				>>> server = socketserver.UDPServer(('localhost', 0), MyUDPHandler)
				>>> threading.Thread(target=server.serve_forever, daemon=True).start()
				>>> client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				>>> client_socket.sendto("\n", server.server_address)
				>>> data, _ = client_socket.recvfrom(1024)
				>>> data
				b'\n'
				>>> server.shutdown()
				>>>

		Note:
			This method assumes that the incoming request tuple contains a string and a socket,
			as per `socketserver.BaseRequestHandler` for datagram services.

		"""
		# skipcq: TCV-002
		data = self.request[0].strip()  # pragma: no cover
		sock = self.request[1]  # pragma: no cover
		print(f"{self.client_address[0]} wrote: ")  # pragma: no cover
		print(data)  # pragma: no cover
		sock.sendto(data.upper(), self.client_address)  # pragma: no cover


# skipcq: TCV-002
def main() -> None:  # pragma: no cover
	"""
	The main test operations.

	Testing:

		First some test fixtures:

		>>> import socket as socket
		>>> import random as random
		>>>

	Testcase 0: test the function main is.
		A: Test that the MulticastUDPClient component is importable.
		B: Test that the MulticastUDPClient has a main function.

		>>> import tests.MulticastUDPClient
		>>> tests.MulticastUDPClient.main is not None
		True
		>>> type(tests.MulticastUDPClient.main)
		<class 'function'>
		>>>


	"""
	# skipcq: TCV-002
	HOST, PORT = "224.0.0.1", 59991  # pragma: no cover
	data = "TEST This is a test"  # pragma: no cover
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # pragma: no cover
	tsts_fxr = MCastClient()  # pragma: no cover
	print(str((HOST, PORT)))  # pragma: no cover
	tsts_fxr.say(HOST, PORT, sock, data)  # pragma: no cover
	tsts_fxr.say(HOST, PORT, sock, "STOP")  # pragma: no cover


if __name__ == "__main__":  # pragma: no branch
	main()  # skipcq: TCV-002
	# skipcq: PYL-R1722
	exit(0)  # skipcq: PYL-R1722 -- intentionally allow overwriteing exit for testing.
