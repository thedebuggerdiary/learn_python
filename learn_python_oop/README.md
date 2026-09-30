# Python OOP from Scratch

A YouTube video series by **The Debugger Diary** that teaches Python's object model in depth, targeting developers who already write Python or who already know classes in another language.

You will learn why objects exist (and when they do not), classes and instances, properties and encapsulation, inheritance and the MRO, duck typing with ABCs and Protocols, dunder methods and composition, and finish with dataclasses, enums, and tests around a small domain model.

---

## Who This Is For

- Python developers who used classes by copy-paste and want the actual object model
- Java, Kotlin, or C++ developers who expect interfaces, `private`, and `this` and need Python's version of each
- Anyone who wants to understand what makes Python OOP different: duck typing, `self`, and composition over deep hierarchies

You should already be able to write a Python script with functions and dicts. No prior Python OOP is required. If you are new to Python itself, start with [learn_python](https://github.com/thedebuggerdiary/learn_python) and come back for this series.

---

## Episodes

| # | Folder | Title |
|---|--------|-------|
| 1 | [ep01_objects_vs_functions](ep01_objects_vs_functions/) | Objects vs Functions |
| 2 | [ep02_classes_instances_init](ep02_classes_instances_init/) | Classes, Instances & `__init__` |
| 3 | [ep03_encapsulation_and_properties](ep03_encapsulation_and_properties/) | Encapsulation & Properties |
| 4 | [ep04_inheritance_and_super](ep04_inheritance_and_super/) | Inheritance & `super()` |
| 5 | [ep05_polymorphism_abcs_protocols](ep05_polymorphism_abcs_protocols/) | Polymorphism, ABCs & Protocols |
| 6 | [ep06_dunders_and_composition](ep06_dunders_and_composition/) | Dunders & Composition |
| 7 | [ep07_real_world_oop](ep07_real_world_oop/) | Real-World Object-Oriented Python |

---

## How to Use This Repo

Each episode folder contains:

- **`slides.md`** — Marp Markdown presentation. Open in VS Code with the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension for a live slide preview. Export to PDF/HTML for screen recording.
- **`notes.md`** — Complete reference document with full explanations, all source code, talking points, and further reading.
- **`code/`** — Runnable Python source files for the episode.

---

## Setup

### Install Python

This series requires **Python 3.12+**. **3.14** is the current stable release and the version shown in verify comments.

**Windows (recommended):** install the [Python Install Manager](https://www.python.org/downloads/) from python.org or the Microsoft Store. After it is installed, `python` and `py` are available in a new terminal. The first `python` invocation can install a runtime if none is present.

```powershell
python --version
# Python 3.14.x

py list
```

The older standalone python.org installer still works through the 3.14 line. If you use it, enable **Add python.exe to PATH**.

**Via `pyenv` (Linux/macOS/WSL):**

```bash
curl https://pyenv.run | bash
pyenv install 3.14
pyenv global 3.14
python --version
# Python 3.14.x
```

**Via Homebrew (macOS):**

```bash
brew install python@3.14
python3 --version
# Python 3.14.x
```

**pip** ships with Python:

```bash
python -m pip --version
# pip 25.x from ...
```

### Create a virtual environment

Work inside a virtual environment so Episode 7's `pytest` install stays off your system Python:

```bash
python -m venv .venv

# Activate — Linux/macOS
source .venv/bin/activate

# Activate — Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### Run a Python file

```bash
python ep01_objects_vs_functions/code/bank_account.py
```

Or from the episode's `code/` directory:

```bash
cd ep01_objects_vs_functions/code
python bank_account.py
```

### Episode 7 only — pytest

```bash
python -m pip install pytest
cd ep07_real_world_oop/code
python -m pytest test_inventory.py
```

### Marp (for slides)

Install the **Marp for VS Code** extension, or use the CLI:

```bash
npm install -g @marp-team/marp-cli
marp ep01_objects_vs_functions/slides.md --pdf
```

---

## See Also

- `VIDEO_SERIES_PLAN.md` — full episode breakdown with topics, demos, and duration estimates
- [learn_python](https://github.com/thedebuggerdiary/learn_python) — language core, if you need syntax before objects
