# Python from Scratch
**Channel:** The Debugger Diary

## Series Goal

This series teaches Python from the ground up, targeting developers who already know at least one language (Kotlin, Java, JavaScript, C++, or similar) and want to become productive in Python quickly. You will learn the language core — types, functions, classes, collections, and async — and finish with practical real-world patterns: type checking with mypy, testing with pytest, and packaging with pip. Each episode is standalone; you can watch them in order or jump to the topic you need.

---

## Episode Plan

| # | Title | Key Topics | Demo | Duration Est. |
|---|-------|-----------|------|--------------|
| 1 | Setup & Hello World | Install Python, venv, the REPL, `print()`, f-strings, running scripts with `python` | Hello World CLI program | 12–15 min |
| 2 | Variables, Types & Type Hints | Dynamic typing, built-in types, `None`, `Optional`, type hints (PEP 484), `isinstance()` | Typed user profile reader | 15–18 min |
| 3 | Functions & Lambdas | `def`, default params, `*args`/`**kwargs`, `lambda`, higher-order functions, decorators | Custom filter/transform pipeline | 15–18 min |
| 4 | Classes, Dataclasses & Protocols | `class`, `__init__`, `@dataclass`, `@property`, dunder methods, `Protocol`, inheritance | Shape hierarchy with Protocol | 18–22 min |
| 5 | Collections & Comprehensions | `list`, `dict`, `set`, `tuple`, list/dict/set comprehensions, generators, `itertools` | Employee dataset query pipeline | 15–18 min |
| 6 | Async/Await — Concurrency Made Simple | Why async, `async def`, `await`, `asyncio.gather`, `asyncio.run`, `aiohttp`, structured patterns | Concurrent API fetcher (simulated) | 18–22 min |
| 7 | Real-World Python | `mypy` type checking, `pytest` testing, `pip` + `pyproject.toml` packaging, `uv` | Typed, tested, packaged mini library | 15–18 min |

**Total series:** ~108–131 minutes across 7 episodes

---

## Prerequisites

### Knowledge
- Basic programming experience in any language (Kotlin, Java, JavaScript, C++)
- Understanding of what a function, variable, and class is
- For Episode 6: familiarity with the concept of async/threading helps but is not required
- For Episode 7: basic understanding of what a package manager does

### Tools to Install

**Python 3.12+**
- Download from python.org or via `pyenv`
- Verify: `python --version`

**pip** (bundled with Python)
- Verify: `pip --version`

**VS Code (recommended)**
- Install the Python extension by Microsoft
- Gives you IntelliSense, debugger, test runner integration

**Marp** (for slides)
- VS Code extension: "Marp for VS Code"
- Or CLI: `npm install -g @marp-team/marp-cli`

---

## Repository Structure

```
learn_python/
├── VIDEO_SERIES_PLAN.md       ← You are here
├── README.md
├── ep01_setup_and_hello_world/
│   ├── slides.md              ← Marp presentation
│   ├── notes.md               ← Full reference + source code
│   └── code/
│       └── hello_world.py
├── ep02_variables_types_hints/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── types_demo.py
├── ep03_functions_and_lambdas/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── functions.py
├── ep04_classes_dataclasses/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── shapes.py
├── ep05_collections_comprehensions/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── employees.py
├── ep06_async_await/
│   ├── slides.md
│   ├── notes.md
│   └── code/
│       └── fetcher.py
└── ep07_real_world_python/
    ├── slides.md
    ├── notes.md
    └── code/
        ├── pyproject.toml
        ├── greet.py
        └── test_greet.py
```

---

## How to Use This Repo

- **Slides** (`slides.md`): Open in VS Code with the Marp extension for a live preview. Export to PDF or HTML for recording.
- **Notes** (`notes.md`): Full script/reference. Read before recording. Contains all source code, explanations, and talking points.
- **Code** (`code/`): Runnable Python files for each episode. Run with `python <file>.py`, or open the folder in VS Code and press **F5** to debug.
