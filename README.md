# Python from Scratch

A YouTube video series by **The Debugger Diary** that teaches Python from the ground up, targeting developers who already know at least one language and want to learn Python quickly.

You will learn variables and type hints, functions and lambdas, classes and dataclasses, collections, async/await, and finish with a practical introduction to writing real-world Python with type checking and testing.

---

## Who This Is For

- Kotlin, Java, or C++ developers who want to add Python to their toolkit
- Data engineers and backend developers curious about Python's ecosystem
- Anyone who wants to understand what makes Python's dynamic typing, comprehensions, and async model special

No prior Python knowledge needed. Basic programming experience in any language is enough to follow from Episode 1.

---

## Episodes

| # | Folder | Title |
|---|--------|-------|
| 1 | [ep01_setup_and_hello_world](ep01_setup_and_hello_world/) | Setup & Hello World |
| 2 | [ep02_variables_types_hints](ep02_variables_types_hints/) | Variables, Types & Type Hints |
| 3 | [ep03_functions_and_lambdas](ep03_functions_and_lambdas/) | Functions & Lambdas |
| 4 | [ep04_classes_dataclasses](ep04_classes_dataclasses/) | Classes, Dataclasses & Protocols |
| 5 | [ep05_collections_comprehensions](ep05_collections_comprehensions/) | Collections & Comprehensions |
| 6 | [ep06_async_await](ep06_async_await/) | Async/Await — Concurrency Made Simple |
| 7 | [ep07_real_world_python](ep07_real_world_python/) | Real-World Python: Types, Tests & Packaging |

---

## How to Use This Repo

Each episode folder contains:

- **`slides.md`** — Marp Markdown presentation. Open in VS Code with the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension for a live slide preview. Export to PDF/HTML for screen recording.
- **`notes.md`** — Complete reference document with full explanations, all source code, talking points, and further reading.
- **`code/`** — Runnable Python source files for the episode.

---

## Setup

### Install Python

Download Python 3.12+ from [python.org](https://python.org/downloads) or use a version manager.

**Via `pyenv` (Linux/macOS/WSL):**
```bash
curl https://pyenv.run | bash
pyenv install 3.12
pyenv global 3.12
python --version
# Python 3.12.x
```

**Windows:** Download the installer from python.org. Check "Add Python to PATH" during install.

Verify:
```bash
python --version
# Python 3.12.x
pip --version
# pip 24.x from ...
```

### Create a virtual environment

Always work inside a virtual environment to isolate project dependencies:

```bash
python -m venv .venv

# Activate — Linux/macOS
source .venv/bin/activate

# Activate — Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Install packages
pip install <package-name>
```

### Run a Python file

```bash
python hello_world.py
# Hello, World!
```

Or use the interactive REPL:

```bash
python
# Python 3.12.x
# >>>
```

### Marp (for slides)

Install the **Marp for VS Code** extension, or use the CLI:

```bash
npm install -g @marp-team/marp-cli
marp ep01_setup_and_hello_world/slides.md --pdf
```

---

## See Also

- `VIDEO_SERIES_PLAN.md` — full episode breakdown with topics, demos, and duration estimates
