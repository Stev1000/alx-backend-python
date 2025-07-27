#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


# ---------------- Task 4, 5, 6: Unit Tests ---------------- #

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

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns expected repos_url from org"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

        client = GithubOrgClient("test_org")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names and mocks properly"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake.url"
            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake.url")


# ---------------- Task 9: Integration Tests ---------------- #

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
        """Patch requests.get and configure side effects"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mock response for org
        mock_org_response = Mock()
        mock_org_response.json.return_value = cls.org_payload

        # Mock response for repos
        mock_repos_response = Mock()
        mock_repos_response.json.return_value = cls.repos_payload

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return mock_org_response
            elif url == cls.org_payload["repos_url"]:
                return mock_repos_response
            raise ValueError(f"Unhandled URL: {url}")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        print("🔍 Got:", result)
        print("✅ Expected:", self.expected_repos)
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license"""
        client = GithubOrgClient("google")
        result = client.public_repos("apache-2.0")
        print("🔍 Got (licensed):", result)
        print("✅ Expected (licensed):", self.expected_repos_with_license)
        self.assertEqual(result, self.expected_repos_with_license)


# ---------------- Manual runner ---------------- #

if __name__ == "__main__":
    unittest.main()
