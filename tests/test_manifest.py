#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Require Parsing Tests
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

	__module__ = "tests.test_manifest"

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
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
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
