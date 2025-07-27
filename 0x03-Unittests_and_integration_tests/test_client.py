#!/usr/bin/env python3
"""Tests for GithubOrgClient"""

import sys
import os
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos
)

sys.path.append(os.path.dirname(__file__))


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        """Test .org"""
        mock_get.return_value = {"mocked": "data"}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"mocked": "data"})
        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url"""
        mock_org.return_value = {
            "repos_url":
                "https://api.github.com/orgs/test_org/repos"
        }
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/test_org/repos"
        )

    @patch("client.get_json")
    @patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=PropertyMock
    )
    def test_public_repos(self, mock_url, mock_get_json):
        """Test public_repos"""
        mock_url.return_value = (
            "https://api.github.com/orgs/test_org/repos"
        )
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "bsd-3-clause"}}
        ]
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        expected = ["repo1", "repo2"]

        self.assertEqual(result, expected)
        mock_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test_org/repos"
        )


@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "expected_repos_with_license": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests"""

    @classmethod
    def setUpClass(cls):
        """Start mock"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        mock_org = Mock()
        mock_org.json.return_value = cls.org_payload

        mock_repos = Mock()
        mock_repos.json.return_value = cls.repos_payload

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return mock_org
            if url == cls.org_payload["repos_url"]:
                return mock_repos
            raise ValueError(f"Unhandled URL: {url}")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop mock"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test repos"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self):
        """Test by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.expected_repos_with_license
        )


if __name__ == "__main__":
    unittest.main()
