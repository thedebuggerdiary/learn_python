# Episode 2 — Variables, Types & Type Hints

**Series:** Python from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episode 1 complete — Python installed, REPL working

---

## Episode Overview

Python is dynamically typed — variables don't have types, values do. This feels liberating coming from Java or Kotlin, but it means you can pass a `str` where an `int` is expected and not know until runtime. Type hints (PEP 484, Python 3.5+) let you annotate variables and functions so that tools can catch those mistakes before you run the code. This episode covers both: the dynamic reality and the practical discipline of annotating your code.

---

## Section 1: Dynamic Typing vs Static Typing

In Python, a variable is a label that points to a value. The label has no type — only the value does:

```python
x = 42
print(type(x))   # <class 'int'>

x = "hello"
print(type(x))   # <class 'str'>  — same variable, different type

x = [1, 2, 3]
print(type(x))   # <class 'list'>
```

Compare to Kotlin:
```kotlin
var x: Int = 42
x = "hello"   // Compile error: Type mismatch
```

**Tradeoffs of dynamic typing:**
- Faster to write, less ceremony
- Great for scripting, prototyping, data exploration
- Mistakes show up at runtime rather than compile time — unless you add type hints

---

## Section 2: Built-in Types

Python ships with a rich set of built-in types. Here are the most common:

### Numbers

```python
age     = 30       # int  — arbitrary precision, no overflow
ratio   = 3.14     # float — 64-bit IEEE 754 double
discount = 0.05j   # complex — rarely needed
```

Integer arithmetic:
```python
print(10 // 3)    # 3   — floor division (always an int)
print(10 / 3)     # 3.333...  — true division (always a float)
print(10 % 3)     # 1   — modulo
print(2 ** 10)    # 1024 — exponentiation
print(abs(-5))    # 5
```

Conversion:
```python
int("42")          # 42
float("3.14")      # 3.14
str(100)           # "100"
int(3.9)           # 3 — truncates, does not round
round(3.14159, 2)  # 3.14
```

### Strings

Strings are immutable sequences of Unicode characters:

```python
s = "Hello, World!"

# Common methods
s.upper()                   # "HELLO, WORLD!"
s.lower()                   # "hello, world!"
s.strip()                   # strips whitespace from both ends
s.split(", ")               # ["Hello", "World!"]
s.replace("World", "Python")  # "Hello, Python!"
s.startswith("Hello")       # True
s.endswith("!")             # True
", ".join(["a", "b", "c"])  # "a, b, c"

# Indexing and slicing
s[0]         # "H"   — first character
s[-1]        # "!"   — last character
s[0:5]       # "Hello" — characters 0,1,2,3,4
s[7:]        # "World!"
s[::-1]      # reversed string
```

Multi-line strings with triple quotes:
```python
message = """
This is a
multi-line string.
"""
```

### Booleans

`True` and `False` are the only boolean values. They are a subclass of `int`:
```python
int(True)    # 1
int(False)   # 0
True + True  # 2
```

Falsy values (evaluate to `False` in a boolean context):
```python
False, None, 0, 0.0, "", [], {}, set()
```

Everything else is truthy.

### None

`None` is the singleton that represents the absence of a value:
```python
result = None
print(type(result))       # <class 'NoneType'>
print(result is None)     # True — use "is", not "=="
```

---

## Section 3: Variables and Naming

Variable names follow `snake_case` in Python (PEP 8). There is no `val`/`var` distinction — Python variables are always reassignable:

```python
user_name = "Alice"
max_retries = 3
is_active = True
```

**Constants** — Python has no built-in `const`. Convention is `UPPER_SNAKE_CASE`:
```python
MAX_CONNECTIONS = 100
BASE_URL = "https://api.example.com"
```

The name signals "don't reassign this" — the interpreter won't stop you, but the convention is universally understood.

**Multiple assignment:**
```python
x = y = z = 0
a, b, c = 1, 2, 3     # tuple unpacking
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2,3,4]
```

---

## Section 4: Type Hints (PEP 484)

Type hints are annotations that tell tools what type a variable or function parameter should hold. They are completely ignored at runtime:

```python
name: str = "Alice"
age: int = 30
ratio: float = 3.14
active: bool = True
```

Function annotations:
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def log(message: str) -> None:
    print(message)
```

The `-> ReturnType` annotation after the parameter list declares the return type. `-> None` means the function returns nothing meaningful (like `void`).

### Collection types

```python
from typing import Any  # rarely needed but exists

names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
unique: set[int] = {1, 2, 3}
point: tuple[int, int] = (10, 20)
```

Python 3.9+ allows the lowercase `list[str]` syntax directly. On Python 3.8 and earlier, you need `from typing import List` and `List[str]`.

---

## Section 5: Optional and Union Types

`Optional[T]` means the value is either type `T` or `None`:

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)  # .get() returns None if key absent
```

Python 3.10 introduced the `|` union syntax as a cleaner alternative:
```python
def find_user(user_id: int) -> str | None:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)
```

**Multi-type unions:**
```python
def process(value: int | str | float) -> str:
    return str(value)
```

### Handling None safely

```python
user: str | None = find_user(99)

# Pattern 1 — guard clause
if user is None:
    print("User not found")
else:
    print(user.upper())

# Pattern 2 — default
display_name = user if user is not None else "Anonymous"
# Shorter (but careful — empty string "" is also falsy):
display_name = user or "Anonymous"

# Pattern 3 — walrus operator (Python 3.8+)
if (user := find_user(1)) is not None:
    print(user.upper())
```

---

## Section 6: isinstance() and Type Narrowing

```python
def describe(value: object) -> str:
    if isinstance(value, str):
        return f"String of length {len(value)}"
    elif isinstance(value, (int, float)):
        return f"Number: {value}"
    elif isinstance(value, list):
        return f"List with {len(value)} items"
    else:
        return f"Unknown: {type(value).__name__}"
```

`isinstance(value, SomeType)` returns `True` if `value` is an instance of `SomeType` or any subclass. It accepts a tuple of types as the second argument: `isinstance(x, (int, float))`.

After an `isinstance` check, mypy (and pyright) know the type is narrowed — the same way Kotlin's smart casts work.

---

## Section 7: Type Aliases

```python
from typing import TypeAlias

# Simple alias
UserId: TypeAlias = int
UserMap: TypeAlias = dict[int, str]

def get_users() -> UserMap:
    return {1: "Alice", 2: "Bob"}
```

For more powerful nominal type aliases (Python 3.12+):
```python
type UserId = int  # new syntax
```

---

## Key Takeaways

- Dynamic typing — variables hold any type; the interpreter never checks
- Type hints — `name: str`, `def f(x: int) -> str:` — for mypy, pyright, and IDEs
- Built-in types: `int`, `float`, `str`, `bool`, `None`
- `Optional[str]` = `str | None` — a value that might be absent
- Check `None` with `is None` / `is not None`, not `==`
- `isinstance(x, T)` — runtime type check; also narrows for mypy
- Install mypy (`pip install mypy`) and run `mypy <file>.py` to catch type errors

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `AttributeError: 'NoneType' object has no attribute 'x'` | Called a method on `None` | Check `if value is not None:` first |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | Added int and str directly | Convert: `str(num) + text` or `f"{num}{text}"` |
| `ValueError: invalid literal for int() with base 10: 'abc'` | `int("abc")` — can't convert | Validate the string first or use `try/except` |
| `NameError: name 'x' is not defined` | Used a variable before assigning it | Assign a value before use |

---

## Further Reading

- peps.python.org/pep-0484 — PEP 484: Type Hints specification
- mypy.readthedocs.io — mypy documentation
- docs.python.org/3/library/typing — `typing` module reference
- Episode 3: Functions & Lambdas — `def`, `*args`/`**kwargs`, `lambda`, decorators
