# -*- coding: utf-8 -*-
"""Test server for 200 OK response"""
import pytest


def test_response_200():
    """Test server responds with http 200."""
    from server import response_ok
    assert b'HTTP/1.1 200 OK\r\n' == response_ok()


def test_response_500():
    """Test server responds with http 500."""
    from server import response_error
    assert b'HTTP/1.1 500 OK\r\n' == response_error()
