# Python Functools Cheatsheet

## Table of Contents
- [What is Functools?](#what-is-functools)
- [reduce()](#reduce)
- [partial()](#partial)
- [lru_cache()](#lru_cache)
- [cached_property()](#cached_property)
- [wraps()](#wraps)
- [total_ordering()](#total_ordering)
- [singledispatch()](#singledispatch)
- [cmp_to_key()](#cmp_to_key)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)

---

## What is Functools?

The **functools** module provides higher-order functions that act on or return other functions. It's essential for functional programming in Python.

**Key Benefits:**
- 🎯 Function composition and transformation
- 🚀 Performance optimization (caching)
- 🔧 Decorator utilities
- 📊 Functional programming tools

```python
import functools

# All functools features
dir(functools)
# ['partial', 'reduce', 'wraps', 'lru_cache', 'singledispatch', ...]
```

---

## reduce()

Apply a function cumulatively to items of an iterable, reducing it to a single value.

### Basic Usage

```python
from functools import reduce

# Sum all numbers
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# Equivalent to:
total = numbers[0]  # 1
total = total + numbers[1]  # 1 + 2 = 3
total = total + numbers[2]  # 3 + 3 = 6
total = total + numbers[3]  # 6 + 4 = 10
total = total + numbers[4]  # 10 + 5 = 15
```

### With Initial Value

```python
from functools import reduce

# Sum with initial value
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers, 10)
print(total)  # 25 (10 + 1 + 2 + 3 + 4 + 5)

# Multiply all numbers
product = reduce(lambda x, y: x * y, numbers, 1)
print(product)  # 120
```

### Practical Examples

```python
from functools import reduce

# Find maximum
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(maximum)  # 9

# Concatenate strings
words = ['Hello', ' ', 'World', '!']
sentence = reduce(lambda x, y: x + y, words)
print(sentence)  # "Hello World!"

# Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda x, y: x + y, nested)
print(flat)  # [1, 2, 3, 4, 5, 6]

# Compute factorial
def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n + 1))

print(factorial(5))  # 120

# Count occurrences
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
counts = reduce(
    lambda acc, word: {**acc, word: acc.get(word, 0) + 1},
    words,
    {}
)
print(counts)  # {'apple': 3, 'banana': 2, 'cherry': 1}
```

### When to Use reduce()

```python
from functools import reduce

# ✅ Good use cases
# Mathematical operations
product = reduce(lambda x, y: x * y, [1, 2, 3, 4])

# Building complex data structures
data = reduce(
    lambda acc, item: acc | {item['id']: item},
    items,
    {}
)

# ❌ Better alternatives exist
# Sum - use built-in
total = reduce(lambda x, y: x + y, numbers)  # Don't do this
total = sum(numbers)  # Do this instead

# Any/all - use built-ins
any_positive = reduce(lambda x, y: x or y > 0, numbers, False)  # Don't
any_positive = any(x > 0 for x in numbers)  # Do this

# Max/min - use built-ins
maximum = reduce(lambda x, y: x if x > y else y, numbers)  # Don't
maximum = max(numbers)  # Do this
```

---

## partial()

Create a new function with some arguments pre-filled.

### Basic Usage

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# Partial application
double = partial(power, exponent=2)
print(double(3))  # 9
```

### With Multiple Arguments

```python
from functools import partial

def greet(greeting, name, punctuation='!'):
    return f"{greeting}, {name}{punctuation}"

# Pre-fill greeting
say_hello = partial(greet, "Hello")
print(say_hello("Alice"))  # "Hello, Alice!"

# Pre-fill greeting and punctuation
say_hi = partial(greet, "Hi", punctuation=".")
print(say_hi("Bob"))  # "Hi, Bob."

# Pre-fill all but one
greet_alice = partial(greet, name="Alice")
print(greet_alice("Hey"))  # "Hey, Alice!"
```

### Practical Examples

```python
from functools import partial
import re

# Create specialized regex functions
is_email = partial(re.match, r'^[\w\.-]+@[\w\.-]+\.\w+$')
is_phone = partial(re.match, r'^\d{3}-\d{3}-\d{4}$')

print(bool(is_email("user@example.com")))  # True
print(bool(is_phone("555-123-4567")))      # True

# Database operations
def query_db(table, columns, where=None):
    return f"SELECT {columns} FROM {table}" + (f" WHERE {where}" if where else "")

query_users = partial(query_db, "users")
query_user_names = partial(query_db, "users", "name, email")

print(query_users("*", "id > 100"))
# SELECT * FROM users WHERE id > 100

print(query_user_names(where="active = true"))
# SELECT name, email FROM users WHERE active = true

# Callback with context
def process_item(item, prefix):
    return f"{prefix}: {item}"

# Create callbacks with different prefixes
error_handler = partial(process_item, prefix="ERROR")
warning_handler = partial(process_item, prefix="WARNING")
info_handler = partial(process_item, prefix="INFO")

print(error_handler("File not found"))    # ERROR: File not found
print(warning_handler("Low memory"))      # WARNING: Low memory
```

### Partial with Methods

```python
from functools import partial

class Calculator:
    def __init__(self, base):
        self.base = base

    def compute(self, operation, value):
        if operation == 'add':
            return self.base + value
        elif operation == 'multiply':
            return self.base * value

calc = Calculator(10)

# Create specialized methods
add_to_base = partial(calc.compute, 'add')
multiply_base = partial(calc.compute, 'multiply')

print(add_to_base(5))      # 15
print(multiply_base(3))    # 30
```

---

## lru_cache()

Least Recently Used cache decorator for memoization.

### Basic Usage

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Fast! Cached results

# Cache info
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)

# Clear cache
fibonacci.cache_clear()
```

### With maxsize

```python
from functools import lru_cache

# Unlimited cache
@lru_cache(maxsize=None)
def expensive_operation(n):
    print(f"Computing {n}...")
    return n ** 2

print(expensive_operation(5))  # Computing 5... -> 25
print(expensive_operation(5))  # 25 (cached, no print)

# Limited cache (LRU eviction when full)
@lru_cache(maxsize=2)
def limited_cache(n):
    print(f"Computing {n}...")
    return n * 2

limited_cache(1)  # Computing 1...
limited_cache(2)  # Computing 2...
limited_cache(3)  # Computing 3... (cache full)
limited_cache(1)  # Computing 1... (evicted earlier, recomputed)
```

### Practical Examples

```python
from functools import lru_cache
import time

# Expensive API call simulation
@lru_cache(maxsize=100)
def fetch_user_data(user_id):
    print(f"Fetching user {user_id} from API...")
    time.sleep(1)  # Simulated network delay
    return {"id": user_id, "name": f"User{user_id}"}

# First call - slow
start = time.time()
user = fetch_user_data(123)
print(f"Took {time.time() - start:.2f}s")  # ~1 second

# Second call - fast (cached)
start = time.time()
user = fetch_user_data(123)
print(f"Took {time.time() - start:.2f}s")  # ~0 seconds

# Database query caching
@lru_cache(maxsize=256)
def get_product(product_id):
    # Expensive database query
    return query_database(f"SELECT * FROM products WHERE id={product_id}")

# Recursive with memoization
@lru_cache(maxsize=None)
def count_paths(x, y):
    """Count paths in grid from (0,0) to (x,y)"""
    if x == 0 or y == 0:
        return 1
    return count_paths(x - 1, y) + count_paths(x, y - 1)

print(count_paths(10, 10))  # Fast with caching!
```

### cache() - Unlimited Cache (Python 3.9+)

```python
from functools import cache

@cache  # Equivalent to @lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Very fast
```

### Important Considerations

```python
from functools import lru_cache

# ✅ Cacheable - immutable arguments
@lru_cache
def process_numbers(a, b, c):
    return a + b + c

process_numbers(1, 2, 3)  # Works

# ❌ Not cacheable - mutable arguments
@lru_cache
def process_list(items):  # TypeError: unhashable type: 'list'
    return sum(items)

# ✅ Solution: convert to tuple
@lru_cache
def process_list(items):
    items = tuple(items)  # Convert to hashable type
    return sum(items)

process_list((1, 2, 3))  # Works

# Only hashable arguments can be cached
# Hashable: int, str, tuple, frozenset
# Not hashable: list, dict, set
```

---

## cached_property()

Cache a property value after first access (Python 3.8+).

### Basic Usage

```python
from functools import cached_property

class DataProcessor:
    def __init__(self, data):
        self.data = data

    @cached_property
    def processed_data(self):
        print("Processing data...")
        # Expensive computation
        return [x * 2 for x in self.data]

    @cached_property
    def data_sum(self):
        print("Computing sum...")
        return sum(self.processed_data)

processor = DataProcessor([1, 2, 3, 4, 5])

# First access - computes and caches
print(processor.processed_data)  # Processing data... [2, 4, 6, 8, 10]

# Second access - uses cache (no print)
print(processor.processed_data)  # [2, 4, 6, 8, 10]

# Sum uses cached processed_data
print(processor.data_sum)  # Computing sum... 30
```

### Practical Examples

```python
from functools import cached_property
import re

class Document:
    def __init__(self, text):
        self.text = text

    @cached_property
    def word_count(self):
        """Expensive: count words"""
        print("Counting words...")
        return len(self.text.split())

    @cached_property
    def unique_words(self):
        """Expensive: find unique words"""
        print("Finding unique words...")
        return set(word.lower() for word in self.text.split())

    @cached_property
    def links(self):
        """Expensive: extract all links"""
        print("Extracting links...")
        pattern = r'https?://[^\s]+'
        return re.findall(pattern, self.text)

doc = Document("Hello world! Visit https://example.com and https://python.org")

print(doc.word_count)      # Counting words... 6
print(doc.word_count)      # 6 (cached)
print(doc.unique_words)    # Finding unique words... {...}
print(doc.links)           # Extracting links... [...]
```

### vs @property

```python
from functools import cached_property
import time

class Example:
    @property
    def regular_property(self):
        """Computed every time"""
        print("Computing regular property...")
        time.sleep(0.1)
        return 42

    @cached_property
    def cached_prop(self):
        """Computed once, then cached"""
        print("Computing cached property...")
        time.sleep(0.1)
        return 42

obj = Example()

# Regular property - slow every time
obj.regular_property  # Computing... (0.1s)
obj.regular_property  # Computing... (0.1s)
obj.regular_property  # Computing... (0.1s)

# Cached property - slow once, fast after
obj.cached_prop  # Computing... (0.1s)
obj.cached_prop  # Fast (cached)
obj.cached_prop  # Fast (cached)
```

### Clearing Cache

```python
from functools import cached_property

class DataStore:
    def __init__(self):
        self._data = []

    @cached_property
    def summary(self):
        return {"count": len(self._data), "sum": sum(self._data)}

    def add_data(self, value):
        self._data.append(value)
        # Clear cache when data changes
        if 'summary' in self.__dict__:
            del self.__dict__['summary']

store = DataStore()
store.add_data(10)
print(store.summary)  # {'count': 1, 'sum': 10}

store.add_data(20)
print(store.summary)  # {'count': 2, 'sum': 30} (recomputed)
```

---

## wraps()

Preserve function metadata when creating decorators.

### The Problem

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone"""
    return f"Hello, {name}"

print(greet.__name__)  # wrapper (WRONG!)
print(greet.__doc__)   # Wrapper docstring (WRONG!)
```

### The Solution

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone"""
    return f"Hello, {name}"

print(greet.__name__)  # greet (CORRECT!)
print(greet.__doc__)   # Greet someone (CORRECT!)
print(greet.__wrapped__)  # <function greet> (access original)
```

### Practical Decorator with wraps

```python
from functools import wraps
import time

def timer(func):
    """Measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    """This function is slow"""
    time.sleep(1)
    return "Done"

# Metadata preserved
print(slow_function.__name__)  # slow_function
print(slow_function.__doc__)   # This function is slow

# Access original function
original = slow_function.__wrapped__
```

### Decorator with Arguments

```python
from functools import wraps

def repeat(times):
    """Decorator factory"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    """Greet someone"""
    print(f"Hello, {name}!")

greet("Alice")
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!

print(greet.__name__)  # greet (preserved)
```

---

## total_ordering()

Auto-generate ordering methods from `__eq__` and one other comparison.

### Basic Usage

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        return self.grade == other.grade

    def __lt__(self, other):
        return self.grade < other.grade

# Now has all comparison methods!
alice = Student("Alice", 90)
bob = Student("Bob", 85)

print(alice > bob)   # True (__gt__ auto-generated)
print(alice >= bob)  # True (__ge__ auto-generated)
print(alice <= bob)  # False (__le__ auto-generated)
print(alice == bob)  # False
print(alice != bob)  # True (__ne__ auto-generated)
```

### Practical Examples

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, version_string):
        self.parts = tuple(map(int, version_string.split('.')))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

    def __str__(self):
        return '.'.join(map(str, self.parts))

v1 = Version("1.2.3")
v2 = Version("1.2.10")
v3 = Version("2.0.0")

print(v1 < v2)   # True
print(v2 < v3)   # True
print(v3 > v1)   # True
print(sorted([v3, v1, v2]))  # [1.2.3, 1.2.10, 2.0.0]

# Priority Queue
@total_ordering
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task({self.name}, pri={self.priority})"

import heapq
tasks = [
    Task("Low priority", 3),
    Task("High priority", 1),
    Task("Medium priority", 2)
]
heapq.heapify(tasks)
print(heapq.heappop(tasks))  # Task(High priority, pri=1)
```

---

## singledispatch()

Create generic functions with different implementations for different types.

### Basic Usage

```python
from functools import singledispatch

@singledispatch
def process(data):
    """Default implementation"""
    print(f"Processing {type(data).__name__}: {data}")

@process.register
def _(data: int):
    print(f"Processing integer: {data * 2}")

@process.register
def _(data: str):
    print(f"Processing string: {data.upper()}")

@process.register
def _(data: list):
    print(f"Processing list: {len(data)} items")

# Dispatch based on type
process(42)           # Processing integer: 84
process("hello")      # Processing string: HELLO
process([1, 2, 3])    # Processing list: 3 items
process(3.14)         # Processing float: 3.14 (default)
```

### Multiple Types

```python
from functools import singledispatch

@singledispatch
def to_json(obj):
    raise TypeError(f"Cannot serialize {type(obj)}")

@to_json.register(int)
@to_json.register(float)
@to_json.register(str)
def _(obj):
    return obj

@to_json.register(list)
def _(obj):
    return [to_json(item) for item in obj]

@to_json.register(dict)
def _(obj):
    return {key: to_json(value) for key, value in obj.items()}

@to_json.register(type(None))
def _(obj):
    return None

# Use it
data = {
    "name": "Alice",
    "age": 30,
    "scores": [95, 87, 92],
    "active": None
}
print(to_json(data))
```

### Practical Examples

```python
from functools import singledispatch
from datetime import datetime, date

@singledispatch
def format_value(value):
    """Default formatter"""
    return str(value)

@format_value.register
def _(value: int):
    return f"{value:,}"

@format_value.register
def _(value: float):
    return f"{value:.2f}"

@format_value.register
def _(value: datetime):
    return value.strftime("%Y-%m-%d %H:%M:%S")

@format_value.register
def _(value: date):
    return value.strftime("%Y-%m-%d")

@format_value.register
def _(value: bool):
    return "Yes" if value else "No"

# Use with different types
print(format_value(1000000))           # 1,000,000
print(format_value(3.14159))           # 3.14
print(format_value(datetime.now()))    # 2024-01-15 10:30:45
print(format_value(True))              # Yes
```

### Check Registered Implementations

```python
from functools import singledispatch

@singledispatch
def process(data):
    return "default"

@process.register(int)
def _(data):
    return "int"

@process.register(str)
def _(data):
    return "str"

# Get implementation for type
print(process.registry[int])  # <function ...>
print(process.registry[str])  # <function ...>

# Dispatch manually
impl = process.dispatch(int)
print(impl(42))  # "int"
```

---

## cmp_to_key()

Convert old-style comparison function to key function for sorting.

### Basic Usage

```python
from functools import cmp_to_key

# Old-style comparison function
def compare(x, y):
    """Return -1, 0, or 1"""
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return 0

# Convert to key function
numbers = [5, 2, 8, 1, 9]
sorted_numbers = sorted(numbers, key=cmp_to_key(compare))
print(sorted_numbers)  # [1, 2, 5, 8, 9]
```

### Practical Examples

```python
from functools import cmp_to_key

# Custom string comparison (case-insensitive, then by length)
def compare_strings(a, b):
    # First compare case-insensitive
    a_lower = a.lower()
    b_lower = b.lower()
    if a_lower < b_lower:
        return -1
    elif a_lower > b_lower:
        return 1
    # If equal, compare by length
    elif len(a) < len(b):
        return -1
    elif len(a) > len(b):
        return 1
    else:
        return 0

words = ["apple", "APPLE", "Banana", "cherry", "CHERRY"]
sorted_words = sorted(words, key=cmp_to_key(compare_strings))
print(sorted_words)  # ['apple', 'APPLE', 'Banana', 'cherry', 'CHERRY']

# Sort by multiple criteria
def compare_people(person1, person2):
    # Sort by age, then by name
    age1, name1 = person1
    age2, name2 = person2

    if age1 != age2:
        return -1 if age1 < age2 else 1

    if name1 < name2:
        return -1
    elif name1 > name2:
        return 1
    else:
        return 0

people = [(30, "Alice"), (25, "Bob"), (30, "Charlie")]
sorted_people = sorted(people, key=cmp_to_key(compare_people))
print(sorted_people)  # [(25, 'Bob'), (30, 'Alice'), (30, 'Charlie')]
```

---

## Advanced Patterns

### Chaining Decorators with wraps

```python
from functools import wraps

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Took {time.time() - start:.4f}s")
        return result
    return wrapper

@debug
@timer
def slow_function():
    """Slow function"""
    import time
    time.sleep(1)

slow_function()
# Calling slow_function
# Took 1.0001s
```

### Combining partial and lru_cache

```python
from functools import partial, lru_cache

@lru_cache(maxsize=128)
def power(base, exponent):
    return base ** exponent

# Create cached specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

# Both benefit from shared cache
print(square(5))  # Computes
print(cube(5))    # Computes
print(power(5, 2))  # Cached!
```

### Generic Function with singledispatch

```python
from functools import singledispatch
from collections.abc import Sequence, Mapping

@singledispatch
def serialize(obj):
    raise TypeError(f"Cannot serialize {type(obj)}")

@serialize.register(int)
@serialize.register(float)
@serialize.register(str)
@serialize.register(bool)
@serialize.register(type(None))
def _(obj):
    return obj

@serialize.register(Sequence)
def _(obj):
    return [serialize(item) for item in obj]

@serialize.register(Mapping)
def _(obj):
    return {key: serialize(value) for key, value in obj.items()}

# Handles nested structures
data = {
    "users": [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ],
    "count": 2
}
print(serialize(data))
```

---

## Best Practices

### ✅ DO

```python
from functools import wraps, lru_cache, partial

# 1. Always use @wraps in decorators
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# 2. Use lru_cache for expensive pure functions
@lru_cache(maxsize=128)
def expensive_computation(n):
    # Pure function (same input = same output)
    return sum(range(n))

# 3. Use partial for callback configuration
def process_data(data, callback):
    return callback(data)

error_handler = partial(process_data, callback=handle_error)
success_handler = partial(process_data, callback=handle_success)

# 4. Use cached_property for expensive properties
from functools import cached_property

class DataProcessor:
    @cached_property
    def expensive_result(self):
        return self._compute_expensive_thing()

# 5. Use singledispatch for type-based dispatch
@singledispatch
def process(data):
    return str(data)
```

### ❌ DON'T

```python
# 1. Don't forget @wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):  # Loses metadata
        return func(*args, **kwargs)
    return wrapper

# 2. Don't cache functions with mutable arguments
@lru_cache
def bad_cache(items):  # TypeError: unhashable type: 'list'
    return sum(items)

# 3. Don't use lru_cache on methods without considering self
class Example:
    @lru_cache  # Wrong! Caches per instance
    def method(self, x):
        return x * 2

# 4. Don't use reduce when built-ins exist
from functools import reduce
total = reduce(lambda x, y: x + y, numbers)  # Don't
total = sum(numbers)  # Do this instead

# 5. Don't overuse singledispatch
@singledispatch
def process(x):
    pass

# If you only have 2-3 types, just use if/isinstance
```

---

## Quick Reference

### Common Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `reduce` | Cumulative operation | `reduce(lambda x,y: x+y, [1,2,3])` |
| `partial` | Pre-fill arguments | `double = partial(multiply, 2)` |
| `lru_cache` | Memoization | `@lru_cache(maxsize=128)` |
| `cached_property` | Cache property | `@cached_property` |
| `wraps` | Preserve metadata | `@wraps(func)` |
| `total_ordering` | Auto-generate comparisons | `@total_ordering` |
| `singledispatch` | Type-based dispatch | `@singledispatch` |

### Performance Guide

| Function | Use Case | Benefit |
|----------|----------|---------|
| `lru_cache` | Repeated function calls | 10-100x speedup |
| `cached_property` | Expensive properties | Compute once |
| `partial` | Callback configuration | Code reuse |
| `reduce` | Cumulative operations | Functional style |

---

## Summary

**Key Takeaways:**

1. **`reduce()`** - cumulative operations (but prefer built-ins when available)
2. **`partial()`** - pre-fill function arguments
3. **`lru_cache()`** - automatic memoization for pure functions
4. **`cached_property()`** - cache expensive property computations
5. **`wraps()`** - essential for decorators to preserve metadata
6. **`total_ordering()`** - auto-generate comparison methods
7. **`singledispatch()`** - type-based function dispatch

**Most Used:**
- `@lru_cache` - performance optimization
- `@wraps` - decorator development
- `partial` - function specialization

**Basic Pattern:**
```python
from functools import wraps, lru_cache, partial

# Decorator with metadata preserved
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Cached function
@lru_cache(maxsize=128)
def expensive(n):
    return sum(range(n))

# Specialized function
multiply = lambda x, y: x * y
double = partial(multiply, 2)
```

🔧 Master functools for more elegant, efficient Python code!
