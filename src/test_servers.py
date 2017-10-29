# -*- coding: utf-8 -*-
"""Test server"""
import pytest


# def test_response_200():
    # """Test server responds with http 200 and URI."""
    # from server import response_ok
    # URI = b'http-server/src/server.py'
    # URI2 = 'http-server/src/server.py'
    # assert URI + b' HTTP/1.1 200 OK\r\n' == response_ok(URI2)


def test_response_error():
    """Test server responds with http 500 response"""
    from server import response_error
    err = b"405 error: only GET method accepted"
    assert err + b' HTTP/1.1 500 OK\r\n' == response_error(err)


def test_parse_function_raises_value_error_with_405():
    """Read function name"""
    from server import parse_request
    with pytest.raises(ValueError,
                       match='405 error: only GET method accepted'):
        parse_request('potato')


def test_parse_function_raises_value_error_with_505():
    """Read function name"""
    from server import parse_request
    with pytest.raises(ValueError,
                       match='505 error: HTTP Request is not version 1.1'):
        parse_request('GET potato')


def test_parse_function_raises_value_error_with_400_bad_request():
    """Read function name"""
    from server import parse_request
    with pytest.raises(ValueError, match='400 error: Bad Request'):
        parse_request('GET HTTP/1.1 potato')


def test_parse_function_raises_value_error_with_400_malformed_request():
    """Read function name"""
    from server import parse_request
    with pytest.raises(ValueError, match='400: Malformed-Request'):
        parse_request('GET HTTP/1.1 Host: 127.0.0.1:5000 potato')


# def test_parse_function_returns_URI():
    # """Check function raises no errors and returns URI"""
    # from server import parse_request
    # header = "GET /http-server/src/server.py HTTP/1.1 200\r\n" \
             # "Host: 127.0.0.1:5000\r\n"
    # assert parse_request(header) == "/http-server/src/server.py"
