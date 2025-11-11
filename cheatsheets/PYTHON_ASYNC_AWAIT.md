# Python Async/Await Cheatsheet

## Table of Contents
- [What is Async/Await?](#what-is-asyncawait)
- [Basic Concepts](#basic-concepts)
- [Async Functions](#async-functions)
- [Await Expression](#await-expression)
- [Running Async Code](#running-async-code)
- [Creating Tasks](#creating-tasks)
- [Gathering Multiple Coroutines](#gathering-multiple-coroutines)
- [Timeouts and Cancellation](#timeouts-and-cancellation)
- [Async Context Managers](#async-context-managers)
- [Async Iterators](#async-iterators)
- [Common Patterns](#common-patterns)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## What is Async/Await?

**Async/await** is Python's way of writing **asynchronous** code that can handle **concurrent operations** efficiently, especially for I/O-bound tasks.

**Key Benefits:**
- 🚀 Handle thousands of concurrent connections
- ⏱️ Better performance for I/O-bound operations
- 🔄 Non-blocking code execution
- 📡 Perfect for network requests, file I/O, databases

**Not for:**
- ❌ CPU-bound tasks (use multiprocessing instead)
- ❌ Simple synchronous scripts
- ❌ When blocking libraries are required

---

## Basic Concepts

### Synchronous vs Asynchronous

```python
# Synchronous - blocks while waiting
import time

def fetch_data():
    time.sleep(2)  # Blocks for 2 seconds
    return "Data"

def main():
    result1 = fetch_data()  # Wait 2s
    result2 = fetch_data()  # Wait 2s
    # Total: 4 seconds

# Asynchronous - can do other work while waiting
import asyncio

async def fetch_data_async():
    await asyncio.sleep(2)  # Doesn't block other tasks
    return "Data"

async def main():
    result1 = asyncio.create_task(fetch_data_async())
    result2 = asyncio.create_task(fetch_data_async())
    await result1  # Both run concurrently
    await result2
    # Total: ~2 seconds
```

### Core Terminology

| Term | Definition |
|------|------------|
| **Coroutine** | Function defined with `async def` |
| **Awaitable** | Object that can be used with `await` |
| **Task** | Wrapper for coroutine that schedules its execution |
| **Event Loop** | Manages and executes async tasks |
| **Future** | Low-level awaitable object representing eventual result |

---

## Async Functions

### Defining Async Functions

```python
# Regular function
def regular_function():
    return "Hello"

# Async function (coroutine)
async def async_function():
    return "Hello"

# Calling differences
result = regular_function()  # Returns "Hello"
coro = async_function()      # Returns coroutine object, doesn't execute!

# To execute async function, you must await it
result = await async_function()  # Returns "Hello"
```

### Async Function Characteristics

```python
import asyncio

async def my_coroutine():
    """This is a coroutine function"""
    print("Starting")
    await asyncio.sleep(1)  # Async sleep
    print("Finished")
    return "Result"

# Check if it's a coroutine
import inspect
print(inspect.iscoroutinefunction(my_coroutine))  # True

# Calling it returns a coroutine object
coro = my_coroutine()
print(type(coro))  # <class 'coroutine'>

# Must run in event loop
asyncio.run(coro)  # Actually executes it
```

---

## Await Expression

### What Can Be Awaited?

```python
import asyncio

# 1. Coroutines
async def my_coro():
    return "Result"

async def main():
    result = await my_coro()
    print(result)

# 2. Tasks
async def main():
    task = asyncio.create_task(my_coro())
    result = await task

# 3. Futures
async def main():
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    future.set_result("Result")
    result = await future
```

### Await Rules

```python
async def good_example():
    # ✅ Can use await inside async function
    result = await async_function()
    return result

def bad_example():
    # ❌ Cannot use await in regular function
    # result = await async_function()  # SyntaxError
    pass

async def main():
    # ✅ Await coroutines
    await my_coroutine()

    # ✅ Await tasks
    task = asyncio.create_task(my_coroutine())
    await task

    # ❌ Cannot await regular functions
    # await regular_function()  # TypeError
```

---

## Running Async Code

### asyncio.run() - Main Entry Point

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Run the main coroutine
asyncio.run(main())

# asyncio.run() does:
# 1. Creates new event loop
# 2. Runs the coroutine
# 3. Closes the loop
# Use this at the top level of your program
```

### Getting Event Loop (Advanced)

```python
import asyncio

# Get current running loop (inside async function)
async def get_loop_example():
    loop = asyncio.get_running_loop()
    print(f"Loop: {loop}")

# Get or create loop (deprecated in 3.10+)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(my_coroutine())
# loop.close()

# Modern way: just use asyncio.run()
asyncio.run(get_loop_example())
```

---

## Creating Tasks

### asyncio.create_task()

```python
import asyncio

async def fetch_data(id):
    await asyncio.sleep(1)
    return f"Data {id}"

async def main():
    # Create task - starts running immediately
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    task3 = asyncio.create_task(fetch_data(3))

    # Do other work here while tasks run
    print("Tasks are running in background")

    # Wait for results
    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1, result2, result3)
    # Total time: ~1 second (concurrent)

asyncio.run(main())
```

### Task with Name (Python 3.8+)

```python
import asyncio

async def main():
    task = asyncio.create_task(
        fetch_data(1),
        name="fetch_task_1"
    )

    print(f"Task name: {task.get_name()}")
    result = await task
```

### Checking Task State

```python
import asyncio

async def long_operation():
    await asyncio.sleep(2)
    return "Done"

async def main():
    task = asyncio.create_task(long_operation())

    print(f"Done? {task.done()}")      # False
    print(f"Cancelled? {task.cancelled()}")  # False

    # Check periodically
    await asyncio.sleep(0.5)
    print(f"Done? {task.done()}")      # Still False

    # Wait for completion
    result = await task
    print(f"Done? {task.done()}")      # True
    print(f"Result: {task.result()}")  # "Done"

asyncio.run(main())
```

---

## Gathering Multiple Coroutines

### asyncio.gather()

```python
import asyncio

async def fetch_user(user_id):
    await asyncio.sleep(1)
    return f"User {user_id}"

async def main():
    # Run multiple coroutines concurrently
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )

    print(results)  # ['User 1', 'User 2', 'User 3']
    # Takes ~1 second, not 3!

asyncio.run(main())
```

### gather() vs create_task()

```python
import asyncio

async def task(n):
    await asyncio.sleep(1)
    return n * 2

async def using_gather():
    # All results in one call
    results = await asyncio.gather(
        task(1),
        task(2),
        task(3)
    )
    return results  # [2, 4, 6]

async def using_tasks():
    # More control over individual tasks
    task1 = asyncio.create_task(task(1))
    task2 = asyncio.create_task(task(2))
    task3 = asyncio.create_task(task(3))

    # Can check status, cancel, etc.
    results = [
        await task1,
        await task2,
        await task3
    ]
    return results  # [2, 4, 6]
```

### Error Handling with gather()

```python
import asyncio

async def might_fail(n):
    if n == 2:
        raise ValueError(f"Error with {n}")
    return n * 2

async def main():
    # Default: stops on first exception
    try:
        results = await asyncio.gather(
            might_fail(1),
            might_fail(2),
            might_fail(3)
        )
    except ValueError as e:
        print(f"Error: {e}")

    # return_exceptions=True: returns exceptions instead of raising
    results = await asyncio.gather(
        might_fail(1),
        might_fail(2),
        might_fail(3),
        return_exceptions=True
    )
    print(results)  # [2, ValueError(...), 6]

asyncio.run(main())
```

---

## Timeouts and Cancellation

### asyncio.wait_for() - Timeout

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(5)
    return "Done"

async def main():
    try:
        # Timeout after 2 seconds
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=2.0
        )
    except asyncio.TimeoutError:
        print("Operation timed out!")

asyncio.run(main())
```

### Cancelling Tasks

```python
import asyncio

async def cancellable_task():
    try:
        print("Task started")
        await asyncio.sleep(10)
        print("Task completed")
    except asyncio.CancelledError:
        print("Task was cancelled")
        raise  # Re-raise to properly cancel

async def main():
    task = asyncio.create_task(cancellable_task())

    await asyncio.sleep(1)
    task.cancel()  # Request cancellation

    try:
        await task
    except asyncio.CancelledError:
        print("Confirmed: task cancelled")

asyncio.run(main())
```

### asyncio.wait() - Advanced Control

```python
import asyncio

async def task(n):
    await asyncio.sleep(n)
    return f"Task {n}"

async def main():
    tasks = [
        asyncio.create_task(task(1)),
        asyncio.create_task(task(2)),
        asyncio.create_task(task(3))
    ]

    # Wait for first completion
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )

    print(f"Done: {len(done)}, Pending: {len(pending)}")

    # Cancel remaining
    for task in pending:
        task.cancel()

asyncio.run(main())
```

---

## Async Context Managers

### Using async with

```python
import asyncio

class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(1)
        return False

async def main():
    async with AsyncResource() as resource:
        print("Using resource")
        await asyncio.sleep(1)

asyncio.run(main())
```

### Practical Example: Async HTTP Client

```python
import asyncio
import aiohttp  # pip install aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    html = await fetch_url('https://example.com')
    print(f"Fetched {len(html)} bytes")

# asyncio.run(main())
```

### Async File Operations

```python
import asyncio
import aiofiles  # pip install aiofiles

async def read_file(filename):
    async with aiofiles.open(filename, 'r') as f:
        content = await f.read()
        return content

async def write_file(filename, content):
    async with aiofiles.open(filename, 'w') as f:
        await f.write(content)

async def main():
    await write_file('test.txt', 'Hello, async world!')
    content = await read_file('test.txt')
    print(content)

# asyncio.run(main())
```

---

## Async Iterators

### async for

```python
import asyncio

class AsyncCounter:
    def __init__(self, limit):
        self.limit = limit
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count >= self.limit:
            raise StopAsyncIteration

        await asyncio.sleep(0.5)
        self.count += 1
        return self.count

async def main():
    async for number in AsyncCounter(5):
        print(number)
    # Prints 1, 2, 3, 4, 5 (with delays)

asyncio.run(main())
```

### Async Generators

```python
import asyncio

async def async_range(count):
    """Async generator function"""
    for i in range(count):
        await asyncio.sleep(0.5)
        yield i

async def main():
    async for value in async_range(5):
        print(value)

asyncio.run(main())
```

### Async Comprehensions (Python 3.6+)

```python
import asyncio

async def get_value(n):
    await asyncio.sleep(0.1)
    return n * 2

async def main():
    # Async list comprehension
    results = [await get_value(i) for i in range(5)]
    print(results)  # [0, 2, 4, 6, 8]

    # Async generator expression
    gen = (await get_value(i) for i in range(5))
    async for value in gen:
        print(value)

asyncio.run(main())
```

---

## Common Patterns

### Concurrent API Requests

```python
import asyncio
import aiohttp

async def fetch_pokemon(session, pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    async with session.get(url) as response:
        data = await response.json()
        return data['name']

async def fetch_multiple_pokemon():
    async with aiohttp.ClientSession() as session:
        # Fetch 10 pokemon concurrently
        tasks = [
            fetch_pokemon(session, i)
            for i in range(1, 11)
        ]
        names = await asyncio.gather(*tasks)
        return names

async def main():
    names = await fetch_multiple_pokemon()
    print(names)

# asyncio.run(main())
```

### Producer-Consumer Pattern

```python
import asyncio
import random

async def producer(queue, n):
    """Produce items"""
    for i in range(n):
        await asyncio.sleep(random.random())
        item = f"item-{i}"
        await queue.put(item)
        print(f"Produced: {item}")

    # Signal completion
    await queue.put(None)

async def consumer(queue, name):
    """Consume items"""
    while True:
        item = await queue.get()
        if item is None:
            break

        await asyncio.sleep(random.random())
        print(f"{name} consumed: {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    # Start producer and consumers
    await asyncio.gather(
        producer(queue, 10),
        consumer(queue, "Consumer-1"),
        consumer(queue, "Consumer-2")
    )

asyncio.run(main())
```

### Retry with Exponential Backoff

```python
import asyncio

async def unstable_api_call():
    """Simulated API that might fail"""
    import random
    if random.random() < 0.7:
        raise Exception("API Error")
    return "Success"

async def retry_with_backoff(coro_func, max_retries=3, base_delay=1):
    """Retry coroutine with exponential backoff"""
    for attempt in range(max_retries):
        try:
            result = await coro_func()
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Retrying in {delay}s...")
            await asyncio.sleep(delay)

async def main():
    result = await retry_with_backoff(unstable_api_call)
    print(f"Result: {result}")

asyncio.run(main())
```

### Rate Limiting

```python
import asyncio
import time

class RateLimiter:
    def __init__(self, rate, per_seconds):
        self.rate = rate
        self.per_seconds = per_seconds
        self.allowance = rate
        self.last_check = time.time()

    async def acquire(self):
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current

        self.allowance += time_passed * (self.rate / self.per_seconds)
        if self.allowance > self.rate:
            self.allowance = self.rate

        if self.allowance < 1.0:
            sleep_time = (1.0 - self.allowance) * (self.per_seconds / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0.0
        else:
            self.allowance -= 1.0

async def api_call(limiter, n):
    await limiter.acquire()
    print(f"API call {n} at {time.time():.2f}")
    return n

async def main():
    # 2 requests per second
    limiter = RateLimiter(rate=2, per_seconds=1)

    tasks = [api_call(limiter, i) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

---

## Error Handling

### Try-Except in Async

```python
import asyncio

async def might_fail():
    await asyncio.sleep(1)
    raise ValueError("Something went wrong")

async def main():
    try:
        result = await might_fail()
    except ValueError as e:
        print(f"Caught error: {e}")
    except asyncio.TimeoutError:
        print("Operation timed out")
    finally:
        print("Cleanup")

asyncio.run(main())
```

### Handling Multiple Task Errors

```python
import asyncio

async def task_that_fails(n):
    await asyncio.sleep(1)
    if n % 2 == 0:
        raise ValueError(f"Task {n} failed")
    return n

async def main():
    tasks = [
        asyncio.create_task(task_that_fails(i))
        for i in range(5)
    ]

    results = []
    for task in tasks:
        try:
            result = await task
            results.append(result)
        except ValueError as e:
            print(f"Error: {e}")
            results.append(None)

    print(f"Results: {results}")

asyncio.run(main())
```

### Task Exception Retrieval

```python
import asyncio

async def failing_task():
    await asyncio.sleep(1)
    raise ValueError("Task failed")

async def main():
    task = asyncio.create_task(failing_task())

    await asyncio.sleep(2)

    if task.done():
        try:
            result = task.result()
        except ValueError as e:
            print(f"Task raised: {e}")

asyncio.run(main())
```

---

## Best Practices

### ✅ DO

```python
import asyncio

# 1. Use asyncio.run() for main entry point
async def main():
    await do_async_work()

if __name__ == "__main__":
    asyncio.run(main())

# 2. Use create_task() for fire-and-forget
async def main():
    task = asyncio.create_task(background_work())
    # Task runs in background
    await other_work()
    await task  # Wait when needed

# 3. Use gather() for multiple operations
async def main():
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )

# 4. Always await coroutines
async def good():
    result = await async_function()  # ✓

# 5. Use timeout for external operations
async def main():
    try:
        result = await asyncio.wait_for(
            external_api_call(),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        print("Request timed out")

# 6. Close resources properly
async def main():
    async with aiohttp.ClientSession() as session:
        # Use session
        pass  # Automatically closed

# 7. Handle cancellation
async def cancellable_work():
    try:
        await long_operation()
    except asyncio.CancelledError:
        # Cleanup
        raise  # Re-raise!
```

### ❌ DON'T

```python
# 1. Don't forget to await
async def bad():
    result = async_function()  # ✗ Returns coroutine, doesn't run!

async def good():
    result = await async_function()  # ✓

# 2. Don't use time.sleep in async code
async def bad():
    import time
    time.sleep(1)  # ✗ Blocks entire event loop!

async def good():
    await asyncio.sleep(1)  # ✓ Non-blocking

# 3. Don't mix sync and async incorrectly
def bad():
    await async_function()  # ✗ SyntaxError!

async def good():
    await async_function()  # ✓

# 4. Don't create too many tasks
async def bad():
    # ✗ 1 million concurrent tasks!
    tasks = [asyncio.create_task(work()) for _ in range(1_000_000)]

async def good():
    # ✓ Use semaphore to limit concurrency
    sem = asyncio.Semaphore(100)
    async def limited_work():
        async with sem:
            await work()

# 5. Don't ignore task exceptions
async def bad():
    task = asyncio.create_task(might_fail())
    # ✗ Exception is lost if not awaited

async def good():
    task = asyncio.create_task(might_fail())
    try:
        await task
    except Exception as e:
        print(f"Task failed: {e}")

# 6. Don't use blocking operations
async def bad():
    import requests
    response = requests.get(url)  # ✗ Blocking!

async def good():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()  # ✓ Non-blocking
```

---

## Quick Reference

### Basic Async Template

```python
import asyncio

async def async_operation():
    """Your async operation"""
    await asyncio.sleep(1)
    return "Result"

async def main():
    """Main async function"""
    result = await async_operation()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Common Patterns Quick Guide

| Task | Code |
|------|------|
| Define async function | `async def func():` |
| Call async function | `await func()` |
| Run main coroutine | `asyncio.run(main())` |
| Create background task | `task = asyncio.create_task(func())` |
| Wait for multiple | `await asyncio.gather(f1(), f2())` |
| Timeout | `await asyncio.wait_for(func(), timeout=5)` |
| Sleep | `await asyncio.sleep(1)` |
| Async context manager | `async with resource:` |
| Async iterator | `async for item in iterator:` |
| Cancel task | `task.cancel()` |

### When to Use Async

| Use Async | Don't Use Async |
|-----------|-----------------|
| ✅ Network requests | ❌ CPU-intensive calculations |
| ✅ File I/O | ❌ Simple scripts |
| ✅ Database queries | ❌ When libraries aren't async |
| ✅ Web scraping | ❌ Quick prototypes |
| ✅ API servers | ❌ Single synchronous task |
| ✅ Websockets | ❌ No concurrency needed |

---

## Summary

**Key Takeaways:**

1. **`async def`** creates coroutine functions
2. **`await`** pauses until awaitable completes
3. **`asyncio.run()`** is the main entry point
4. **`create_task()`** runs coroutines concurrently
5. **`gather()`** waits for multiple coroutines
6. Use **async libraries** (aiohttp, aiofiles, etc.)
7. **Don't block** the event loop (no `time.sleep()`, blocking I/O)

**Mental Model:**
```
async def = "this function can pause"
await = "pause here until this completes"
asyncio.run() = "start the async world"
```

**Basic Pattern:**
```python
import asyncio

async def fetch_data(id):
    await asyncio.sleep(1)  # Simulated I/O
    return f"Data {id}"

async def main():
    # Concurrent execution
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    print(results)

asyncio.run(main())
```

🚀 Master async/await for high-performance I/O-bound Python applications!
