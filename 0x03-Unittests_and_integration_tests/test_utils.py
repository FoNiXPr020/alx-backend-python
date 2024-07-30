#!/usr/bin/env python3
"""
Unittest for utils module ( 0x03-Unittests_and_integration_tests )
"""

import unittest
import requests
from unittest import mock
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """  Test the access of a nested map. """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),

    ])
    def test_access_nested_map(self, dict, path, expected):
        """ test that access_nested_map returns the expected result. """
        result = access_nested_map(dict, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",), KeyError, 'a'),
        ({"a": 1}, ("a", "b"), KeyError, 'b')
    ])
    def test_access_nested_map_exception(
            self, dict, path, expected, expected_key):
        with self.assertRaises(expected):
            access_nested_map(dict, path)


class TestGetJson(unittest.TestCase):
    """  test that utils.get_json returns the expected result. """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @mock.patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """ test that utils.get_json returns the expected result. """
        mock_get.value.json.value = test_payload
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """ test that utils.memoize returns the expected result. """

    def test_memoize(self):
        """ test that utils.memoize returns the expected result. """

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', value=42) as mock_method:
            inst = TestClass()
            inst.a_property
            inst.a_property

            mock_method.assert_called_once()
