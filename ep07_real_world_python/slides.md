---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Real-World Python
### Types, Tests & Packaging
### Episode 7 — Python from Scratch
**The Debugger Diary**

---

# What This Episode Covers

Three tools that separate a "Python script" from a "Python project":

1. **mypy** — catch type errors before you run the code
2. **pytest** — write and run tests in seconds
3. **pyproject.toml + uv** — modern dependency management and packaging

We will build a small typed, tested, packaged library end-to-end.

---

# mypy — Static Type Checking

```bash
pip install mypy
mypy greet.py
```

```python
# greet.py
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet(42)   # passes at runtime
```

```bash
$ mypy greet.py
greet.py:4: error: Argument 1 to "greet" has incompatible type "int"; expected "str"
Found 1 error in 1 file (checked 1 source file)
```

mypy reads your type hints and reports errors without running the code.

---

# mypy — Optional and None

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice"}
    return users.get(user_id)

user = find_user(1)
print(user.upper())   # error — user might be None!
```

```bash
$ mypy greet.py
error: Item "None" of "str | None" has no attribute "upper"
```

mypy forces you to handle `None` before calling methods on optional values.

---

# pytest — Testing in Seconds

```bash
pip install pytest
```

```python
# test_greet.py
from greet import greet, find_user

def test_greet_returns_string():
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_string():
    assert greet("") == "Hello, !"

def test_find_user_existing():
    assert find_user(1) == "Alice"

def test_find_user_missing():
    assert find_user(99) is None
```

```bash
pytest
# 4 passed in 0.12s
```

---

# pytest — Parametrize

```python
import pytest

@pytest.mark.parametrize("name,expected", [
    ("Alice", "Hello, Alice!"),
    ("Bob",   "Hello, Bob!"),
    ("",      "Hello, !"),
])
def test_greet_parametrized(name: str, expected: str) -> None:
    assert greet(name) == expected
```

```bash
pytest -v
# test_greet.py::test_greet_parametrized[Alice-Hello, Alice!] PASSED
# test_greet.py::test_greet_parametrized[Bob-Hello, Bob!] PASSED
# test_greet.py::test_greet_parametrized[-Hello, !] PASSED
```

One test function, many inputs — no copy-paste.

---

# pytest — Testing Exceptions

```python
import pytest
from greet import validate_name

def test_validate_name_raises_on_empty() -> None:
    with pytest.raises(ValueError, match="Name cannot be empty"):
        validate_name("")

def test_validate_name_raises_on_too_long() -> None:
    with pytest.raises(ValueError, match="too long"):
        validate_name("A" * 101)
```

`pytest.raises` asserts that the code inside the `with` block raises the expected exception. `match` checks the error message with a regex.

---

# pyproject.toml — Modern Packaging

```toml
[project]
name = "greetlib"
version = "0.1.0"
description = "A tiny greeting library"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "mypy"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

`pyproject.toml` is the single config file for Python projects (PEP 517/518). It replaces `setup.py`, `setup.cfg`, and `requirements.txt`.

---

# uv — Fast Modern Toolchain

```bash
# Install uv
pip install uv

# Create a project
uv init greetlib
cd greetlib

# Add dependencies
uv add requests
uv add --dev pytest mypy

# Run the project
uv run python greet.py

# Run tests
uv run pytest

# Type check
uv run mypy greet.py
```

`uv` replaces `pip` + `venv` with a single fast tool. It resolves and installs packages 10–100× faster than pip.

---

# Project Layout

```
greetlib/
├── pyproject.toml
├── src/
│   └── greetlib/
│       ├── __init__.py
│       └── greet.py
└── tests/
    └── test_greet.py
```

- `src/` layout prevents accidental imports from the wrong place during development
- `tests/` at the project root — separate from source

Run tests from the project root:
```bash
pytest tests/
mypy src/
```

---

# Key Takeaways

- `mypy` — catches type errors before runtime; run it in CI
- `pytest` — `def test_*()` + `assert` — dead simple; `@parametrize` for many inputs
- `pyproject.toml` — single file for metadata, deps, and build config
- `uv` — fast drop-in replacement for pip + venv
- `src/` layout — keeps source separate from tests and tooling
- The three together — typed, tested, packaged — is what "production Python" looks like

---

# You've Completed the Series!

**Topics covered:**
1. Setup & Hello World
2. Variables, Types & Type Hints
3. Functions & Lambdas
4. Classes, Dataclasses & Protocols
5. Collections & Comprehensions
6. Async/Await
7. Real-World Python: Types, Tests & Packaging

**Where to go next:**
- **Web:** FastAPI or Django REST Framework
- **Data:** pandas, NumPy, Jupyter
- **ML:** scikit-learn, PyTorch
- **CLI:** Typer, Click, Rich

**The Debugger Diary** — Python from Scratch
_"Understand the tools, not just the syntax."_
