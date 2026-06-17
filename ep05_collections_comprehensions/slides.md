---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Collections & Comprehensions
### Episode 5 — Python from Scratch
**The Debugger Diary**

---

# Four Core Collection Types

| Type | Literal | Ordered | Mutable | Duplicates |
|---|---|---|---|---|
| `list` | `[1, 2, 3]` | Yes | Yes | Yes |
| `tuple` | `(1, 2, 3)` | Yes | **No** | Yes |
| `set` | `{1, 2, 3}` | No | Yes | **No** |
| `dict` | `{"a": 1}` | Yes* | Yes | Keys: No |

*dict preserves insertion order since Python 3.7

---

# list — Ordered Mutable Sequence

```python
fruits = ["apple", "banana", "cherry"]

fruits.append("date")         # add to end
fruits.insert(1, "avocado")   # insert at index
fruits.remove("banana")       # remove by value
popped = fruits.pop()         # remove and return last

print(fruits[0])      # apple — first element
print(fruits[-1])     # cherry — last element
print(fruits[1:3])    # ['avocado', 'cherry'] — slice
print(len(fruits))    # 3
```

---

# dict — Key-Value Mapping

```python
user = {"name": "Alice", "age": 30, "active": True}

# Access
print(user["name"])              # Alice
print(user.get("email", "N/A"))  # N/A — safe default

# Modify
user["age"] = 31
user["email"] = "alice@example.com"

# Iterate
for key, value in user.items():
    print(f"{key}: {value}")

# Merge (Python 3.9+)
extra = {"role": "admin"}
merged = user | extra
```

---

# set — Unordered Unique Collection

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)    # {1, 2, 3, 4, 5, 6} — union
print(a & b)    # {3, 4}             — intersection
print(a - b)    # {1, 2}             — difference
print(a ^ b)    # {1, 2, 5, 6}       — symmetric difference

# Deduplication
words = ["apple", "banana", "apple", "cherry", "banana"]
unique = list(set(words))
```

---

# tuple — Immutable Sequence

```python
point = (3.0, 4.0)          # coordinates
rgb   = (255, 128, 0)       # fixed structure
empty = ()
single = (42,)              # comma required for single-element

x, y = point               # unpacking
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2,3,4]

# Named tuple — self-documenting
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p = Point(3.0, 4.0)
print(p.x, p.y)   # 3.0 4.0
```

---

# List Comprehensions

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# [expression for item in iterable]
squares = [x ** 2 for x in numbers]

# [expression for item in iterable if condition]
even_squares = [x ** 2 for x in numbers if x % 2 == 0]

# Nested
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]

print(squares)       # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
print(even_squares)  # [4, 16, 36, 64, 100]
print(matrix)        # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

---

# Dict & Set Comprehensions

```python
names = ["Alice", "Bob", "Carol"]

# Dict comprehension
name_lengths = {name: len(name) for name in names}
# {'Alice': 5, 'Bob': 3, 'Carol': 5}

# Invert a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Set comprehension
first_letters = {name[0] for name in names}
# {'A', 'B', 'C'}
```

---

# Generator Expressions

```python
# List comprehension — builds the whole list in memory
total = sum([x ** 2 for x in range(1_000_000)])

# Generator expression — lazy, processes one element at a time
total = sum(x ** 2 for x in range(1_000_000))  # no []

# Only materialise when you need it
gen = (x ** 2 for x in range(10))
print(next(gen))   # 0
print(next(gen))   # 1
print(list(gen))   # [4, 9, 16, 25, 36, 49, 64, 81]
```

Use generators when the sequence is large or potentially infinite.

---

# Built-in Aggregation Functions

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

print(sum(numbers))             # 39
print(min(numbers))             # 1
print(max(numbers))             # 9
print(sorted(numbers))          # [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
print(sorted(numbers, reverse=True))  # [9, 6, 5, 5, ...]

words = ["banana", "apple", "cherry"]
print(sorted(words, key=len))   # ['apple', 'banana', 'cherry']
print(all(x > 0 for x in numbers))  # True
print(any(x > 8 for x in numbers))  # True
```

---

# itertools — Powerful Iteration Tools

```python
import itertools

# Chain multiple iterables
print(list(itertools.chain([1, 2], [3, 4], [5])))
# [1, 2, 3, 4, 5]

# Group by a key
employees = [("Alice", "Eng"), ("Bob", "HR"), ("Carol", "Eng")]
for dept, group in itertools.groupby(employees, key=lambda e: e[1]):
    print(dept, list(group))

# Sliding windows (Python 3.12+)
print(list(itertools.pairwise([1, 2, 3, 4])))
# [(1, 2), (2, 3), (3, 4)]
```

---

# Key Takeaways

- `list` — ordered, mutable; `tuple` — ordered, immutable; `set` — unordered, unique; `dict` — key-value pairs
- List comprehension: `[expr for x in iterable if cond]`
- Dict comprehension: `{k: v for k, v in ...}`
- Generator expression: same as list comprehension but with `()` — lazy
- `sorted(items, key=func)` — non-mutating sort
- `sum`, `min`, `max`, `any`, `all` — built-in aggregation
- `itertools` — chain, group, pair, and combine iterables

---

# What's Next — Episode 6

**Async/Await — Concurrency Made Simple**

- Why async? The problem with blocking I/O
- `async def` and `await` — writing async code
- `asyncio.run()` — entry point for async programs
- `asyncio.gather()` — run tasks concurrently
- `aiohttp` — async HTTP requests
- Structured patterns and error handling

**The Debugger Diary** — Python from Scratch
_"Understand the tools, not just the syntax."_
