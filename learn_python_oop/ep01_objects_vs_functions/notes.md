# Episode 1 — Objects vs Functions

**Series:** Python OOP from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** You can write and run a Python script with functions, lists, and dicts. Python 3.12+.

---

## Episode Overview

By the end of this episode you will have a clear test for when a class is worth writing, you will know the difference between `is` and `==`, and you will have run a bank-account demo that fails as functions-on-a-dict (shared mutable state) and then works as a class. The episode also covers `self` as an ordinary argument, identity versus value, and the cases where a dict plus functions is the right design — not a half-finished class.

---

## Section 1: What This Series Assumes

This is not Python from scratch. You already know how to define a function, build a dict, and run `python some_file.py`. If that is not true yet, use the [Python from Scratch](https://github.com/thedebuggerdiary/learn_python) series first.

What this series *does* assume you might be missing: how Python's object model actually works. Java and Kotlin give you `private`, interfaces, and a compiler that rejects a missing method. Python gives you conventions, duck typing, and a runtime that looks attributes up on the instance, then the class, then the bases. The syntax looks like a class in any language. The rules are not the same.

Python 3.12 or newer. 3.14 is the current stable release. Verify before you record:

```bash
python --version
# Python 3.14.x
```

On Windows, the [Python Install Manager](https://www.python.org/downloads/) from python.org or the Microsoft Store provides `python` and `py`. On Linux and macOS, use python.org, Homebrew, or `pyenv`. Always work in a virtual environment for later episodes that install packages:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
```

---

## Section 2: What an Object Is

An object is a value that has **identity**, **type**, and **state**. In Python, everything you can name is an object: `3`, `"ada"`, a function, a class, a module. That is not a slogan. It means you can put a function in a list, pass a class as an argument, and ask any value for its type.

```python
def greet(name: str) -> str:
    return f"hello, {name}"


print(type(3))         # <class 'int'>
print(type(greet))     # <class 'function'>
print(type(str))       # <class 'type'>
print(id(greet))       # an integer that identifies this function object
```

**`type(x)`**
Returns the class of `x`. `type(3)` is `int` because `3` is an instance of `int`. `type(str)` is `type` because classes are objects too — instances of `type`.

**`id(x)`**
Returns an integer that is unique for this object for as long as it is alive. CPython uses the memory address. Do not depend on the number itself; depend on whether two names share it.

A class is a factory for objects of one type. An **instance** is one such object. `BankAccount` is the class; `BankAccount("Ada", 100)` is an instance. The rest of the series is about how instances store data, how methods find it, and how types relate to each other.

---

## Section 3: Identity vs Equality — `is` and `==`

Two questions that look similar and are not:

- **`a is b`** — do these names refer to the *same object*? (identity)
- **`a == b`** — do these objects *compare as equal*? (value)

```python
ada = {"owner": "Ada", "balance": 100.0}
grace = {"owner": "Ada", "balance": 100.0}

print(ada == grace)   # True  — same keys and values
print(ada is grace)   # False — two dict objects
```

**`==`**
Calls `a.__eq__(b)` (Episode 6). For dicts, lists, and strings, Python compares contents. For instances of a class you write yourself, the default `__eq__` is identity — two `BankAccount` instances are `==` only if they are the same object, until you define `__eq__`.

**`is`**
Compares identity. Use it for `None`, sentinels, and "is this the same object I already have?" Never use `is` to compare strings or numbers you care about as values — CPython intern small integers and some strings, so `is` can be `True` by accident:

```python
print(256 is 256)     # often True — small ints interned
print(257 is 257)     # often True in the same statement, not a rule to rely on
print("ada" is "ada") # often True — interned literals
```

Do not teach `is` as a faster `==`. Teach it as a different question. The bank-account bug in this episode is an identity bug: two accounts share *one* list object.

### Compare to Java

Java separates `==` (identity for objects, value for primitives) from `.equals()`. Python has no primitives in the Java sense, so both operators work on objects: `==` for value (when defined), `is` for identity. `None` is the one value you should compare with `is` / `is not`, the way Java uses `==` with `null`.

---

## Section 4: The Account as Functions on a Dict

You do not need a class to model an account. A dict holds the data; functions take the dict as the first argument and mutate it.

```python
def make_account(
    owner: str, balance: float = 0.0, ledger: list | None = None
) -> dict:
    if ledger is None:
        ledger = []
    return {"owner": owner, "balance": balance, "ledger": ledger}


def deposit(account: dict, amount: float) -> None:
    account["balance"] += amount
    account["ledger"].append(("deposit", amount))


def withdraw(account: dict, amount: float) -> None:
    if amount > account["balance"]:
        raise ValueError("insufficient funds")
    account["balance"] -= amount
    account["ledger"].append(("withdraw", amount))
```

**`make_account`**
Returns a dict with three keys. `ledger: list | None = None` plus `if ledger is None: ledger = []` is the correct pattern for "optional mutable default." Each call gets its own list.

**`deposit` / `withdraw`**
Take the account as an explicit argument. There is no `self`. The relationship between data and behavior is a naming convention: you remember to pass the right dict.

This style is how a lot of real Python starts, and how a lot of it should stay: config blobs, JSON payloads, functions in a module that operate on plain data. A class is not a promotion. It is a different grouping.

---

## Section 5: The Mutable Default Bug

The version that looks shorter is the one that fails. Default argument values are evaluated **once**, when the function is defined, not once per call.

```python
def make_account_broken(
    owner: str, balance: float = 0.0, ledger: list = []
) -> dict:
    return {"owner": owner, "balance": balance, "ledger": ledger}
```

Run two accounts through `deposit`:

```python
a = make_account_broken("Ada", 100)
b = make_account_broken("Grace", 50)
deposit(a, 25)
print(a["ledger"])          # [('deposit', 25)]
print(b["ledger"])          # [('deposit', 25)]  — Grace never deposited
print(a["ledger"] is b["ledger"])  # True — one list, two names
```

**Why this happens**
`ledger=[]` creates one list object and stores it on the function object (`make_account_broken.__defaults__`). Every call that omits `ledger` reuses that same list. Ada's deposit appends to Grace's ledger because they are not two ledgers.

This is the same class of bug as a mutable class attribute (Episode 2). The lesson is identity: if two pieces of state `is` the same object, mutations are shared whether you meant them to be or not.

The fix in the dict style is the `None` sentinel from Section 4. The fix in the class style is creating the list in `__init__` on `self`.

---

## Section 6: The Same Account as a Class

A class binds the data and the functions that belong to it. The dict is replaced by attributes on `self`. The first argument of each method is the instance, passed automatically on `acct.deposit(25)`.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance
        self.ledger: list[tuple[str, float]] = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.ledger.append(("deposit", amount))

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.ledger.append(("withdraw", amount))

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
```

**`class BankAccount:`**
Creates a class object named `BankAccount` and executes the body once, at definition time. Methods defined in the body are functions stored on the class. Instances do not get their own copy of `deposit`; they look it up on the class.

**`__init__`**
Not a constructor in the C++ sense. Python allocates the instance first (`__new__`, almost never overridden), then calls `__init__` to initialize it. `__init__` must not return a value other than `None`. The list is created here, so each instance gets its own ledger.

**`self`**
A conventional name for the instance. You could call it `this` or `acct`; Python does not care. What it requires is that the instance is the first parameter of an instance method. `acct.deposit(25)` is implemented as `BankAccount.deposit(acct, 25)`.

**`__repr__`**
The unambiguous developer string. The REPL and `print` of a container of accounts use it. Episode 6 covers `__str__` vs `__repr__` and `__eq__`. Without `__eq__`, `acct == other` is `False` for two distinct instances even if owner and balance match — identity is the default equality.

---

## Section 7: Compare to Java and Kotlin

Java makes the grouping mandatory. Data lives on a class; methods live on a class; `this` is implicit.

```java
public class BankAccount {
    private String owner;
    private double balance;

    public BankAccount(String owner, double balance) {
        this.owner = owner;
        this.balance = balance;
    }

    public void deposit(double amount) {
        this.balance += amount;
    }
}
```

Kotlin is closer to Python in ceremony but still compiles the class boundary:

```kotlin
class BankAccount(val owner: String, var balance: Double) {
    fun deposit(amount: Double) {
        balance += amount
    }
}
```

Python's version of `this` is an explicit first argument. That is why you can take a method off an instance (`bound method`) or call it on the class with the instance passed in. It is also why forgetting `self` in the parameter list produces `TypeError: ... takes 1 positional argument but 2 were given` — `acct.deposit(25)` still passes the instance, and your function did not declare a slot for it.

The dict-plus-functions style has no Java equivalent that the compiler likes. In Python it is a first-class design, not a missing class.

---

## Section 8: When You Should Not Write a Class

Write a class when you have **state that changes together** and **operations that only make sense on that state**, and you expect more than one instance.

Do not write a class when:

- The "object" is a single dict you load from JSON and pass through functions.
- Every method is `@staticmethod` and never reads `self` — that is a module with functions.
- You need one copy of the data in the whole program — that is a module-level dict or a function with a default, not a singleton class.
- You are about to create `UserManager`, `AccountHelper`, `Utils` with no state. Those names are a smell: the functions belong in a module.

A module of functions plus plain data is OOP-optional Python. Classes become worth it when the invariant (balance never negative, ledger matches balance) has to be enforced in one place, or when you need many instances that must not share mutable state.

---

## Section 9: Running the Demo

The file `code/bank_account.py` contains the broken factory, the fixed factory, and `BankAccount`. From the `code/` directory:

```bash
python bank_account.py
```

Output:

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

Walk the three pairs:

1. Two dicts with the same contents: `==` True, `is` False.
2. Broken factory: one ledger list, two accounts.
3. Fixed factory and class: Grace's ledger stays empty; Ada's deposit does not leak.

`equality by default: False` is the cliffhanger for Episode 6: two `BankAccount` instances with different owners are not equal, but even two with the same owner would not be equal until you define `__eq__`.

---

## Section 10: `self` Is Just an Argument

You can call the method through the class and pass the instance yourself:

```python
acct = BankAccount("Ada", 100)
BankAccount.deposit(acct, 25)
print(acct.balance)   # 125
```

That is not a trick. `acct.deposit(25)` is syntactic sugar for looking up `deposit` on the class and inserting `acct` as the first argument. Bound methods exist so you can pass `acct.deposit` as a callback without wrapping it.

If you write `def deposit(amount):` inside the class and then call `acct.deposit(25)`, Python still passes `acct`. The function only declared one parameter, so you get:

```
TypeError: BankAccount.deposit() takes 1 positional argument but 2 were given
```

The "2" is `self` plus `25`. The error is easier to read once you believe `self` is real.

---

## Key Takeaways

- An object has identity, type, and state; in Python every value is an object, including functions and classes.
- `is` tests identity; `==` tests value. Default class equality is identity until you define `__eq__`.
- A dict plus functions is a valid design. A class groups the same data and operations and passes the instance as `self`.
- Default argument values are created once at definition time. `def f(x=[])` shares one list across calls.
- `__init__` initializes an already-created instance; create per-instance mutables there, not in the class body.
- `acct.deposit(25)` is `BankAccount.deposit(acct, 25)`. Forgetting `self` in the parameter list is the "takes 1 but 2 were given" error.
- Do not write a class for stateless helpers or a single global blob of data — use a module.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `TypeError: BankAccount.deposit() takes 1 positional argument but 2 were given` | Instance method missing `self` in the parameter list; the call still passes the instance | Add `self` as the first parameter |
| `NameError: name 'self' is not defined` | Used `self` in `__init__` or a method without declaring it | `def __init__(self, ...):` |
| `TypeError: __init__() should return None, not 'BankAccount'` | `return self` (or anything) from `__init__` | Do not return a value from `__init__`; the instance is created before `__init__` runs |
| Two instances unexpectedly share a list | Mutable default argument, or a list assigned on the class instead of on `self` | Use `None` as the default, or assign `self.ledger = []` in `__init__` |
| `acct.deposit` vs `acct.deposit()` confusion | Printed or stored the bound method instead of calling it | Add `()`; `acct.deposit` is the bound method object |

---

## Further Reading

- [Data model — objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types) — identity, type, and value in the language reference
- [Mutable default arguments](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments) — the same bug in the Hitchhiker's Guide
- Episode 2: Classes, Instances & `__init__` — instance vs class attributes, `@classmethod` / `@staticmethod`, and the shared `transactions = []` pitfall on the class itself
