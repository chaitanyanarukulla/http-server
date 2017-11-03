# -*- coding: utf-8 -*-
"""Test server for 200 OK response."""
import pytest


def test_response_200():
    """Test server responds with http 200."""
    from server import response_ok
    assert b'HTTP/1.1 200 OK\r\n' == response_ok()


def test_response_500():
    """Test server responds with http 500."""
    from server import response_error
    assert b'HTTP/1.1 500 OK\r\n' == response_error()


def test_buffer_of_length_8():
    """Send message of exactly 8 bytes."""
    from client import client
    assert client('message!') == 'HTTP/1.1 200 OK\r\n'


def test_buffer_of_length_greater_than_8_bytes():
    """Send message of exactly 8 bytes."""
    from client import client
    assert client('This is a longer message') == 'HTTP/1.1 200 OK\r\n'


def test_buffer_of_length_8_that_ends_with_space():
    """Send message of 8 bytes that ends with space."""
    from client import client
    assert client('message ') == 'HTTP/1.1 200 OK\r\n'


def test_buffer_of_length_8_that_starts_with_space():
    """Send message of 8 bytes that starts with space."""
    from client import client
    assert client(' message') == 'HTTP/1.1 200 OK\r\n'


def test_long_string_with_spaces():
    """Send message of 8 bytes that starts with space."""
    from client import client
    assert client("""message
    that is really long and will also span multiple lines.
    The next line is actually all space

    And this is the last line.""") == 'HTTP/1.1 200 OK\r\n'


NON_ASCII = [
    ('test&', u'test&'),
    ('bob!', u'bob!'),
    (' fred @', u' fred @')]


@pytest.mark.parametrize('val, result', NON_ASCII)
def test_non_ascii_characters(val, result):
    """Test non ascii characters echo."""
    from client import client
    assert client(val) == 'HTTP/1.1 200 OK\r\n'
