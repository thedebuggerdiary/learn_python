---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Setup & Hello World
### Episode 1 — Python from Scratch
**The Debugger Diary**

---

# Why Python?

- Created by **Guido van Rossum** — runs everywhere (Linux, macOS, Windows)
- **#1 language for data science, ML, scripting, and backend**
- Fixes complexity problems from Java/C++ style languages:
  - **Readable syntax** — no braces, no semicolons, no boilerplate
  - **Dynamic typing** — write less, move fast
  - **Huge ecosystem** — pip + PyPI with 500 000+ packages
- First-class support for async, type hints, and functional patterns

---

# What Python Replaces

```java
// Java — Hello World
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

```python
# Python — Hello World
print("Hello, World!")
```

No class wrapper. No `static`. No `System.out.`. No semicolons. No compilation step.

---

# Step 1: Install Python

**pyenv (Linux / macOS / WSL) — recommended**
```bash
curl https://pyenv.run | bash
pyenv install 3.12
pyenv global 3.12
python --version
# Python 3.12.x
```

**Homebrew (macOS)**
```bash
brew install python@3.12
```

**Windows** — download the installer from python.org
Check "Add Python to PATH" during setup.

---

# Verify the Install

```bash
python --version
# Python 3.12.x

pip --version
# pip 24.x from /usr/local/lib/python3.12/...
```

`pip` is the package manager — it comes bundled with Python 3.

---

# The Python REPL

```bash
python
# Python 3.12.x (main, ...)
# >>>
```

```python
>>> print("Hello, World!")
Hello, World!

>>> name = "Debugger"
>>> print(f"Hello, {name}!")
Hello, Debugger!

>>> [x * x for x in range(1, 6)]
[1, 4, 9, 16, 25]
```

Type `exit()` or press **Ctrl+D** to quit.

---

# Hello World

```python
print("Hello, World!")
```

| Piece | What it does |
|---|---|
| `print` | Built-in function — writes to stdout with a newline |
| `"Hello, World!"` | A string literal |
| No semicolons | Python uses newlines as statement terminators |
| No `main()` | Top-level code runs immediately |

---

# Running a Python Script

```bash
python hello_world.py
# Hello, World!
```

No compile step. The interpreter reads and runs the file directly.

**Making a script executable (Linux/macOS):**
```python
#!/usr/bin/env python3
print("Hello, World!")
```
```bash
chmod +x hello_world.py
./hello_world.py
```

---

# f-Strings (Formatted String Literals)

```python
name = "Debugger Diary"

# f"..." — embed any expression inside { }
print(f"Hello, {name}!")
print(f"Length: {len(name)}")
print(f"Upper: {name.upper()}")
print(f"2 + 2 = {2 + 2}")
```

Output:
```
Hello, Debugger Diary!
Length: 14
Upper: DEBUGGER DIARY
2 + 2 = 4
```

No concatenation needed. Works with any expression inside `{ }`.

---

# Command-Line Arguments

```python
import sys

if len(sys.argv) < 2:
    print("Usage: python hello_world.py <name>")
    sys.exit(1)

name = sys.argv[1]
print(f"Hello, {name}!")
```

```bash
python hello_world.py Alice
# Hello, Alice!
```

`sys.argv[0]` is always the script name itself.

---

# Virtual Environments

Always isolate project dependencies with a venv:

```bash
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install a package
pip install requests

# Deactivate when done
deactivate
```

Your prompt shows `(.venv)` while active.

---

# VS Code Workflow

1. **File → Open Folder** — open your project directory
2. Install the **Python** extension by Microsoft
3. **Ctrl+Shift+P** → "Python: Select Interpreter" → pick your `.venv`
4. Create a new `.py` file
5. Press **F5** to run with the debugger
6. **Ctrl+` ** opens the integrated terminal

No separate tool needed. The extension handles linting, formatting, and IntelliSense.

---

# Key Takeaways

- Python 3.12+ — install via pyenv, Homebrew, or python.org
- `python <file>.py` — no compile step, runs immediately
- `print()` — built-in, no import needed
- f-strings — `f"Hello, {name}"` — any expression inside `{ }`
- No semicolons — newlines terminate statements
- `python` with no arguments — opens the interactive REPL
- Virtual environments — `python -m venv .venv` — always use one

---

# What's Next — Episode 2

**Variables, Types & Type Hints**

- Dynamic typing — variables hold any type
- Built-in types — `int`, `str`, `float`, `bool`, `None`
- Type hints — `name: str = "Alice"` — for tooling and clarity
- `Optional[str]` — the Python equivalent of nullable
- `isinstance()` — check types at runtime
- Why type hints matter even though Python doesn't enforce them

**The Debugger Diary** — Python from Scratch
_"Understand the tools, not just the syntax."_
