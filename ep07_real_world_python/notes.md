# Episode 7 — Real-World Python: Types, Tests & Packaging

**Series:** Python from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episodes 1–6

---

## Episode Overview

Writing Python that works is step one. Writing Python that stays working as it grows requires three more things: a type checker to catch mistakes before runtime, a test suite to catch regressions, and a packaging setup that makes your code shareable and reproducible. This episode walks through all three, building a small typed, tested, packaged library from scratch.

---

## Section 1: mypy — Static Type Checking

### Install and basic usage

```bash
pip install mypy
mypy greet.py
```

mypy reads your Python source files, follows your type annotations, and reports type errors without executing the code — similar to how Kotlin's compiler rejects type mismatches before the program runs.

### Type error detection

```python
# greet.py
def greet(name: str) -> str:
    return f"Hello, {name}!"

result = greet(42)          # mypy error: expected str, got int
result.nonexistent_method() # mypy error: str has no nonexistent_method
```

```bash
$ mypy greet.py
greet.py:4: error: Argument 1 to "greet" has incompatible type "int"; expected "str"
greet.py:5: error: "str" has no attribute "nonexistent_method"
Found 2 errors in 1 file
```

### None safety

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    users: dict[int, str] = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

user = find_user(1)
print(user.upper())   # mypy error: Item "None" of "str | None" has no attribute "upper"
```

After the `isinstance` check, mypy narrows the type:

```python
user = find_user(1)
if user is not None:
    print(user.upper())  # OK — mypy knows user is str here
```

### mypy configuration (mypy.ini or pyproject.toml)

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

`strict = true` enables all optional checks including disallowing untyped functions. Start with this for new projects.

### Running mypy on a whole project

```bash
mypy src/
# or
mypy .
```

Add mypy to your CI pipeline so type errors are caught before merge.

---

## Section 2: pytest — Testing

### Install and first test

```bash
pip install pytest
```

pytest discovers tests by looking for files named `test_*.py` or `*_test.py` and functions named `test_*`. No test class or base class required:

```python
# tests/test_greet.py
from greetlib.greet import greet, find_user, validate_name

def test_greet_alice() -> None:
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_string() -> None:
    assert greet("") == "Hello, !"

def test_find_user_existing() -> None:
    assert find_user(1) == "Alice"

def test_find_user_missing() -> None:
    assert find_user(99) is None
```

Run:
```bash
pytest
# ====== 4 passed in 0.08s ======

pytest -v    # verbose output — one line per test
pytest -x    # stop at first failure
```

### assert rewriting

pytest rewrites `assert` statements to provide detailed failure messages:

```python
def test_mismatch() -> None:
    assert greet("Alice") == "Hi, Alice!"
```

```
AssertionError: assert 'Hello, Alice!' == 'Hi, Alice!'
  - Hello, Alice!
  + Hi, Alice!
```

No need to write `assertEqual` or `assertEquals` — plain `assert` is enough.

### @pytest.mark.parametrize — test many inputs at once

```python
import pytest

@pytest.mark.parametrize("name,expected", [
    ("Alice",   "Hello, Alice!"),
    ("Bob",     "Hello, Bob!"),
    ("",        "Hello, !"),
    ("  Alice", "Hello,   Alice!"),  # spaces are preserved
])
def test_greet_parametrized(name: str, expected: str) -> None:
    assert greet(name) == expected
```

Each tuple in the list becomes a separate test case. The verbose output shows each individually, making it easy to see which inputs fail.

### Testing exceptions

```python
import pytest

def test_validate_name_raises_on_empty() -> None:
    with pytest.raises(ValueError, match="Name cannot be empty"):
        validate_name("")

def test_validate_name_raises_on_too_long() -> None:
    with pytest.raises(ValueError, match="too long"):
        validate_name("A" * 101)
```

`pytest.raises(ExceptionType)` asserts the body raises that exception. `match` is a regex applied to the error message string.

### Fixtures — shared setup

```python
import pytest

@pytest.fixture
def user_db() -> dict[int, str]:
    return {1: "Alice", 2: "Bob", 3: "Carol"}

def test_find_existing_user(user_db: dict[int, str]) -> None:
    assert find_user(1, user_db) == "Alice"

def test_find_missing_user(user_db: dict[int, str]) -> None:
    assert find_user(99, user_db) is None
```

pytest injects fixtures by name. The fixture runs once per test function (by default). Scope can be `"module"` or `"session"` to run less often.

---

## Section 3: pyproject.toml — Modern Packaging

PEP 517/518 (2017–2018) defined `pyproject.toml` as the single configuration file for Python projects. It replaces `setup.py`, `setup.cfg`, and per-tool `*.cfg`/`*.ini` files.

```toml
[project]
name = "greetlib"
version = "0.1.0"
description = "A tiny greeting library — Episode 7 demo"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "mypy>=1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Installing in editable mode

```bash
pip install -e .
```

`-e` installs your package in "editable" mode — Python imports your source files directly, so changes take effect immediately without reinstalling.

---

## Section 4: uv — Fast Modern Toolchain

`uv` (by Astral) is a Rust-based replacement for `pip` + `venv` that is 10–100× faster.

```bash
pip install uv
```

### Starting a new project

```bash
uv init greetlib
cd greetlib
```

This creates `pyproject.toml`, `src/greetlib/__init__.py`, and `.venv` automatically.

### Managing dependencies

```bash
uv add requests          # add runtime dependency
uv add --dev pytest mypy # add dev dependencies

uv remove requests       # remove a dependency
uv sync                  # install all deps from pyproject.toml lockfile
```

`uv` writes a `uv.lock` file that pins exact versions — commit this for reproducible builds.

### Running commands

```bash
uv run python greet.py   # run inside the venv
uv run pytest            # run tests
uv run mypy src/         # type check
```

### Building and publishing

```bash
uv build                 # create dist/*.whl and dist/*.tar.gz
uv publish               # upload to PyPI
```

---

## Section 5: Project Layout

The `src` layout is the recommended standard for installable packages:

```
greetlib/
├── pyproject.toml
├── uv.lock
├── README.md
├── src/
│   └── greetlib/
│       ├── __init__.py
│       └── greet.py
└── tests/
    ├── __init__.py
    └── test_greet.py
```

**Why `src/`?** Without it, running `pytest` from the project root adds the project directory to `sys.path`. This means Python can import your source files directly without installing the package. The test then passes locally but fails in CI or after installation because the import path is different. The `src/` layout prevents this: Python must install the package to import it, so tests always test the installed version.

---

## Section 6: CI with GitHub Actions

A minimal CI workflow that runs mypy and pytest on every push:

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --frozen
      - run: uv run mypy src/
      - run: uv run pytest
```

`--frozen` ensures CI uses the exact versions in `uv.lock` — no surprises from version drift.

---

## Demo: The Full greetlib Package

### src/greetlib/greet.py

```python
"""Core greeting functions for greetlib."""

MAX_NAME_LENGTH = 100

_USERS: dict[int, str] = {
    1: "Alice",
    2: "Bob",
    3: "Carol",
}


def validate_name(name: str) -> None:
    if not name:
        raise ValueError("Name cannot be empty")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Name is too long (max {MAX_NAME_LENGTH} chars)")


def greet(name: str) -> str:
    return f"Hello, {name}!"


def greet_loud(name: str) -> str:
    validate_name(name)
    return f"HELLO, {name.upper()}!"


def find_user(user_id: int) -> str | None:
    return _USERS.get(user_id)
```

### tests/test_greet.py

```python
import pytest
from greetlib.greet import greet, greet_loud, find_user, validate_name


def test_greet_basic() -> None:
    assert greet("Alice") == "Hello, Alice!"


@pytest.mark.parametrize("name,expected", [
    ("Alice", "Hello, Alice!"),
    ("Bob",   "Hello, Bob!"),
    ("",      "Hello, !"),
])
def test_greet_parametrized(name: str, expected: str) -> None:
    assert greet(name) == expected


def test_greet_loud() -> None:
    assert greet_loud("alice") == "HELLO, ALICE!"


def test_validate_name_raises_empty() -> None:
    with pytest.raises(ValueError, match="Name cannot be empty"):
        validate_name("")


def test_validate_name_raises_too_long() -> None:
    with pytest.raises(ValueError, match="too long"):
        validate_name("A" * 101)


def test_find_user_existing() -> None:
    assert find_user(1) == "Alice"


def test_find_user_missing() -> None:
    assert find_user(99) is None
```

---

## Key Takeaways

- `mypy greet.py` — type check without running; add `strict = true` in config
- `pytest` — `test_*.py` + `def test_*()` + `assert` — zero boilerplate
- `@pytest.mark.parametrize` — one test function, many inputs
- `pytest.raises(ExceptionType, match="regex")` — test exception messages
- `pyproject.toml` — single file for project metadata, deps, and tool config
- `uv` — fast pip + venv replacement; `uv add`, `uv run`, `uv sync`
- `src/` layout — ensures you test the installed package, not raw source files
- Run mypy and pytest in CI on every push

---

## Further Reading

- mypy.readthedocs.io — mypy documentation
- docs.pytest.org — pytest documentation
- packaging.python.org — Python Packaging User Guide
- github.com/astral-sh/uv — uv documentation and changelog
- github.com/astral-sh/ruff — ruff: fast Python linter (also by Astral)
