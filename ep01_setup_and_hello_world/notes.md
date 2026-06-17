# Episode 1 — Setup & Hello World

**Series:** Python from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Basic programming experience in any language

---

## Episode Overview

This is the starting point for the Python from Scratch series. By the end of this episode you will have Python installed, a working Hello World program running from the command line, and an understanding of what makes Python worth learning. We also tour the Python REPL so you can experiment interactively.

---

## Section 1: Why Python?

Python is a dynamically-typed, interpreted language created by Guido van Rossum and first released in 1991. It is consistently ranked the most popular programming language in the world (TIOBE, Stack Overflow Survey). It is the dominant language for data science and machine learning, has a thriving web backend ecosystem (Django, FastAPI), and is widely used for scripting, automation, and DevOps.

**What Python does well:**
- Readable, expressive syntax with minimal boilerplate
- Enormous standard library — "batteries included"
- 500 000+ third-party packages on PyPI (pip install anything)
- Fast iteration — edit a file, run it, see results immediately
- First-class support for async, type hints, and functional patterns

**What Python is similar to:**
- Ruby — concise, readable, expressive
- Kotlin — both support type inference, lambdas, and functional patterns
- JavaScript — both are dynamically typed with first-class functions

**Where Python is used:**
- Data science and ML: NumPy, pandas, scikit-learn, PyTorch, TensorFlow
- Web backends: Django, FastAPI, Flask
- Scripting and automation: system scripts, CI pipelines, AWS Lambda
- CLIs: Click, Typer

---

## Section 2: Install Python

### Option A — pyenv (Linux / macOS / WSL) — Recommended

pyenv manages multiple Python versions the same way nvm manages Node versions.

```bash
curl https://pyenv.run | bash
```

Follow the instructions it prints to add pyenv to your shell profile, then restart your terminal.

```bash
pyenv install 3.12
pyenv global 3.12
python --version
# Python 3.12.x
```

### Option B — Homebrew (macOS)

```bash
brew install python@3.12
python3 --version
```

### Option C — python.org installer (Windows / any OS)

1. Go to python.org/downloads
2. Download the latest Python 3.12+ installer
3. Run it — check **"Add Python to PATH"** before clicking Install
4. Open a new terminal: `python --version`

### Verify the install

```bash
python --version
# Python 3.12.x

pip --version
# pip 24.x from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

If `python` maps to Python 2 on your system, use `python3` instead. On macOS with Homebrew you may need `python3` explicitly.

---

## Section 3: The Python REPL

Before writing files, try the interactive REPL. Start it:

```bash
python
# Python 3.12.x (main, Dec  7 2023, 15:14:16)
# [GCC 11.4.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>>
```

Try these one by one:

```python
>>> print("Hello, World!")
Hello, World!

>>> name = "Debugger"
>>> print(f"Hello, {name}!")
Hello, Debugger!

>>> 2 + 2
4

>>> [x * x for x in range(1, 6)]
[1, 4, 9, 16, 25]

>>> type(42)
<class 'int'>

>>> type("hello")
<class 'str'>
```

Exit with `exit()` or **Ctrl+D** (Linux/macOS) / **Ctrl+Z Enter** (Windows).

The REPL evaluates every expression and prints its value. It is great for trying syntax, testing one-liners, and exploring the standard library. Everything you type in the REPL also works in `.py` files.

---

## Section 4: Hello World — Step by Step

### Create the file

Create `hello_world.py`:

```python
print("Hello, World!")
```

That is the entire program. Compare this to the Java equivalent:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

Python eliminates:
- `public class HelloWorld { }` wrapper — Python files run top-to-bottom; no class needed
- `public static void main(String[] args)` — there is no entry-point ceremony
- `System.out.println` — `print` is a built-in global function
- Semicolons — Python uses newlines as statement terminators
- The compile step — `python hello_world.py` interprets the file directly

### Run it

```bash
python hello_world.py
# Hello, World!
```

### Breaking it down

**`print("Hello, World!")**`
`print` is a built-in function — it is always available without any import. It writes the argument to standard output and appends a newline. You can pass multiple arguments: `print("a", "b", "c")` outputs `a b c`.

**`"Hello, World!"`**
A string literal. Python accepts both `"double"` and `'single'` quotes — they are identical. Use whichever you prefer; the Debugger Diary convention is double quotes for prose strings, single quotes for short internal keys.

**No semicolons**
Python treats a newline as the end of a statement. You can put a semicolon at the end of a line, but the style guide (PEP 8) says not to.

**No class, no main()**
In Python, every `.py` file is a module. Top-level code runs immediately when the file is executed. The `if __name__ == "__main__":` guard (covered below) is a convention — not a requirement — for code that should only run when the file is the entry point, not when it is imported.

### The `if __name__ == "__main__":` guard

```python
def greet(name: str) -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    greet("World")
```

When Python runs a file directly, `__name__` is set to `"__main__"`. When the file is imported as a module, `__name__` is the module name instead. This guard lets you write files that are both importable and directly runnable — a common Python pattern.

---

## Section 5: f-Strings

Python 3.6 introduced f-strings (formatted string literals), the idiomatic way to embed values in strings.

```python
name = "Debugger Diary"
version = 3

# Simple variable
print(f"Hello, {name}!")

# Any expression
print(f"Python version: {version}.12")
print(f"Name length: {len(name)} characters")
print(f"Uppercase: {name.upper()}")
print(f"2 + 2 = {2 + 2}")
```

Output:
```
Hello, Debugger Diary!
Python version: 3.12
Name length: 14 characters
Uppercase: DEBUGGER DIARY
2 + 2 = 4
```

**Rules:**
- Prefix the string with `f` (or `F`) before the opening quote
- `{expression}` — anything inside braces is evaluated at runtime
- Works with variables, method calls, arithmetic, conditionals — any valid Python expression

**Format specifiers** — control number formatting:
```python
pi = 3.14159265
print(f"Pi to 2 decimal places: {pi:.2f}")  # 3.14
print(f"Big number: {1_000_000:,}")          # 1,000,000
print(f"Percentage: {0.853:.1%}")            # 85.3%
```

f-strings compile to efficient string formatting calls — they are the fastest string formatting option in Python and the recommended approach since Python 3.6.

---

## Section 6: Command-Line Arguments

```python
import sys

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python hello_world.py <name>")
        sys.exit(1)

    name = sys.argv[1]
    print(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

```bash
python hello_world.py Alice
# Hello, Alice!

python hello_world.py
# Usage: python hello_world.py <name>
```

`sys.argv` is a list of strings. `sys.argv[0]` is the script name; arguments start at index 1. For real CLI programs use the `argparse` module (standard library) or the third-party `click`/`typer` packages — they handle help text, type conversion, and validation automatically.

---

## Section 7: Virtual Environments

A virtual environment is an isolated directory containing a specific Python version and a set of installed packages. Every project should have its own.

**Why:**
- Project A needs `requests==2.28`, project B needs `requests==2.31` — without venvs they conflict
- Your system Python stays clean
- You can reproduce the environment exactly with `pip freeze > requirements.txt`

**Create and activate:**
```bash
# Create (run once per project)
python -m venv .venv

# Activate — Linux/macOS
source .venv/bin/activate

# Activate — Windows PowerShell
.venv\Scripts\Activate.ps1

# Install packages (inside the activated venv)
pip install requests

# Freeze dependencies
pip freeze > requirements.txt

# Deactivate when done
deactivate
```

Your terminal prompt shows `(.venv)` while the environment is active.

**Restoring on a different machine:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**uv** (modern alternative, much faster):
```bash
pip install uv
uv venv
uv pip install requests
```

Episode 7 covers `uv` and `pyproject.toml` in depth.

---

## Section 8: VS Code Workflow

For longer programs the IDE is much faster than the command line.

1. **File → Open Folder** — open your project directory
2. Install the **Python** extension by Microsoft (identifier: `ms-python.python`)
3. Press **Ctrl+Shift+P** → type "Python: Select Interpreter" → pick `.venv/bin/python`
4. Create a new file: `hello_world.py`
5. Press **F5** to run with the debugger, or **Ctrl+F5** to run without
6. Output appears in the integrated terminal at the bottom

**Useful shortcuts:**
- **Ctrl+` ** — toggle integrated terminal
- **F5** — run with debugger
- **Shift+F5** — stop debugger
- **F9** — toggle breakpoint

**Recommended extensions:**
- `ms-python.python` — IntelliSense, debugger, test runner
- `ms-python.mypy-type-checker` — inline type error display
- `ms-python.black-formatter` — auto-format on save
- `marp-team.marp-vscode` — live Marp slide preview

---

## Key Takeaways

- Python 3.12+ — install via pyenv (recommended), Homebrew, or python.org
- `python <file>.py` — no compile step; the interpreter runs the file directly
- `print()` — built-in function, always available, no import needed
- f-strings — `f"Hello, {name}"` — any expression inside `{ }`
- No semicolons — newlines terminate statements
- `python` with no arguments — opens the interactive REPL; exit with `exit()` or Ctrl+D
- Virtual environments — `python -m venv .venv` — always isolate your dependencies
- `if __name__ == "__main__":` — lets a file be both importable and runnable

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `python: command not found` | Python not on PATH | Add Python to PATH and restart terminal |
| `SyntaxError: invalid syntax` | Indentation error or typo | Check indentation; Python uses 4 spaces |
| `ModuleNotFoundError: No module named 'X'` | Package not installed | `pip install X` inside your active venv |
| `PermissionError: .venv/Scripts/Activate.ps1` | PowerShell execution policy | Run `Set-ExecutionPolicy -Scope Process Unrestricted` |
| `IndentationError: unexpected indent` | Mixed tabs and spaces | Configure editor to use spaces only |

---

## Further Reading

- docs.python.org/3/tutorial — official Python tutorial
- peps.python.org/pep-0008 — PEP 8: Python style guide
- realpython.com — tutorials for Python beginners and beyond
- Episode 2: Variables, Types & Type Hints — dynamic typing, `Optional`, type annotations
