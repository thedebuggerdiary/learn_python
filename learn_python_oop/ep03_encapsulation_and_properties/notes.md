# Episode 3 — Encapsulation & Properties

**Series:** Python OOP from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episode 2 — instance vs class attributes, `__init__`.

---

## Episode Overview

By the end of this episode you will treat encapsulation as convention plus properties, not as Java `private`. You will know what `_name` means, what `__name` actually does (mangling, not privacy), and how `@property` lets you keep `obj.celsius` syntax while validating and computing values. The demo is a `Temperature` type with Celsius and Fahrenheit properties that reject values below absolute zero, plus a small `Ledger` that shows mangling across a subclass.

---

## Section 1: Python Has No `private`

Java and C++ enforce access with the compiler. Python does not. Every attribute is reachable from outside the class if the caller is willing to type the name. What Python gives you instead is a social contract and a couple of tools that make accidents harder.

| Prefix | Meaning | Enforced? |
|---|---|---|
| `name` | Public. Callers may read and write. | No |
| `_name` | Internal. Callers *should* not touch it. | No — a convention |
| `__name` | Name-mangled to `_Class__name`. Avoids clashes with subclasses, not with attackers. | The mangling is real; privacy is not |

That is not a deficiency. It is a language that assumes you and your teammates are adults. If you need a true boundary, you put the object behind a process, a capability, or an API — not behind two underscores.

---

## Section 2: `_` Means "You Were Warned"

```python
class Ledger:
    def __init__(self) -> None:
        self._entries: list[str] = []
        self.__audit_key = "secret"

    def add(self, line: str) -> None:
        self._entries.append(line)
```

**`_entries`**
A single leading underscore is documentation. `led._entries` works. Linters and humans treat it as "implementation". Tools like `from module import *` skip `_` names. That is the entire mechanism.

Use `_` for storage that a property or method is supposed to own. In `Temperature`, `_celsius` is the backing field. Callers use `room.celsius`. If they poke `_celsius` they skip validation — and that is on them.

Do not prefix everything with `_`. Public attributes are normal Python. `user.email` is better than `user.get_email()` when there is no invariant to protect.

---

## Section 3: `__` Is Mangling, Not Privacy

Two leading underscores (and at most one trailing underscore) rewrite the name at compile time: `__audit_key` inside `Ledger` becomes `_Ledger__audit_key`.

```python
led = Ledger()
print(led._Ledger__audit_key)          # secret
print(hasattr(led, "__audit_key"))     # False
```

**Why this exists**
Subclasses often want their own `__audit_key` without overwriting the base class's attribute. Mangling scopes the name to the class that wrote it.

```python
class SubLedger(Ledger):
    def __init__(self) -> None:
        super().__init__()
        self.__audit_key = "subclass-secret"
```

`SubLedger` stores `_SubLedger__audit_key`. `Ledger.audit_key` still reads `_Ledger__audit_key`. The inherited method returns `"secret"`. That surprise is the lesson: mangling prevents accidental override; it does not hide data.

Never use `__` for "make this private." Use it when you are writing a mixin or a base class and need an attribute that subclasses must not clobber. For ordinary internals, `_` is enough.

Names of the form `__dunder__` (two underscores on both sides) are not mangled. Those are the data-model hooks in Episode 6.

---

## Section 4: `@property` — A Method That Looks Like a Field

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = 0.0
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius
```

**`@property`**
Turns a method into a managed attribute. `room.celsius` calls the getter. There are no parentheses. That lets you start with a plain attribute and later insert logic without changing callers — the same reason C# has properties and Java eventually grew records.

**Why `__init__` writes `self.celsius = celsius`**
That assignment goes through the setter, so construction is validated the same way as later updates. The dummy `self._celsius = 0.0` first exists so the setter has a field to write; you could also assign to `_celsius` only after checking, but routing through the setter keeps one rule.

If you forget the backing field and write `self.celsius = value` inside the setter, you recurse until `RecursionError`.

---

## Section 5: Setters Validate

```python
    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"celsius below absolute zero: {value}")
        self._celsius = float(value)
```

**`@celsius.setter`**
The name must match the property. The function receives the assigned value. Raise `ValueError` (or a domain exception) when the invariant fails. Do not silently clamp unless the type is explicitly "best effort."

Compare to Java:

```java
public void setCelsius(double value) {
    if (value < -273.15) throw new IllegalArgumentException();
    this.celsius = value;
}
```

Java callers write `setCelsius`. Python callers write `room.celsius = -300` and still hit the check. The syntax stayed an attribute; the behavior became a method.

A deleter is `@celsius.deleter` plus `del room.celsius`. Use it rarely — usually for caches, not for required state.

---

## Section 6: Computed Attributes

Fahrenheit is not stored. It is derived from Celsius, so it cannot drift.

```python
    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (float(value) - 32) * 5 / 9
```

**Getter**
`room.fahrenheit` computes. No `_fahrenheit` field, so there is only one source of truth.

**Setter**
Converts and assigns `self.celsius`, which reuses the absolute-zero check. Setting Fahrenheit to a value that would be below -273.15 °C still raises.

This is the pattern for `full_name`, `area`, `is_empty`: if it can be computed, do not store it unless measuring shows a cost.

---

## Section 7: Compare to Kotlin and C#

Kotlin `var` with a custom setter:

```kotlin
var celsius: Double = 0.0
    set(value) {
        require(value >= -273.15)
        field = value
    }
```

C# properties are compiled into `get_` / `set_` methods. Python properties are descriptors: objects that implement `__get__` and `__set__` and live on the class. `@property` is the convenient way to build that descriptor. You do not need to write a descriptor class until you have the same access pattern on many attributes (Episode 7 mentions this; you will not need it for `Temperature`).

---

## Section 8: When a Property Is the Wrong Tool

- **No invariant, no computation** — use a public attribute. `self.owner = owner` is correct.
- **Expensive work** — a property that hits the network or walks a huge graph lies to the reader. Use a method `load_rows()`.
- **Conversion that can fail in surprising ways** — a method `as_fahrenheit()` can be clearer than a setter that accepts strings, floats, and `Decimal`.
- **Hiding mutation** — `order.total` that also ships the order is a trap. Properties should look cheap and local.

Java culture over-uses getters. Python culture under-uses properties until a field needs a rule. Start with attributes; promote to properties when the rule appears.

---

## Section 9: Running the Demo

`code/temperature.py` defines `Temperature`, `Ledger`, and `SubLedger`.

```bash
python temperature.py
```

Output:

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

Walk it on camera:

1. 0 °C is 32 °F; 100 °C is 212 °F — exact, so the conversion is visible.
2. Assigning `-300` hits the setter and raises; `_celsius` does not change (you already set it back to 0 via 32 °F).
3. `_entries` is readable — convention, not a lock.
4. `__audit_key` is not on the instance under that name; `_Ledger__audit_key` is.
5. `SubLedger.audit_key()` still returns the *base* secret because the method was compiled in `Ledger`.

---

## Section 10: Properties and Inheritance

A subclass can override a property by redefining it. Call `super()` inside a getter if you need the base value. Do not reach into `self._celsius` from a subclass unless you accepted the coupling; the public `celsius` property is the API.

If a subclass only needs to tighten validation, override the setter and call `super(Temperature, self.__class__).celsius.fset(self, value)` — that is ugly, which is a signal. Prefer a hook method `_validate_celsius(value)` that both the base setter and the subclass can call. Properties stay thin; named methods carry the policy.

---

## Key Takeaways

- Python encapsulation is convention: `_` means internal, not private.
- `__name` mangles to `_Class__name` to avoid subclass clashes, not to hide data.
- `@property` keeps attribute syntax and adds a getter.
- `@x.setter` is where invariants belong; construction should go through it too.
- Store one source of truth; compute the rest (`fahrenheit` from `_celsius`).
- Inside a setter, assign the backing field — assigning the property name recurses.
- Prefer a public attribute until a rule or a computation appears.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `RecursionError: maximum recursion depth exceeded` | Setter does `self.celsius = value` instead of `self._celsius = value` | Write the backing field, or a different name |
| `AttributeError: property 'celsius' of 'Temperature' object has no setter` | Assignment to a read-only property | Add `@celsius.setter` or stop assigning |
| `AttributeError: 'Ledger' object has no attribute '__audit_key'` | Looked up the unmangled name from outside | Use the public method, or `_Ledger__audit_key` if you must debug |
| Subclass `__x` overwrote the base and "broke" a base method | Expected privacy; got two mangled names | Read `_Base__x` vs `_Sub__x`; do not use `__` as privacy |
| `ValueError: celsius below absolute zero: ...` | Setter invariant | Pass a value ≥ -273.15, or catch `ValueError` at the call site |

---

## Further Reading

- [property — built-in](https://docs.python.org/3/library/functions.html#property) — getter, setter, deleter
- [Private-name mangling](https://docs.python.org/3/tutorial/classes.html#private-variables) — what `__` actually does
- [Descriptor HowTo](https://docs.python.org/3/howto/descriptor.html) — the mechanism under `@property`
- Episode 4: Inheritance & `super()` — `super()`, the MRO, `isinstance` vs `type()`, and when a hierarchy is the wrong shape
