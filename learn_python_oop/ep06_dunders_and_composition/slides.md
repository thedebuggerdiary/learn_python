---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Dunders & Composition
### Episode 6 — Python OOP from Scratch
**The Debugger Diary**

---

# Syntax Is Method Calls

| You write | Python calls |
|---|---|
| `repr(x)` / f`{x!r}` | `x.__repr__()` |
| `print(x)` | `x.__str__()` |
| `a == b` | `a.__eq__(b)` |
| `a + b` | `a.__add__(b)` |
| `len(x)` | `x.__len__()` |

Opt in by implementing the hook. No compiler switch.

---

# `__repr__` vs `__str__`

```python
def __repr__(self) -> str:
    return f"Money({self._cents}, {self.currency!r})"

def __str__(self) -> str:
    whole, frac = divmod(abs(self._cents), 100)
    return f"${whole}.{frac:02d}"
```

- **`__repr__`** — debugger, containers, ideally reconstructible
- **`__str__`** — humans, receipts
- If you write one, write **`__repr__`**

---

# `__eq__` Replaces Identity

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Money):
        return NotImplemented
    return self._cents == other._cents and self.currency == other.currency
```

Default `==` is **`is`** (Episode 1).

Return **`NotImplemented`** (the singleton), not `raise NotImplementedError`.

---

# `__hash__` Needs Stable Equality

```python
def __hash__(self) -> int:
    return hash((self._cents, self.currency))
```

- `__eq__` without `__hash__` → **unhashable**
- Equal objects **must** share a hash
- **Do not mutate** `_cents` after hashing
- Demo: `{price, Money(1250), Money(100)}` has **size 2**

---

# Operators Return New Money

```python
def __add__(self, other: Money) -> Money:
    if other.currency != self.currency:
        raise ValueError("currency mismatch")
    return Money(self._cents + other._cents, self.currency)
```

No `self._cents +=`. Values are **immutable in practice**.

---

# `__rmul__` for `3 * price`

```python
def __mul__(self, n: int) -> Money:
    return Money(self._cents * n, self.currency)

def __rmul__(self, n: int) -> Money:
    return self.__mul__(n)
```

`price * 3` → `__mul__`.
`3 * price` → int fails, then **`__rmul__`**.

---

# Composition: Order Has Lines

```python
class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        self._items: list[LineItem] = []
```

Not `class Order(list):`.

Inheriting `list` exports `clear`, `sort`, `extend`. A paid order must not grow `append` from callers. **`add` is the API.**

---

# `__len__` / `__iter__`

```python
def __len__(self) -> int:
    return len(self._items)

def __iter__(self):
    return iter(self._items)
```

`len(order)` and `for line in order` without being a sequence.

Skip `__getitem__` unless you want `order[0]`.

---

# Mixin vs Compose vs Inherit `int`

| Need | Tool |
|---|---|
| Extra behavior on `send` | mixin (Ep 4) |
| Order made of lines | **composition** |
| `class Money(int)` | **no** — loses currency |

---

# Demo — `money_order.py`

```bash
python money_order.py
```

```
repr: Money(1250, 'USD')
str: $12.50
eq: True
hashable set size: 2
contains 100 cents: True
line total: Money(2500, 'USD')
len: 2
skus: ['SKU-1', 'SKU-2']
order total: Money(2699, 'USD')
3 * price: Money(3750, 'USD')
```

---

# Key Takeaways

- Dunders hook your type into syntax
- `__repr__` for you; `__str__` for users
- `__eq__` + `__hash__` only if values stay stable
- Operators return **new** objects
- `__rmul__` for reversed `*`
- Compose collections; do not inherit `list`
- `__len__` / `__iter__` are enough for many containers

---

# What's Next — Episode 7

**Real-World Object-Oriented Python**

- `@dataclass` / `frozen=True`
- `Enum` status machine
- Mixin vs composition on `Order`
- `pytest` on inventory

**The Debugger Diary** — Python OOP from Scratch
_"Understand the tools, not just the syntax."_
