#!/usr/bin/env python3
"""Fixtures for integration tests"""

org_payload = {
    "login": "google",
    "id": 1342004,
    "url": "https://api.github.com/orgs/google",
    "repos_url": "https://api.github.com/orgs/google/repos",
    "description": "Google organization"
}

repos_payload = [
    {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "repo2", "license": {"key": "other"}}
]

expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1"]

__all__ = [
    "org_payload",
    "repos_payload",
    "expected_repos",
    "apache2_repos"
]
