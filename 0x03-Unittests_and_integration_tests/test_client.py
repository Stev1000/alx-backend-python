#!/usr/bin/env python3
"""Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Create mock response objects for each URL
        # These mocks will be returned by requests.get
        mock_org_response = Mock()
        # mock_org_response.json() returns cls.org_payload
        mock_org_response.json.return_value = cls.org_payload

        mock_repos_response = Mock()
        # mock_repos_response.json() returns cls.repos_payload
        mock_repos_response.json.return_value = cls.repos_payload

        def side_effect(url):
            """
            Custom side effect function for requests.get.
            Returns the appropriate mock response based on the URL.
            """
            if url == "https://api.github.com/orgs/google":
                return mock_org_response
            # This URL comes from org_payload["repos_url"]
            if url == cls.org_payload["repos_url"]:
                return mock_repos_response
            # If an unexpected URL is requested, raise an error for debugging
            raise ValueError(f"Unhandled URL: {url}")

        # Assign the custom side_effect function to the mock requests.get
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public repos from client"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public repos filtered by apache-2.0"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
