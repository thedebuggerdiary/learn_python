---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Async/Await — Concurrency Made Simple
### Episode 6 — Python from Scratch
**The Debugger Diary**

---

# The Problem: Blocking I/O

```python
import time, requests

def fetch(url: str) -> str:
    return requests.get(url).text   # blocks the whole program

# Sequential — waits for each request to finish before starting the next
start = time.perf_counter()
fetch("https://api.example.com/users/1")   # 200ms wait
fetch("https://api.example.com/users/2")   # 200ms wait
fetch("https://api.example.com/users/3")   # 200ms wait
# Total: ~600ms
```

Each `requests.get` blocks the thread. Three independent requests run one by one.

---

# The Solution: Async I/O

```python
import asyncio, aiohttp, time

async def fetch(session, url: str) -> str:
    async with session.get(url) as resp:
        return await resp.text()

async def main():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            fetch(session, "https://api.example.com/users/1"),
            fetch(session, "https://api.example.com/users/2"),
            fetch(session, "https://api.example.com/users/3"),
        )
    print(results)

asyncio.run(main())   # ~200ms total — all three run concurrently
```

---

# `async def` and `await`

```python
import asyncio

async def say_hello(name: str) -> str:
    await asyncio.sleep(1)          # simulates I/O wait
    return f"Hello, {name}!"

async def main() -> None:
    result = await say_hello("Alice")
    print(result)

asyncio.run(main())
# Hello, Alice!
```

- `async def` — defines a coroutine function
- `await` — suspends the coroutine until the awaitable completes
- `asyncio.run()` — runs the top-level coroutine and closes the event loop

---

# Coroutines vs Threads

| | Async / Coroutines | Threads |
|---|---|---|
| Concurrency model | Cooperative — yields at `await` | Preemptive — OS decides |
| Overhead | Very low (no OS context switch) | Higher (OS thread per task) |
| Shared state | Safe — only one coroutine runs at a time | Needs locks |
| Best for | I/O-bound work (HTTP, DB, files) | CPU-bound work |
| In Python | `asyncio` | `threading` / `concurrent.futures` |

For CPU-bound work: use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.

---

# `asyncio.gather` — Run Concurrently

```python
import asyncio

async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.2)   # simulated network delay
    return {"id": user_id, "name": f"User {user_id}"}

async def main() -> None:
    # All three run at the same time
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    for user in users:
        print(user)

asyncio.run(main())
# ~0.2s total instead of ~0.6s
```

`gather` returns a list of results in the same order as the input coroutines.

---

# `asyncio.gather` with Error Handling

```python
async def risky(n: int) -> int:
    if n == 2:
        raise ValueError("n cannot be 2")
    await asyncio.sleep(0.1)
    return n * 10

async def main() -> None:
    # return_exceptions=True — errors become results, don't cancel others
    results = await asyncio.gather(
        risky(1), risky(2), risky(3),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"Error: {r}")
        else:
            print(f"Result: {r}")

asyncio.run(main())
```

---

# `asyncio.create_task` — Fire and Forget

```python
import asyncio

async def background_job(name: str) -> None:
    await asyncio.sleep(1)
    print(f"{name} done")

async def main() -> None:
    task1 = asyncio.create_task(background_job("A"))
    task2 = asyncio.create_task(background_job("B"))

    print("Tasks started, doing other work...")
    await asyncio.sleep(0.5)
    print("Still doing work...")

    await task1   # wait for task1 to complete
    await task2   # wait for task2 to complete

asyncio.run(main())
```

`create_task` schedules the coroutine to run on the event loop immediately.

---

# Async Context Managers

```python
import asyncio

class AsyncDB:
    async def __aenter__(self):
        print("Connecting...")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, *args):
        print("Disconnecting...")

    async def query(self, sql: str) -> list[dict]:
        await asyncio.sleep(0.05)
        return [{"id": 1, "name": "Alice"}]

async def main() -> None:
    async with AsyncDB() as db:
        results = await db.query("SELECT * FROM users")
        print(results)

asyncio.run(main())
```

---

# Key Takeaways

- `async def` — defines a coroutine; calling it returns a coroutine object, not the result
- `await expr` — suspends and waits; can only be used inside `async def`
- `asyncio.run(coro)` — entry point for async programs; runs and closes the event loop
- `asyncio.gather(*coros)` — run multiple coroutines concurrently; collect results
- `asyncio.create_task(coro)` — schedule a coroutine to run "in the background"
- Async is great for **I/O-bound** work; for CPU-bound use `ProcessPoolExecutor`
- `async with` / `async for` — async context managers and iterators

---

# What's Next — Episode 7

**Real-World Python: Types, Tests & Packaging**

- `mypy` — catch type errors before you run the code
- `pytest` — write and run tests in seconds
- `pyproject.toml` — modern Python packaging
- `uv` — the fast modern pip + venv replacement
- Project layout — where to put your files

**The Debugger Diary** — Python from Scratch
_"Understand the tools, not just the syntax."_
