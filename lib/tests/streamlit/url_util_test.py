# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from typing import Any

from parameterized import parameterized

from streamlit import url_util

GITHUB_URLS = [
    (
        "https://github.com/aritropaul/streamlit/blob/b72adbcf00c91775db14e739e2ea33d6df9079c3/lib/streamlit/cli.py",
        "https://github.com/aritropaul/streamlit/raw/b72adbcf00c91775db14e739e2ea33d6df9079c3/lib/streamlit/cli.py",
    ),
    (
        "https://github.com/streamlit/streamlit/blob/develop/examples/video.py",
        "https://github.com/streamlit/streamlit/raw/develop/examples/video.py",
    ),
    (
        "https://github.com/text2gene/text2gene/blob/master/sbin/clinvar.hgvs_citations.sql",
        "https://github.com/text2gene/text2gene/raw/master/sbin/clinvar.hgvs_citations.sql",
    ),
    (
        "https://github.com/mekarpeles/math.mx/blob/master/README.md",
        "https://github.com/mekarpeles/math.mx/raw/master/README.md",
    ),
]

GIST_URLS = [
    (
        "https://gist.github.com/nthmost/b521b80fbd834e67b3f5e271e9548232",
        "https://gist.github.com/nthmost/b521b80fbd834e67b3f5e271e9548232/raw",
    ),
    (
        "https://gist.github.com/scottyallen/1888e058261fc21f184f6be192bbe131",
        "https://gist.github.com/scottyallen/1888e058261fc21f184f6be192bbe131/raw",
    ),
    (
        "https://gist.github.com/tvst/faf057abbedaccaa70b48216a1866cdd",
        "https://gist.github.com/tvst/faf057abbedaccaa70b48216a1866cdd/raw",
    ),
]

INVALID_URLS = [
    "blah",
    "google.com",
    "http://homestarrunner.com",
    "https://somethinglikegithub.com/withablob",
    "gist.github.com/nothing",
    "https://raw.githubusercontent.com/streamlit/streamlit/develop/examples/video.py",
    "streamlit.io/raw/blob",
]


class GitHubUrlTest(unittest.TestCase):
    def test_github_url_is_replaced(self):
        for target, processed in GITHUB_URLS:
            assert url_util.process_gitblob_url(target) == processed

    def test_gist_url_is_replaced(self):
        for target, processed in GIST_URLS:
            assert url_util.process_gitblob_url(target) == processed

    def test_nonmatching_url_is_not_replaced(self):
        for url in INVALID_URLS:
            assert url == url_util.process_gitblob_url(url)


class UrlUtilTest(unittest.TestCase):

    @parameterized.expand(
        [
            # Valid URLs:
            ("http://www.cwi.nl:80/%7Eguido/Python.html", True),
            ("https://stackoverflow.com", True),
            ("mailto:test@example.com", True),
            ("data:image/svg+xml;base64,PHN2ZyB4aHcvMjAwMC9zdmci", True),
            ("data:application/pdf;base64,PHN2ZyB4aHcvMjAwMC9zdmci", True),
            ("http://127.0.0.1", True),  # IP as domain
            ("https://[::1]", True),  # IPv6 address in URL
            # Invalid URLs:
            ("/data/Python.html", False),
            (532, False),
            ("dkakasdkjdjakdjadjfalskdjfalk", False),
            ("mailto:", False),
            ("ftp://example.com/resource", False),  # Unsupported scheme
            ("https:///path/to/resource", False),  # Missing netloc
            ("mailto:invalid_email", False),  # Invalid email format
            ("data:text/plain;base64,", False),  # Valid scheme but missing data
            ("http://example.com/illegal<chars", False),  # URL with illegal characters
        ]
    )
    def test_is_url(self, url: Any, expected_value: bool):
        """Test the is_url utility function."""
        self.assertEqual(
            url_util.is_url(url, ("http", "https", "data", "mailto")), expected_value
        )
