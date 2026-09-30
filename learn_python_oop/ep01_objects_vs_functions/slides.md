---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Objects vs Functions
### Episode 1 — Python OOP from Scratch
**The Debugger Diary**

---

# What This Series Is

- You already write **Python functions**, lists, dicts
- This series is the **object model**, not syntax from zero
- Java / Kotlin classes help as **contrast**, not a prerequisite
- Python **3.12+** — 3.14 is current stable

```bash
python --version
# Python 3.14.x
```

---

# Everything Is an Object

```python
def greet(name: str) -> str:
    return f"hello, {name}"

print(type(3))      # <class 'int'>
print(type(greet))  # <class 'function'>
print(type(str))    # <class 'type'>
```

- An object has **identity**, **type**, **state**
- Classes are objects too — instances of **`type`**
- A **class** is the factory; an **instance** is one value

---

# `is` vs `==`

```python
ada = {"owner": "Ada", "balance": 100.0}
grace = {"owner": "Ada", "balance": 100.0}

print(ada == grace)   # True  — same contents
print(ada is grace)   # False — two dict objects
```

- **`==`** — value (`__eq__`)
- **`is`** — identity (same object)
- Default class `==` is **identity** until you define `__eq__`
- Compare `None` with **`is` / `is not`**

---

# Compare to Java

```java
// Java: == is identity for objects; use equals()
ada.equals(grace)
ada == grace   // same reference?
```

```python
# Python: both operators work on objects
ada == grace   # value
ada is grace   # identity
```

No primitives in the Java sense. **`is` is not a faster `==`.**

---

# Account as a Dict + Functions

```python
def make_account(owner: str, balance: float = 0.0,
                 ledger: list | None = None) -> dict:
    if ledger is None:
        ledger = []
    return {"owner": owner, "balance": balance, "ledger": ledger}

def deposit(account: dict, amount: float) -> None:
    account["balance"] += amount
    account["ledger"].append(("deposit", amount))
```

Data in the dict. Behavior in module functions. **Valid Python.**

---

# The Mutable Default Bug

```python
def make_account_broken(owner: str, balance: float = 0.0,
                        ledger: list = []) -> dict:
    return {"owner": owner, "balance": balance, "ledger": ledger}

a = make_account_broken("Ada", 100)
b = make_account_broken("Grace", 50)
deposit(a, 25)
print(a["ledger"] is b["ledger"])  # True
print(b["ledger"])                 # [('deposit', 25)]
```

Defaults are evaluated **once**, at definition time. One list. Two accounts.

---

# The Same Account as a Class

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance
        self.ledger: list[tuple[str, float]] = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.ledger.append(("deposit", amount))
```

Per-instance list in **`__init__`**, not in the class body.

---

# `self` Is the Instance

```python
acct = BankAccount("Ada", 100)
acct.deposit(25)
# same as:
BankAccount.deposit(acct, 25)
```

- **`self`** is a convention — the first parameter is the instance
- Lookup: instance → class → bases
- Methods live on the **class**; instances share them

---

# `__init__` Is Not `new`

- Python **allocates** the instance (`__new__`)
- Then calls **`__init__(self, ...)`** to fill it in
- Return nothing from `__init__` (implicit `None`)
- Create mutables here: `self.ledger = []`

`__repr__` — developer string for the REPL:

```python
def __repr__(self) -> str:
    return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
```

---

# Java / Kotlin Contrast

```java
public void deposit(double amount) {
    this.balance += amount;   // this is implicit
}
```

```kotlin
fun deposit(amount: Double) {
    balance += amount
}
```

```python
def deposit(self, amount: float) -> None:
    self.balance += amount    # self is explicit
```

Forgetting `self` in the parameter list still passes the instance.

---

# When Not to Write a Class

- JSON / config **dict** passed through functions
- Every method is `@staticmethod` — use a **module**
- One blob of data for the whole program — **module-level** state
- `UserManager` / `Utils` with no instance state

Write a class when **state and operations travel together** and you need **many instances** that must not share mutables.

---

# Demo — `bank_account.py`

```bash
python bank_account.py
```

```
same values, different objects: True False
broken — Ada ledger: [('deposit', 25)]
broken — Grace ledger: [('deposit', 25)]
same list object: True
fixed dict — Grace ledger: []
class — Ada: BankAccount(owner='Ada', balance=125)
class — Grace ledger: []
identity: False equality by default: False
```

Three designs. One identity leak. Default `==` is still identity.

---

# The Error That Teaches `self`

```
TypeError: BankAccount.deposit() takes 1 positional
argument but 2 were given
```

- You wrote `def deposit(amount):`
- The call `acct.deposit(25)` still passed **`acct`** and **`25`**
- The `2` is `self` plus your argument

---

# Key Takeaways

- Every value is an object — identity, type, state
- **`is`** identity, **`==`** value — default class `==` is identity
- Dict + functions is a complete design, not a missing class
- Mutable defaults are **shared** — use `None` or `__init__`
- **`self`** is the instance, passed as the first argument
- `__init__` initializes; it does not allocate
- Stateless helpers belong in a **module**

---

# What's Next — Episode 2

**Classes, Instances & `__init__`**

- Instance attributes vs class attributes
- The shared `transactions = []` on the class
- `@classmethod` and `@staticmethod`
- Alternate constructors like `User.from_email`

**The Debugger Diary** — Python OOP from Scratch
_"Understand the tools, not just the syntax."_
