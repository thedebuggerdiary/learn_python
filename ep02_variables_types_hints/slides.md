---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Variables, Types & Type Hints
### Episode 2 — Python from Scratch
**The Debugger Diary**

---

# Dynamic Typing

Python variables hold any type — the type lives on the value, not the variable.

```python
x = 42          # int
x = "hello"     # now a str — perfectly valid
x = [1, 2, 3]  # now a list
```

```kotlin
// Kotlin — statically typed
var x: Int = 42
x = "hello"  // Compile error
```

Dynamic typing means fast iteration. Type hints (coming later) give you safety back.

---

# Built-in Types

```python
name    = "Alice"        # str
age     = 30             # int
ratio   = 3.14           # float
active  = True           # bool
nothing = None           # NoneType
```

Check the type at runtime:
```python
>>> type(name)
<class 'str'>
>>> isinstance(age, int)
True
```

---

# Strings

```python
s = "Hello, World!"

print(s.upper())           # HELLO, WORLD!
print(s.lower())           # hello, world!
print(s.replace("World", "Python"))  # Hello, Python!
print(s.split(", "))       # ['Hello', 'World!']
print(len(s))              # 13
print(s[0])                # H
print(s[-1])               # !
print(s[0:5])              # Hello  (slicing)
```

Strings are **immutable** — every method returns a new string.

---

# Numbers

```python
# Integer arithmetic
print(10 // 3)   # 3   — floor division
print(10 %  3)   # 1   — modulo
print(2 ** 10)   # 1024 — exponentiation

# Float
print(round(3.14159, 2))   # 3.14

# Conversion
print(int("42"))            # 42
print(float("3.14"))        # 3.14
print(str(100))             # "100"
```

No overflow in Python — integers grow as large as memory allows.

---

# None — Python's Null

```python
result = None

if result is None:
    print("No result yet")

# Best practice: use "is None", not "== None"
def find_user(user_id: int):
    ...  # returns a User or None
```

`None` is the only instance of `NoneType`. It represents the absence of a value — equivalent to `null` in Java/Kotlin or `nil` in Swift.

---

# Type Hints (PEP 484)

Type hints tell tools (and readers) what type a variable or function expects.

```python
# Variable annotation
name: str = "Alice"
age:  int = 30

# Function annotation
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Python does NOT enforce these at runtime
name = 42  # No error — hints are for tools, not the interpreter
```

---

# Why Type Hints?

```python
# Without hints — what does this return?
def process(data, threshold):
    ...

# With hints — immediately clear
def process(data: list[float], threshold: float) -> list[float]:
    ...
```

Benefits:
- **mypy / pyright** catch type errors before you run the code
- **VS Code IntelliSense** gives better autocomplete
- **Documentation** — the signature tells you everything
- **Refactoring** — rename a type, the tool finds all usages

---

# Optional — Nullable Values

```python
from typing import Optional

# Python 3.9 style (3.10+ can use str | None)
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None

user = find_user(1)
user = find_user(99)   # Returns None

# Python 3.10+ union syntax
def find_user(user_id: int) -> str | None:
    ...
```

`Optional[str]` is exactly `str | None` — a value that is either a string or absent.

---

# Checking for None

```python
user: str | None = find_user(99)

# Option 1 — explicit check
if user is not None:
    print(user.upper())   # safe

# Option 2 — walrus operator (Python 3.8+)
if (user := find_user(1)) is not None:
    print(user.upper())

# Option 3 — default with "or"
display = user or "Anonymous"
print(display)
```

Unlike Kotlin's `?.` and `?:`, Python has no special null-safe operators — you check explicitly. Type hints + mypy enforce that you always handle `None`.

---

# isinstance() — Runtime Type Checks

```python
def describe(value: object) -> str:
    if isinstance(value, str):
        return f"String of length {len(value)}"
    if isinstance(value, int):
        return f"Integer: {value}"
    if isinstance(value, list):
        return f"List with {len(value)} items"
    return f"Unknown type: {type(value).__name__}"

print(describe("hello"))   # String of length 5
print(describe(42))        # Integer: 42
print(describe([1, 2, 3])) # List with 3 items
```

---

# Type Aliases

```python
from typing import TypeAlias

UserId: TypeAlias = int
UserName: TypeAlias = str

def get_user(user_id: UserId) -> UserName | None:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)
```

Type aliases make complex signatures readable without introducing new types.

---

# Key Takeaways

- Dynamic typing — variables hold any type; types live on values
- Built-in types: `int`, `float`, `str`, `bool`, `None`
- `type()` and `isinstance()` — inspect types at runtime
- Type hints — `name: str`, `def f(x: int) -> str:` — for tools, not the interpreter
- `Optional[str]` = `str | None` — a value that might be absent
- Check for `None` with `if x is not None:` or `if x is None:`
- `mypy` enforces your hints at development time

---

# What's Next — Episode 3

**Functions & Lambdas**

- `def` — default parameters and keyword arguments
- `*args` and `**kwargs` — variadic functions
- `lambda` — anonymous single-expression functions
- Higher-order functions — `map`, `filter`, passing functions as arguments
- Decorators — wrapping functions with extra behaviour

**The Debugger Diary** — Python from Scratch
_"Understand the tools, not just the syntax."_
