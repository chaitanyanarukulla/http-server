# -*- coding: utf-8 -*-
import pytest

def test_send_message():
    from client import client
    assert client("This is a test") == "This is a test"


def test_buff_short_message():
    from client import client
    assert len(client("anothe")) == 6


def test_buff_long_message():
    from client import client
    assert len(client("Caticus cuteicus throwup on")) == 27


def test_non_ascii_message():
    from client import client
    assert client("éclairs") == "éclairs"


def test_buffer_length_exact_multiple():
    from client import client
    assert len(client("This is 8 awesum")) % 8 == 0