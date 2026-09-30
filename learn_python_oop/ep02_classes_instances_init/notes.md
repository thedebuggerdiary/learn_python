# Episode 2 — Classes, Instances & `__init__`

**Series:** Python OOP from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episode 1 — `self`, `__init__`, identity of mutable objects.

---

## Episode Overview

By the end of this episode you will know where Python looks up an attribute (instance dict, then class, then bases), why `transactions = []` on the class is the same identity bug as a mutable default, and when to use `@classmethod` versus `@staticmethod`. The demo is a `User` with an alternate constructor `from_email` and an `Account` that records transactions correctly, next to a `BrokenAccount` that shares one list across every instance.

---

## Section 1: The Class Statement Runs Once

`class` is executable. Python creates a new namespace, runs the body, then binds the resulting class object to the name.

```python
class User:
    species = "human"          # runs now, once

    def __init__(self, name: str) -> None:
        self.name = name       # runs later, per instance
```

**Class body**
Assignments and `def` statements execute at definition time. `species = "human"` is stored on the class. `def __init__` creates a function object and stores it on the class under the name `__init__`.

**Instances**
`User("Ada")` allocates an instance and calls `__init__`. The instance gets its own `__dict__` (unless you use `__slots__`, which this series does not). `self.name = name` writes into that dict.

You can inspect both:

```python
ada = User("Ada")
print(ada.__dict__)     # {'name': 'Ada'}
print(User.__dict__["species"])  # human
```

`ada.species` works even though `species` is not in `ada.__dict__`. Lookup walks outward.

---

## Section 2: Attribute Lookup

Reading `ada.email` is a search:

1. The instance's `__dict__` (or slots)
2. The class's `__dict__`
3. Each base class, in MRO order (Episode 4)

Writing `ada.email = "..."` **always** writes on the instance (for a normal attribute). It does not update the class. That asymmetry is why `ada.roles.append("admin")` and `ada.roles = ["admin"]` are different operations: the first mutates the object found by lookup (often the class list); the second installs a new list on the instance.

```python
class User:
    roles: list[str] = ["viewer"]

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
```

| Expression | Read finds | Write goes to |
|---|---|---|
| `ada.name` | instance | instance |
| `ada.roles` | class (no instance key) | — |
| `ada.roles.append(...)` | class list, then mutates it | the list object |
| `ada.roles = ["admin"]` | — | instance, shadows the class attr |
| `User.roles` | class | class |

---

## Section 3: Instance Attributes vs Class Attributes

**Instance attributes** are per object. Put anything that differs between instances here: name, email, a transaction list.

**Class attributes** are shared. Put constants, defaults that you never mutate, and data that is genuinely one copy for the type: `species`, a registry, a format string.

Shared **mutable** class attributes are a bug almost every time. The intent was a default empty list per account. The result is one list for the program.

```python
class BrokenAccount:
    transactions: list[tuple[str, float]] = []

    def __init__(self, owner: "User", number: str) -> None:
        self.owner = owner
        self.number = number

    def record(self, kind: str, amount: float) -> None:
        self.transactions.append((kind, amount))
```

`self.transactions` on a new instance is `BrokenAccount.transactions`. `append` mutates that list. A second instance sees the first instance's deposits.

The fix is the same as Episode 1: create the list in `__init__`.

```python
class Account:
    def __init__(self, owner: "User", number: str) -> None:
        self.owner = owner
        self.number = number
        self.transactions: list[tuple[str, float]] = []

    def record(self, kind: str, amount: float) -> None:
        self.transactions.append((kind, amount))
```

Immutable class attributes are fine: `DEFAULT_ROLE = "viewer"` as a string. Nobody appends to a string in place.

---

## Section 4: Methods Are Functions on the Class

```python
ada = User.from_email("ada@example.com")
print(ada.record)           # if it existed — bound method
print(Account.record)       # function
print(Account.record(ada_account, "deposit", 10))
```

**Unbound (on the class)**
`Account.record` is a function. You must pass the instance yourself.

**Bound (on the instance)**
`good_a.record` is a bound method: the instance is already filled in. `good_a.record("deposit", 25)` calls `Account.record(good_a, "deposit", 25)`.

This is why you declare `self`. Python does not invent a hidden `this`; it inserts the instance as argument zero.

---

## Section 5: `@classmethod` — Alternate Constructors

A class method receives the **class** as its first argument, conventionally `cls`, not an instance. Use it when the method needs to construct or talk about the type, including subclasses.

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

**`cls`**
If you later write `class Admin(User):` and call `Admin.from_email("a@x.com")`, `cls` is `Admin`, so you get an `Admin` instance. If `from_email` hardcoded `return User(...)`, subclasses would be broken. That is the reason `cls` exists.

**When to use it**
Alternate constructors (`from_email`, `from_json`, `from_row`), bookkeeping that lives on the type (`User.all_emails` if you had a registry), and anything that must respect subclassing.

Java's `static` factory `User.fromEmail` does not automatically become a subclass factory. Python's `@classmethod` does, because it receives the actual class that was called.

---

## Section 6: `@staticmethod` — A Function in the Class Namespace

A static method receives neither instance nor class. It is a function grouped with the class for naming.

```python
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email.split("@", 1)[-1]
```

Call it as `User.is_valid_email("ada@example.com")` or `ada.is_valid_email(...)`. Both work; neither passes `self`.

**When to use it**
Rarely. If it does not need `self` or `cls`, a module-level function `is_valid_email` is clearer and easier to test. Use `@staticmethod` when you want the name next to the class in docs and `dir(User)`, or when a library API expects a method on the type.

If you find a class whose every method is static, you wanted a module.

---

## Section 7: Compare to Java `static`

```java
public class User {
    public static User fromEmail(String email) {
        String name = email.split("@")[0];
        return new User(name, email);
    }

    public static boolean isValidEmail(String email) {
        return email.contains("@");
    }
}
```

Java has one `static`. Python splits that idea in two:

| Python | Receives | Java analogue |
|---|---|---|
| instance method | `self` | ordinary method |
| `@classmethod` | `cls` | `static` factory that should have been polymorphic |
| `@staticmethod` | nothing | `static` helper |

There is no `new User()` keyword. `User(...)` calls `type.__call__`, which calls `__new__` then `__init__`. `cls(...)` in a classmethod is the same path with a possibly subclassed `cls`.

---

## Section 8: `type()` vs the Class Object

```python
ada = User.from_email("ada@example.com")
print(type(ada))          # <class '__main__.User'>
print(type(ada) is User)  # True
print(isinstance(ada, User))  # True
```

**`type(ada)`**
The exact class of the instance. After inheritance (Episode 4), `type(sms) is Notification` is False while `isinstance(sms, Notification)` is True. Prefer `isinstance` for "can I treat this as an X?" Prefer `type(x) is C` only when you mean exactly `C`, no subclasses.

`User` itself has type `type`. `type(User)` is `type`. Metaclasses change that; this series does not need them.

---

## Section 9: Running the Demo

`code/user_account.py` defines `User`, `Account`, and `BrokenAccount`.

```bash
python user_account.py
```

Output:

```
valid email: True
from_email: User(name='ada', email='ada@example.com')
good A: [('deposit', 25)]
good B: []
broken A: [('deposit', 25)]
broken B: [('deposit', 25)]
same list: True
on the class: [('deposit', 25)]
Ada.roles: ['viewer', 'admin']
class roles: ['viewer', 'admin']
new user roles: ['viewer', 'admin']
```

Two leaks, one lesson. `BrokenAccount.transactions` is one list. `User.roles` is one list; `ada.roles.append("admin")` mutates the class default, so a user created afterward is already `"admin"`.

The repair for roles is the same as for transactions: set `self.roles = ["viewer"]` in `__init__`, or use an immutable default (`tuple`) if the value should never change per instance.

---

## Section 10: `__init__` Patterns Worth Using

**Required fields first, defaults after** — same rule as functions.

**Do not do I/O in `__init__`** unless the class is explicitly a "connected" resource. Opening files, talking to the network, or reading the clock makes the object hard to test. A classmethod `from_path(cls, path)` that reads then calls `cls(...)` keeps construction data-only.

**`__init__` should not return.** Returning a value raises `TypeError: __init__() should return None`. If you need a factory that returns a cached instance, that is `__new__` or a classmethod, not a return from `__init__`.

**Annotate `self` attributes in `__init__`** so checkers and readers know the shape: `self.transactions: list[tuple[str, float]] = []`.

---

## Key Takeaways

- The `class` body runs once; `__init__` runs per instance.
- Attribute **read** walks instance → class → bases; **write** of a normal attribute goes to the instance.
- Mutable objects on the class are shared by every instance — `transactions = []` is a bug.
- `instance.method(...)` is `Class.method(instance, ...)`.
- `@classmethod` receives `cls` so alternate constructors respect subclasses.
- `@staticmethod` receives nothing; prefer a module function unless the name belongs on the class.
- `isinstance` is for types-and-subtypes; `type(x) is C` is for an exact class.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| All instances share one list | Class attribute `transactions = []` plus `self.transactions.append` | `self.transactions = []` in `__init__` |
| `TypeError: ... missing 1 required positional argument: 'self'` | Called an instance method on the class without passing an instance: `Account.record("deposit", 1)` | `Account.record(acct, "deposit", 1)` or `acct.record("deposit", 1)` |
| `TypeError: from_email() takes 1 positional argument but 2 were given` | Forgot `@classmethod`; the call `User.from_email(email)` passed the class into a function that expected only `email` | Add `@classmethod` and `cls` |
| `TypeError: is_valid_email() takes 1 positional argument but 2 were given` | Forgot `@staticmethod` / `@classmethod`; instance call passed `self` | Add the decorator, or call `User.is_valid_email(email)` on a real staticmethod |
| Subclass `from_email` returns the base class | Used `return User(...)` instead of `return cls(...)` | Construct with `cls` |

---

## Further Reading

- [Python tutorial — classes](https://docs.python.org/3/tutorial/classes.html) — scopes, class objects, and instance objects
- [classmethod and staticmethod](https://docs.python.org/3/library/functions.html#classmethod) — official definitions
- Episode 3: Encapsulation & Properties — `_` vs `__`, `@property`, setters, and validating a `Temperature` type
