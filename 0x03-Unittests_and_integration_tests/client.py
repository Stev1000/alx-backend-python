#!/usr/bin/env python3
"""GithubOrgClient module"""
from utils import get_json
import requests


class GithubOrgClient:
    """Client for GitHub organizations"""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Return org data"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
