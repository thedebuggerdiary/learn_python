---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Classes, Dataclasses & Protocols
### Episode 4 — Python from Scratch
**The Debugger Diary**

---

# Defining a Class

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"

c = Circle(5.0)
print(c.area())   # 78.53...
print(c)          # Circle(radius=5.0)
```

`self` is the instance — always the first parameter of instance methods.

---

# `@dataclass` — Less Boilerplate

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)
print(p)             # Point(x=3.0, y=4.0)
print(p.x, p.y)     # 3.0 4.0
print(p == Point(3.0, 4.0))  # True
```

`@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__`.
Compare Kotlin's `data class Point(val x: Float, val y: Float)`.

---

# Dataclass Options

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)   # immutable — like Kotlin val
class Config:
    host: str
    port: int = 8080
    tags: list[str] = field(default_factory=list)

cfg = Config(host="localhost")
print(cfg)   # Config(host='localhost', port=8080, tags=[])

cfg.port = 9000   # FrozenInstanceError — immutable!
```

`frozen=True` makes the dataclass immutable and hashable.
`field(default_factory=list)` creates a fresh list per instance.

---

# `@property` — Computed Attributes

```python
import math
from dataclasses import dataclass

@dataclass
class Circle:
    radius: float

    @property
    def area(self) -> float:
        return math.pi * self.radius ** 2

    @property
    def diameter(self) -> float:
        return self.radius * 2

c = Circle(5.0)
print(c.area)      # 78.53...  — no () needed
print(c.diameter)  # 10.0
```

`@property` lets you compute a value on access without exposing the implementation.

---

# Dunder Methods

```python
@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self) -> int:
        return 2

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

v1 = Vector(1.0, 2.0)
v2 = Vector(3.0, 4.0)
print(v1 + v2)   # (4.0, 6.0)
print(len(v1))   # 2
```

Dunder (double-underscore) methods implement Python's operator protocol.

---

# Inheritance

```python
from dataclasses import dataclass
import math

@dataclass
class Shape:
    color: str = "red"

    def area(self) -> float:
        raise NotImplementedError

@dataclass
class Circle(Shape):
    radius: float = 0.0

    def area(self) -> float:
        return math.pi * self.radius ** 2

@dataclass
class Rectangle(Shape):
    width: float = 0.0
    height: float = 0.0

    def area(self) -> float:
        return self.width * self.height
```

---

# Protocol — Structural Typing

```python
from typing import Protocol

class HasArea(Protocol):
    def area(self) -> float: ...

def print_area(shape: HasArea) -> None:
    print(f"Area: {shape.area():.2f}")

# Circle and Rectangle satisfy HasArea — no inheritance needed
print_area(Circle(radius=5.0))       # Area: 78.54
print_area(Rectangle(width=4.0, height=3.0))  # Area: 12.00
```

`Protocol` is **structural** — any class with the right methods qualifies.
No `implements` keyword. This is duck typing with static checking.

---

# Class Methods and Static Methods

```python
from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    name: str
    birth_year: int

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "User":
        return cls(name=str(data["name"]), birth_year=int(str(data["birth_year"])))

    @staticmethod
    def is_valid_year(year: int) -> bool:
        return 1900 <= year <= date.today().year

u = User.from_dict({"name": "Alice", "birth_year": 1995})
print(u)                    # User(name='Alice', birth_year=1995)
print(User.is_valid_year(1995))   # True
```

---

# Key Takeaways

- `class Name:` + `def __init__(self, ...)` — standard class definition
- `self` is the instance; it must be the first parameter of every instance method
- `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` — use it for data holders
- `frozen=True` makes a dataclass immutable; `field(default_factory=...)` for mutable defaults
- `@property` — computed read-only attribute; access without `()`
- Dunder methods — `__add__`, `__str__`, `__len__` — implement operator protocols
- `Protocol` — structural typing; any class with the right methods qualifies
- `@classmethod` — alternative constructor; `@staticmethod` — utility on the class namespace

---

# What's Next — Episode 5

**Collections & Comprehensions**

- `list`, `dict`, `set`, `tuple` — built-in collection types
- List, dict, and set comprehensions
- Generator expressions — lazy sequences
- `sorted`, `min`, `max`, `any`, `all`
- `itertools` — chaining, grouping, combining collections

**The Debugger Diary** — Python from Scratch
_"Understand the tools, not just the syntax."_
