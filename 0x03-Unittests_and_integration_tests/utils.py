#!/usr/bin/env python3
"""Generic utilities for ALX backend testing."""

import requests
from typing import Mapping, Sequence, Any


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested dictionary values by following keys in path."""
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> dict:
    """GET request to fetch and return JSON from a URL."""
    response = requests.get(url)
    return response.json()
