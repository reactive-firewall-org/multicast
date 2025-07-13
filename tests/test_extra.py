#! /usr/bin/env python3
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

"""Extra Test module for optional functionality.

> [!CAUTION]
> Multicast project testing code is under an MIT license like the Multicast module; however
> the project's Testing can use tools which are split between multiple licenses.
> While all the source-code is open-source, using some of the project test code is only possible
> in an environment where additional restrictions apply, due to third-party licensing which is
> incompatible if it were to be included with the rest of the project.
>
> Environment Compatibility: Users must ensure that their testing environments are equipped
> with the necessary components and licenses to run the testing code. This is akin to a
> "batteries not included" disclaimer, indicating that additional setup may be required.
> AS-IS Disclaimer: Please note that the Multicast project is provided "AS-IS," and we do not
> guarantee compatibility or support for the testing code outside of the specified environments.
> Users are responsible for ensuring compliance with all applicable licenses and for setting up
> their environments accordingly.

This module provides extra test cases for some of the optional components and are expected to fail.

"""


__module__ = "tests"


try:
	try:
		import context
	except ImportError as _cause:  # pragma: no branch
		del _cause  # skipcq - cleanup any error vars early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import unittest
except ImportError as baton:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from baton


_HAS_DOCS: bool = False
"""
This module optionally provides extra test cases for the docs.utils module, focusing on the
utils.sanitize_url method for url encoding.

	Bundling documentation is not supported by this project, however for users that accept the
	relevant terms and conditions of the optional docs module's dependencies, and have installed it,
	the following optional tests hopefully extend to testing some of the multicast documentation
	code.

	Otherwise this file is effectively omitted from testing.

	Disclaimer:
	For clarity this file (as python sourcecode) is Licensed under MIT (the "License");
	The resulting python tests (as software) are only provided "AS IS" and WITHOUT WARRANTIES OR
	CONDITIONS OF ANY KIND, either express or implied. The dependencies of the resulting
	python tests (as software), are NOT covered by the same Licensed. Assembly may be required.
"""


if not _HAS_DOCS:
	try:
		import docs.utils
		_HAS_DOCS = True
	except ImportError:  # pragma: no branch
		_HAS_DOCS = False


def onlyIfHasDocs(has_docs: bool) -> callable:
	"""
	Conditionally enable a test suite class based on the availability of the multicast docs library.

	If the provided flag is False, returns a dummy class with a placeholder method that does nothing,
	allowing tests dependent on docs to be safely bypassed. If the provided flag is True,
	the original class is returned unchanged.

	Arguments:
		has_docs (bool): Flag indicating whether the docs module is available.

	Returns:
		callable: A decorator function that returns either the original class or a dummy class
		with a placeholder method, depending on the has_docs flag.

	Meta-Testing:

		>>> @onlyIfHasDocs(has_docs=False)
		... class TestClass: pass
		>>> hasattr(TestClass(), 'method')
		True

	"""
	def decorator(cls: callable) -> callable:  # skipcq: PY-D0003 -- decorator ok
		if not has_docs:
			# Create an empty class with a method that returns None
			return type(cls.__name__, (object,), {
				'method': lambda self: None
			})
		return cls
	return decorator


@context.markWithMetaTag("extra", "security")
@onlyIfHasDocs(has_docs=_HAS_DOCS)
class ExtraDocsUtilsTestSuite(context.BasicUsageTestSuite):
	"""Test cases for docs.utils module."""

	__module__ = "tests.test_extra"

	URL_TEST_FIXTURES = [
		{
			"input_url": "https://github.com/user/repo",
			"expected": "https://github.com/user/repo",
		},
		{
			"input_url": "https://github.com/user/repo with spaces",
			"expected": "https://github.com/user/repo%20with%20spaces",
		},
		{
			"input_url": "https://github.com/user/repo?q=test&sort=desc",
			"expected": "https://github.com/user/repo?q=test&sort=desc",
		},
		{
			"input_url": "https://github.com/user/repo#section",
			"expected": "https://github.com/user/repo#section",
		},
		{
			"input_url": "https://github.com/user/repo/<script>alert('xss')</script>",
			"expected": "https://github.com/user/repo/%3Cscript%3Ealert%28%27xss%27%29%3C/script%3E",
		},
	]

	def test_sanitize_url_GIVEN_raw_url_IS_reliable(self) -> None:
		"""Test case 1: Test to ensure reliable URL sanitization."""
		# Mock _hearstep to return a non-empty response
		for test_params in self.URL_TEST_FIXTURES:
			sanitized_url = docs.utils.sanitize_url(test_params["input_url"])
			# check for results
			self.assertIsNotNone(sanitized_url)
			# Verify results
			if test_params["input_url"] == test_params["expected"]:
				self.assertEqual(
					test_params["input_url"], sanitized_url,
					"Input and output URLs were different, should be the same.",
				)
			else:
				self.assertNotEqual(
					test_params["input_url"], sanitized_url,
					"Input and output URLs were the same, should be different.",
				)
			self.assertEqual(sanitized_url, test_params["expected"])


if __name__ == '__main__':
	unittest.main()
