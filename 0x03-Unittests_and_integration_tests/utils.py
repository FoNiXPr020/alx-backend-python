#!/usr/bin/env python3
"""
Unittest for utils module ( 0x03-Unittests_and_integration_tests )
"""
import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a nested map.

    Parameters
    ----------
    nested_map: Mapping
        The nested map to access
    path: Sequence
        The path to the value

    Returns
    -------
    Any
        The value at the specified path
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map


def get_json(url: str) -> Dict:
    """Get JSON from remote URL.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """
    Memoize fn

    Parameters
    ----------
    fn: Callable
        A function to memoize

    Returns
    -------
    Callable
        A memoized function
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        """"memoized wraps"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
