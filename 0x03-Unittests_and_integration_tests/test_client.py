#!/usr/bin/env python3
"""Tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns expected URL"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        client = GithubOrgClient("test_org")
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test_org/repos")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_url, mock_get_json):
        """Test public_repos returns expected list"""
        mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "bsd-3-clause"}}
        ]
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with parameterized inputs"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "expected_repos_with_license": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return fixture data"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        org_mock = Mock()
        org_mock.json.return_value = cls.org_payload

        repos_mock = Mock()
        repos_mock.json.return_value = cls.repos_payload

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return org_mock
            elif url == cls.org_payload["repos_url"]:
                return repos_mock
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.expected_repos_with_license)


if __name__ == "__main__":
    unittest.main()
