# Python OOP from Scratch
**Channel:** The Debugger Diary

## Series Goal

This series teaches Python's object model in depth, targeting developers who already write Python -- or who already know classes in Java, Kotlin, C++, or JavaScript -- and want to understand how Python actually does OOP, not how a textbook says objects work. You will start with why a class exists at all (and when a `dict` plus functions is enough), then build through instances, properties, inheritance, duck typing, dunder methods, and composition, and finish with the patterns you will see in production code: dataclasses, enums, and tests around a small domain model.

`learn_python` Episode 4 compresses classes, dataclasses, and protocols into one sitting. This series unpacks that ground and stays there. Each episode is standalone -- watch in order for the full picture, or jump to the topic you need.

---

## Episode Plan

| # | Title | Key Topics | Demo | Duration Est. |
|---|-------|-----------|------|--------------|
| 1 | Objects vs Functions | Why a class exists, identity vs equality (`is` / `==`), `self` as the first argument, when a `dict` + functions is enough | Bank account as functions-on-a-dict vs a class -- the shared-mutable-state bug | 12-15 min |
| 2 | Classes, Instances & `__init__` | `class`, instance vs class attributes, methods, `__init__`, `@classmethod` / `@staticmethod`, the mutable class-attribute pitfall | `User` + `Account` showing a shared `transactions = []` on the class | 15-18 min |
| 3 | Encapsulation & Properties | Public-by-convention, `_`, `__` name mangling, `@property` / setter / deleter, computed attributes, validation | `Temperature` with Celsius/Fahrenheit properties that reject invalid values | 15-18 min |
| 4 | Inheritance & `super()` | Single inheritance, `super()`, MRO (`C3`), `isinstance` vs `type()`, when inheritance is the wrong tool | Notification senders (`Email`, `SMS`) sharing setup via `super()` | 18-22 min |
| 5 | Polymorphism, ABCs & Protocols | Duck typing vs Java interfaces, `abc.ABC` / `@abstractmethod`, `typing.Protocol`, `isinstance` checks that actually help | Payment processors behind an ABC, then the same shape as a `Protocol` | 18-22 min |
| 6 | Dunders & Composition | `__repr__` / `__eq__` / `__hash__`, `__len__` / `__iter__`, operators, composition over inheritance | `Money` value type with operators, composed into an `Order` | 18-22 min |
| 7 | Real-World Object-Oriented Python | `@dataclass`, `Enum`, mixins vs composition, typing the model, testing classes with `pytest` | Order/inventory domain as dataclasses + a small `pytest` suite | 15-18 min |

**Total series:** ~111-135 minutes across 7 episodes

---

## Prerequisites

### Knowledge
- Working Python: functions, variables, lists/dicts, running a script with `python file.py`
- Understanding of what a function, variable, and class is in any language
- No prior Python OOP required. Java/Kotlin/C++ class experience helps as contrast, not as a prerequisite
- For Episode 7: knowing what a unit test is helps but is not required

### Tools to Install

**Python 3.12+** (3.14 recommended -- current stable)
- Windows (recommended): [Python Install Manager](https://www.python.org/downloads/) from python.org or the Microsoft Store, then `python` / `py`
- Linux/macOS: [python.org](https://www.python.org/downloads/) installer, Homebrew `python@3.14`, or `pyenv`
- Verify: `python --version`  # Python 3.14.x

**pip** (bundled with Python)
- Verify: `python -m pip --version`

**VS Code (recommended)**
- Python extension by Microsoft (`ms-python.python`)
- Gives you IntelliSense, debugger, and test runner integration for Episode 7

**pytest** (Episode 7 only)
- `python -m pip install pytest`
- Verify: `python -m pytest --version`

**Marp** (for slides)
- VS Code extension: "Marp for VS Code" (`marp-team.marp-vscode`)
- Or CLI: `npm install -g @marp-team/marp-cli`

---

## Repository Structure

```
learn_python_oop/
├── VIDEO_SERIES_PLAN.md              <- You are here
├── README.md
├── ep01_objects_vs_functions/
│   ├── slides.md                     <- Marp presentation
│   ├── notes.md                      <- Full reference + source code
│   └── code/
│       └── bank_account.py           <- Runnable demo
├── ep02_classes_instances_init/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── user_account.py
├── ep03_encapsulation_and_properties/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── temperature.py
├── ep04_inheritance_and_super/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── notifications.py
├── ep05_polymorphism_abcs_protocols/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── payments.py
├── ep06_dunders_and_composition/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── money_order.py
└── ep07_real_world_oop/
    ├── slides.md
    ├── notes.md
    └── code/
        ├── inventory.py
        └── test_inventory.py
```

---

## How to Use This Repo

- **Slides** (`slides.md`): Open in VS Code with the Marp extension for a live preview. Export to PDF or HTML for recording.
- **Notes** (`notes.md`): Full script/reference. Read before recording. Contains all source code, explanations, and talking points.
- **Code** (`code/`): Runnable Python files for each episode. Run with `python <file>.py`, or open the folder in VS Code and press **F5** to debug. Episode 7 tests: `python -m pytest test_inventory.py` from that `code/` directory.
