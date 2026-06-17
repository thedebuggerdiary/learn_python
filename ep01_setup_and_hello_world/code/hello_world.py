import sys


def greet(name: str) -> None:
    print(f"Hello, {name}!")
    print(f"Name has {len(name)} characters")
    print(f"Uppercase: {name.upper()}")


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    greet(name)

    # f-string format specifiers
    pi = 3.14159265
    print(f"Pi to 2 decimal places: {pi:.2f}")
    print(f"Big number: {1_000_000:,}")

    # Sneak peek at Episode 5
    squares = [x * x for x in range(1, 6)]
    print(f"Squares 1–5: {squares}")


if __name__ == "__main__":
    main()
