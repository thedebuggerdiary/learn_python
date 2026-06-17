import time
import functools
from typing import Callable, TypeVar

T = TypeVar("T")


def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"


def total(*numbers: int) -> int:
    return sum(numbers)


def log(message: str, **context: object) -> None:
    parts = ", ".join(f"{k}={v}" for k, v in context.items())
    print(f"{message} | {parts}" if parts else message)


def make_multiplier(factor: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:
        return x * factor
    return multiply


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


@timer
def slow_add(a: int, b: int) -> int:
    time.sleep(0.05)
    return a + b


def pipeline(*steps: Callable) -> Callable:
    def apply(value):
        for step in steps:
            value = step(value)
        return value
    return apply


def main() -> None:
    # Default parameters
    print(greet("Alice"))
    print(greet("Bob", "Hi"))
    print(greet("Carol", greeting="Hey"))
    print()

    # *args
    print(total(1, 2, 3))
    values = [10, 20, 30]
    print(total(*values))
    print()

    # **kwargs
    log("User signed in", user_id=42, ip="192.168.1.1")
    print()

    # Higher-order functions
    numbers = [1, 2, 3, 4, 5, 6]
    doubled = [x * 2 for x in numbers]
    evens = [x for x in numbers if x % 2 == 0]
    print(f"doubled: {doubled}")
    print(f"evens:   {evens}")
    print()

    # Closures
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")
    print()

    # Decorator
    result = slow_add(3, 4)
    print(f"slow_add result: {result}")
    print()

    # Pipeline
    process = pipeline(
        str.strip,
        str.lower,
        lambda s: s.replace(" ", "_"),
    )
    print(process("  Hello World  "))
    print(process("  Python Tips  "))


if __name__ == "__main__":
    main()
