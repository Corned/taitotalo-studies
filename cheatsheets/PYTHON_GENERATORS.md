# Python Generators Cheatsheet

## Table of Contents
- [What are Generators?](#what-are-generators)
- [Generator Functions](#generator-functions)
- [Generator Expressions](#generator-expressions)
- [Key Characteristics](#key-characteristics)
- [Generator Methods](#generator-methods)
- [Advanced Patterns](#advanced-patterns)
- [Practical Use Cases](#practical-use-cases)
- [Performance Tips](#performance-tips)
- [Common Pitfalls](#common-pitfalls)

---

## What are Generators?

Generators are **iterators** that generate values **lazily** (on-demand) without storing the entire sequence in memory.

**Key Benefits:**
- 🔋 Memory efficient
- ♾️ Can represent infinite sequences
- 🔄 Maintain state between iterations
- 📊 Perfect for data pipelines

---

## Generator Functions

### Basic Syntax

```python
def count_up_to(n):
    """Generator that yields numbers from 1 to n"""
    count = 1
    while count <= n:
        yield count  # yield instead of return
        count += 1

# Create generator object
gen = count_up_to(5)
print(type(gen))  # <class 'generator'>

# Iterate through values
for num in gen:
    print(num)  # 1, 2, 3, 4, 5
```

### How `yield` Works

```python
def demonstrate_yield():
    print("Starting")
    yield 1          # Pause here, return 1
    print("Middle")
    yield 2          # Pause here, return 2
    print("End")
    yield 3          # Pause here, return 3

gen = demonstrate_yield()
# Nothing printed yet!

next(gen)  # "Starting", returns 1
next(gen)  # "Middle", returns 2
next(gen)  # "End", returns 3
next(gen)  # Raises StopIteration
```

**Execution Flow:**
1. Call function → returns generator object (doesn't execute body)
2. Call `next()` → executes until first `yield`
3. `yield` → returns value, saves state
4. Next `next()` → resumes after last `yield`
5. Function ends → raises `StopIteration`

### Multiple Yields

```python
def multiple_yields():
    yield "first"
    yield "second"
    yield "third"

for value in multiple_yields():
    print(value)
```

### Yield in Loops

```python
def fibonacci(limit):
    """Generate Fibonacci numbers up to limit"""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

list(fibonacci(100))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

### Infinite Generators

```python
def infinite_counter(start=0):
    """Count infinitely"""
    while True:
        yield start
        start += 1

# Safe to create!
counter = infinite_counter()

# Use with caution
from itertools import islice
first_10 = list(islice(counter, 10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## Generator Expressions

Syntax: `(expression for item in iterable if condition)`

### Basic Generator Expression

```python
# List comprehension - creates entire list in memory
squares_list = [x**2 for x in range(1000000)]  # Uses ~8MB

# Generator expression - creates values on demand
squares_gen = (x**2 for x in range(1000000))   # Uses ~128 bytes!

# Usage
for square in squares_gen:
    print(square)
```

### With Conditions

```python
# Even numbers only
evens = (x for x in range(100) if x % 2 == 0)

# Multiple conditions
filtered = (x for x in range(100) if x % 2 == 0 if x > 50)
```

### Nested Generator Expressions

```python
# All pairs
pairs = ((x, y) for x in range(3) for y in range(3))
# (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)

# Matrix flattening
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = (item for row in matrix for item in row)
```

### In Function Calls

```python
# Parentheses can be omitted if it's the only argument
total = sum(x**2 for x in range(100))

# Multiple arguments
max_even = max((x for x in range(100) if x % 2 == 0), default=0)
```

---

## Key Characteristics

### 1. Lazy Evaluation

```python
# Values computed only when requested
def slow_generator():
    for i in range(5):
        print(f"Computing {i}...")
        yield i

gen = slow_generator()  # Nothing printed yet!
next(gen)  # "Computing 0...", returns 0
next(gen)  # "Computing 1...", returns 1
```

### 2. Memory Efficiency

```python
import sys

# Compare memory usage
list_obj = [i for i in range(1000000)]
gen_obj = (i for i in range(1000000))

print(sys.getsizeof(list_obj))  # ~8,000,000 bytes
print(sys.getsizeof(gen_obj))   # ~128 bytes
```

### 3. One-Time Iteration

```python
gen = (x for x in range(5))
print(list(gen))  # [0, 1, 2, 3, 4]
print(list(gen))  # [] - Exhausted!

# Need to recreate
gen = (x for x in range(5))
print(list(gen))  # [0, 1, 2, 3, 4]
```

### 4. State Preservation

```python
def stateful():
    count = 0
    while True:
        count += 1
        value = yield count
        if value is not None:
            count = value

gen = stateful()
next(gen)      # 1
next(gen)      # 2
gen.send(10)   # Reset to 10, returns 11
next(gen)      # 12
```

---

## Generator Methods

### `next(gen)` / `gen.__next__()`

```python
def simple():
    yield 1
    yield 2
    yield 3

gen = simple()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
# next(gen)  # StopIteration

# With default value
print(next(gen, "done"))  # "done"
```

### `gen.send(value)`

Send a value INTO the generator (becomes result of `yield` expression).

```python
def echo():
    while True:
        received = yield
        print(f"Received: {received}")

gen = echo()
next(gen)  # Prime the generator (must reach first yield)

gen.send("Hello")  # Received: Hello
gen.send("World")  # Received: World
```

**Accumulator Example:**

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

acc = accumulator()
next(acc)         # 0 (prime)
acc.send(10)      # 10
acc.send(5)       # 15
acc.send(3)       # 18
```

### `gen.throw(exception)`

Throw an exception at the point where generator is paused.

```python
def resilient():
    try:
        yield 1
        yield 2
        yield 3
    except ValueError:
        print("ValueError caught!")
        yield "recovered"

gen = resilient()
next(gen)               # 1
gen.throw(ValueError)   # ValueError caught!, returns "recovered"
```

### `gen.close()`

Stop the generator and raise `GeneratorExit`.

```python
def cleanup():
    try:
        yield 1
        yield 2
        yield 3
    finally:
        print("Cleanup!")

gen = cleanup()
next(gen)    # 1
gen.close()  # Cleanup!
# next(gen)  # StopIteration - generator is closed
```

---

## Advanced Patterns

### 1. Generator Pipelining

Chain generators for data processing pipelines.

```python
def read_lines(filename):
    """Read lines from file"""
    with open(filename) as f:
        for line in f:
            yield line.strip()

def filter_comments(lines):
    """Remove comment lines"""
    for line in lines:
        if not line.startswith('#'):
            yield line

def filter_empty(lines):
    """Remove empty lines"""
    for line in lines:
        if line:
            yield line

def to_uppercase(lines):
    """Convert to uppercase"""
    for line in lines:
        yield line.upper()

# Chain generators together
pipeline = read_lines('data.txt')
pipeline = filter_comments(pipeline)
pipeline = filter_empty(pipeline)
pipeline = to_uppercase(pipeline)

for line in pipeline:
    process(line)  # Memory efficient!
```

### 2. `yield from` - Generator Delegation

Delegate to another generator (Python 3.3+).

```python
# Without yield from
def flatten_wrong(nested):
    for item in nested:
        if isinstance(item, list):
            for subitem in flatten_wrong(item):
                yield subitem
        else:
            yield item

# With yield from - cleaner!
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

data = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
print(list(flatten(data)))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

**Combining Generators:**

```python
def first_gen():
    yield 1
    yield 2

def second_gen():
    yield 3
    yield 4

def combined():
    yield from first_gen()
    yield from second_gen()

list(combined())  # [1, 2, 3, 4]
```

### 3. Coroutines (Pre-async/await)

Use generators as coroutines for cooperative multitasking.

```python
def moving_average():
    """Calculate running average"""
    total = 0
    count = 0
    average = None

    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = moving_average()
next(avg)          # Prime
print(avg.send(10))  # 10.0
print(avg.send(20))  # 15.0
print(avg.send(30))  # 20.0
```

### 4. Generator Context Managers

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Acquiring resource")
    resource = acquire_resource()
    try:
        yield resource
    finally:
        print("Releasing resource")
        release_resource(resource)

with managed_resource() as res:
    use(res)
```

---

## Practical Use Cases

### 1. Reading Large Files

```python
def read_large_file(filepath):
    """Read file line by line - memory efficient"""
    with open(filepath) as f:
        for line in f:
            yield line.strip()

# Process huge file without loading into memory
for line in read_large_file('huge_log.txt'):
    if 'ERROR' in line:
        process_error(line)
```

### 2. CSV Processing

```python
def process_csv(filepath):
    """Process CSV file efficiently"""
    with open(filepath) as f:
        header = next(f).strip().split(',')
        for line in f:
            values = line.strip().split(',')
            yield dict(zip(header, values))

for row in process_csv('data.csv'):
    if row['status'] == 'active':
        process(row)
```

### 3. Batching

```python
def batch_generator(iterable, batch_size):
    """Create batches from iterable"""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:  # Don't forget last partial batch
        yield batch

# Process data in batches
for batch in batch_generator(range(100), batch_size=10):
    process_batch(batch)
```

### 4. Infinite Sequences

```python
def fibonacci_infinite():
    """Infinite Fibonacci sequence"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def primes():
    """Infinite prime numbers"""
    yield 2
    primes_list = [2]
    candidate = 3
    while True:
        is_prime = all(candidate % p != 0 for p in primes_list)
        if is_prime:
            yield candidate
            primes_list.append(candidate)
        candidate += 2

# Use with itertools
from itertools import islice, takewhile

# First 10 Fibonacci numbers
list(islice(fibonacci_infinite(), 10))

# Primes less than 100
list(takewhile(lambda x: x < 100, primes()))
```

### 5. Tree Traversal

```python
def inorder(node):
    """In-order tree traversal"""
    if node:
        yield from inorder(node.left)
        yield node.value
        yield from inorder(node.right)

def level_order(root):
    """Level-order (breadth-first) traversal"""
    if not root:
        return
    queue = [root]
    while queue:
        node = queue.pop(0)
        yield node.value
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

### 6. Data Transformation Pipeline

```python
def load_data(source):
    for item in source:
        yield item

def filter_data(data, condition):
    for item in data:
        if condition(item):
            yield item

def transform_data(data, transform_func):
    for item in data:
        yield transform_func(item)

# Build pipeline
pipeline = load_data(source)
pipeline = filter_data(pipeline, lambda x: x > 0)
pipeline = transform_data(pipeline, lambda x: x * 2)

results = list(pipeline)
```

---

## Performance Tips

### When to Use Generators

✅ **Use generators when:**
- Working with large datasets
- Processing streams of data
- Creating infinite sequences
- Building data pipelines
- One-time iteration is sufficient
- Memory is a constraint

❌ **Use lists when:**
- Need random access (`list[5]`)
- Multiple iterations required
- Small datasets
- Need list methods (`append`, `sort`, `reverse`)
- Need length (`len()`)

### Performance Comparison

```python
import time

# Generator - lazy
start = time.time()
gen = (i**2 for i in range(1000000))
gen_time = time.time() - start
# ~0.000001s - instant!

# List - eager
start = time.time()
lst = [i**2 for i in range(1000000)]
list_time = time.time() - start
# ~0.1s - must compute all values

# But accessing values:
# Generator: O(n) to get nth item
# List: O(1) to get nth item
```

### Converting Generators

```python
gen = (x for x in range(10))

# To list
lst = list(gen)

# To tuple
tpl = tuple(gen)  # Note: gen is now exhausted

# To set
gen = (x for x in range(10))
st = set(gen)

# To dict (if yielding tuples)
gen = ((i, i**2) for i in range(5))
dct = dict(gen)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

---

## Common Pitfalls

### 1. Generator Exhaustion

```python
❌ # WRONG
gen = (x for x in range(5))
print(list(gen))  # [0, 1, 2, 3, 4]
print(list(gen))  # [] - Exhausted!

✅ # CORRECT
def create_gen():
    return (x for x in range(5))

print(list(create_gen()))  # [0, 1, 2, 3, 4]
print(list(create_gen()))  # [0, 1, 2, 3, 4]

# Or use itertools.tee
from itertools import tee
gen = (x for x in range(5))
gen1, gen2 = tee(gen, 2)
print(list(gen1))  # [0, 1, 2, 3, 4]
print(list(gen2))  # [0, 1, 2, 3, 4]
```

### 2. Late Binding (See PYTHON_LATE_BINDING.md)

```python
❌ # WRONG
generators = [((x + i) for x in range(3)) for i in range(3)]
for gen in generators:
    print(list(gen))  # All use final value of i

✅ # CORRECT
generators = [((x + i) for x in range(3)) for i in range(3)]
# Use immediately or capture with factory function
```

### 3. No Random Access

```python
gen = (x for x in range(100))
# gen[50]  # TypeError: 'generator' object is not subscriptable

# Use list() if you need indexing
lst = list(gen)
print(lst[50])
```

### 4. Can't Get Length

```python
gen = (x for x in range(100))
# len(gen)  # TypeError: object of type 'generator' has no len()

# Convert to list if you need length
lst = list(gen)
print(len(lst))
```

### 5. Not Priming Coroutines

```python
❌ # WRONG
def coroutine():
    while True:
        x = yield
        print(x)

c = coroutine()
c.send(5)  # TypeError!

✅ # CORRECT
c = coroutine()
next(c)    # Prime first!
c.send(5)  # Now it works

# Or use decorator
def coroutine_decorator(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # Auto-prime
        return gen
    return wrapper

@coroutine_decorator
def my_coroutine():
    while True:
        x = yield
        print(x)

c = my_coroutine()  # Already primed!
c.send(5)  # Works immediately
```

---

## Quick Reference

### Creating Generators

```python
# Function with yield
def gen_func():
    yield 1

# Generator expression
gen_expr = (x for x in range(10))

# yield from
def delegating():
    yield from other_gen()
```

### Using Generators

```python
# Iteration
for item in generator:
    process(item)

# next()
next(gen)
next(gen, default_value)

# Convert to collection
list(gen)
tuple(gen)
set(gen)
dict(gen)  # if yielding tuples

# Useful itertools
from itertools import islice, takewhile, dropwhile, chain

islice(gen, 10)           # First 10 items
takewhile(pred, gen)      # While predicate is true
dropwhile(pred, gen)      # Drop while predicate is true
chain(gen1, gen2)         # Combine generators
```

### Generator Methods

```python
next(gen)              # Get next value
gen.send(value)        # Send value into generator
gen.throw(exception)   # Throw exception
gen.close()            # Close generator
```

---

## Summary

**Generators are powerful for:**
- 💾 Memory efficiency (lazy evaluation)
- ♾️ Infinite sequences
- 🔄 Stateful iteration
- 📊 Data pipelines
- 📁 Processing large files

**Remember:**
- Use `yield` to create generators
- Generators are **one-time use** (exhausted after iteration)
- Use **generator expressions** `()` for simple cases
- Use **`yield from`** to delegate to other generators
- Perfect for **streaming data** and **large datasets**

**Key Pattern:**
```python
def process_data(source):
    """Memory-efficient data processing"""
    for item in source:
        if condition(item):
            yield transform(item)
```

🚀 Master generators for efficient, elegant Python code!
