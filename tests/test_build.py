#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast PEP-517 Tests
# ..................................
# Copyright (c) 2025, Mr. Walls
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

"""Build and packaging tests for the multicast package.

This module contains test cases that verify the build process, package structure,
and installation requirements of the multicast package.

Classes:
	BuildPEP517TestSuite: Test cases for build verification.
	BuildPEP621TestSuite: Test cases for metadata verification.

Meta Testing:

	>>> import tests.test_build
	>>> tests.test_build.__name__
	'tests.test_build'
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
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import sys
		from context import os
		from context import unittest
		from context import subprocess
		from context import BasicUsageTestSuite
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause


@context.markWithMetaTag("mat", "build")
class BuildPEP517TestSuite(BasicUsageTestSuite):
	"""
	Test suite for PEP 621 metadata compliance.

	This test suite verifies that the project adheres to PEP 621 standards
	for project metadata specification in pyproject.toml.

	Meta Testing:

		>>> import tests.test_build
		>>> tests.test_build.BuildPEP621TestSuite
		<class 'tests.test_build.BuildPEP621TestSuite'>
		>>>

	"""

	__module__ = "tests.test_build"

	def test_build_works_WHEN_supporting_pep517(self) -> None:
		"""
		Test building the package using PEP 517 standards.

		This test verifies:
		1. Successful package build (both sdist and wheel)
		3. Presence of expected distribution files

		References:
		- PEP 517: https://peps.python.org/pep-0517/

		Args:
			None

		Returns:
			None
		"""
		# Arguments need to clean
		# Arguments need to build
		build_arguments = [
			f"{str(sys.executable)} -m coverage run", "-p", "-m", "build", "--sdist", "--wheel",
		]
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn("running build", str(theBuildtxt))
		self.assertIn("Successfully built", str(theBuildtxt))
		# Verify that the dist directory contains the expected files
		dist_dir = os.path.join(os.getcwd(), "dist")
		pkg_version = str(self._should_get_package_version_WHEN_valid())
		dist_files = sorted(os.listdir(dist_dir), reverse=True)
		expected_files = [
			f"multicast-{pkg_version}.tar.gz",
			f"multicast-{pkg_version}-py3-none-any.whl",
		]
		for expected_file in expected_files:
			self.assertIn(
				expected_file,
				dist_files,
				f"Missing {expected_file} in dist directory. Looking for version {pkg_version}",
			)


@context.markWithMetaTag("mat", "build")
class BuildPEP621TestSuite(BasicUsageTestSuite):

	__module__ = "tests.test_build"

	def test_has_configs_WHEN_supporting_pep621(self) -> None:
		"""
		Test presence of the package config pyproject.toml for using PEP 621 standards.

		This test verifies:
		1. Presence of expected project config files (pyproject.toml)

		References:
		- PEP 621: https://peps.python.org/pep-0621/
		"""
		# Verify that the project directory contains the expected files
		project_base_dir = os.path.normpath(os.getcwd())
		project_files = sorted(os.listdir(project_base_dir), reverse=True)
		expected_files = [
			"pyproject.toml",
		]
		for expected_file in expected_files:
			self.assertIn(
				expected_file,
				project_files,
				f"Missing {expected_file} in project directory. See PEP 621.",
			)


# leave this part
if __name__ == "__main__":
	unittest.main()
