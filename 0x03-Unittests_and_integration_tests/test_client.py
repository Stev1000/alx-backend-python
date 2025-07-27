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
        result = client.org  # correct @property access

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
        try:
            result = client.public_repos()
            print("🔍 Got:", result)
            print("✅ Expected:", self.expected_repos)
            self.assertEqual(result, self.expected_repos)
        except Exception as e:
            print("❌ ERROR in test_public_repos:", e)
            raise

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license"""
        client = GithubOrgClient("google")
        try:
            result = client.public_repos("apache-2.0")
            print("🔍 Got (licensed):", result)
            print("✅ Expected (licensed):", self.expected_repos_with_license)
            self.assertEqual(result, self.expected_repos_with_license)
        except Exception as e:
            print("❌ ERROR in test_public_repos_with_license:", e)
            raise


# ---------------- requests.get Patch for Integration Tests ---------------- #

def setUpModule():
    """Patch requests.get before integration tests"""
    get_patcher = patch("requests.get")
    TestIntegrationGithubOrgClient.get_patcher = get_patcher
    TestIntegrationGithubOrgClient.mock_get = get_patcher.start()

    # Mocks
    mock_org_response = Mock()
    mock_org_response.json.return_value = org_payload

    mock_repos_response = Mock()
    mock_repos_response.json.return_value = repos_payload

    def side_effect(url):
        if url == "https://api.github.com/orgs/google":
            return mock_org_response
        elif url == org_payload["repos_url"]:
            return mock_repos_response
        raise ValueError(f"Unhandled URL: {url}")

    TestIntegrationGithubOrgClient.mock_get.side_effect = side_effect


def tearDownModule():
    """Unpatch requests.get after integration tests"""
    TestIntegrationGithubOrgClient.get_patcher.stop()


# ---------------- Manual runner ---------------- #

if __name__ == "__main__":
    unittest.main()
