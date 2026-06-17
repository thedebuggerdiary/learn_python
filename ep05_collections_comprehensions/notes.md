# Episode 5 — Collections & Comprehensions

**Series:** Python from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episodes 1–4

---

## Episode Overview

Python's four built-in collection types — `list`, `tuple`, `set`, `dict` — handle most real-world data needs. Comprehensions are the idiomatic way to build and transform collections in one readable expression. Generator expressions add lazy evaluation for large or streaming data. This episode builds an employee dataset query pipeline to demonstrate them all together.

---

## Section 1: list

A `list` is an ordered, mutable, dynamically-sized sequence. It is the most versatile Python collection.

```python
fruits: list[str] = ["apple", "banana", "cherry"]

# Adding items
fruits.append("date")             # add to end: ['apple', 'banana', 'cherry', 'date']
fruits.insert(1, "avocado")       # insert at index: ['apple', 'avocado', ...]
fruits.extend(["elderberry"])     # add all from iterable

# Removing items
fruits.remove("banana")           # remove first match by value
popped = fruits.pop()             # remove and return last item
popped_at = fruits.pop(0)         # remove and return item at index 0

# Indexing and slicing
print(fruits[0])                  # first element
print(fruits[-1])                 # last element
print(fruits[1:3])                # elements at index 1, 2
print(fruits[::2])                # every other element
print(fruits[::-1])               # reversed

# Querying
print(len(fruits))                # count
print("apple" in fruits)          # membership test — O(n)
print(fruits.count("apple"))      # number of occurrences
print(fruits.index("cherry"))     # index of first occurrence

# Sorting
fruits.sort()                     # sort in place
fruits.sort(key=str.lower)        # sort by lowercase (case-insensitive)
sorted_fruits = sorted(fruits)    # return new sorted list, don't mutate
```

**list vs tuple — when to use which:**
- `list` — ordered sequence that will grow or shrink, or where mutation is needed
- `tuple` — fixed-size, heterogeneous record (like a row in a database); hashable if elements are hashable

---

## Section 2: dict

A `dict` is an ordered (Python 3.7+) mapping from keys to values. Keys must be hashable (strings, numbers, tuples — not lists or dicts).

```python
user: dict[str, object] = {
    "name": "Alice",
    "age": 30,
    "active": True,
}

# Access
name = user["name"]                    # KeyError if missing
email = user.get("email")              # None if missing
email = user.get("email", "N/A")       # default if missing

# Modify
user["age"] = 31
user["email"] = "alice@example.com"
del user["active"]

# Querying
print("name" in user)                  # key membership test
print(list(user.keys()))               # ["name", "age", "email"]
print(list(user.values()))             # ["Alice", 31, "alice@..."]
print(list(user.items()))              # [("name", "Alice"), ...]

# Iterating
for key, value in user.items():
    print(f"{key}: {value}")

# Merging
extra = {"role": "admin", "team": "backend"}
merged = user | extra                  # Python 3.9+ — returns new dict
user |= extra                          # Python 3.9+ — merge in place

# setdefault — insert if key absent
user.setdefault("score", 0)

# dict.fromkeys — create with default value
keys = ["a", "b", "c"]
template = dict.fromkeys(keys, 0)      # {'a': 0, 'b': 0, 'c': 0}
```

---

## Section 3: set

A `set` is an unordered collection of unique, hashable objects.

```python
a: set[int] = {1, 2, 3, 4}
b: set[int] = {3, 4, 5, 6}

# Set operations
print(a | b)    # union:                {1, 2, 3, 4, 5, 6}
print(a & b)    # intersection:         {3, 4}
print(a - b)    # difference (a not b): {1, 2}
print(b - a)    # difference (b not a): {5, 6}
print(a ^ b)    # symmetric difference: {1, 2, 5, 6}

# Subset/superset
print({1, 2} <= a)   # True — {1,2} is a subset of a
print(a >= {1, 2})   # True — a is a superset of {1,2}

# Membership is O(1) — unlike list O(n)
print(3 in a)   # True

# Deduplication pattern
words = ["apple", "banana", "apple", "cherry", "banana"]
unique_words = list(set(words))
```

---

## Section 4: tuple

```python
point: tuple[float, float] = (3.0, 4.0)
color: tuple[int, int, int] = (255, 128, 0)

# Unpacking
x, y = point
r, g, b = color

# Extended unpacking
first, *middle, last = (1, 2, 3, 4, 5)
# first=1, middle=[2, 3, 4], last=5

# Tuples as dict keys (lists cannot be dict keys)
grid: dict[tuple[int, int], str] = {}
grid[(0, 0)] = "origin"
grid[(1, 0)] = "right"
```

**NamedTuple** — self-documenting tuples with field names:

```python
from typing import NamedTuple

class Employee(NamedTuple):
    name: str
    department: str
    salary: float

emp = Employee("Alice", "Engineering", 95_000.0)
print(emp.name)        # Alice
print(emp[0])          # Alice — still subscriptable
dept, name = emp.department, emp.name
```

---

## Section 5: List Comprehensions

Comprehensions are the idiomatic Python way to build and transform collections in a single readable expression.

```python
numbers = range(1, 11)

# Basic: [expression for item in iterable]
squares = [x ** 2 for x in numbers]
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# With filter: [expression for item in iterable if condition]
even_squares = [x ** 2 for x in numbers if x % 2 == 0]
# [4, 16, 36, 64, 100]

# Transform strings
names = ["  Alice ", "  BOB  ", "carol"]
clean = [name.strip().title() for name in names]
# ['Alice', 'Bob', 'Carol']

# Nested — flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

**Comprehension vs for loop:**
Comprehensions are faster than equivalent `for` loops building a list (the `LOAD_FAST` / `LIST_APPEND` bytecodes are tighter). More importantly, they communicate *intent* — "I am building a list from this iterable" — rather than "I am running a loop that also builds a list".

---

## Section 6: Dict and Set Comprehensions

```python
names = ["Alice", "Bob", "Carol", "Dave"]

# Dict comprehension
name_lengths: dict[str, int] = {name: len(name) for name in names}
# {'Alice': 5, 'Bob': 3, 'Carol': 5, 'Dave': 4}

# Filter in dict comprehension
long_names = {name: len(name) for name in names if len(name) > 3}
# {'Alice': 5, 'Carol': 5, 'Dave': 4}

# Invert a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}

# Set comprehension — unique first characters
first_chars: set[str] = {name[0] for name in names}
# {'A', 'B', 'C', 'D'}
```

---

## Section 7: Generator Expressions

Generator expressions look like list comprehensions but use `()` instead of `[]`. They are lazy — they produce values one at a time instead of building the whole list.

```python
# List comprehension — allocates the full list
all_squares = [x ** 2 for x in range(1_000_000)]

# Generator — computes one value per iteration, constant memory
gen = (x ** 2 for x in range(1_000_000))

# Works with aggregation functions directly
total = sum(x ** 2 for x in range(1_000_000))  # no [] needed
maximum = max(x ** 2 for x in range(1, 11))

# Chaining generators
evens = (x for x in range(100) if x % 2 == 0)
even_squares = (x ** 2 for x in evens)
first_five = list(itertools.islice(even_squares, 5))
# [0, 4, 16, 36, 64]
```

Use generators when:
- The collection is large (millions of items)
- You only need to iterate once
- You are passing the result to `sum`, `min`, `max`, `any`, `all`

---

## Section 8: Built-in Aggregation

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
words = ["banana", "apple", "cherry", "date"]

# Numeric
print(sum(numbers))                            # 39
print(min(numbers))                            # 1
print(max(numbers))                            # 9

# Sorting — always returns a new list
print(sorted(numbers))                         # ascending
print(sorted(numbers, reverse=True))           # descending
print(sorted(words, key=len))                  # by length
print(sorted(words, key=lambda w: (-len(w), w)))  # length desc, alpha asc

# Predicates
print(all(x > 0 for x in numbers))            # True
print(any(x > 8 for x in numbers))            # True
print(any(x > 100 for x in numbers))          # False

# Enumerate — index + value
for i, name in enumerate(words, start=1):
    print(f"{i}. {name}")

# zip — combine multiple iterables
names = ["Alice", "Bob"]
scores = [95, 87]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

---

## Section 9: itertools

`itertools` provides efficient building blocks for working with iterables:

```python
import itertools

# chain — concatenate iterables without copying
all_items = list(itertools.chain([1, 2], [3, 4], [5]))
# [1, 2, 3, 4, 5]

# islice — lazy slice
first_five = list(itertools.islice(range(1000), 5))
# [0, 1, 2, 3, 4]

# groupby — group consecutive elements by key
employees = [
    ("Alice", "Eng"), ("Carol", "Eng"),
    ("Bob", "HR"), ("Dave", "HR"),
    ("Eve", "Sales"),
]
# Must be sorted by the grouping key first
employees_sorted = sorted(employees, key=lambda e: e[1])
for dept, group in itertools.groupby(employees_sorted, key=lambda e: e[1]):
    members = [e[0] for e in group]
    print(f"{dept}: {members}")

# pairwise (Python 3.12+)
pairs = list(itertools.pairwise([1, 2, 3, 4]))
# [(1, 2), (2, 3), (3, 4)]

# product — cartesian product
for suit, rank in itertools.product(["♠", "♥"], ["A", "K", "Q"]):
    print(f"{rank}{suit}", end=" ")
```

---

## Demo: Employee Dataset Query Pipeline

```python
from dataclasses import dataclass
import itertools

@dataclass
class Employee:
    name: str
    department: str
    salary: float
    years: int

employees = [
    Employee("Alice",   "Engineering", 95_000, 5),
    Employee("Bob",     "HR",          65_000, 3),
    Employee("Carol",   "Engineering", 105_000, 8),
    Employee("Dave",    "HR",          72_000, 6),
    Employee("Eve",     "Engineering", 88_000, 2),
    Employee("Frank",   "Sales",       78_000, 4),
]

# Top earners in Engineering
eng_top = sorted(
    (e for e in employees if e.department == "Engineering"),
    key=lambda e: e.salary,
    reverse=True,
)
print("Top Engineering earners:")
for e in eng_top:
    print(f"  {e.name}: ${e.salary:,.0f}")

# Average salary by department
by_dept = sorted(employees, key=lambda e: e.department)
for dept, group in itertools.groupby(by_dept, key=lambda e: e.department):
    members = list(group)
    avg = sum(e.salary for e in members) / len(members)
    print(f"{dept}: avg ${avg:,.0f}")

# Senior employees (5+ years) across all departments
seniors = [e.name for e in employees if e.years >= 5]
print(f"Seniors: {seniors}")
```

---

## Key Takeaways

- `list` — ordered mutable; `tuple` — ordered immutable; `set` — unique unordered; `dict` — key→value
- List comprehension: `[expr for x in it if cond]` — build a list in one expression
- Dict comprehension: `{k: v for k, v in pairs}` — build a dict in one expression
- Generator expression: `(expr for x in it)` — lazy; pass directly to `sum`/`min`/`max`
- `sorted(items, key=func, reverse=bool)` — non-mutating sort
- `enumerate(items, start=0)` — index + value pairs
- `zip(a, b)` — parallel iteration
- `any(pred)` / `all(pred)` — boolean aggregation
- `itertools.chain`, `groupby`, `islice`, `pairwise`, `product`

---

## Further Reading

- docs.python.org/3/tutorial/datastructures — official collection tutorial
- docs.python.org/3/library/itertools — itertools reference
- peps.python.org/pep-0202 — list comprehensions (PEP 202)
- Episode 6: Async/Await — Concurrency Made Simple
