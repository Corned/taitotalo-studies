# Python Itertools Cheatsheet

## Table of Contents
- [What is Itertools?](#what-is-itertools)
- [Infinite Iterators](#infinite-iterators)
- [Combinatoric Iterators](#combinatoric-iterators)
- [Terminating Iterators](#terminating-iterators)
- [Grouping and Filtering](#grouping-and-filtering)
- [Recipes](#recipes)
- [Performance Tips](#performance-tips)
- [Best Practices](#best-practices)

---

## What is Itertools?

The **itertools** module provides fast, memory-efficient tools for working with iterators. All functions return **iterators** (lazy evaluation).

**Benefits:**
- 🚀 Memory efficient (lazy evaluation)
- ⚡ Fast (implemented in C)
- 🔄 Composable (chain operations)
- 📊 Perfect for data processing pipelines

```python
import itertools

# All itertools functions return iterators
result = itertools.count(1, 2)  # Iterator, not list
print(list(itertools.islice(result, 5)))  # [1, 3, 5, 7, 9]
```

---

## Infinite Iterators

### count(start=0, step=1)

Count infinitely from start with step.

```python
import itertools

# Count from 10
counter = itertools.count(10)
print(next(counter))  # 10
print(next(counter))  # 11
print(next(counter))  # 12

# Count with step
counter = itertools.count(0, 5)
print(list(itertools.islice(counter, 5)))  # [0, 5, 10, 15, 20]

# Negative step
counter = itertools.count(10, -1)
print(list(itertools.islice(counter, 5)))  # [10, 9, 8, 7, 6]

# Use with zip for enumeration
for i, item in zip(itertools.count(1), ['a', 'b', 'c']):
    print(f"{i}: {item}")
# 1: a
# 2: b
# 3: c
```

### cycle(iterable)

Cycle through elements infinitely.

```python
import itertools

# Cycle through list
cycler = itertools.cycle(['A', 'B', 'C'])
print([next(cycler) for _ in range(7)])
# ['A', 'B', 'C', 'A', 'B', 'C', 'A']

# Round-robin task assignment
tasks = ['task1', 'task2', 'task3']
workers = itertools.cycle(['Alice', 'Bob', 'Charlie'])

for task, worker in zip(tasks, workers):
    print(f"{task} -> {worker}")

# Alternating patterns
pattern = itertools.cycle([0, 1])
print(list(itertools.islice(pattern, 10)))
# [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
```

### repeat(object, times=None)

Repeat object infinitely or n times.

```python
import itertools

# Repeat indefinitely
repeater = itertools.repeat('A')
print(list(itertools.islice(repeater, 5)))  # ['A', 'A', 'A', 'A', 'A']

# Repeat n times
repeater = itertools.repeat('X', 3)
print(list(repeater))  # ['X', 'X', 'X']

# Use with map for constant values
result = list(map(pow, range(5), itertools.repeat(2)))
print(result)  # [0, 1, 4, 9, 16] (squares)

# Use with zip for padding
names = ['Alice', 'Bob', 'Charlie']
ages = [30, 25]
result = list(zip(names, itertools.chain(ages, itertools.repeat(None))))
print(result)  # [('Alice', 30), ('Bob', 25), ('Charlie', None)]
```

---

## Combinatoric Iterators

### product(*iterables, repeat=1)

Cartesian product (like nested for-loops).

```python
import itertools

# Basic product
result = itertools.product([1, 2], ['a', 'b'])
print(list(result))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# Three iterables
result = itertools.product([1, 2], [3, 4], [5, 6])
print(list(result))
# [(1,3,5), (1,3,6), (1,4,5), (1,4,6), (2,3,5), (2,3,6), (2,4,5), (2,4,6)]

# Repeat parameter (self-product)
result = itertools.product([0, 1], repeat=3)
print(list(result))
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]

# All coordinates in 2D grid
grid = itertools.product(range(3), range(3))
print(list(grid))
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# Password combinations
chars = 'ab'
passwords = itertools.product(chars, repeat=3)
print(list(passwords))
# [('a','a','a'), ('a','a','b'), ('a','b','a'), ..., ('b','b','b')]
```

### permutations(iterable, r=None)

All permutations of length r.

```python
import itertools

# All permutations
result = itertools.permutations([1, 2, 3])
print(list(result))
# [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

# Length 2 permutations
result = itertools.permutations([1, 2, 3], 2)
print(list(result))
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

# String permutations
result = itertools.permutations('ABC', 2)
print([''.join(p) for p in result])
# ['AB', 'AC', 'BA', 'BC', 'CA', 'CB']

# Order matters: (1,2) != (2,1)
# Number of permutations: n! / (n-r)!
# For n=3, r=2: 3! / 1! = 6
```

### combinations(iterable, r)

All combinations of length r (order doesn't matter).

```python
import itertools

# All combinations of length 2
result = itertools.combinations([1, 2, 3, 4], 2)
print(list(result))
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

# All 3-element combinations
result = itertools.combinations('ABCD', 3)
print([''.join(c) for c in result])
# ['ABC', 'ABD', 'ACD', 'BCD']

# Order doesn't matter: (1,2) == (2,1), only one is included
# No repeats: each element used at most once
# Number of combinations: n! / (r! * (n-r)!)

# All subsets of specific size
items = ['apple', 'banana', 'cherry']
for size in range(len(items) + 1):
    print(f"Size {size}:", list(itertools.combinations(items, size)))
```

### combinations_with_replacement(iterable, r)

Combinations with replacement (repeats allowed).

```python
import itertools

# Combinations with replacement
result = itertools.combinations_with_replacement([1, 2, 3], 2)
print(list(result))
# [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]

# Compare with regular combinations
regular = itertools.combinations([1, 2, 3], 2)
print(list(regular))
# [(1,2), (1,3), (2,3)] - no (1,1), (2,2), (3,3)

# Dice rolls (order doesn't matter)
result = itertools.combinations_with_replacement(range(1, 7), 2)
print(list(result))
# [(1,1), (1,2), ..., (6,6)] - 21 combinations

# Choose items with replacement
items = ['A', 'B', 'C']
result = itertools.combinations_with_replacement(items, 2)
print(list(result))
# [('A','A'), ('A','B'), ('A','C'), ('B','B'), ('B','C'), ('C','C')]
```

---

## Terminating Iterators

### chain(*iterables)

Chain multiple iterables together.

```python
import itertools

# Chain lists
result = itertools.chain([1, 2], [3, 4], [5, 6])
print(list(result))  # [1, 2, 3, 4, 5, 6]

# Chain different types
result = itertools.chain('ABC', [1, 2, 3], ('x', 'y'))
print(list(result))  # ['A', 'B', 'C', 1, 2, 3, 'x', 'y']

# chain.from_iterable - flatten nested structure
nested = [[1, 2], [3, 4], [5, 6]]
result = itertools.chain.from_iterable(nested)
print(list(result))  # [1, 2, 3, 4, 5, 6]

# Flatten matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = list(itertools.chain.from_iterable(matrix))
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### islice(iterable, start, stop, step)

Slice an iterator.

```python
import itertools

# First n items
result = itertools.islice(range(100), 5)
print(list(result))  # [0, 1, 2, 3, 4]

# Items from index 10 to 15
result = itertools.islice(range(100), 10, 15)
print(list(result))  # [10, 11, 12, 13, 14]

# Every other item, first 10
result = itertools.islice(range(100), 0, 10, 2)
print(list(result))  # [0, 2, 4, 6, 8]

# Works with infinite iterators
counter = itertools.count(1)
first_ten = list(itertools.islice(counter, 10))
print(first_ten)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Skip first n items
data = range(20)
skip_5 = itertools.islice(data, 5, None)
print(list(skip_5))  # [5, 6, 7, ..., 19]
```

### compress(data, selectors)

Filter data by selector values.

```python
import itertools

# Select based on boolean mask
data = ['A', 'B', 'C', 'D', 'E']
selectors = [1, 0, 1, 0, 1]
result = itertools.compress(data, selectors)
print(list(result))  # ['A', 'C', 'E']

# Filter with custom logic
numbers = range(10)
even_mask = [n % 2 == 0 for n in numbers]
evens = list(itertools.compress(numbers, even_mask))
print(evens)  # [0, 2, 4, 6, 8]

# Select columns from matrix
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]
column_mask = [1, 0, 1, 0]  # Select columns 0 and 2
for row in matrix:
    selected = list(itertools.compress(row, column_mask))
    print(selected)
# [1, 3]
# [5, 7]
# [9, 11]
```

### dropwhile(predicate, iterable)

Drop items while predicate is true, then return all remaining.

```python
import itertools

# Drop while less than 5
result = itertools.dropwhile(lambda x: x < 5, [1, 3, 5, 7, 2, 8])
print(list(result))  # [5, 7, 2, 8]

# Drop leading whitespace lines
lines = ['', '', 'First line', 'Second line', '', 'Third line']
result = itertools.dropwhile(lambda x: not x, lines)
print(list(result))
# ['First line', 'Second line', '', 'Third line']

# Skip header rows
data = ['Header 1', 'Header 2', 'Data 1', 'Data 2']
result = itertools.dropwhile(lambda x: 'Header' in x, data)
print(list(result))  # ['Data 1', 'Data 2']
```

### takewhile(predicate, iterable)

Take items while predicate is true, then stop.

```python
import itertools

# Take while less than 5
result = itertools.takewhile(lambda x: x < 5, [1, 3, 5, 7, 2, 8])
print(list(result))  # [1, 3]

# Take increasing numbers
result = itertools.takewhile(
    lambda x: x < 10,
    itertools.count(0, 2)
)
print(list(result))  # [0, 2, 4, 6, 8]

# Read until blank line
lines = ['line1', 'line2', '', 'line3']
result = itertools.takewhile(lambda x: x != '', lines)
print(list(result))  # ['line1', 'line2']
```

### filterfalse(predicate, iterable)

Filter items where predicate is false (opposite of filter).

```python
import itertools

# Get odd numbers (filter false for even)
result = itertools.filterfalse(lambda x: x % 2 == 0, range(10))
print(list(result))  # [1, 3, 5, 7, 9]

# Compare with filter
evens = filter(lambda x: x % 2 == 0, range(10))
print(list(evens))  # [0, 2, 4, 6, 8]

# Remove empty strings
data = ['hello', '', 'world', '', 'python']
result = itertools.filterfalse(lambda x: x == '', data)
print(list(result))  # ['hello', 'world', 'python']
```

### starmap(function, iterable)

Apply function using * unpacking on each item.

```python
import itertools

# Compute powers
pairs = [(2, 3), (3, 2), (10, 2)]
result = itertools.starmap(pow, pairs)
print(list(result))  # [8, 9, 100] (2³, 3², 10²)

# Without starmap (for comparison)
result = [pow(*pair) for pair in pairs]
print(result)  # [8, 9, 100]

# Multiple arguments
def multiply(a, b, c):
    return a * b * c

data = [(2, 3, 4), (1, 5, 2), (3, 3, 3)]
result = itertools.starmap(multiply, data)
print(list(result))  # [24, 10, 27]
```

### tee(iterable, n=2)

Split iterator into n independent iterators.

```python
import itertools

# Split into 2 iterators
data = range(5)
iter1, iter2 = itertools.tee(data, 2)

print(list(iter1))  # [0, 1, 2, 3, 4]
print(list(iter2))  # [0, 1, 2, 3, 4]

# Split into 3
data = range(5)
i1, i2, i3 = itertools.tee(data, 3)
print(list(i1))  # [0, 1, 2, 3, 4]
print(list(i2))  # [0, 1, 2, 3, 4]
print(list(i3))  # [0, 1, 2, 3, 4]

# Use case: process data multiple ways
numbers = range(10)
evens_iter, odds_iter = itertools.tee(numbers, 2)
evens = [x for x in evens_iter if x % 2 == 0]
odds = [x for x in odds_iter if x % 2 == 1]
```

### zip_longest(*iterables, fillvalue=None)

Zip iterables, filling shorter ones with fillvalue.

```python
import itertools

# Different length iterables
a = [1, 2, 3]
b = ['a', 'b']
result = itertools.zip_longest(a, b)
print(list(result))
# [(1, 'a'), (2, 'b'), (3, None)]

# Custom fill value
result = itertools.zip_longest(a, b, fillvalue='X')
print(list(result))
# [(1, 'a'), (2, 'b'), (3, 'X')]

# Compare with regular zip (stops at shortest)
result = zip(a, b)
print(list(result))
# [(1, 'a'), (2, 'b')]

# Multiple iterables
result = itertools.zip_longest([1, 2], ['a'], [10, 20, 30], fillvalue='-')
print(list(result))
# [(1, 'a', 10), (2, '-', 20), ('-', '-', 30)]
```

---

## Grouping and Filtering

### groupby(iterable, key=None)

Group consecutive items by key function.

```python
import itertools

# Group consecutive duplicates
data = [1, 1, 2, 2, 2, 3, 1, 1]
groups = itertools.groupby(data)
for key, group in groups:
    print(key, list(group))
# 1 [1, 1]
# 2 [2, 2, 2]
# 3 [3]
# 1 [1, 1]

# IMPORTANT: Only groups CONSECUTIVE items!
# Sort first for grouping all occurrences
data = [1, 2, 1, 2, 3, 1]
data_sorted = sorted(data)
groups = itertools.groupby(data_sorted)
for key, group in groups:
    print(key, list(group))
# 1 [1, 1, 1]
# 2 [2, 2]
# 3 [3]

# Group with key function
words = ['apple', 'apricot', 'banana', 'blueberry', 'cherry']
words_sorted = sorted(words, key=lambda x: x[0])
groups = itertools.groupby(words_sorted, key=lambda x: x[0])
for letter, group in groups:
    print(f"{letter}: {list(group)}")
# a: ['apple', 'apricot']
# b: ['banana', 'blueberry']
# c: ['cherry']

# Count occurrences
data = [1, 1, 2, 2, 2, 3, 3]
result = {key: len(list(group)) for key, group in itertools.groupby(data)}
print(result)  # {1: 2, 2: 3, 3: 2}
```

### accumulate(iterable, func=operator.add, initial=None)

Running accumulation (cumulative sum by default).

```python
import itertools
import operator

# Cumulative sum (default)
result = itertools.accumulate([1, 2, 3, 4, 5])
print(list(result))  # [1, 3, 6, 10, 15]

# Cumulative product
result = itertools.accumulate([1, 2, 3, 4, 5], operator.mul)
print(list(result))  # [1, 2, 6, 24, 120]

# Cumulative maximum
result = itertools.accumulate([3, 1, 4, 1, 5, 9, 2], max)
print(list(result))  # [3, 3, 4, 4, 5, 9, 9]

# Cumulative minimum
result = itertools.accumulate([3, 1, 4, 1, 5, 9, 2], min)
print(list(result))  # [3, 1, 1, 1, 1, 1, 1]

# Custom function
result = itertools.accumulate([1, 2, 3, 4], lambda x, y: x + y * 2)
print(list(result))  # [1, 5, 11, 19]

# With initial value (Python 3.8+)
result = itertools.accumulate([1, 2, 3], initial=10)
print(list(result))  # [10, 11, 13, 16]
```

---

## Recipes

Common patterns using itertools (from Python docs).

### take(n, iterable)

```python
import itertools

def take(n, iterable):
    """Return first n items"""
    return list(itertools.islice(iterable, n))

print(take(5, range(100)))  # [0, 1, 2, 3, 4]
```

### nth(iterable, n, default=None)

```python
import itertools

def nth(iterable, n, default=None):
    """Return nth item or default"""
    return next(itertools.islice(iterable, n, None), default)

print(nth(range(10), 5))  # 5
print(nth(range(3), 5, 'N/A'))  # 'N/A'
```

### all_equal(iterable)

```python
import itertools

def all_equal(iterable):
    """Check if all items are equal"""
    g = itertools.groupby(iterable)
    return next(g, True) and not next(g, False)

print(all_equal([1, 1, 1, 1]))  # True
print(all_equal([1, 2, 1]))      # False
```

### flatten(list_of_lists)

```python
import itertools

def flatten(list_of_lists):
    """Flatten one level of nesting"""
    return itertools.chain.from_iterable(list_of_lists)

nested = [[1, 2], [3, 4], [5, 6]]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6]
```

### pairwise(iterable)

```python
import itertools

def pairwise(iterable):
    """Return successive pairs"""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

print(list(pairwise([1, 2, 3, 4])))
# [(1, 2), (2, 3), (3, 4)]

# Built-in in Python 3.10+
# result = itertools.pairwise([1, 2, 3, 4])
```

### sliding_window(iterable, n)

```python
import itertools
from collections import deque

def sliding_window(iterable, n):
    """Sliding window of size n"""
    it = iter(iterable)
    window = deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

result = sliding_window([1, 2, 3, 4, 5], 3)
print(list(result))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

### partition(pred, iterable)

```python
import itertools

def partition(pred, iterable):
    """Split into true and false groups"""
    t1, t2 = itertools.tee(iterable)
    return filter(pred, t1), itertools.filterfalse(pred, t2)

is_even = lambda x: x % 2 == 0
evens, odds = partition(is_even, range(10))
print(list(evens))  # [0, 2, 4, 6, 8]
print(list(odds))   # [1, 3, 5, 7, 9]
```

### unique_everseen(iterable, key=None)

```python
import itertools

def unique_everseen(iterable, key=None):
    """List unique elements, preserving order"""
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

data = [1, 2, 3, 2, 1, 4, 3, 5]
print(list(unique_everseen(data)))  # [1, 2, 3, 4, 5]

# With key function
words = ['apple', 'Banana', 'APPLE', 'cherry']
print(list(unique_everseen(words, key=str.lower)))
# ['apple', 'Banana', 'cherry']
```

---

## Performance Tips

### Memory Efficiency

```python
import itertools
import sys

# List - stores everything in memory
data_list = list(range(1000000))
print(f"List size: {sys.getsizeof(data_list)} bytes")  # ~8MB

# Iterator - minimal memory
data_iter = iter(range(1000000))
print(f"Iterator size: {sys.getsizeof(data_iter)} bytes")  # ~48 bytes

# Itertools chain - combines without creating new list
combined = itertools.chain(range(1000), range(1000))
print(f"Chain size: {sys.getsizeof(combined)} bytes")  # ~48 bytes
```

### Speed Comparison

```python
import itertools
import timeit

# Using itertools.chain
def with_chain():
    return list(itertools.chain([1, 2, 3], [4, 5, 6]))

# Using list concatenation
def with_concat():
    return [1, 2, 3] + [4, 5, 6]

print(timeit.timeit(with_chain, number=100000))   # Faster for large data
print(timeit.timeit(with_concat, number=100000))  # Faster for small data
```

### Lazy Evaluation Benefits

```python
import itertools

# Generate huge amount of data lazily
def expensive_operation(x):
    # Simulate expensive computation
    return x ** 2

# Only computes first 5 (stops early)
huge_data = range(1000000)
result = itertools.islice(
    (expensive_operation(x) for x in huge_data),
    5
)
print(list(result))  # [0, 1, 4, 9, 16]
# Only computed 5 items, not 1 million!
```

---

## Best Practices

### ✅ DO

```python
import itertools

# 1. Use itertools for memory efficiency
# Instead of:
squares = [x**2 for x in range(1000000)]  # Uses lots of memory

# Use:
squares = (x**2 for x in range(1000000))  # Lazy
# Or:
squares = map(lambda x: x**2, range(1000000))

# 2. Chain operations for pipelines
result = itertools.islice(
    itertools.filterfalse(
        lambda x: x % 2 == 0,
        itertools.count(1)
    ),
    10
)
# First 10 odd numbers

# 3. Use islice with infinite iterators
counter = itertools.count()
first_10 = list(itertools.islice(counter, 10))

# 4. Sort before groupby
data = [1, 2, 1, 3, 2]
sorted_data = sorted(data)
for key, group in itertools.groupby(sorted_data):
    print(key, list(group))

# 5. Convert to list only when needed
result = itertools.chain([1, 2], [3, 4])
# Process as iterator if possible
for item in result:
    process(item)
```

### ❌ DON'T

```python
import itertools

# 1. Don't reuse exhausted iterators
result = itertools.chain([1, 2], [3, 4])
list(result)  # [1, 2, 3, 4]
list(result)  # [] - Exhausted!

# 2. Don't convert to list unnecessarily
# Bad
data = list(itertools.chain([1, 2], [3, 4]))
sum(data)

# Good
data = itertools.chain([1, 2], [3, 4])
sum(data)  # Iterators work with sum()

# 3. Don't use groupby without sorting
data = [1, 2, 1, 3, 2]
# Wrong - won't group all 1s together
for k, g in itertools.groupby(data):
    print(k, list(g))

# Right - sort first
for k, g in itertools.groupby(sorted(data)):
    print(k, list(g))

# 4. Don't forget to consume group iterators immediately
groups = itertools.groupby([1, 1, 2, 2])
result = [(k, g) for k, g in groups]  # Wrong! g is exhausted
result = [(k, list(g)) for k, g in groups]  # Right!
```

---

## Quick Reference

### Function Categories

| Category | Functions |
|----------|-----------|
| **Infinite** | `count`, `cycle`, `repeat` |
| **Terminating** | `chain`, `compress`, `dropwhile`, `filterfalse`, `islice`, `starmap`, `takewhile`, `tee`, `zip_longest` |
| **Combinatoric** | `product`, `permutations`, `combinations`, `combinations_with_replacement` |
| **Grouping** | `groupby`, `accumulate` |

### Common Patterns

| Task | Solution |
|------|----------|
| Flatten list | `chain.from_iterable(nested)` |
| First n items | `islice(iter, n)` |
| Skip n items | `islice(iter, n, None)` |
| All combinations | `product(*iterables)` |
| Unique ordered | `groupby` after sorting |
| Pairwise | `zip(a, a[1:])` or `pairwise` (3.10+) |
| Partition | `filter` + `filterfalse` |
| Cumulative sum | `accumulate(iter)` |

### Memory Usage

```python
# Memory efficient ✓
result = itertools.chain(iter1, iter2)
result = itertools.islice(huge_data, 100)
result = (x for x in data)

# Memory intensive ✗
result = list(chain(iter1, iter2))
result = list(huge_data)[:100]
result = [x for x in data]
```

---

## Summary

**Key Takeaways:**

1. **Itertools returns iterators** - lazy evaluation, memory efficient
2. **All functions are composable** - chain operations together
3. **Three main categories:** infinite, terminating, combinatoric
4. **groupby requires sorting** for complete grouping
5. **Iterators are exhausted** after one use
6. **Use islice** to safely handle infinite iterators

**Most Useful Functions:**
- `chain` - combine iterables
- `islice` - slice iterators
- `groupby` - group consecutive items
- `product` - cartesian product
- `combinations` - all combinations
- `zip_longest` - zip with padding

**Basic Pattern:**
```python
import itertools

# Chain operations
result = itertools.islice(
    itertools.filterfalse(
        lambda x: x % 2 == 0,
        range(100)
    ),
    10
)
# First 10 odd numbers from 0-99
```

🔧 Master itertools for efficient, elegant data processing!
