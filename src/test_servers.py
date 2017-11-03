# -*- coding: utf-8 -*-
"""Test the server."""
import pytest


def test_send_message():
    """Test message is returned to client when sent from client."""
    from client import client
    assert client("This is a test") == "This is a test"


def test_buff_short_message():
    """Test message is echoed when message is under 8 bytes."""
    from client import client
    assert len(client("anothe")) == 6


def test_buff_long_message():
    """Test message longer than 8 bytes is echoed."""
    from client import client
    assert len(client("Caticus cuteicus throwup on")) == 27


def test_buffer_length_exact_multiple():
    """Test message echoed when exactly 8 bytes."""
    from client import client
    assert len(client("This is 8 awesum")) % 8 == 0
