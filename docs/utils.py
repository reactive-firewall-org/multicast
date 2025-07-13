# -*- coding: utf-8 -*-

# Multicast Documentation Utilities
# ..................................
# Copyright (c) 2024-2025, Mr. Walls
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

import re
import unicodedata
from urllib.parse import ParseResult, urlparse, urlunparse, quote


# Git reference validation pattern
# Enforces:
# - Must start with alphanumeric character
# - Can contain alphanumeric characters, underscore, hyphen, forward slash, and dot
GIT_REF_PATTERN: str = r'^[a-zA-Z0-9][a-zA-Z0-9_\-./]*$'


# URL allowed scheme list
# Enforces:
# - URLs Must start with https
URL_ALLOWED_SCHEMES: frozenset = frozenset({"https"})


# URL allowed domain list
# Enforces:
# - URLs Must belong to one of these domains
URL_ALLOWED_NETLOCS: frozenset = frozenset({
	"github.com", "gist.github.com", "readthedocs.com", "docs.python.org", "peps.python.org",
})


# Maximum allowed URL length
MAX_URL_LENGTH: int = 2048  # Common browser limit
"""Maximum allowed length for URL validation.

Should be large enough for most URLs but no larger than common browser limits.

Unit-Testing:

	First set up test fixtures by importing utils.

		>>> import docs.utils as _utils
		>>>

		>>> _utils.MAX_URL_LENGTH is not None
		True
		>>> type(_utils.MAX_URL_LENGTH) is type(int())
		True
		>>> _utils.MAX_URL_LENGTH > 0
		True
		>>> _utils.MAX_URL_LENGTH >= 256
		True
		>>> _utils.MAX_URL_LENGTH <= 2048
		True
		>>>

"""


# Error messages for URL validation
INVALID_LENGTH_ERROR: str = f"URL exceeds maximum length of {MAX_URL_LENGTH} characters."
"""Length error message for URL validation.

Unit-Testing:

	First set up test fixtures by importing utils.

		>>> import docs.utils as _utils
		>>>

		>>> _utils.INVALID_LENGTH_ERROR is not None
		True
		>>> type(_utils.INVALID_LENGTH_ERROR) is type(str())
		True
		>>> len(_utils.INVALID_LENGTH_ERROR) > 0
		True
		>>>

"""


INVALID_SCHEME_ERROR: str = "Invalid URL scheme. Only 'https' is allowed."
"""Scheme error message for URL validation.

Unit-Testing:

	First set up test fixtures by importing utils.

		>>> import docs.utils as _utils
		>>>

		>>> _utils.INVALID_SCHEME_ERROR is not None
		True
		>>> type(_utils.INVALID_SCHEME_ERROR) is type(str())
		True
		>>> len(_utils.INVALID_SCHEME_ERROR) > 0
		True
		>>>

"""


INVALID_DOMAIN_ERROR: str = f"Invalid or untrusted domain. Only {URL_ALLOWED_NETLOCS} are allowed."
"""Domain error message for URL validation.

Unit-Testing:

	First set up test fixtures by importing utils.

		>>> import docs.utils as _utils
		>>>

		>>> _utils.INVALID_DOMAIN_ERROR is not None
		True
		>>> type(_utils.INVALID_DOMAIN_ERROR) is type(str())
		True
		>>> len(_utils.INVALID_DOMAIN_ERROR) > 0
		True
		>>>

"""


def _validate_git_ref(ref: str) -> str:
	"""
	Validate if the provided string is a valid Git reference.

	Git reference naming rules:
		- Must start with an alphanumeric character
		- Can contain alphanumeric characters, underscore, hyphen, forward slash, and dot
		- Cannot contain consecutive dots (..)
	Args:
		ref (str) -- The Git reference to validate.

	Returns:
		str -- The validated Git reference.

	Raises:
		ValueError -- If the reference contains invalid characters.

	Meta-Testing:

		Testcase 1: Valid reference.

			>>> _validate_git_ref('main')
			'main'

		Testcase 2: Valid reference with special characters.

			>>> _validate_git_ref('feature/new-feature')
			'feature/new-feature'

		Testcase 3: Invalid reference with disallowed characters.

			>>> _validate_git_ref('invalid$ref')  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			...
			ValueError: Invalid Git reference: invalid$ref

		Testcase 4: Empty reference.

			>>> _validate_git_ref('')  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			...
			ValueError: Invalid Git reference:...

		Testcase 5: Invalid reference with disallowed dot-dot characters.

			>>> _validate_git_ref('invalid..ref')  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			...
			ValueError: Invalid Git reference: invalid..ref
	"""
	if not re.match(GIT_REF_PATTERN, ref) or ".." in ref:
		raise ValueError(f"Invalid Git reference: {ref}")
	return ref


def slugify_header(s: str) -> str:
	"""
	Convert header text to a URL-friendly slug.

	This function transforms header text into a URL-friendly slug by removing special characters,
	converting to lowercase, and replacing consecutive spaces or dashes with a single dash.
	The resulting slug is suitable for use in header anchors and URL paths.

	Arguments:
		s (str) -- The header text to be converted into a slug.

	Returns:
		str -- A URL-friendly slug derived from the input text.

	Unit-Testing:

		Testcase 1: Basic header with spaces and special characters.

			>>> slugify_header("Hello, World!")
			'hello-world'

		Testcase 2: Header with multiple spaces and mixed case.

			>>> slugify_header("  API   Documentation  ")
			'api-documentation'

		Testcase 3: Header with consecutive spaces and dashes.

			>>> slugify_header("API -- Documentation")
			'api-documentation'

		Testcase 4: Header with Unicode characters and accents.

			>>> slugify_header("über café 123")
			'über-café-123'

		Testcase 5: Header with special markdown characters.

			>>> slugify_header("[CEP-7] Documentation *Guide*")
			'cep-7-documentation-guide'
	"""
	# First Normalize Unicode characters to prevent homograph attacks
	text: str = unicodedata.normalize('NFKC', s)  # added in v2.0.9a6
	# Then, remove special characters and convert to lowercase
	text = re.sub(r'[^\w\- ]', "", text).strip().lower()
	# Then replace consecutive spaces or dashes with a single dash
	return re.sub(r'[-\s]+', "-", text)


def sanitize_url(url: str) -> str:
	"""
	Sanitize and validate a URL according to allowed schemes and domains.

	This function validates that the URL uses an allowed scheme (https) and points
	to a trusted domain, then safely encodes its path and query components.

	Args:
		url (str) -- The URL to sanitize.

	Returns:
		str -- The sanitized URL.

	Raises:
		ValueError -- If the URL has an invalid scheme or points to an untrusted domain.


	Unit-Testing:

		Testcase 0: First set up test fixtures by importing utils.

		>>> import docs.utils as _utils
		>>>

		Testcase 1: Basic URL with spaces and special characters.

		>>> url_fxtr = "https://github.com/user/Hello World!"
		>>> _utils.sanitize_url(url_fxtr)
		'https://github.com/user/Hello%20World%21'
		>>>

	"""
	# Validate length
	if len(url) > MAX_URL_LENGTH:
		raise ValueError(INVALID_LENGTH_ERROR)
	parsed_url: ParseResult = urlparse(url)
	# Validate scheme
	if parsed_url.scheme not in URL_ALLOWED_SCHEMES:
		raise ValueError(INVALID_SCHEME_ERROR)
	# Validate netloc
	if parsed_url.netloc not in URL_ALLOWED_NETLOCS:
		raise ValueError(INVALID_DOMAIN_ERROR)
	# Normalize netloc to prevent homograph attacks
	sanitized_netloc: str = unicodedata.normalize('NFKC', parsed_url.netloc)  # added in v2.0.9a6
	# Sanitize path and query - using the safe parameter to preserve URL structure
	sanitized_path: str = quote(unicodedata.normalize('NFKC', parsed_url.path), safe="/=")
	sanitized_query: str = quote(parsed_url.query, safe="&=")
	# Reconstruct the sanitized URL
	return urlunparse((
		parsed_url.scheme,
		sanitized_netloc,
		sanitized_path,
		parsed_url.params,
		sanitized_query,
		parsed_url.fragment,
	))


def sanitize_intersphinx_mapping(mapping: dict) -> dict:
	"""
	Sanitize URLs in an intersphinx mapping dictionary.

	This function applies URL sanitization to each URL in the mapping while
	preserving the associated extra values.

	Args:
		mapping (dict) -- A dictionary mapping names to tuples of (url, extra_value).

	Returns:
		dict -- A dictionary with the same structure but with sanitized URLs.

	Unit-Testing:

		Testcase 1: Basic intersphinx mapping.

		>>> mapping = {'python': ('https://docs.python.org/3', None)}
		>>> sanitize_intersphinx_mapping(mapping)
		{'python': ('https://docs.python.org/3', None)}

		Testcase 2: Mapping with URL containing special characters.

		>>> mapping = {'project': ('https://github.com/user/project with spaces', None)}
		>>> result = sanitize_intersphinx_mapping(mapping)
		>>> result['project'][0]
		'https://github.com/user/project%20with%20spaces'
		>>>

	"""
	return {key: (sanitize_url(url), extra_value) for key, (url, extra_value) in mapping.items()}
