from typing import Optional


def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob", 3: "Carol"}
    return users.get(user_id)


def describe(value: object) -> str:
    if isinstance(value, str):
        return f"String: '{value}' (length {len(value)})"
    if isinstance(value, bool):
        return f"Boolean: {value}"
    if isinstance(value, (int, float)):
        return f"Number: {value}"
    if isinstance(value, list):
        return f"List with {len(value)} items: {value}"
    return f"Unknown type: {type(value).__name__}"


def format_profile(user_id: int) -> str:
    name: str | None = find_user(user_id)
    display = name if name is not None else "Anonymous"
    return f"[ID {user_id}] {display}"


def main() -> None:
    # Built-in types
    name: str = "Debugger Diary"
    age: int = 3
    ratio: float = 3.14
    active: bool = True
    nothing: None = None

    print(f"name={name!r}, type={type(name).__name__}")
    print(f"age={age!r},  type={type(age).__name__}")
    print(f"ratio={ratio}, type={type(ratio).__name__}")
    print(f"active={active}, type={type(active).__name__}")
    print(f"nothing={nothing!r}, is None: {nothing is None}")
    print()

    # isinstance checks
    for val in ["hello", 42, 3.14, True, [1, 2, 3], None]:
        print(describe(val))
    print()

    # Optional pattern
    for uid in [1, 2, 99]:
        print(format_profile(uid))
    print()

    # String operations
    s = "Hello, World!"
    print(f"upper:   {s.upper()}")
    print(f"split:   {s.split(', ')}")
    print(f"slice:   {s[0:5]}")
    print(f"reverse: {s[::-1]}")


if __name__ == "__main__":
    main()
