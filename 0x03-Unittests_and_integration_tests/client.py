#!/usr/bin/env python3
"""GithubOrgClient module"""

from utils import get_json


class GithubOrgClient:
    """Client for GitHub organizations"""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch organization data"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self):
        """Get the repos_url from org"""
        return self.org.get("repos_url")

    def public_repos(self, license=None):
        """Fetch and return public repository names, optionally filtered by license"""
        repos = get_json(self._public_repos_url)
        repo_names = [
            repo["name"]
            for repo in repos
            if license is None or self.has_license(repo, license)
        ]
        return repo_names

    @staticmethod
    def has_license(repo, license_key):
        """Check if repo has the given license"""
        return repo.get("license", {}).get("key") == license_key
