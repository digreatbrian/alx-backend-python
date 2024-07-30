#!/usr/bin/env python3
"""Module for testing utility functions from utils.py."""

from parameterized import parameterized
import unittest
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize
import requests


class TestAccessNestedMap(unittest.TestCase):
    """Class for testing the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the correct value for given inputs.

        Args:
            nested_map (dict): The nested dictionary to traverse.
            path (tuple): The path of keys to follow in the nested dictionary.
            expected: The expected result from the nested map.

        Asserts:
            The returned value from access_nested_map is equal to expected.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        Test that a KeyError is raised for missing keys in the nested map.

        Args:
            nested_map (dict): The nested dictionary to traverse.
            path (tuple): The path of keys to follow in the nested dictionary.
            expected (str): The expected missing key.

        Asserts:
            A KeyError is raised and the exception message matches the expected key.
        """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(e.exception))

class TestGetJson(unittest.TestCase):
    """Class for testing the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns the expected result.

        Args:
            test_url (str): The URL to request.
            test_payload (dict): The expected JSON payload from the request.

        Asserts:
            The returned JSON from get_json is equal to test_payload.
        """
        config = {'return_value.json.return_value': test_payload}
        patcher = patch('requests.get', **config)
        mock = patcher.start()
        self.assertEqual(get_json(test_url), test_payload)
        mock.assert_called_once()
        patcher.stop()

class TestMemoize(unittest.TestCase):
    """Class for testing the memoize decorator."""

    def test_memoize(self):
        """
        Test that memoize caches the result of a method.

        Ensures that when a_property is called twice, the correct result
        is returned but a_method is only called once.
        """

        class TestClass:
            """Test class for demonstrating memoize functionality."""

            def a_method(self):
                """A method that returns a constant value."""
                return 42

            @memoize
            def a_property(self):
                """A property that calls a_method, memoized to cache the result."""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock.assert_called_once()
