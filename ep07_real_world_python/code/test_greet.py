import pytest
from greet import greet, greet_loud, find_user, validate_name


def test_greet_basic() -> None:
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty_string() -> None:
    assert greet("") == "Hello, !"


@pytest.mark.parametrize("name,expected", [
    ("Alice", "Hello, Alice!"),
    ("Bob",   "Hello, Bob!"),
    ("Carol", "Hello, Carol!"),
])
def test_greet_parametrized(name: str, expected: str) -> None:
    assert greet(name) == expected


def test_greet_loud() -> None:
    assert greet_loud("alice") == "HELLO, ALICE!"


def test_greet_loud_preserves_upper() -> None:
    assert greet_loud("Alice") == "HELLO, ALICE!"


def test_validate_name_raises_on_empty() -> None:
    with pytest.raises(ValueError, match="Name cannot be empty"):
        validate_name("")


def test_validate_name_raises_on_too_long() -> None:
    with pytest.raises(ValueError, match="too long"):
        validate_name("A" * 101)


def test_validate_name_accepts_max_length() -> None:
    validate_name("A" * 100)  # should not raise


def test_find_user_existing() -> None:
    assert find_user(1) == "Alice"
    assert find_user(2) == "Bob"
    assert find_user(3) == "Carol"


def test_find_user_missing() -> None:
    assert find_user(99) is None
    assert find_user(0) is None
