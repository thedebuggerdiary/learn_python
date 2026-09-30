# Episode 7 — Real-World Object-Oriented Python

**Series:** Python OOP from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episodes 1–6.

---

## Episode Overview

By the end of this episode you will replace hand-written `__init__` / `__repr__` / `__eq__` with `@dataclass`, model order status as an `Enum`, keep `Money` frozen, and put a `pytest` suite next to the domain. You will see a tiny `PrintableMixin` beside real composition (`Order` holds `LineItem`s) and know which one is doing the design work. The demo is `code/inventory.py` plus `code/test_inventory.py`.

---

## Section 1: Dataclasses Generate the Boilerplate You Learned

Episodes 2 and 6 wrote `__init__`, `__repr__`, and `__eq__` by hand so you would know what they mean. `@dataclass` generates them from annotated fields:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"
```

**Generated**
`__init__(self, cents, currency="USD")`, `__repr__`, `__eq__`. With `frozen=True`, also `__hash__` (because equality is field-wise and mutation is forbidden).

**Still yours**
`__add__` and `__mul__` — the generator does not know currency rules.

This is Kotlin `data class` / Java records. You are not abandoning OOP; you are stopping copying `__init__` lines.

---

## Section 2: `frozen=True` Enforces Episode 6's Hash Rule

```python
m = Money(100)
m.cents = 0  # FrozenInstanceError
```

`FrozenInstanceError` is a subclass of `AttributeError`. Assignment to a field on a frozen instance raises it. That is how `Money` stays a safe `dict` key.

`Product` and `Order` are **not** frozen: stock and status change. Freeze values; keep entities mutable behind methods (`allocate`, `pay`), not by poking fields from every caller. In this demo, tests still read `.stock` and `.status` — small enough. In a larger system you might expose read-only properties.

---

## Section 3: `field(default_factory=list)`

```python
from dataclasses import dataclass, field

@dataclass
class Order(PrintableMixin):
    order_id: str
    status: Status = Status.PENDING
    lines: list[LineItem] = field(default_factory=list)
```

`lines: list[LineItem] = []` would be the Episode 1 bug: one list on the class. `default_factory=list` calls `list()` **per instance**. Same rule as `self.lines = []` in `__init__`, generated for you.

Mutable defaults are the dataclass foot-gun. `mypy` and ruff will nag; listen.

---

## Section 4: `Enum` for a State Machine

```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
```

Strings `"paid"` invite typos (`"Paid"`). `Status.PAID` is a singleton. Compare with `is`:

```python
def pay(self) -> None:
    if self.status is not Status.PENDING:
        raise ValueError(f"cannot pay from {self.status}")
    self.status = Status.PAID
```

`is` works because Enum members are unique objects. `==` also works. Prefer `is` for enum members the same way you prefer `is` for `None`.

Java `enum Status { PENDING, PAID }` is the same idea. Python enums can hold extra behavior; this series keeps them as labels.

---

## Section 5: Mixin vs Composition on the Same Class

```python
class PrintableMixin:
    def summary(self) -> str:
        order_id = getattr(self, "order_id", "?")
        return f"{type(self).__name__}({order_id})"


@dataclass
class Order(PrintableMixin):
    ...
```

**Mixin**
Adds `summary()`. No extra state. If you delete it, `Order` still allocates stock and totals. Mixins are for *behavior sprinkles*.

**Composition**
`lines: list[LineItem]` **is** the design. An order without lines is empty, not "missing a mixin." Stock lives on `Product`; `Order.add` asks the product to `allocate`.

Do not replace composition with mixins (`TotalingMixin`, `StockMixin`, `PayingMixin`). That is an inheritance soup. One mixin in this file is a contrast, not a pattern to scale.

Dataclass + mixin: put the mixin **left** (`Order(PrintableMixin)`) so generated dataclass methods still win on `__init__`. Field order in multiple dataclass bases is a specialist topic — avoid stacking dataclass parents.

---

## Section 6: The Domain Methods

```python
def allocate(self, qty: int) -> None:
    if qty > self.stock:
        raise ValueError(f"only {self.stock} in stock for {self.sku}")
    self.stock -= qty

def add(self, product: Product, qty: int) -> None:
    product.allocate(qty)
    self.lines.append(LineItem(product, qty))
```

`add` does not decrement stock itself. `Product` owns the invariant. That is encapsulation (Episode 3) without `__` mangling: the method is the API.

`total` folds `Money` addition from Episode 6. `pay` is the only legal `PENDING → PAID` transition in this model. Shipping and cancel are enum members for the real world; they are unused in the tests on purpose — do not implement a warehouse in a 15-minute episode.

---

## Section 7: pytest on Classes

```bash
python -m pip install pytest
python -m pytest test_inventory.py
```

Tests import the same module you run as a script. `test_inventory.py` lives beside `inventory.py`.

**`assert Money(100) + Money(50) == Money(150)`**
Dataclass `__eq__` makes this read as domain language.

**`pytest.raises(ValueError, match="currency mismatch")`**
The `match` is a regex against the message. Keep messages stable; they are part of the API for tests.

**`FrozenInstanceError`**
Imported from `dataclasses`. The test documents that frozen means frozen.

**State machine**
Pay twice: second `pay` raises. Over-allocate: `only 1 in stock`.

You do not need a test class. Functions named `test_*` are enough. Java JUnit would use `@Test` methods on a class — pytest collected functions instead.

---

## Section 8: Running the Script

```bash
python inventory.py
```

```
Order(ORD-1)
total cents: 4095
status: Status.PAID
mug stock: 8
```

`2 * 1299 + 3 * 499 = 2598 + 1497 = 4095`. Mug stock `10 - 2 = 8`. `summary()` comes from the mixin; the total comes from composition.

---

## Section 9: Typing the Model

Field annotations are dataclass requirements and documentation. `lines: list[LineItem]` needs `from __future__ import annotations` or quotes in older code; 3.12+ is fine as written for `Money` quoted in `__add__` (`"Money"`) to avoid forward-ref issues inside the class body... actually `Money.__add__` uses `"Money"` because the class is still being defined. Dataclass `Order` can use `list[LineItem]` because `LineItem` is already defined above.

`mypy` on this folder would catch `order.add(mug, "2")`. This episode installs pytest only; mypy was `learn_python` Episode 7. Mention it; do not require it.

---

## Section 10: What Production Adds Next

- Persistence (not an extra base class — a repository function).
- `decimal.Decimal` or integer cents only (you already chose cents).
- `Optional` / `Status` transitions as a table if the machine grows.
- Pydantic if this model is a JSON API boundary — different library, same frozen-value instinct.
- Mixins remain rare; composition remains default.

---

## Key Takeaways

- `@dataclass` generates `__init__`, `__repr__`, `__eq__`; you keep domain methods.
- `frozen=True` makes values hashable and assignment a `FrozenInstanceError`.
- `field(default_factory=list)` — never `= []` on a dataclass field.
- `Enum` members are singletons; compare status with `is`.
- Mixins sprinkle behavior; composition holds the data.
- `Product.allocate` owns stock; `Order.add` calls it.
- `pytest` tests classes via functions, `raises`, and dataclass equality.
- Freeze values, mutate entities through methods.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `ValueError: mutable default ... for field lines` | `lines: list[...] = []` | `field(default_factory=list)` |
| `FrozenInstanceError` | Assigned to a frozen dataclass field | Don't; create a new `Money(...)` |
| `TypeError: cannot inherit frozen dataclass from a non-frozen one` | Mixed frozen/non-frozen dataclass bases | Don't stack dataclass parents |
| `ValueError: cannot pay from Status.PAID` | `pay` called twice | Status machine; test the second call |
| `ModuleNotFoundError: pytest` | Forgot install | `python -m pip install pytest` |

---

## Further Reading

- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [enum](https://docs.python.org/3/library/enum.html)
- [pytest](https://docs.pytest.org/)
- Series recap: identity → instances → properties → MRO → ABC/Protocol → dunders → dataclasses
