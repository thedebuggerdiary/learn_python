---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Polymorphism, ABCs & Protocols
### Episode 5 — Python OOP from Scratch
**The Debugger Diary**

---

# Three Ways to Share a Verb

| Style | Relationship | Typical fail |
|---|---|---|
| Duck typing | none | `AttributeError` at call |
| **ABC** | must **subclass** | `TypeError` at construction |
| **Protocol** | **has the methods** | type checker (`isinstance` optional) |

Java ≈ ABC. Go interfaces ≈ Protocol.

---

# Duck Typing

```python
def checkout_duck(processor: Chargeable, amount: int) -> str:
    return processor.charge(amount, "USD")
```

If it has `charge`, the call runs.

- Fast to write
- Typos fail **in production**
- Annotation is for **humans and mypy**, not the VM

---

# `GiftCard` Subclasses Nothing

```python
class GiftCard:
    def charge(self, amount: int, currency: str) -> str:
        if amount > self.remaining:
            raise ValueError("gift card empty")
        self.remaining -= amount
        return f"gift:{amount}{currency}"
```

Still works with `checkout_duck`. That is the point — and the risk.

---

# ABC — Nominal Contract

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: int, currency: str) -> str:
        """Amount is integer minor units (cents)."""
```

- `PaymentProcessor()` → **`TypeError`**
- `isinstance(stripe, PaymentProcessor)` True only if it **subclasses**
- Incomplete subclass fails at **`PaypalProcessor()`**, not at first charge

---

# Concrete Processors

```python
class StripeProcessor(PaymentProcessor):
    def charge(self, amount: int, currency: str) -> str:
        return f"stripe:{self.merchant}:{amount}{currency}"

def checkout(processor: PaymentProcessor, amount: int) -> str:
    return processor.charge(amount, "USD")
```

You **own** this hierarchy. Force the name.

---

# Protocol — Structural

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Chargeable(Protocol):
    def charge(self, amount: int, currency: str) -> str: ...
```

- `GiftCard` is a `Chargeable` **without inheriting**
- `StripeProcessor` matches too
- Like **Go**: implement by having the methods

---

# `@runtime_checkable`

Without it, `isinstance(card, Chargeable)` raises `TypeError`.

With it:

```python
isinstance(card, Chargeable)            # True
isinstance(card, PaymentProcessor)      # False
```

Checks **names exist**, not signatures. Coarse filter only.

---

# Pick One Per Function

- **ABC** — you control subclasses (`PaymentProcessor`)
- **Protocol** — you do not own the objects (`GiftCard`)
- **Duck** — tiny internal helpers

`checkout` vs `checkout_duck` in the demo is teaching. Production: **one**.

---

# Java vs Go vs Python

```java
class GiftCard implements PaymentProcessor { }
```

Must declare. Compiler refuses otherwise.

```go
// GiftCard implements Chargeable with no line of declaration
```

Python **Protocol** ≈ Go. Python **ABC** ≈ Java.

---

# Demo — `payments.py`

```bash
python payments.py
```

```
stripe:acct_ada:1999USD
paypal:500USD
stripe is PaymentProcessor: True
gift card is PaymentProcessor: False
gift card is Chargeable: True
gift:250USD
stripe:acct_ada:250USD
abstract: TypeError - missing charge
```

Last line wording varies by Python version. Name the **exception** and **`charge`**.

---

# Cents, Not Floats

`amount: int` is minor units.

`19.99` as `float` is a money bug. Episode 6 stores cents on `Money`.

Polymorphism does not excuse a sloppy domain type.

---

# Key Takeaways

- Duck typing: the method is the contract
- ABC: **nominal**, fail at construction
- Protocol: **structural**, mainly for type checkers
- `@runtime_checkable` ≠ signature check
- ABC if you own the tree; Protocol if you do not
- One contract per function
- Money as **integers**

---

# What's Next — Episode 6

**Dunders & Composition**

- `__repr__` / `__str__` / `__eq__` / `__hash__`
- Operators `__add__` / `__mul__`
- `__len__` / `__iter__`
- `Money` composed into `Order` — not inherited

**The Debugger Diary** — Python OOP from Scratch
_"Understand the tools, not just the syntax."_
