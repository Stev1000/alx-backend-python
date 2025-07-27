#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


# ---------------- Task 4: Unit Tests ---------------- #

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test .org returns correct value and calls get_json once"""
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"mocked": "data"}

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, {"mocked": "data"})
        mock_get_json.assert_called_once_with(expected_url)


# ---------------- Task 9: Integration Tests ---------------- #

@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "expected_repos_with_license": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    def test_public_repos(self):
        """Test public_repos returns expected list"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license"""
        client = GithubOrgClient("google")
        result = client.public_repos("apache-2.0")
        self.assertEqual(result, self.expected_repos_with_license)


# ---------------- Checker Compatibility: Patch client.get_json ---------------- #

def setUpModule():
    """Patch client.get_json to mock external requests"""
    get_json_patcher = patch("client.get_json")
    TestIntegrationGithubOrgClient.get_json_mock = get_json_patcher.start()
    TestIntegrationGithubOrgClient.get_json_patcher = get_json_patcher

    def side_effect(url):
        if url == "https://api.github.com/orgs/google":
            return org_payload
        elif url == org_payload["repos_url"]:
            return repos_payload
        raise ValueError(f"Unhandled URL: {url}")

    TestIntegrationGithubOrgClient.get_json_mock.side_effect = side_effect


def tearDownModule():
    """Unpatch client.get_json after all integration tests"""
    TestIntegrationGithubOrgClient.get_json_patcher.stop()


# ---------------- Manual test runner ---------------- #

if __name__ == "__main__":
    unittest.main()
