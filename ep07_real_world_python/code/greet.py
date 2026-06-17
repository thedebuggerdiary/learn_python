MAX_NAME_LENGTH = 100

_USERS: dict[int, str] = {
    1: "Alice",
    2: "Bob",
    3: "Carol",
}


def validate_name(name: str) -> None:
    if not name:
        raise ValueError("Name cannot be empty")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Name is too long (max {MAX_NAME_LENGTH} chars)")


def greet(name: str) -> str:
    return f"Hello, {name}!"


def greet_loud(name: str) -> str:
    validate_name(name)
    return f"HELLO, {name.upper()}!"


def find_user(user_id: int) -> str | None:
    return _USERS.get(user_id)


if __name__ == "__main__":
    print(greet("World"))
    print(greet_loud("alice"))
    print(find_user(1))
    print(find_user(99))
