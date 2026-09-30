# Episode 5 — Polymorphism, ABCs & Protocols

**Series:** Python OOP from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episode 4 — inheritance, `super()`, `isinstance`.

---

## Episode Overview

By the end of this episode you will distinguish duck typing, nominal types (`ABC`), and structural types (`Protocol`). You will know when `isinstance` against an ABC is a contract you opted into by subclassing, and when `@runtime_checkable` Protocol is a shape check that a `GiftCard` can pass without inheriting anything. The demo is `checkout` over `StripeProcessor` / `PaypalProcessor`, then the same `charge` method on a gift card that is not a `PaymentProcessor`.

---

## Section 1: Polymorphism Without a Shared Base

`dispatch` in Episode 4 worked because Email and SMS shared a parent. Python also lets you call `charge` on anything that has `charge`. That is duck typing: if it walks and quacks, the function does not ask for a pedigree.

```python
def checkout_duck(processor: Chargeable, amount: int) -> str:
    return processor.charge(amount, "USD")
```

The annotation `Chargeable` is for readers and type checkers. At runtime this function will call `.charge` on whatever you pass. A missing method is an `AttributeError` at the call, not a compile error.

Java requires an `interface` or a shared superclass before `processor.charge(...)` type-checks. Python will run the call regardless. Types are optional; the object protocol is not.

---

## Section 2: Duck Typing Is a Runtime Contract

```python
class GiftCard:
    def __init__(self, remaining: int) -> None:
        self.remaining = remaining

    def charge(self, amount: int, currency: str) -> str:
        if amount > self.remaining:
            raise ValueError("gift card empty")
        self.remaining -= amount
        return f"gift:{amount}{currency}"
```

`GiftCard` never mentions `PaymentProcessor`. `checkout_duck(card, 250)` still works. That is the flexibility people mean by "Pythonic." It is also the failure mode: a typo `charage` fails in production, not in `javac`.

Use duck typing at the edges (adapters, tests, scripts). Use an ABC or Protocol at the center of a library, where you want a documented contract and a good error.

---

## Section 3: ABCs — Nominal, Checked at Construction

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: int, currency: str) -> str:
        """Amount is integer minor units (cents)."""
```

**`ABC`**
A metaclass hook. Instantiating a class that still has abstract methods raises `TypeError`. Episode 4's `Notification` constructed and failed later. An ABC fails when you write `PaymentProcessor()`.

**`@abstractmethod`**
Marks a method that subclasses must implement. The body can be `...` or a docstring; it will not run unless a subclass calls `super().charge(...)` on purpose.

**Nominal**
`isinstance(stripe, PaymentProcessor)` is True because `StripeProcessor` *subclasses* `PaymentProcessor`. `GiftCard` is not a `PaymentProcessor` no matter how perfect its `charge` method is. You opted into the name.

Java `interface PaymentProcessor { String charge(...); }` is the same idea: the type is the name you implement, not the shape you happen to have (until Java's unnamed classes / Go-style... they still do not do Python Protocols).

---

## Section 4: Concrete Processors

```python
class StripeProcessor(PaymentProcessor):
    def __init__(self, merchant: str) -> None:
        self.merchant = merchant

    def charge(self, amount: int, currency: str) -> str:
        return f"stripe:{self.merchant}:{amount}{currency}"


class PaypalProcessor(PaymentProcessor):
    def charge(self, amount: int, currency: str) -> str:
        return f"paypal:{amount}{currency}"
```

If you forget `charge` on a subclass, `PaypalProcessor()` raises `TypeError` naming the missing abstract method. That is the point of the ABC: fail at the factory, not at the first payment at 2 a.m.

```python
def checkout(processor: PaymentProcessor, amount: int) -> str:
    return processor.charge(amount, "USD")
```

Callers of `checkout` are expected to pass a `PaymentProcessor`. A type checker enforces that. The runtime still only needs `.charge`. `checkout(card, 250)` would work at runtime and fail `mypy` — you would use `checkout_duck` for that.

---

## Section 5: Protocols — Structural Typing

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Chargeable(Protocol):
    def charge(self, amount: int, currency: str) -> str: ...
```

**`Protocol`**
A typing construct: "anything with this method signature." `GiftCard` matches `Chargeable` without inheriting it. `StripeProcessor` matches too, because it has `charge`.

**Static vs runtime**
Without `@runtime_checkable`, `isinstance(card, Chargeable)` is a `TypeError`. Protocols are primarily for type checkers. `@runtime_checkable` makes `isinstance` walk the methods and return True if they exist. It does **not** check signatures — only that the names are present.

**Go analogy**
Go interfaces are structural: you implement `io.Reader` by having `Read`. Python `Protocol` is that idea in the type system. ABCs are Java interfaces.

---

## Section 6: When to Use Which

| Tool | Relationship | Fail time | `isinstance` |
|---|---|---|---|
| Duck typing | none | missing attribute at call | you don't |
| `ABC` | must subclass | constructing a concrete class | nominal, True for subclasses |
| `Protocol` | has the methods | type check (and `isinstance` if runtime_checkable) | structural if decorated |

**ABC** when you own the hierarchy and want to forbid incomplete subclasses (`PaymentProcessor`).

**Protocol** when you do not own the objects (stdlib types, third-party classes, `GiftCard` in another package) and still want to type `checkout_duck`.

**Duck typing** when the function is tiny and the audience is you.

Do not stack all three on every API. `checkout` is ABC-typed. `checkout_duck` is Protocol-typed. The demo shows both on purpose; a real module picks one per function.

---

## Section 7: `runtime_checkable` Pitfalls

`isinstance(x, Chargeable)` does not prove `charge` takes `(amount, currency)`. A method `charge(self)` still passes the check. Treat runtime Protocol checks as a coarse filter, not as validation.

Calling `issubclass(GiftCard, Chargeable)` works for runtime_checkable Protocols with only methods. Protocols with data members (`remaining: int`) have restrictions — stick to methods in this series.

---

## Section 8: Compare to Java and Go

```java
public interface PaymentProcessor {
    String charge(int amount, String currency);
}
public class GiftCard implements PaymentProcessor { ... }
```

Without `implements`, Java will not pass `GiftCard` to `checkout(PaymentProcessor p)`.

```go
type Chargeable interface {
    Charge(amount int, currency string) string
}
```

Go: GiftCard implements Chargeable with no declaration. Python Protocol matches Go; Python ABC matches Java.

---

## Section 9: Running the Demo

`code/payments.py`:

```bash
python payments.py
```

Output (the last line is a `TypeError` whose text names `PaymentProcessor` and `charge`; wording varies slightly by Python version):

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

Walk it:

1. ABC checkout works for Stripe and Paypal.
2. Gift card is not a `PaymentProcessor` (nominal).
3. Gift card *is* `Chargeable` (structural, runtime_checkable).
4. `checkout_duck` accepts both the gift card and Stripe.
5. `PaymentProcessor()` is illegal.

Do not screenshot-depend on the exact `TypeError` string; Python 3.12+ reworded it. Name the exception type and the missing method on camera.

---

## Section 10: Amounts as Integers

`charge` takes `amount: int` in minor units (cents). Float dollars (`19.99`) are a classic money bug. Episode 6 stores cents on `Money` for the same reason. Polymorphism is not an excuse for a sloppy domain type.

---

## Key Takeaways

- Duck typing: call the method; the type is implied by use.
- ABCs are nominal: you subclass, construction fails if abstract methods remain.
- Protocols are structural: the shape is enough for type checkers.
- `@runtime_checkable` enables `isinstance`; it does not check signatures.
- Use an ABC when you own the hierarchy; a Protocol when you do not.
- One function, one contract — do not require subclass *and* Protocol *and* luck.
- Money: integers (cents), not floats.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `TypeError: Can't instantiate abstract class PaymentProcessor ... charge` | Instantiated the ABC or a subclass that forgot `charge` | Implement `charge`, or instantiate `StripeProcessor` |
| `TypeError: Instance and class checks can only be used with @runtime_checkable protocols` | `isinstance(x, Chargeable)` without the decorator | Add `@runtime_checkable` or drop the check |
| `AttributeError: 'GiftCard' object has no attribute 'charge'` | Duck-typed call, missing method | Implement `charge` or pass a real processor |
| `mypy` error passing `GiftCard` to `checkout` | `checkout` is annotated `PaymentProcessor` | Use `checkout_duck` / `Chargeable`, or subclass the ABC |
| Gift card `isinstance(..., PaymentProcessor)` is False | Expected structural ABC | ABCs are nominal; use Protocol |

---

## Further Reading

- [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [Protocols and structural subtyping](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [PEP 544 — Protocols](https://peps.python.org/pep-0544/)
- Episode 6: Dunders & Composition — `__repr__` / `__eq__` / `__hash__`, operators, `Money` inside `Order`
