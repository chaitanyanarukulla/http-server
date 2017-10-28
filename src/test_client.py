# -*- coding: utf-8 -*-
import pytest


def test_client_gets_message_back_from_server():
    """Send message to client and make sure it returns"""
    from client import client
    message = "Hello"
    assert client(message) == "400: Malformed-Request HTTP/1.1 500 OK\r\n"
