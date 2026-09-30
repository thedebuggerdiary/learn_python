---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Real-World Object-Oriented Python
### Episode 7 — Python OOP from Scratch
**The Debugger Diary**

---

# What You Hand-Wrote, Generated

```python
@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"
```

`@dataclass` builds `__init__`, `__repr__`, `__eq__`.
`frozen=True` adds `__hash__` and blocks field writes.

You still write `__add__` / `__mul__` — currency is **your** rule.

---

# Kotlin / Java Cousins

```kotlin
data class Money(val cents: Int, val currency: String = "USD")
```

```java
public record Money(int cents, String currency) {}
```

Same job: a value type with generated equality. Python's version is a **decorator**.

---

# `frozen=True`

```python
m = Money(100)
m.cents = 0   # FrozenInstanceError
```

Episode 6: hash only if equality cannot drift.
Episode 7: the language **enforces** it.

`Product` / `Order` stay mutable. Freeze **values**, not every entity.

---

# `default_factory` — Episode 1 Again

```python
lines: list[LineItem] = field(default_factory=list)
```

`= []` is **one list** on the class.

`default_factory=list` → a **new** list per `Order()`.

---

# `Enum` Status

```python
class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"

if self.status is not Status.PENDING:
    raise ValueError(f"cannot pay from {self.status}")
```

Members are singletons. Compare with **`is`**, like `None`.
`"paid"` strings will typo.

---

# Mixin vs Composition

```python
class PrintableMixin:
    def summary(self) -> str: ...

@dataclass
class Order(PrintableMixin):
    lines: list[LineItem] = field(default_factory=list)
```

| Piece | Role |
|---|---|
| `PrintableMixin.summary` | optional behavior |
| `lines: list[LineItem]` | **the model** |
| `Product.allocate` | stock invariant |

Do not mixin your way to a domain.

---

# Methods Own Invariants

```python
def allocate(self, qty: int) -> None:
    if qty > self.stock:
        raise ValueError(f"only {self.stock} in stock for {self.sku}")
    self.stock -= qty

def add(self, product: Product, qty: int) -> None:
    product.allocate(qty)
    self.lines.append(LineItem(product, qty))
```

`Order` does not decrement stock on its own. **`Product` does.**

---

# pytest

```bash
python -m pip install pytest
python -m pytest test_inventory.py
```

```python
assert Money(100) + Money(50) == Money(150)

with pytest.raises(ValueError, match="cannot pay"):
    order.pay()
```

Functions named `test_*`. No required test class.
Dataclass `__eq__` makes asserts readable.

---

# Demo Script

```bash
python inventory.py
```

```
Order(ORD-1)
total cents: 4095
status: Status.PAID
mug stock: 8
```

`2×1299 + 3×499 = 4095`. Mug `10 − 2 = 8`.

---

# Series Map

1. Identity vs `==` — dict or class
2. Instance vs class attributes
3. Properties and `_` / `__`
4. `super()` and MRO
5. ABC vs Protocol
6. Dunders and composition
7. Dataclasses, Enum, tests

---

# Key Takeaways

- `@dataclass` generates the boilerplate you now understand
- `frozen=True` for hashable values
- `default_factory` for mutable fields
- `Enum` + `is` for status
- Mixin = sprinkle; composition = structure
- Invariants live on methods (`allocate`, `pay`)
- `pytest.raises` documents the failure

---

# The Series Is Complete

You can now choose a class **on purpose**: when state and operations travel together, when a value must be frozen, when a Protocol is enough, and when a function on a dict was already the right design.

**The Debugger Diary** — Python OOP from Scratch
_"Understand the tools, not just the syntax."_

---

# Thanks for Watching

**The Debugger Diary**

github.com/thedebuggerdiary/learn_python_oop
