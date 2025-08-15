#!/usr/bin/env python3
"""A GitHub org client"""

from typing import List, Dict
from utils import get_json, access_nested_map


class GithubOrgClient:
    """A GitHub organization client"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        self._org_name = org_name

    @property
    def org(self) -> Dict:
        """Return the org data"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Return the repos URL from the org data"""
        return self.org["repos_url"]

    @property
    def repos_payload(self) -> Dict:
        """Return the repos payload"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Return public repo names, optionally filtered by license"""
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]
        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if a repo has the specified license"""
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
