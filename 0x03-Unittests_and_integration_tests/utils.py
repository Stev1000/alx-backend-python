#!/usr/bin/env python3
"""Generic utilities for ALX backend testing."""

import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Callable


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


def memoize(fn: Callable) -> Callable:
    """Decorator to cache method result as a property."""
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
