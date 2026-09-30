---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Classes, Instances & `__init__`
### Episode 2 — Python OOP from Scratch
**The Debugger Diary**

---

# The Class Body Runs Once

```python
class User:
    species = "human"          # now, once

    def __init__(self, name: str) -> None:
        self.name = name       # later, per instance

ada = User("Ada")
print(ada.__dict__)            # {'name': 'Ada'}
print(User.species)            # human
```

Methods are **functions stored on the class**. Instances share them.

---

# Attribute Lookup

Reading `ada.roles` searches:

1. **Instance** `__dict__`
2. **Class** `__dict__`
3. **Bases** (MRO — Episode 4)

Writing `ada.email = "..."` writes on the **instance**.

`append` is not a write to `ada.roles` — it mutates the list lookup found.

---

# Instance vs Class Data

- **Instance** — differs per object: `name`, `email`, a ledger
- **Class** — one copy for the type: constants, true shared state
- Mutable class attributes are **shared identity**

```python
class BrokenAccount:
    transactions: list[tuple[str, float]] = []  # one list
```

Same bug as `def f(x=[])` from Episode 1.

---

# The Fix — Create Mutables in `__init__`

```python
class Account:
    def __init__(self, owner: User, number: str) -> None:
        self.owner = owner
        self.number = number
        self.transactions: list[tuple[str, float]] = []

    def record(self, kind: str, amount: float) -> None:
        self.transactions.append((kind, amount))
```

Each instance gets a **new** list.

---

# Bound vs Unbound

```python
good_a.record("deposit", 25)
Account.record(good_a, "deposit", 25)   # equivalent
```

| Looked up on | What you get |
|---|---|
| instance | **bound method** — `self` already filled |
| class | **function** — you pass the instance |

Python does not hide `this`. It inserts argument zero.

---

# `@classmethod` — Alternate Constructor

```python
class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    @classmethod
    def from_email(cls, email: str) -> "User":
        local = email.split("@", 1)[0]
        return cls(name=local, email=email)
```

**`cls`** is the class that was called — subclasses stay subclasses.

---

# `@staticmethod` — Namespace Only

```python
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email.split("@", 1)[-1]

User.is_valid_email("ada@example.com")  # True
```

Receives **neither** `self` nor `cls`.

If nothing needs the class, a **module function** is usually clearer.

---

# Java `static` Splits in Two

```java
public static User fromEmail(String email) { ... }
public static boolean isValidEmail(String email) { ... }
```

| Python | Receives |
|---|---|
| instance method | `self` |
| `@classmethod` | `cls` |
| `@staticmethod` | nothing |

`User(...)` is a call, not a `new` keyword. `cls(...)` uses the same path.

---

# `type` vs `isinstance`

```python
ada = User.from_email("ada@example.com")
print(type(ada) is User)       # True
print(isinstance(ada, User))   # True
```

- **`type(x) is C`** — exact class
- **`isinstance(x, C)`** — `C` or a subclass (Episode 4)

Prefer **`isinstance`** for "can I use this as a C?"

---

# Demo — Shared `roles` Too

```bash
python user_account.py
```

```
good A: [('deposit', 25)]
good B: []
broken A: [('deposit', 25)]
broken B: [('deposit', 25)]
same list: True
Ada.roles: ['viewer', 'admin']
new user roles: ['viewer', 'admin']
```

`ada.roles.append("admin")` mutated **`User.roles`**. The next user is already admin.

---

# `__init__` Habits

- Required fields first — same as functions
- **No I/O** in `__init__` — use `from_path` classmethods
- Do not **return** a value
- Annotate attributes: `self.transactions: list[...] = []`

Returning from `__init__` → `TypeError: __init__() should return None`.

---

# Key Takeaways

- Class body once; `__init__` per instance
- Read walks **out**; normal write stays on the **instance**
- `transactions = []` on the class is shared
- Bound method = function + instance
- `@classmethod` + **`cls(...)`** for factories
- `@staticmethod` is a namespaced function — often a module fn
- `isinstance` over exact `type` for subtypes

---

# What's Next — Episode 3

**Encapsulation & Properties**

- Public by convention, `_`, `__` name mangling
- `@property`, setter, deleter
- Computed attributes
- Validating `Temperature` (Celsius / Fahrenheit)

**The Debugger Diary** — Python OOP from Scratch
_"Understand the tools, not just the syntax."_
