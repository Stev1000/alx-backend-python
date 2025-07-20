#!/usr/bin/env python3
"""Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "expected_repos_with_license": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up a mock for requests.get before running tests"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mock response for org
        mock_org_response = Mock()
        mock_org_response.json.return_value = cls.org_payload

        # Mock response for repos
        mock_repos_response = Mock()
        mock_repos_response.json.return_value = cls.repos_payload

        def side_effect(url):
            """Custom response depending on the URL requested"""
            if url == "https://api.github.com/orgs/google":
                return mock_org_response
            if url == cls.org_payload["repos_url"]:
                return mock_repos_response
            raise ValueError(f"Unhandled URL: {url}")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patch after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns correct repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos filtered by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.expected_repos_with_license
        )
