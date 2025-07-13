#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
# ..................................
# Copyright (c) 2025, Mr. Walls
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

"""
Selective test runner for the Multicast project.

This script provides a command-line interface for running specific test groups
and categories from the test suite. It allows developers to focus on particular
areas of testing during development and debugging.

Usage:
	python3 -m tests.run_selective --group [mat|extra|fuzzing|performance] [--category CATEGORY]
"""

__module__ = "tests"  # pragma: no cover

import sys  # pragma: no cover
import argparse  # pragma: no cover
import unittest  # pragma: no cover
import logging  # pragma: no cover

if __debug__ and __name__ == "__main__":  # pragma: no branch
	logging.getLogger(__module__).debug(
		"Bootstrapping %s",  # lazy formatting to avoid PYL-W1203
		__file__,
	)

from tests import get_test_suite  # pragma: no cover
from tests import TEST_GROUPS  # pragma: no cover


def main() -> None:  # pragma: no cover
	"""Run selective tests based on specified group and category.

	Parses command line arguments to select the appropriate test suite and executes the tests using
	`unittest.TextTestRunner`. Exits the program with a status code corresponding to the test
	results.

	Returns:
		None: Exits the application.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--group",
		help="Specify test group to run (valid values: mat, extra, fuzzing, performance)",
		choices=TEST_GROUPS.keys(),
	)
	parser.add_argument("--category", help="Specify test category within the selected group")
	args = parser.parse_args()
	try:
		_bar = str("-" * 20)
		logger = logging.getLogger(__module__)
		logger.info(f"{_bar}GROUP{_bar}")  # skipcq PYL-W1203 - test code ok
		logger.info(f"{args.group}:{args.category}")  # skipcq PYL-W1203 - test code ok
		logger.info(f"{_bar}START{_bar}")  # skipcq PYL-W1203 - test code ok
		suite = get_test_suite(args.group, args.category)
		runner = unittest.TextTestRunner(verbosity=2)
		result = runner.run(suite)
		logger.info(f"{_bar} END {_bar}")  # skipcq PYL-W1203 - test code ok
		del _bar  # skipcq - cleanup any object leaks early
		sys.exit(not result.wasSuccessful())
	except ValueError:  # pragma: no branch
		logger.exception("Error occurred")
		sys.exit(1)


if __name__ == "__main__":  # pragma: no branch
	main()
