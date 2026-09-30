# Episode 6 — Dunders & Composition

**Series:** Python OOP from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episode 5 — calling methods through a shared shape.

---

## Episode Overview

By the end of this episode you will implement the data-model methods that make a type feel built-in: `__repr__`, `__str__`, `__eq__`, `__hash__`, `__add__`, `__mul__`, `__len__`, `__iter__`. You will keep `Money` hashable only because it is treated as a value, and you will build `Order` by **containing** `LineItem`s instead of inheriting from `list`. The demo is `code/money_order.py`.

---

## Section 1: The Data Model Is a Protocol With the Language

Python does not special-case `len(order)` for lists only. `len(x)` calls `x.__len__()`. `a + b` tries `a.__add__(b)`. `repr(x)` calls `x.__repr__()`. Your class opts into syntax by implementing those methods.

Java overloads `+` only for `String` and numbers; you write `money.add(other)`. Python lets `Money` participate in `+` so the domain reads as arithmetic. That is power and a foot-gun: overload operators that stay obvious (`Money + Money`), not cute ones (`Order + Coupon`).

---

## Section 2: `__repr__` vs `__str__`

```python
def __repr__(self) -> str:
    return f"Money({self._cents}, {self.currency!r})"

def __str__(self) -> str:
    sign = "-" if self._cents < 0 else ""
    whole, frac = divmod(abs(self._cents), 100)
    return f"{sign}${whole}.{frac:02d}"
```

**`__repr__`**
Unambiguous, developer-facing, ideally `eval`-able. The REPL, tracebacks, and container prints use it. `!r` in f-strings is `repr`.

**`__str__`**
Human-facing. `print(money)` uses `__str__` if present, else `__repr__`. `$12.50` is for receipts; `Money(1250, 'USD')` is for debugging.

If you implement only one, implement `__repr__`. `__str__` can wait.

---

## Section 3: `__eq__` and `NotImplemented`

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Money):
        return NotImplemented
    return self._cents == other._cents and self.currency == other.currency
```

Episode 1: default `==` is identity. Two `Money(1250)` objects would be unequal until `__eq__` compares cents and currency.

**`NotImplemented` (the singleton)**
Not `raise NotImplementedError`. Returning `NotImplemented` tells Python to try `other.__eq__(self)` or fall back to identity. Returning `False` for unknown types blocks that fallback and makes `money == "nope"` a hard False, which is usually what you want for values — but `NotImplemented` is still the correct "I don't know this type" signal so `int` vs `Money` can be symmetric if you ever add `__eq__` on a wrapper.

`from_dollars(12.50)` uses `round(dollars * 100)` because `12.50 * 100` as float is not a teaching moment you want to lose — 12.50 is exact in binary enough for this demo. Real money parsers take strings. Keep cents as `int` from here on.

---

## Section 4: `__hash__` Only With Immutable Equality

```python
def __hash__(self) -> int:
    return hash((self._cents, self.currency))
```

Rule: if you define `__eq__`, Python sets `__hash__ = None` unless you define `__hash__` yourself. Unhashable objects cannot live in `set`s or as `dict` keys.

If two objects compare equal, they **must** have the same hash. If you hash `Money` and then mutate `_cents`, the object is lost in the set. So hashable `Money` must be treated as immutable: no setters for cents. Episode 7 will freeze it with `@dataclass(frozen=True)`.

Here `_cents` has no setter; only `__init__` writes it. That is the discipline. The demo builds `{price, Money(1250), Money(100)}` — size 2 because `price == Money(1250)`.

---

## Section 5: Operators Return New Values

```python
def __add__(self, other: Money) -> Money:
    if not isinstance(other, Money):
        return NotImplemented
    if other.currency != self.currency:
        raise ValueError("currency mismatch")
    return Money(self._cents + other._cents, self.currency)

def __mul__(self, n: int) -> Money:
    if not isinstance(n, int):
        return NotImplemented
    return Money(self._cents * n, self.currency)

def __rmul__(self, n: int) -> Money:
    return self.__mul__(n)
```

**`__add__`**
Does not mutate `self`. Value types produce new instances. `order.total()` loops `total = total + item.total()`.

**`__mul__` / `__rmul__`**
`price * 3` calls `__mul__`. `3 * price` calls `int.__mul__(price)`, fails, then `__rmul__`. Without `__rmul__`, `3 * price` is a `TypeError`.

Refuse mixed currencies. Silent conversion is how accounting bugs ship.

---

## Section 6: Composition — `Order` Has Line Items

```python
class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        self._items: list[LineItem] = []
```

`Order` is not a `list`. It **has** a list. You get `add`, `total`, `__len__`, `__iter__` without inheriting `append`, `extend`, `sort`, and `clear`.

**Java**
`class Order extends ArrayList<LineItem>` shows up in old codebases. Callers then `order.clear()` and destroy a paid order. Composition would have been `private final List<LineItem> lines`. Python makes the same mistake with `class Order(list):`. Don't.

**`LineItem`**
Holds `sku`, `unit_price`, `qty`. `total` is `unit_price * qty` — that is `__mul__` earning its keep.

---

## Section 7: `__len__` and `__iter__`

```python
def __len__(self) -> int:
    return len(self._items)

def __iter__(self):
    return iter(self._items)
```

`len(order)` and `for line in order` now work. `list(order)` too. You implemented *collection behavior* without *being* a list.

Do not implement `__getitem__` unless you want `order[0]` and slicing. This demo does not. Iteration is enough for `total`.

---

## Section 8: Inheritance vs Composition (Again)

Episode 4 said mixins wrap behavior. Episode 6 says data wrappers compose.

| Need | Tool |
|---|---|
| Same `send`, extra logging | mixin (`Logged`) |
| Order made of lines | composition (`_items`) |
| Money is a kind of int | **neither** — `int` has no currency |

`class Money(int)` looks clever (`Money(1250) + 10`). You then inherit every `int` method and lose currency checks. Composition (or a dataclass with an `int` field) stays honest.

---

## Section 9: Running the Demo

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

Set size 2: `price` and `Money(1250)` collapse. `Money(100)` remains. `3 * price` proves `__rmul__`. Order total is `2500 + 199` cents.

---

## Section 10: What You Did Not Implement

- `__lt__` / `@total_ordering` — only if you sort money.
- `__bool__` — default is "nonzero `__len__`" for orders; `Money` would be true if you add `__bool__` based on cents; we skip it.
- `__iadd__` — `total += x` without `__iadd__` still works: it does `total = total + x` and rebinds. Fine for immutable values.

---

## Key Takeaways

- Syntax hooks are dunders: `len`, `+`, `==`, `repr`.
- `__repr__` for developers; `__str__` for humans.
- `__eq__` returns `NotImplemented` for unknown types.
- `__hash__` only if equality is stable — treat `Money` as immutable.
- Operators return **new** `Money`; check currency.
- `__rmul__` makes `3 * price` work.
- `Order` contains a list; it is not a list.
- `__len__` / `__iter__` give collection syntax without inheritance.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `TypeError: unhashable type: 'Money'` | `__eq__` without `__hash__` | Define `__hash__` or stop using sets |
| Set "loses" a Money | Hashed then mutated `_cents` | No mutation after hash; freeze in Ep 7 |
| `TypeError: unsupported operand type(s) for *: 'int' and 'Money'` | Missing `__rmul__` | Implement `__rmul__` |
| `ValueError: currency mismatch` | Adding USD to another code | Convert explicitly or reject |
| `Order` callers use `.append` | Inherited `list` | Compose a private list; expose `add` |

---

## Further Reading

- [Data model](https://docs.python.org/3/reference/datamodel.html) — the dunder catalog
- [emulating numeric types](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types)
- Episode 7: Real-World OOP — `dataclass`, `Enum`, mixins vs composition, `pytest` on the inventory model
