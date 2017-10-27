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

test = [("GET http-server/src/server.py HOST: 127.0.0.1:5000 HTTP/1.1", )]


@pytest.mark.parametrize('parm,result', test)
def test_parse_request(parm, result):
    """Test server for parser function."""
    from server import parse_request
    assert parse_request(parm) == result
