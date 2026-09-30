# Episode 4 — Inheritance & `super()`

**Series:** Python OOP from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episode 3 — attributes, `_` / `__`, properties.

---

## Episode Overview

By the end of this episode you will use single inheritance without cargo-culting Java class trees, you will know what `super()` actually looks up (the next class in the MRO, not "my parent"), and you will prefer `isinstance` over `type() is` when you mean "this or a subclass." The demo is a `Notification` base with `Email` and `SMS` subclasses, plus a `Logged` mixin composed as `LoggedEmail(Logged, Email)`.

---

## Section 1: Inheritance Is Sharing, Not Taxonomy

A subclass reuses a base class's attributes and methods, then overrides or extends them. Python uses the same `class Child(Parent):` syntax as Java, but it does not push you toward deep trees. Most production Python is one or two levels, or a mixin plus a concrete class.

```python
class Notification:
    def __init__(self, recipient: str) -> None:
        self.recipient = recipient
        self.sent = False

    def send(self, body: str) -> str:
        raise NotImplementedError("use a subclass")

    def mark_sent(self) -> None:
        self.sent = True
```

**`Notification`**
Holds the shared state (`recipient`, `sent`) and a hook `send` that the base cannot implement. Raising `NotImplementedError` is the light version of an abstract method. Episode 5 replaces this with `abc.ABC` so you cannot even construct `Notification()`.

**`class Email(Notification):`**
`Email` is a `Notification`. Every `Email` instance has `recipient` and `sent`. `isinstance(email, Notification)` is True.

Do not invent a hierarchy because the domain has categories. If Email and SMS only share `recipient` and `sent`, that is a small base. If they share nothing but a verb `send`, that is a Protocol (Episode 5), not a parent class.

---

## Section 2: `super()` Forwards Along the MRO

```python
class Email(Notification):
    def __init__(self, recipient: str, sender: str) -> None:
        super().__init__(recipient)
        self.sender = sender

    def send(self, body: str) -> str:
        line = f"email from {self.sender} to {self.recipient}: {body}"
        self.mark_sent()
        return line
```

**`super().__init__(recipient)`**
In Python 3, `super()` with no arguments is correct inside a method. It does not mean "call my literal parent." It means "call the next method in this instance's MRO." For a plain `Email`, that next class is `Notification`. For `LoggedEmail`, the chain is longer — Section 6.

**Why not `Notification.__init__(self, recipient)`?**
Hard-coding the base breaks cooperative multiple inheritance. A mixin that also needs `__init__` would be skipped. `super()` is the cooperative form; use it even when you have one parent, so the day you add a mixin you are not rewriting constructors.

**Java `super()`**
Java `super(recipient)` calls the direct superclass constructor and nothing else. Python `super()` is MRO-aware. Same word, different lookup.

---

## Section 3: `SMS` — Same Shape, Different Channel

```python
class SMS(Notification):
    def __init__(self, recipient: str, gateway: str) -> None:
        super().__init__(recipient)
        self.gateway = gateway

    def send(self, body: str) -> str:
        line = f"sms via {self.gateway} to {self.recipient}: {body}"
        self.mark_sent()
        return line
```

`dispatch` does not care which subclass it received:

```python
def dispatch(note: Notification, body: str) -> str:
    return note.send(body)
```

That is runtime polymorphism: one call site, two implementations. Java does this with virtual methods. Python does it with attribute lookup. There is no `virtual` keyword. If `send` exists on the instance's class, that is the method that runs.

---

## Section 4: `isinstance` vs `type()`

```python
email = Email("ada@example.com", sender="noreply@app.test")
print(isinstance(email, Notification))  # True
print(type(email) is Notification)      # False
```

**`isinstance(obj, cls)`**
True if `obj`'s class is `cls` or a subclass. This is the question you almost always mean: "can I treat this as a Notification?"

**`type(obj) is cls`**
True only for that exact class. Use it when a subclass must *not* match — serializers, registries, or "this is the base sentinel." Default to `isinstance`.

`isinstance(email, (Email, SMS))` accepts either. `isinstance` also understands virtual subclasses registered with ABCs (Episode 5).

---

## Section 5: The MRO Is a List, Not a Tree Walk

Python computes a linear order of classes with the C3 algorithm. You can print it:

```python
print(Email.__mro__)
# (Email, Notification, object)
```

Attribute lookup for `email.send` walks that tuple left to right until it finds `send`. `object` is always last: every new-style class inherits from `object`.

**C3 in one sentence**
Children come before parents; the order of bases in the class header is preserved; the same class appears once.

If C3 cannot build an order (a contradictory diamond), you get `TypeError: Cannot create a consistent method resolution order`. That is a design bug, not a puzzle to clever around.

---

## Section 6: Mixins and `super()` Cooperation

A mixin is a class meant to be combined, not instantiated alone. `Logged` wraps `send`:

```python
class Logged:
    def send(self, body: str) -> str:
        result = super().send(body)  # type: ignore[misc]
        print(f"LOG: {result}")
        return result


class LoggedEmail(Logged, Email):
    pass
```

**Base order**
`LoggedEmail(Logged, Email)` puts `Logged` first. MRO:

```
LoggedEmail → Logged → Email → Notification → object
```

`Logged.send` calls `super().send`, which is `Email.send`, which calls `mark_sent`. The log line runs after the real send. Swap to `LoggedEmail(Email, Logged)` and `Email.send` is found first — `Logged.send` never runs. Mixin order is part of the API.

**`type: ignore[misc]`**
Alone, `Logged` is not a `Notification`. Checkers complain that `super().send` is wrong. At runtime, `Logged` is only used under `LoggedEmail`, where `super()` is valid. Mixins often look incomplete in isolation. That is expected.

**Java has no mixins**
Java uses interfaces with default methods (Java 8+) or wrappers. Python mixins are classes. They can hold state; they usually should not. If the mixin needs data, prefer composition (Episode 6): an `Order` that *has* line items, not *is* a list.

---

## Section 7: When Inheritance Is the Wrong Tool

- **`Utils` / `BaseManager` with no instances** — a module.
- **`class Square(Rectangle)`** because a square "is a" rectangle — the Liskov trap: `rect.width = 3; rect.height = 4` does not hold for squares. Use a `Shape` protocol or separate types.
- **Deep trees to share one helper** — a function, or composition.
- **Copying a Java domain model** with `AbstractFooFactory`. Python will let you, and then you will fight the MRO.

Inheritance is for genuine "is-a plus shared implementation." Shared *behavior without shared identity* is a Protocol or a function.

---

## Section 8: Compare to Java

```java
public abstract class Notification {
    protected final String recipient;
    public abstract String send(String body);
}
public class Email extends Notification { ... }
```

Java: `extends` one class, `implements` many interfaces, `super()` is the parent constructor. `abstract` prevents `new Notification()`.

Python: multiple concrete bases are allowed; `super()` is MRO; abstract is optional until you opt into `ABC`. `Notification("x").send("nope")` constructs and then raises `NotImplementedError`. Episode 5 moves the failure to construction time.

---

## Section 9: Running the Demo

`code/notifications.py`:

```bash
python notifications.py
```

Output:

```
email from noreply@app.test to ada@example.com: welcome
sms via twilio to +15550100: otp 123456
email is Notification: True
type is Notification: False
MRO LoggedEmail: ['LoggedEmail', 'Logged', 'Email', 'Notification', 'object']
LOG: email from noreply@app.test to ada@example.com: welcome
base send: use a subclass
```

Walk it:

1. `dispatch` prints Email and SMS lines — one function, two classes.
2. `isinstance` vs `type is` — subclass vs exact class.
3. MRO list — `Logged` before `Email`.
4. `LoggedEmail` prints `LOG:` then the same email line (the LOG is printed inside `send`; `dispatch` returns the line and `main` does not print it a second time).
5. Bare `Notification.send` raises `NotImplementedError`.

---

## Section 10: `super()` in `__init__` Chains

If both mixin and concrete class define `__init__`, every class should call `super().__init__(**kwargs)` or accept `*args, **kwargs` and pass them on. That is cooperative construction. This demo keeps `__init__` only on `Notification` / `Email` / `SMS`; `Logged` has no `__init__`, so `LoggedEmail(...)` goes `LoggedEmail` (nothing) → `Logged` (nothing) → `Email.__init__`. Simple on purpose.

When you add mixin state, give the mixin `__init__` that calls `super().__init__` and only reads its own keyword arguments. Signature design becomes the hard part — another reason composition is often cheaper.

---

## Key Takeaways

- A subclass shares implementation; it is not mandatory taxonomy.
- `super()` follows the instance MRO, not a hardcoded parent.
- `isinstance` means "this type or a subclass"; `type is` means exact.
- C3 linearizes bases; print `__mro__` when lookup surprises you.
- Mixin order in the class header is behavior: `Logged` before `Email` wraps `send`.
- Prefer a shallow tree or a mixin over a Java-style forest.
- `NotImplementedError` in a base is a runtime hint; ABCs fail at construction (Episode 5).

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `NotImplementedError: use a subclass` | Called `send` on `Notification` itself | Instantiate `Email` or `SMS` |
| Mixin methods never run | Bases listed as `(Email, Logged)` so `Email.send` wins | Put the mixin first: `(Logged, Email)` |
| `TypeError: Cannot create a consistent method resolution order` | Contradictory diamond | Redesign bases; do not force C3 |
| `TypeError: __init__() got an unexpected keyword argument` | Cooperative mixin `__init__` did not accept/forward kwargs | Use `**kwargs` and `super().__init__(**kwargs)` |
| Forgot `super().__init__` | Subclass `__init__` replaced the base; `recipient` missing | Call `super().__init__(...)` first |

---

## Further Reading

- [Tutorial — Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)
- [super()](https://docs.python.org/3/library/functions.html#super)
- [C3 method resolution](https://www.python.org/download/releases/2.3/mro/) — Raymond Hettinger / Python 2.3 docs
- Episode 5: Polymorphism, ABCs & Protocols — duck typing, `ABC` / `@abstractmethod`, `Protocol`, `runtime_checkable`
