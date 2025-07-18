#!/usr/bin/env python3
"""Client module for interacting with GitHub API."""

import requests
from functools import lru_cache
from typing import List, Dict


def get_json(url: str) -> Dict:
    """GET JSON content from a URL."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """GitHub Organization Client"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize with org name"""
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """Get organization info"""
        url = self.ORG_URL.format(self.org_name)
        return get_json(url)

    @property
    def _public_repos_url(self) -> str:
        """Return public repositories URL from org payload"""
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """Return list of public repo names. Filter by license if provided."""
        repos = get_json(self._public_repos_url)
        repo_names = []

        for repo in repos:
            if license is None or self.has_license(repo, license):
                repo_names.append(repo["name"])

        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repository has the given license key"""
        return repo.get("license", {}).get("key") == license_key
