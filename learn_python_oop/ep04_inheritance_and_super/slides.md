---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Inheritance & `super()`
### Episode 4 — Python OOP from Scratch
**The Debugger Diary**

---

# Inheritance Is Sharing

```python
class Notification:
    def __init__(self, recipient: str) -> None:
        self.recipient = recipient
        self.sent = False

    def send(self, body: str) -> str:
        raise NotImplementedError("use a subclass")
```

Share **implementation**. Do not build a taxonomy because the domain has categories.

---

# `super()` Follows the MRO

```python
class Email(Notification):
    def __init__(self, recipient: str, sender: str) -> None:
        super().__init__(recipient)
        self.sender = sender
```

- Not "my parent" — **the next class on this instance's MRO**
- Hard-coding `Notification.__init__(self, ...)` breaks mixins
- Java `super()` is the superclass constructor — **different lookup**

---

# Same Call Site, Two Types

```python
def dispatch(note: Notification, body: str) -> str:
    return note.send(body)

dispatch(Email(..., sender="noreply@app.test"), "welcome")
dispatch(SMS(..., gateway="twilio"), "otp 123456")
```

No `virtual` keyword. Lookup finds `send` on the **instance's class**.

---

# `isinstance` vs `type is`

```python
isinstance(email, Notification)  # True  — Email or subclass
type(email) is Notification      # False — exact class only
```

Ask **"can I treat this as a Notification?"** — that is `isinstance`.

Use `type is` for exact-class registries and sentinels.

---

# MRO Is a List

```python
Email.__mro__
# (Email, Notification, object)
```

- Lookup walks **left to right**
- C3: child before parent; header order preserved; each class once
- Contradiction → `TypeError: Cannot create a consistent method resolution order`

Print `__mro__` when a method "isn't the one you wrote."

---

# Mixin: `Logged` Wraps `send`

```python
class Logged:
    def send(self, body: str) -> str:
        result = super().send(body)  # type: ignore[misc]
        print(f"LOG: {result}")
        return result

class LoggedEmail(Logged, Email):
    pass
```

`Logged` first. MRO: `LoggedEmail → Logged → Email → Notification → object`

---

# Mixin Order Is Behavior

| Header | Who wins `send` |
|---|---|
| `(Logged, Email)` | `Logged` wraps `Email` |
| `(Email, Logged)` | `Email.send` — **log never runs** |

Java: one `extends`, many `implements`.
Python: mixin is a **class**. Prefer no state on mixins.

---

# When Not to Inherit

- `Utils` / `BaseManager` with no instances → **module**
- `Square(Rectangle)` → Liskov trap
- Deep tree for one helper → **function** or composition
- Copied Java `AbstractFooFactory`

Is-a **plus shared implementation**. Shared verb only → Protocol (Ep 5).

---

# Java Contrast

```java
public abstract class Notification {
    public abstract String send(String body);
}
// new Notification() — compile error
```

Python `Notification("x")` **constructs**. `.send()` raises at **call** time.
Episode 5: `ABC` fails at **construction**.

---

# Demo — `notifications.py`

```bash
python notifications.py
```

```
email from noreply@app.test to ada@example.com: welcome
sms via twilio to +15550100: otp 123456
email is Notification: True
type is Notification: False
MRO LoggedEmail: ['LoggedEmail', 'Logged', 'Email', 'Notification', 'object']
LOG: email from noreply@app.test to ada@example.com: welcome
base send: use a subclass
```

---

# Key Takeaways

- Inheritance shares implementation — not mandatory taxonomy
- `super()` = next on the **MRO**, not "my parent"
- `isinstance` vs exact `type is`
- Print `__mro__` when lookup surprises you
- Mixin **header order** is the wrap order
- Shallow trees; mixins over forests
- `NotImplementedError` is a runtime hint

---

# What's Next — Episode 5

**Polymorphism, ABCs & Protocols**

- Duck typing vs Java interfaces
- `abc.ABC` / `@abstractmethod`
- `typing.Protocol` / `@runtime_checkable`
- Payment processors: nominal vs structural

**The Debugger Diary** — Python OOP from Scratch
_"Understand the tools, not just the syntax."_
