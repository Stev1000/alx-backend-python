#!/usr/bin/env python3
"""
Unit and Integration tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

# -------------------------------
# ✅ Task 4: Unit Test for .org
# -------------------------------

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"mocked": "data"}

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, {"mocked": "data"})
        mock_get_json.assert_called_once_with(expected_url)

# --------------------------------------
# ✅ Task 9: Integration Test for public_repos
# --------------------------------------

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
        """Patch requests.get before all tests"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mocked org response
        mock_org_response = Mock()
        mock_org_response.json.return_value = cls.org_payload

        # Mocked repos response
        mock_repos_response = Mock()
        mock_repos_response.json.return_value = cls.repos_payload

        def side_effect(url):
            if url == f"https://api.github.com/orgs/google":
                return mock_org_response
            elif url == cls.org_payload["repos_url"]:
                return mock_repos_response
            raise ValueError(f"Unhandled URL: {url}")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patch after tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected list"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.expected_repos_with_license
        )
