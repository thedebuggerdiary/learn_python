---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Functions & Lambdas
### Episode 3 — Python from Scratch
**The Debugger Diary**

---

# Defining Functions

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Alice"))   # Hello, Alice!
```

| Piece | What it does |
|---|---|
| `def` | Keyword to define a function |
| `name: str` | Parameter with type hint |
| `-> str` | Return type annotation |
| `return` | Returns a value to the caller |

---

# Default Parameters

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

print(greet("Alice"))             # Hello, Alice!
print(greet("Bob", "Hi"))         # Hi, Bob!
print(greet("Carol", greeting="Hey"))  # Hey, Carol!
```

Defaults must come after non-default parameters.
**Never use a mutable default** (list, dict) — use `None` instead.

---

# Keyword Arguments

```python
def create_user(
    name: str,
    age: int,
    active: bool = True,
) -> dict[str, object]:
    return {"name": name, "age": age, "active": active}

# Call with keyword args — order doesn't matter
user = create_user(age=30, name="Alice")
print(user)  # {'name': 'Alice', 'age': 30, 'active': True}
```

Keyword arguments make call sites self-documenting — no need to check the signature.

---

# `*args` — Variadic Positional Arguments

```python
def total(*numbers: int) -> int:
    return sum(numbers)

print(total(1, 2, 3))         # 6
print(total(10, 20, 30, 40))  # 100
```

`*args` collects all positional arguments into a **tuple**.

Unpack a sequence with `*`:
```python
values = [1, 2, 3]
print(total(*values))   # 6
```

---

# `**kwargs` — Variadic Keyword Arguments

```python
def log(message: str, **context: object) -> None:
    parts = ", ".join(f"{k}={v}" for k, v in context.items())
    print(f"{message} | {parts}")

log("User signed in", user_id=42, ip="192.168.1.1")
# User signed in | user_id=42, ip=192.168.1.1
```

`**kwargs` collects all keyword arguments into a **dict**.

Unpack a dict with `**`:
```python
data = {"user_id": 42, "ip": "192.168.1.1"}
log("Event", **data)
```

---

# Functions Are First-Class Objects

```python
def double(x: int) -> int:
    return x * 2

def apply(func, value: int) -> int:
    return func(value)

print(apply(double, 5))   # 10

# Store in a variable
operation = double
print(operation(7))       # 14

# Pass in a list
funcs = [double, abs, str]
print([f(42) for f in funcs])  # [84, 42, '42']
```

---

# Lambda — Anonymous Functions

```python
# Named function
def square(x: int) -> int:
    return x * x

# Equivalent lambda
square = lambda x: x * x

print(square(5))   # 25
```

`lambda params: expression` — single expression, no `return` keyword.

Best used **inline**, not assigned to a variable:
```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort(key=lambda x: -x)
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]
```

---

# Higher-Order Functions: map, filter

```python
numbers = [1, 2, 3, 4, 5, 6]

# map — apply a function to every element
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)   # [2, 4, 6, 8, 10, 12]

# filter — keep elements where function returns True
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)     # [2, 4, 6]
```

In practice, **list comprehensions** are preferred over `map`/`filter` in Python:
```python
doubled = [x * 2 for x in numbers]
evens   = [x for x in numbers if x % 2 == 0]
```

---

# functools.reduce

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

total   = reduce(lambda acc, x: acc + x, numbers)
product = reduce(lambda acc, x: acc * x, numbers)

print(total)    # 15
print(product)  # 120

# But sum() is clearer for this specific case
print(sum(numbers))  # 15
```

---

# Closures

```python
def make_multiplier(factor: int):
    def multiply(x: int) -> int:
        return x * factor   # captures `factor` from outer scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

The inner function **closes over** variables from the enclosing scope. This is the foundation of decorators.

---

# Decorators

```python
import time
from typing import Callable

def timer(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_add(a: int, b: int) -> int:
    time.sleep(0.1)
    return a + b

slow_add(3, 4)   # slow_add took 0.1002s
```

`@timer` is syntactic sugar for `slow_add = timer(slow_add)`.

---

# Key Takeaways

- `def name(param: Type) -> ReturnType:` — full function definition
- Default params: `def f(x, y=10)` — keyword args make call sites readable
- `*args` → tuple of positional args; `**kwargs` → dict of keyword args
- Functions are first-class — pass them, store them, return them
- `lambda params: expression` — anonymous single-expression function
- Use list comprehensions instead of `map`/`filter` in most cases
- Decorators — `@decorator` wraps a function with extra behaviour

---

# What's Next — Episode 4

**Classes, Dataclasses & Protocols**

- `class` — defining types with attributes and methods
- `__init__` and `self` — instance construction
- `@dataclass` — auto-generate `__init__`, `__repr__`, `__eq__`
- `@property` — computed attributes
- Dunder methods — `__str__`, `__len__`, `__add__`
- `Protocol` — structural typing (like Kotlin interfaces)
- Inheritance

**The Debugger Diary** — Python from Scratch
_"Understand the tools, not just the syntax."_
