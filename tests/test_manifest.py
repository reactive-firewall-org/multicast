#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Require Parsing Tests
# ..................................
# Copyright (c) 2025-2026, Mr. Walls
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
	try:
		import context
	except Exception as _root_cause:  # pragma: no branch
		del _root_cause  # skipcq - cleanup any error leaks early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import unittest
		from context import subprocess
		from context import os
		from context import sys
		from context import BasicUsageTestSuite
	import tarfile
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause


@context.markWithMetaTag("mat", "build")
class ManifestInclusionTestSuite(BasicUsageTestSuite):
	"""
	ManifestInclusionTestSuite is a test suite focused on validating the contents
	of the source distribution (sdist) for a package, ensuring that it includes
	required files while excluding unwanted ones.

	This test suite extends the BasicUsageTestSuite provided by the `context` module,
	implementing tests to verify the correct inclusion and exclusion of files as specified
	in the package manifest.

	Attributes:
		__module__ (str): Module identifier
		__name__ (str): Full class name

	Methods:
		_build_sdist_and_get_members():
			Builds the source distribution for the package and retrieves the list
			of files included in the resulting archive along with the package version.
			It temporarily modifies the umask to allow file creations and performs
			necessary assertions on the build outcome.

		test_sdist_includes_required_files():
			Tests that the source distribution contains all mandatory files
			specified for the package by validating their presence in the built
			tar archive.

		test_sdist_excludes_unwanted_files():
			Tests that certain undesired files and directories are excluded from
			the source distribution by asserting their absence in the built
			tar archive.

	Returns:
		tuple: Each test method retrieves a tuple containing the list of member file paths
		and the package version string from the `_build_sdist_and_get_members` method.

	Raises:
		AssertionError:
			- In `_build_sdist_and_get_members`, if the build command does not execute
				successfully or if no files are found in the 'dist' directory.
			- In `test_sdist_includes_required_files`, if any expected file is missing from
				the sdist.
			- In `test_sdist_excludes_unwanted_files`, if any unwanted file is found in the sdist.

	Notes:
		The tests require a functioning environment that can build the source distribution
		and may depend on the presence of specific files and directories as dictated
		by the package's structure. The tests should be run in an appropriate context
		where the build tooling and dependencies are available.

	Usage:
		This test suite can be instantiated and executed within a testing framework
		that supports the discovery and execution of test cases, allowing for thorough validation
		of the source distribution's contents.
	"""

	__module__ = "tests.test_manifest"

	__name__ = "tests.test_manifest.ManifestInclusionTestSuite"

	def _build_sdist_and_get_members(self):
		"""Build the source distribution and return the list of member files and package version.

		This helper method runs the command to create a source distribution (sdist) of the package
		and then extracts the list of files included in the archive.

		Returns:
			tuple: A tuple containing the list of member file paths and the package version string.

		Raises:
			AssertionError: If the build command does not run successfully or if no files are found
				in the 'dist' directory.
		"""
		# Arguments need to build
		build_arguments = [
			f"{str(sys.executable)} -m coverage run", "-p", "-m",
			"build",
			"--sdist",
		]
		theBuildtxt = None
		# Temporarily relax the default umask (to allow creation of venv files)
		original_umask = os.umask(0o027)  # Temporarily set the umask
		# Build the source distribution
		try:
			theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		finally:
			os.umask(original_umask)  # Restore the original umask
			self.assertIsNotNone(theBuildtxt, f"Failed with {build_arguments} in relaxed state")
		self.assertIn(str("running sdist"), str(theBuildtxt))
		dist_dir = os.path.join(os.getcwd(), 'dist')
		dist_files = sorted(os.listdir(dist_dir), reverse=True)
		self.assertTrue(len(dist_files) > 0, 'No files found in dist directory.')
		sdist_path = os.path.join(dist_dir, dist_files[0])
		# Open the tar.gz file to inspect contents
		with tarfile.open(sdist_path, 'r:gz') as tar:
			members = tar.getnames()
		pkg_version = str(self._should_get_package_version_WHEN_valid())
		return members, pkg_version

	def test_sdist_includes_required_files(self):
		"""Test that the source distribution includes all required files.

		This test verifies that the source distribution includes all expected files by building
		the sdist and checking if the required files are present in the tar archive.
		"""
		members, pkg_version = self._build_sdist_and_get_members()
		package_prefix = str("multicast-{}").format(pkg_version)
		expected_files = [
			f"{package_prefix}/README.md",
			f"{package_prefix}/LICENSE.md",
			f"{package_prefix}/requirements.txt",
			f"{package_prefix}/MANIFEST.in",
			f"{package_prefix}/multicast/__init__.py",
			f"{package_prefix}/multicast/__main__.py",
			f"{package_prefix}/multicast/skt.py",
			f"{package_prefix}/multicast/recv.py",
			f"{package_prefix}/multicast/send.py",
			f"{package_prefix}/multicast/hear.py",
			f"{package_prefix}/multicast/env.py",
			f"{package_prefix}/multicast/exceptions.py",
			# Include other important files and directories
		]
		for expected_file in expected_files:
			self.assertIn(
				expected_file,
				members,
				f"Missing {expected_file} in sdist.",
			)

	def test_sdist_excludes_unwanted_files(self):
		"""Test that the source distribution excludes unwanted files.

		This test ensures that unwanted files and directories are not included in the source distribution
		by building the sdist and verifying that these files are absent from the tar archive.
		"""
		members, pkg_version = self._build_sdist_and_get_members()
		package_prefix = str("multicast-{}").format(pkg_version)
		unwanted_files = [
			f"{package_prefix}/.gitignore",
			f"{package_prefix}/.github/",
			f"{package_prefix}/tests/",
			f"{package_prefix}/setup.py",  # changed in v2.0.9a3 for PEP-621 regression check
			# Exclude other files or directories as specified in MANIFEST.in
		]
		for unwanted_file in unwanted_files:
			self.assertNotIn(
				unwanted_file,
				members,
				f"Unwanted file {unwanted_file} found in sdist.",
			)


# leave this part
if __name__ == '__main__':
	unittest.main()
