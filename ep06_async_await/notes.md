# Episode 6 — Async/Await — Concurrency Made Simple

**Series:** Python from Scratch
**Channel:** The Debugger Diary
**Prerequisites:** Episodes 1–5; familiarity with the concept of I/O operations helps

---

## Episode Overview

Python's `asyncio` library provides cooperative multitasking inside a single thread. When a coroutine hits an `await`, it voluntarily suspends itself, letting the event loop run other coroutines while the I/O operation completes. The result is high concurrency for network-bound code (HTTP, databases, file I/O) without the complexity of threads or the overhead of processes. This episode builds a concurrent API fetcher — simulated without real network calls — to demonstrate the full pattern.

---

## Section 1: Why Async?

### The blocking problem

Standard Python code is synchronous. When you call `requests.get(url)`, the calling thread blocks — it does nothing but wait for the server to respond. If you make 10 requests sequentially and each takes 200ms, you wait 2 seconds even though your CPU is idle for 1.998 seconds of that.

```python
import requests, time

def fetch(url: str) -> str:
    return requests.get(url).text   # whole thread blocks here

start = time.perf_counter()
for i in range(5):
    fetch(f"https://api.example.com/users/{i}")
print(f"Sequential: {time.perf_counter() - start:.2f}s")
# Sequential: ~1.00s (5 × 200ms)
```

### The async solution

With `asyncio`, you write cooperative code. Each coroutine runs until it hits an `await`, then suspends. The event loop runs other coroutines while the first one waits for I/O. All five requests above can be in flight simultaneously:

```python
import asyncio, aiohttp, time

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        return await resp.text()

async def main() -> None:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, f"https://api.example.com/users/{i}") for i in range(5)]
        results = await asyncio.gather(*tasks)
    print(f"Got {len(results)} results")

start = time.perf_counter()
asyncio.run(main())
print(f"Async: {time.perf_counter() - start:.2f}s")
# Async: ~0.20s (all 5 in flight at once)
```

---

## Section 2: async def and await

### Coroutine functions

`async def` creates a coroutine function. Calling it returns a coroutine object — it does not execute the body immediately:

```python
async def greet(name: str) -> str:
    return f"Hello, {name}!"

result = greet("Alice")      # returns a coroutine, prints nothing
print(type(result))          # <class 'coroutine'>
# RuntimeWarning: coroutine 'greet' was never awaited
```

You must `await` it to run the body:

```python
async def main() -> None:
    result = await greet("Alice")
    print(result)   # Hello, Alice!

asyncio.run(main())
```

### `await` suspends, not blocks

`await expr` suspends the current coroutine until `expr` completes, then resumes with the result. While suspended, the event loop can run other coroutines. `await` can only appear inside `async def`.

```python
import asyncio

async def say_after(delay: float, message: str) -> None:
    await asyncio.sleep(delay)   # suspends coroutine; event loop is free
    print(message)

async def main() -> None:
    await say_after(1.0, "one second")
    await say_after(0.5, "half second")  # runs after the first completes

asyncio.run(main())
# Total: ~1.5s (sequential awaits)
```

### asyncio.run()

`asyncio.run(coroutine)` is the entry point for async programs. It:
1. Creates a new event loop
2. Runs the coroutine until it completes
3. Closes the event loop and cleans up

Use it exactly once, at the top level of your program. Do not call it inside a coroutine.

---

## Section 3: asyncio.gather — Concurrency

`asyncio.gather(*coroutines)` runs multiple coroutines concurrently and waits for all of them:

```python
import asyncio

async def fetch_user(user_id: int) -> dict[str, object]:
    await asyncio.sleep(0.2)   # simulated network I/O
    return {"id": user_id, "name": f"User {user_id}"}

async def main() -> None:
    import time
    start = time.perf_counter()

    # Sequential — 0.6s
    u1 = await fetch_user(1)
    u2 = await fetch_user(2)
    u3 = await fetch_user(3)
    print(f"Sequential: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    # Concurrent — 0.2s
    u1, u2, u3 = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    print(f"Concurrent: {time.perf_counter() - start:.2f}s")

asyncio.run(main())
```

`gather` returns results in the **same order** as the input coroutines, regardless of completion order.

### Error handling with gather

```python
async def risky(n: int) -> int:
    if n == 2:
        raise ValueError(f"n={n} is not allowed")
    await asyncio.sleep(0.1)
    return n * 10

async def main() -> None:
    # Default: first exception cancels remaining and propagates
    try:
        results = await asyncio.gather(risky(1), risky(2), risky(3))
    except ValueError as e:
        print(f"Caught: {e}")

    # return_exceptions=True: exceptions become results, all tasks complete
    results = await asyncio.gather(
        risky(1), risky(2), risky(3),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"Error: {r}")
        else:
            print(f"OK: {r}")

asyncio.run(main())
```

---

## Section 4: asyncio.create_task

`create_task` schedules a coroutine to run immediately on the event loop and returns a `Task` object:

```python
import asyncio

async def background_job(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    print(f"  {name} completed after {delay}s")
    return name

async def main() -> None:
    # Tasks start running as soon as they're created
    task_a = asyncio.create_task(background_job("A", 1.0))
    task_b = asyncio.create_task(background_job("B", 0.5))

    print("Both tasks started — doing other work now")
    await asyncio.sleep(0.2)
    print("Still working...")

    # Wait for results
    result_a = await task_a
    result_b = await task_b
    print(f"Done: {result_a}, {result_b}")

asyncio.run(main())
# Both tasks started — doing other work now
# Still working...
#   B completed after 0.5s
#   A completed after 1.0s
# Done: A, B
```

**Difference between `gather` and `create_task`:**
- `gather` creates and awaits tasks in one call — simpler when you want all results
- `create_task` gives you more control — you can await each task independently or cancel one

---

## Section 5: Async Context Managers and Iterators

Any object with `__aenter__` and `__aexit__` works with `async with`:

```python
import asyncio

class AsyncDB:
    async def __aenter__(self) -> "AsyncDB":
        print("Connecting to database...")
        await asyncio.sleep(0.05)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        print("Closing connection...")
        await asyncio.sleep(0.01)

    async def query(self, sql: str) -> list[dict[str, object]]:
        await asyncio.sleep(0.05)   # simulated query time
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

async def main() -> None:
    async with AsyncDB() as db:
        rows = await db.query("SELECT * FROM users LIMIT 10")
        for row in rows:
            print(row)

asyncio.run(main())
```

Async iterators work with `async for`:

```python
async def paginated_results():
    for page in range(3):
        await asyncio.sleep(0.1)
        yield {"page": page, "data": list(range(page * 10, page * 10 + 10))}

async def main() -> None:
    async for batch in paginated_results():
        print(f"Page {batch['page']}: {batch['data'][:3]}...")

asyncio.run(main())
```

---

## Section 6: Real aiohttp Usage

Install: `pip install aiohttp`

```python
import asyncio
import aiohttp
from dataclasses import dataclass

@dataclass
class Post:
    id: int
    title: str
    body: str

async def fetch_post(
    session: aiohttp.ClientSession,
    post_id: int,
) -> Post | None:
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return Post(id=data["id"], title=data["title"], body=data["body"])
    except Exception as e:
        print(f"Failed to fetch post {post_id}: {e}")
        return None

async def main() -> None:
    async with aiohttp.ClientSession() as session:
        posts = await asyncio.gather(
            *(fetch_post(session, i) for i in range(1, 6)),
            return_exceptions=False,
        )
    for post in posts:
        if post:
            print(f"[{post.id}] {post.title[:50]}")

asyncio.run(main())
```

---

## Section 7: Async vs Threads vs Processes

| | asyncio | threading | multiprocessing |
|---|---|---|---|
| Best for | I/O-bound | I/O-bound (legacy libs) | CPU-bound |
| GIL | Not an issue — single thread | GIL limits true parallelism | Bypasses GIL |
| Overhead | Very low | Moderate | High (IPC, serialization) |
| Debugging | Easier (single thread) | Harder (race conditions) | Hardest |
| Libraries | Must use async libs | Works with any library | Works with any library |

**Rule of thumb:**
- Network requests, database queries, file I/O → `asyncio`
- Need to use a synchronous library concurrently → `threading`
- CPU-intensive computation (ML, image processing) → `multiprocessing`

---

## Key Takeaways

- `async def` — coroutine function; calling it returns a coroutine, not the result
- `await expr` — suspend and wait; the event loop runs other coroutines meanwhile
- `asyncio.run(main())` — single entry point; creates, runs, and closes the event loop
- `asyncio.gather(*coros)` — concurrent execution; returns results in input order
- `asyncio.create_task(coro)` — schedule coroutine immediately; await later for result
- `return_exceptions=True` in `gather` — collect errors as values, don't propagate
- `async with` / `async for` — async context managers and iterators
- Use `aiohttp` for async HTTP; `asyncpg`/`aiosqlite` for async databases

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `RuntimeWarning: coroutine was never awaited` | Called `async def` without `await` | Add `await` or use `asyncio.run()` |
| `SyntaxError: 'await' outside async function` | Used `await` in a regular function | Change `def` to `async def` |
| `RuntimeError: This event loop is already running` | Called `asyncio.run()` inside a running loop (e.g., Jupyter) | Use `await coro` directly in Jupyter; or `nest_asyncio` |
| `asyncio.TimeoutError` | Network operation exceeded timeout | Wrap in `asyncio.wait_for(coro, timeout=5)` |

---

## Further Reading

- docs.python.org/3/library/asyncio — asyncio documentation
- aiohttp.readthedocs.io — aiohttp client/server
- peps.python.org/pep-0492 — PEP 492: async/await syntax
- Episode 7: Real-World Python — mypy, pytest, pyproject.toml, uv
