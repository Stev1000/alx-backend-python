#!/usr/bin/env python3
"""Unit tests for access_nested_map in utils.py"""

import unittest
from parameterized import parameterized

# ✅ Fix import error by adding current directory to sys.path
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils import access_nested_map  # Now works correctly


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct return values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
