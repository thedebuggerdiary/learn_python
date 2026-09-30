---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Encapsulation & Properties
### Episode 3 — Python OOP from Scratch
**The Debugger Diary**

---

# No `private` Keyword

| Prefix | Meaning | Enforced? |
|---|---|---|
| `name` | Public | No |
| `_name` | Internal by convention | No |
| `__name` | Mangling to `_Class__name` | Mangling, not privacy |

Java's compiler refuses. Python assumes you read the underscore.

---

# `_` Means You Were Warned

```python
class Ledger:
    def __init__(self) -> None:
        self._entries: list[str] = []

led = Ledger()
led._entries.append("opened")   # works
```

- Skipped by `from module import *`
- Linters flag external use
- Not a lock — a **comment the runtime honors as a name**

---

# `__` Is Mangling

```python
class Ledger:
    def __init__(self) -> None:
        self.__audit_key = "secret"

led = Ledger()
print(led._Ledger__audit_key)           # secret
print(hasattr(led, "__audit_key"))      # False
```

Rewritten at compile time. Stops **subclass name clashes**. Does not hide data.

---

# Mangling Across a Subclass

```python
class SubLedger(Ledger):
    def __init__(self) -> None:
        super().__init__()
        self.__audit_key = "subclass-secret"
```

- Base stores `_Ledger__audit_key`
- Sub stores `_SubLedger__audit_key`
- `Ledger.audit_key()` still returns **`"secret"`**

`__dunder__` names are **not** mangled.

---

# `@property` — Attribute Syntax

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = 0.0
        self.celsius = celsius   # goes through the setter

    @property
    def celsius(self) -> float:
        return self._celsius
```

Start with a field. Promote to a property **without changing callers**.

---

# Setters Enforce Invariants

```python
    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(
                f"celsius below absolute zero: {value}"
            )
        self._celsius = float(value)
```

Assign the **backing field**. `self.celsius = ...` inside the setter **recurses**.

---

# Compare to Java

```java
public void setCelsius(double value) {
    if (value < -273.15) throw new IllegalArgumentException();
    this.celsius = value;
}
setCelsius(-300);
```

```python
room.celsius = -300   # still runs the setter
```

Same check. **No `get`/`set` noise** in the happy path.

---

# Computed Fahrenheit

```python
    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (float(value) - 32) * 5 / 9
```

One stored value. The setter **reuses** the Celsius invariant.

---

# When Not to Use a Property

- No rule, no computation — **public attribute**
- Network / heavy work — a **method** (`load_rows()`)
- Hidden side effects — properties should look **cheap**

Java over-getters. Python: **attribute first**, property when a rule appears.

---

# Demo — `temperature.py`

```bash
python temperature.py
```

```
celsius: 0.0
fahrenheit: 32.0
boiling F: 212.0
after 32 F: 0.0 32.0
rejected: celsius below absolute zero: -300
public-by-convention _entries: ['opened']
mangled from outside: secret
hasattr __audit_key: False
base key via method: secret
subclass mangled: subclass-secret
```

0 °C and 100 °C keep the arithmetic **exact** on camera.

---

# Key Takeaways

- `_` is convention, not access control
- `__` mangles; it does not encrypt
- `@property` preserves `obj.x` syntax
- Validate in the **setter**; construct through it
- One source of truth; compute the rest
- Setter writes **`_x`**, not `x`
- Don't property-wrap every field

---

# What's Next — Episode 4

**Inheritance & `super()`**

- Single inheritance and `super()`
- MRO (C3)
- `isinstance` vs `type()`
- Mixins vs a deeper tree
- `Email` / `SMS` notifications

**The Debugger Diary** — Python OOP from Scratch
_"Understand the tools, not just the syntax."_
