from utils import numeric


def test_is_int():
    assert numeric.is_int("3")


def test_is_not_int():
    assert not numeric.is_int("three")


def test_is_float():
    assert numeric.is_float("3.2")


def test_is_not_float():
    assert not numeric.is_float("three point two")
