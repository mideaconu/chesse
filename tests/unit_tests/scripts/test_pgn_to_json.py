from scripts import pgn_to_json


def test_is_int():
    assert pgn_to_json.is_int("3")


def test_is_int_fails():
    assert not pgn_to_json.is_int("three")


def test_is_float():
    assert pgn_to_json.is_float("3.2")


def test_is_float_fails():
    assert not pgn_to_json.is_float("three point two")
