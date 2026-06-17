# Episode 3 — Functions & Lambdas

**Series:** Python from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episodes 1–2

---

## Episode Overview

Functions in Python are first-class objects — they can be passed as arguments, returned from other functions, stored in variables, and put in data structures. This episode covers everything from basic `def` syntax through default parameters, `*args`/`**kwargs`, lambdas, higher-order functions, closures, and decorators.

---

## Section 1: Defining Functions

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Alice"))   # Hello, Alice!
```

**`def`** declares a function. The body is indented (4 spaces by convention). The function ends when the indentation returns to the previous level.

**Return type:** `-> str` annotates what the function returns. Omitting it means the return type is `Any` as far as mypy is concerned — annotate everything.

**`return`** ends execution and hands the value back to the caller. A function that reaches the end without a `return` statement implicitly returns `None`.

```python
def log(message: str) -> None:
    print(f"[LOG] {message}")
```

`-> None` is the correct annotation for functions that produce side effects but return nothing meaningful.

---

## Section 2: Default Parameters

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

greet("Alice")                    # Hello, Alice!
greet("Bob", "Hi")                # Hi, Bob!
greet("Carol", greeting="Hey")    # Hey, Carol!
```

Parameters with defaults must come after parameters without defaults.

**The mutable default trap:**
```python
# WRONG — this list is shared across all calls
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

add_item("a")   # ['a']
add_item("b")   # ['a', 'b'] — bug! reuses the same list

# CORRECT — use None as sentinel
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

Default parameter values are evaluated **once** when the function is defined, not each time the function is called. For mutable objects (list, dict, set), always default to `None` and create a fresh instance inside the function body.

---

## Section 3: Keyword Arguments

Any parameter can be passed by name regardless of position:

```python
def create_user(name: str, age: int, active: bool = True) -> dict[str, object]:
    return {"name": name, "age": age, "active": active}

create_user("Alice", 30)              # positional
create_user(age=30, name="Alice")     # keyword — order irrelevant
create_user("Bob", 25, active=False)  # mixed
```

**Force keyword-only arguments** with a bare `*`:
```python
def send_email(to: str, *, subject: str, body: str) -> None:
    ...

send_email("alice@example.com", subject="Hi", body="Hello!")
send_email("alice@example.com", "Hi", "Hello!")   # TypeError
```

Everything after `*` must be passed by keyword. This prevents confusing positional-only call sites.

**Force positional-only arguments** with `/` (Python 3.8+):
```python
def distance(x: float, y: float, /) -> float:
    return (x ** 2 + y ** 2) ** 0.5

distance(3, 4)           # OK
distance(x=3, y=4)       # TypeError
```

---

## Section 4: *args and **kwargs

### *args — variadic positional arguments

```python
def total(*numbers: int) -> int:
    print(type(numbers))   # <class 'tuple'>
    return sum(numbers)

total(1, 2, 3)         # 6
total(10, 20, 30, 40)  # 100
```

`*args` collects all positional arguments into a tuple. The name `args` is a convention — the `*` is what matters.

Unpack a list/tuple into positional arguments with `*`:
```python
values = [1, 2, 3, 4, 5]
print(total(*values))   # 15
```

### **kwargs — variadic keyword arguments

```python
def log(message: str, **context: object) -> None:
    print(type(context))   # <class 'dict'>
    parts = ", ".join(f"{k}={v}" for k, v in context.items())
    print(f"{message} | {parts}" if parts else message)

log("User signed in", user_id=42, ip="192.168.1.1")
# User signed in | user_id=42, ip=192.168.1.1
```

Unpack a dict into keyword arguments with `**`:
```python
data = {"user_id": 42, "ip": "192.168.1.1"}
log("Event", **data)
```

### Full signature order

Parameters must appear in this order: `positional`, `*args`, `keyword-only`, `**kwargs`:

```python
def full(a, b, *args, kw1, kw2="default", **kwargs):
    pass
```

---

## Section 5: Functions as First-Class Objects

Python functions are objects — they can be passed anywhere an object can:

```python
def double(x: int) -> int:
    return x * 2

def apply(func, value: int) -> int:
    return func(value)

print(apply(double, 5))        # 10
print(apply(abs, -7))          # 7
print(apply(str, 42))          # '42'

# Store in a list
pipeline = [str.strip, str.lower, str.title]
text = "  hello world  "
for step in pipeline:
    text = step(text)
print(text)  # "Hello World"
```

The `Callable` type from `typing` annotates function parameters:
```python
from typing import Callable

def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)
```

`Callable[[ArgType1, ArgType2], ReturnType]` describes the signature.

---

## Section 6: Lambda

`lambda` creates an anonymous single-expression function:

```python
square = lambda x: x * x
square(5)   # 25
```

Lambdas are best used inline — assigning one to a variable is a code smell (use `def` instead):

```python
# Good — inline sorting key
names = ["Charlie", "Alice", "Bob"]
names.sort(key=lambda n: n.lower())

# Good — inline in sorted()
sorted_names = sorted(names, key=lambda n: len(n))

# Less clear — assign to variable
square = lambda x: x * x  # use def square(x): return x * x
```

Lambdas cannot contain statements (only expressions) — no `if/else` blocks, no `for`, no `return`. For anything more complex, use `def`.

Conditional expression (ternary) inside a lambda:
```python
classify = lambda x: "even" if x % 2 == 0 else "odd"
print(classify(4))   # even
print(classify(7))   # odd
```

---

## Section 7: Higher-Order Functions

### map and filter

```python
numbers = [1, 2, 3, 4, 5, 6]

# map — lazily applies a function to every element
doubled = list(map(lambda x: x * 2, numbers))
# [2, 4, 6, 8, 10, 12]

# filter — lazily keeps elements where function is truthy
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6]
```

`map` and `filter` return **lazy iterators** — wrap them in `list()` to materialise. In practice, list comprehensions are more idiomatic in Python:

```python
doubled = [x * 2 for x in numbers]
evens   = [x for x in numbers if x % 2 == 0]
```

### functools

```python
from functools import reduce, partial

# reduce — fold a sequence to a single value
product = reduce(lambda acc, x: acc * x, [1, 2, 3, 4, 5])
# 120

# partial — fix some arguments of a function
def power(base: int, exp: int) -> int:
    return base ** exp

square = partial(power, exp=2)
cube   = partial(power, exp=3)

print(square(5))   # 25
print(cube(3))     # 27
```

---

## Section 8: Closures

A closure is a function that captures variables from its enclosing scope:

```python
def make_multiplier(factor: int):
    def multiply(x: int) -> int:
        return x * factor   # `factor` is captured from the outer call
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

Each call to `make_multiplier` creates a fresh closure with its own copy of `factor`. Closures are the mechanism behind decorators.

---

## Section 9: Decorators

A decorator is a function that wraps another function, adding behaviour before and/or after:

```python
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def timer(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
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

print(slow_add(3, 4))
# slow_add took 0.1002s
# 7
```

`@timer` is exactly `slow_add = timer(slow_add)`. The `@` syntax is just sugar.

**functools.wraps** — preserve the wrapped function's name and docstring:
```python
import functools

def timer(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        ...
    return wrapper
```

Without `@functools.wraps`, `slow_add.__name__` would be `"wrapper"` instead of `"slow_add"`.

---

## Demo: Custom Filter/Transform Pipeline

```python
from typing import Callable, TypeVar

T = TypeVar("T")

def pipeline(*steps: Callable) -> Callable:
    def apply(value):
        for step in steps:
            value = step(value)
        return value
    return apply

process = pipeline(
    str.strip,
    str.lower,
    lambda s: s.replace(" ", "_"),
)

print(process("  Hello World  "))   # hello_world
print(process("  Python Tips  "))   # python_tips
```

---

## Key Takeaways

- `def name(param: Type) -> ReturnType:` — the complete function definition
- Never use mutable defaults; use `None` and create inside the body
- `*args` → tuple; `**kwargs` → dict — collect variadic arguments
- Functions are objects — store, pass, return them
- `lambda params: expr` — anonymous single-expression function; use `def` for anything complex
- List comprehensions are usually clearer than `map`/`filter`
- Closures capture outer variables — the foundation of decorators
- `@decorator` = `func = decorator(func)` — wraps a function with extra behaviour

---

## Further Reading

- docs.python.org/3/tutorial/controlflow.html#defining-functions
- peps.python.org/pep-3102 — keyword-only arguments
- docs.python.org/3/library/functools — `reduce`, `partial`, `wraps`
- Episode 4: Classes, Dataclasses & Protocols
