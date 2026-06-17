# Episode 4 — Classes, Dataclasses & Protocols

**Series:** Python from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episodes 1–3

---

## Episode Overview

Python's object model is flexible and expressive. You can write a full class with `__init__` and custom methods, or use `@dataclass` to auto-generate boilerplate — similar to Kotlin's `data class`. `Protocol` provides structural typing: if a class has the right methods, it qualifies, without inheriting from anything. This episode builds a shape hierarchy to demonstrate all of these concepts together.

---

## Section 1: Defining a Class

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius   # instance attribute

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def scale(self, factor: float) -> "Circle":
        return Circle(self.radius * factor)

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"

    def __str__(self) -> str:
        return f"a circle with radius {self.radius}"
```

**`self`** is a reference to the current instance. It must be the first parameter of every instance method — Python passes it automatically when you call `instance.method()`.

**`__init__`** is the constructor. It receives the instance (`self`) plus any arguments you pass at construction time. Do not return anything from `__init__`.

**`__repr__`** should return an unambiguous developer-facing string, ideally one that can be pasted into the REPL to recreate the object.

**`__str__`** returns a human-readable string. `print(obj)` calls `__str__`; the REPL and `repr(obj)` call `__repr__`.

---

## Section 2: @dataclass

`@dataclass` (Python 3.7+) auto-generates `__init__`, `__repr__`, and `__eq__` from class-body annotations:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(3.0, 4.0)
p2 = Point(3.0, 4.0)

print(p1)          # Point(x=3.0, y=4.0)
print(p1 == p2)    # True — compares field by field
print(p1 is p2)    # False — different objects
```

Compare to Kotlin:
```kotlin
data class Point(val x: Float, val y: Float)
```

Python's dataclass gives you the same zero-boilerplate data holder.

### Default values and field()

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str
    port: int = 8080
    tags: list[str] = field(default_factory=list)
    meta: dict[str, str] = field(default_factory=dict)

cfg = Config(host="localhost")
print(cfg)
# Config(host='localhost', port=8080, tags=[], meta={})
```

`field(default_factory=callable)` is required for mutable defaults — it calls the factory for each new instance, preventing the shared-mutable-default bug.

### frozen=True — immutable dataclass

```python
@dataclass(frozen=True)
class RGB:
    r: int
    g: int
    b: int

    def as_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

red = RGB(255, 0, 0)
print(red.as_hex())   # #ff0000
red.r = 128           # FrozenInstanceError — immutable
```

`frozen=True` also makes the dataclass hashable, so you can use it as a dict key or in a set.

### post_init — custom validation

```python
from dataclasses import dataclass

@dataclass
class Percentage:
    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 100.0:
            raise ValueError(f"Percentage must be 0–100, got {self.value}")
```

`__post_init__` is called by the generated `__init__` after all fields are set.

---

## Section 3: @property

`@property` turns a method into a computed attribute accessed without `()`:

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

    @diameter.setter
    def diameter(self, value: float) -> None:
        self.radius = value / 2

c = Circle(5.0)
print(c.area)       # 78.539...
print(c.diameter)   # 10.0
c.diameter = 20.0
print(c.radius)     # 10.0
```

Properties encapsulate computed values. The setter lets you assign to what looks like an attribute while running logic behind the scenes.

---

## Section 4: Dunder Methods

Dunder (double-underscore) methods let your objects integrate with Python's built-in operators and functions:

```python
from dataclasses import dataclass

@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __len__(self) -> int:
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

v1 = Vector(1.0, 2.0)
v2 = Vector(3.0, 4.0)
print(v1 + v2)     # Vector(x=4.0, y=6.0)
print(abs(v1))     # 2.236...
x, y = v1          # unpacking via __iter__
```

Common dunders:

| Method | Triggered by |
|---|---|
| `__init__` | `Foo()` construction |
| `__repr__` | `repr(obj)`, REPL display |
| `__str__` | `str(obj)`, `print(obj)` |
| `__eq__` | `==` |
| `__lt__` | `<` |
| `__add__` | `+` |
| `__len__` | `len(obj)` |
| `__contains__` | `x in obj` |
| `__iter__` | `for x in obj:`, unpacking |
| `__getitem__` | `obj[key]` |
| `__call__` | `obj()` — callable instances |

---

## Section 5: Inheritance

```python
import math
from dataclasses import dataclass

@dataclass
class Shape:
    color: str = "red"

    def area(self) -> float:
        raise NotImplementedError(f"{type(self).__name__} must implement area()")

    def describe(self) -> str:
        return f"{self.color} {type(self).__name__} with area {self.area():.2f}"


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


shapes: list[Shape] = [
    Circle(color="blue", radius=5.0),
    Rectangle(color="green", width=4.0, height=3.0),
]

for s in shapes:
    print(s.describe())
```

**`super()`** calls the parent class method:
```python
class LoggedCircle(Circle):
    def area(self) -> float:
        result = super().area()
        print(f"Computing area: {result:.2f}")
        return result
```

Python supports multiple inheritance — use it carefully and prefer composition over inheritance in most cases.

---

## Section 6: Protocol — Structural Typing

`Protocol` (Python 3.8+) defines a structural interface. Any class that has the required methods satisfies the protocol — no explicit `implements`:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class HasArea(Protocol):
    def area(self) -> float: ...

def total_area(shapes: list[HasArea]) -> float:
    return sum(s.area() for s in shapes)

# Circle and Rectangle satisfy HasArea implicitly
shapes: list[HasArea] = [Circle(radius=3.0), Rectangle(width=2.0, height=4.0)]
print(f"Total area: {total_area(shapes):.2f}")
print(isinstance(Circle(radius=1.0), HasArea))   # True (runtime_checkable)
```

`@runtime_checkable` allows `isinstance` checks against the protocol — only verifies that the methods exist, not their signatures.

Protocols are the Python equivalent of Kotlin interfaces or Go interfaces — they enable "duck typing with static checking".

---

## Section 7: Class Methods and Static Methods

```python
from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    name: str
    birth_year: int

    @property
    def age(self) -> int:
        return date.today().year - self.birth_year

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "User":
        return cls(
            name=str(data["name"]),
            birth_year=int(str(data["birth_year"])),
        )

    @staticmethod
    def is_valid_year(year: int) -> bool:
        return 1900 <= year <= date.today().year

u = User.from_dict({"name": "Alice", "birth_year": 1995})
print(u.age)
print(User.is_valid_year(1800))  # False
```

- **`@classmethod`** receives the class (`cls`) as the first argument, not the instance. Used for alternative constructors.
- **`@staticmethod`** receives neither `self` nor `cls`. Used for utility functions that belong on the class namespace but don't need instance or class state.

---

## Key Takeaways

- `class Name:` + `def __init__(self, ...)` — standard class; `self` is always first
- `@dataclass` generates `__init__`, `__repr__`, `__eq__` — use for simple data holders
- `frozen=True` → immutable and hashable; `field(default_factory=...)` for mutable fields
- `@property` — computed attribute, accessed without `()`
- Dunders — implement Python's operator protocols (`__add__`, `__len__`, `__iter__`, etc.)
- Inheritance: `class Child(Parent):` — use `super()` to call parent methods
- `Protocol` — structural typing; any class with the right methods qualifies
- `@classmethod` → alternative constructor; `@staticmethod` → utility on class namespace

---

## Further Reading

- docs.python.org/3/reference/datamodel.html — Python data model (all dunders)
- docs.python.org/3/library/dataclasses — dataclasses documentation
- peps.python.org/pep-0544 — PEP 544: Protocols (structural subtyping)
- Episode 5: Collections & Comprehensions
