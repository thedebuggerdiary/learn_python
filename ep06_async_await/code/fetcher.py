"""
Simulated concurrent API fetcher — no real network calls.
Install aiohttp for real HTTP: pip install aiohttp
"""

import asyncio
import time
import random
from dataclasses import dataclass


@dataclass
class UserResult:
    user_id: int
    name: str
    latency_ms: float


async def fetch_user(user_id: int) -> UserResult:
    """Simulate a network request with variable latency."""
    delay = random.uniform(0.1, 0.4)
    await asyncio.sleep(delay)
    return UserResult(
        user_id=user_id,
        name=f"User {user_id}",
        latency_ms=delay * 1000,
    )


async def fetch_user_failing(user_id: int) -> UserResult:
    """Simulate a request that may fail."""
    if user_id % 3 == 0:
        raise ConnectionError(f"Server error for user {user_id}")
    return await fetch_user(user_id)


async def sequential_demo() -> None:
    print("--- Sequential ---")
    start = time.perf_counter()
    for uid in range(1, 6):
        result = await fetch_user(uid)
        print(f"  {result.name} ({result.latency_ms:.0f}ms)")
    print(f"Total: {time.perf_counter() - start:.2f}s\n")


async def concurrent_demo() -> None:
    print("--- Concurrent (gather) ---")
    start = time.perf_counter()
    results = await asyncio.gather(*(fetch_user(uid) for uid in range(1, 6)))
    for r in results:
        print(f"  {r.name} ({r.latency_ms:.0f}ms)")
    print(f"Total: {time.perf_counter() - start:.2f}s\n")


async def error_handling_demo() -> None:
    print("--- Error handling (return_exceptions=True) ---")
    results = await asyncio.gather(
        *(fetch_user_failing(uid) for uid in range(1, 7)),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  ERROR: {r}")
        else:
            print(f"  OK: {r.name}")
    print()


async def create_task_demo() -> None:
    print("--- create_task ---")
    task_a = asyncio.create_task(fetch_user(10))
    task_b = asyncio.create_task(fetch_user(11))

    print("  Tasks created, doing other work...")
    await asyncio.sleep(0.05)
    print("  Still working...")

    a = await task_a
    b = await task_b
    print(f"  Done: {a.name}, {b.name}\n")


async def main() -> None:
    await sequential_demo()
    await concurrent_demo()
    await error_handling_demo()
    await create_task_demo()


if __name__ == "__main__":
    asyncio.run(main())
