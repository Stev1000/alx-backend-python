#!/usr/bin/env python3
"""GithubOrgClient definition"""

import requests


class GithubOrgClient:
    """Github Organization Client"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        """Initialize with organization name"""
        self.org_name = org_name

    def org(self):
        """Get the organization information"""
        url = self.ORG_URL.format(self.org_name)
        return requests.get(url).json()

    def _public_repos_url(self):
        """Extract public repos URL from the organization info"""
        return self.org().get("repos_url")

    def public_repos(self, license=None):
        """List public repositories, optionally filtered by license"""
        repos_url = self._public_repos_url()
        repos = requests.get(repos_url).json()

        if license:
            return [
                repo["name"]
                for repo in repos
                if repo.get("license", {}).get("key") == license
            ]

        return [repo["name"] for repo in repos]
