# Python Comprehensions Cheatsheet

## Table of Contents
- [What are Comprehensions?](#what-are-comprehensions)
- [List Comprehensions](#list-comprehensions)
- [Set Comprehensions](#set-comprehensions)
- [Dictionary Comprehensions](#dictionary-comprehensions)
- [Generator Expressions](#generator-expressions)
- [Nested Comprehensions](#nested-comprehensions)
- [Walrus Operator](#walrus-operator)
- [Performance](#performance)
- [Best Practices](#best-practices)

---

## What are Comprehensions?

Comprehensions provide a **concise** way to create collections from iterables. They're more readable and often faster than traditional loops.

**Benefits:**
- 🚀 More concise than loops
- 📖 More readable (when not nested deeply)
- ⚡ Usually faster than equivalent loops
- 🎯 Pythonic and idiomatic

**Basic Syntax:**
```python
[expression for item in iterable if condition]
```

---

## List Comprehensions

### Basic List Comprehension

```python
# Traditional loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension - cleaner!
squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### With Condition (Filtering)

```python
# Get even numbers
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Get squares of odd numbers
odd_squares = [x ** 2 for x in range(10) if x % 2 == 1]
# [1, 9, 25, 49, 81]

# Multiple conditions (AND)
result = [x for x in range(20) if x % 2 == 0 if x > 10]
# [12, 14, 16, 18]

# Same as:
result = [x for x in range(20) if x % 2 == 0 and x > 10]
```

### With if-else (Conditional Expression)

```python
# Replace negatives with 0
numbers = [5, -3, 8, -1, 10]
result = [x if x >= 0 else 0 for x in numbers]
# [5, 0, 8, 0, 10]

# Label even/odd
labels = ['even' if x % 2 == 0 else 'odd' for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']

# Note the order:
# [expression_if_true if condition else expression_if_false for item in iterable]
```

### String Operations

```python
# Uppercase all strings
words = ['hello', 'world', 'python']
upper = [word.upper() for word in words]
# ['HELLO', 'WORLD', 'PYTHON']

# Get first character
first_chars = [word[0] for word in words]
# ['h', 'w', 'p']

# Filter by length
long_words = [word for word in words if len(word) > 5]
# ['python']

# Split and flatten
sentence = "hello world python"
chars = [char for word in sentence.split() for char in word]
# ['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd', ...]
```

### Working with Multiple Iterables

```python
# Combine two lists
list1 = [1, 2, 3]
list2 = [10, 20, 30]

# Pairs
pairs = [(x, y) for x in list1 for y in list2]
# [(1, 10), (1, 20), (1, 30), (2, 10), (2, 20), (2, 30), (3, 10), (3, 20), (3, 30)]

# Using zip
combined = [(x, y) for x, y in zip(list1, list2)]
# [(1, 10), (2, 20), (3, 30)]

# Sum pairs
sums = [x + y for x, y in zip(list1, list2)]
# [11, 22, 33]
```

### Matrix Operations

```python
# Create matrix
matrix = [[i + j for j in range(3)] for i in range(3)]
# [[0, 1, 2], [1, 2, 3], [2, 3, 4]]

# Flatten matrix
flat = [num for row in matrix for num in row]
# [0, 1, 2, 1, 2, 3, 2, 3, 4]

# Transpose matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

### Common Patterns

```python
# Remove duplicates (preserve order)
items = [1, 2, 2, 3, 1, 4]
seen = set()
unique = [x for x in items if not (x in seen or seen.add(x))]
# [1, 2, 3, 4]

# Extract digits from string
text = "abc123def456"
digits = [char for char in text if char.isdigit()]
# ['1', '2', '3', '4', '5', '6']

# Parse CSV-like data
lines = ["1,2,3", "4,5,6", "7,8,9"]
parsed = [[int(x) for x in line.split(',')] for line in lines]
# [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Function application
def square(x):
    return x ** 2

numbers = [1, 2, 3, 4, 5]
result = [square(x) for x in numbers]
# [1, 4, 9, 16, 25]
```

---

## Set Comprehensions

Create sets with comprehension syntax using `{}`.

### Basic Set Comprehension

```python
# Square numbers (duplicates removed)
squares = {x ** 2 for x in [1, 2, 2, 3, 3, 4]}
# {1, 4, 9, 16}

# Even numbers
evens = {x for x in range(20) if x % 2 == 0}
# {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}
```

### Practical Examples

```python
# Unique lengths
words = ['hello', 'hi', 'world', 'hey', 'python']
lengths = {len(word) for word in words}
# {2, 3, 5, 6}

# Unique first characters
first_chars = {word[0] for word in words}
# {'h', 'w', 'p'}

# Unique values from nested structure
data = [[1, 2], [2, 3], [3, 4]]
unique_values = {num for sublist in data for num in sublist}
# {1, 2, 3, 4}
```

### Set Operations

```python
# Intersection using comprehension
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

# Elements in both
common = {x for x in set1 if x in set2}
# {4, 5}

# Unique to set1
unique_to_set1 = {x for x in set1 if x not in set2}
# {1, 2, 3}
```

---

## Dictionary Comprehensions

Create dictionaries with comprehension syntax using `{}` with key-value pairs.

### Basic Dictionary Comprehension

```python
# Square numbers
squares = {x: x ** 2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Create from two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
dictionary = {k: v for k, v in zip(keys, values)}
# {'a': 1, 'b': 2, 'c': 3}
```

### With Conditions

```python
# Filter by value
numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
evens = {k: v for k, v in numbers.items() if v % 2 == 0}
# {'b': 2, 'd': 4}

# Filter by key
filtered = {k: v for k, v in numbers.items() if k in ['a', 'c', 'e']}
# {'a': 1, 'c': 3, 'e': 5}

# Conditional value
modified = {k: v * 2 if v % 2 == 0 else v for k, v in numbers.items()}
# {'a': 1, 'b': 4, 'c': 3, 'd': 8, 'e': 5}
```

### String Transformations

```python
# Word lengths
words = ['hello', 'world', 'python']
word_lengths = {word: len(word) for word in words}
# {'hello': 5, 'world': 5, 'python': 6}

# Uppercase keys
data = {'name': 'Alice', 'age': 30}
upper_keys = {k.upper(): v for k, v in data.items()}
# {'NAME': 'Alice', 'AGE': 30}

# Invert dictionary
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}
```

### Nested Dictionary Operations

```python
# Extract nested values
users = {
    'user1': {'name': 'Alice', 'age': 30},
    'user2': {'name': 'Bob', 'age': 25},
    'user3': {'name': 'Charlie', 'age': 35}
}

# Extract names
names = {k: v['name'] for k, v in users.items()}
# {'user1': 'Alice', 'user2': 'Bob', 'user3': 'Charlie'}

# Filter by nested value
adults = {k: v for k, v in users.items() if v['age'] >= 30}
# {'user1': {...}, 'user3': {...}}
```

### Grouping Data

```python
# Group by first letter
words = ['apple', 'banana', 'apricot', 'blueberry', 'avocado']
grouped = {}
for word in words:
    first = word[0]
    if first not in grouped:
        grouped[first] = []
    grouped[first].append(word)

# Using comprehension (requires defaultdict or manual handling)
from collections import defaultdict
grouped = defaultdict(list)
{grouped[word[0]].append(word) for word in words}
# Better with regular loop or itertools.groupby

# Count occurrences
items = ['a', 'b', 'a', 'c', 'b', 'a']
counts = {item: items.count(item) for item in set(items)}
# {'a': 3, 'b': 2, 'c': 1}

# Better with Counter
from collections import Counter
counts = dict(Counter(items))
```

---

## Generator Expressions

Generator expressions use `()` and create generators (lazy evaluation).

### Basic Generator Expression

```python
# List comprehension - eager (all at once)
squares_list = [x ** 2 for x in range(1000000)]  # Uses memory

# Generator expression - lazy (on demand)
squares_gen = (x ** 2 for x in range(1000000))   # Minimal memory

# Iterate
for square in squares_gen:
    print(square)
    if square > 100:
        break  # Can stop early, saved computation!
```

### Memory Efficiency

```python
import sys

# Compare sizes
list_comp = [x for x in range(10000)]
gen_expr = (x for x in range(10000))

print(sys.getsizeof(list_comp))  # ~85,176 bytes
print(sys.getsizeof(gen_expr))   # ~128 bytes
```

### Practical Use Cases

```python
# Sum of squares (no need for list)
total = sum(x ** 2 for x in range(100))

# Check if any/all
numbers = range(1000)
has_large = any(x > 900 for x in numbers)  # True
all_positive = all(x >= 0 for x in numbers)  # True

# Max/min
max_square = max(x ** 2 for x in range(100))

# Join strings
words = ['hello', 'world', 'python']
sentence = ' '.join(word.upper() for word in words)
# 'HELLO WORLD PYTHON'

# File processing (memory efficient)
def process_large_file(filename):
    with open(filename) as f:
        # Generator expression - processes line by line
        uppercase_lines = (line.upper() for line in f)
        # Filter
        filtered = (line for line in uppercase_lines if 'ERROR' in line)
        return list(filtered)
```

### Converting Between Types

```python
gen = (x ** 2 for x in range(5))

# To list
list(gen)  # [0, 1, 4, 9, 16]

# Note: generator is exhausted after first use
gen = (x ** 2 for x in range(5))
set(gen)   # {0, 1, 4, 9, 16}

gen = (x ** 2 for x in range(5))
tuple(gen) # (0, 1, 4, 9, 16)
```

---

## Nested Comprehensions

### Nested List Comprehensions

```python
# 2D matrix
matrix = [[i * j for j in range(5)] for i in range(5)]
# [[0, 0, 0, 0, 0],
#  [0, 1, 2, 3, 4],
#  [0, 2, 4, 6, 8],
#  [0, 3, 6, 9, 12],
#  [0, 4, 8, 12, 16]]

# Flattening
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in nested for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Reading order: outer loop first, then inner
# Equivalent to:
flat = []
for row in nested:  # outer loop
    for num in row:  # inner loop
        flat.append(num)
```

### Complex Nesting

```python
# All combinations
result = [(x, y, z)
          for x in range(3)
          for y in range(3)
          for z in range(3)]
# [(0,0,0), (0,0,1), (0,0,2), (0,1,0), ...]

# With filtering
result = [(x, y, z)
          for x in range(10)
          for y in range(10)
          for z in range(10)
          if x + y + z == 10]

# Pythagorean triples
triples = [(a, b, c)
           for a in range(1, 30)
           for b in range(a, 30)
           for c in range(b, 30)
           if a**2 + b**2 == c**2]
# [(3, 4, 5), (5, 12, 13), (6, 8, 10), ...]
```

### When NOT to Use Nested Comprehensions

```python
# ❌ Too complex - hard to read
result = [[[(i, j, k) for k in range(3) if k % 2 == 0]
           for j in range(5) if j > 2]
          for i in range(10) if i % 2 == 1]

# ✅ Use regular loops instead
result = []
for i in range(10):
    if i % 2 == 1:
        sublist = []
        for j in range(5):
            if j > 2:
                subsublist = []
                for k in range(3):
                    if k % 2 == 0:
                        subsublist.append((i, j, k))
                sublist.append(subsublist)
        result.append(sublist)

# Or break into functions
def process_k(i, j):
    return [(i, j, k) for k in range(3) if k % 2 == 0]

def process_j(i):
    return [process_k(i, j) for j in range(5) if j > 2]

result = [process_j(i) for i in range(10) if i % 2 == 1]
```

---

## Walrus Operator

The walrus operator `:=` (Python 3.8+) allows assignment within expressions.

### Basic Usage

```python
# Without walrus
data = get_data()
if data:
    process(data)

# With walrus - assign and use in same expression
if (data := get_data()):
    process(data)
```

### In Comprehensions

```python
# Avoid calling function twice
def expensive_function(x):
    print(f"Computing for {x}")
    return x ** 2

# ❌ Without walrus - calls function twice
results = [val for x in range(5)
           if (val := expensive_function(x)) > 10]

# ✅ With walrus - calls once, reuses value
results = [(val, x) for x in range(5)
           if (val := expensive_function(x)) > 10]
# Computing for 0, 1, 2, 3, 4
# [(16, 4)]
```

### Practical Examples

```python
# Filter and transform in one pass
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
results = [doubled for x in numbers
           if (doubled := x * 2) > 10]
# [12, 14, 16, 18, 20]

# Process matches
import re
text = "abc123def456ghi789"
numbers = [match.group() for line in [text]
           if (match := re.search(r'\d+', line))]

# File reading
with open('data.txt') as f:
    # Read non-empty lines
    lines = [line.strip() for line in f
             if (line := line.strip())]

# While loop with comprehension
def read_chunks(file, size):
    """Read file in chunks using walrus"""
    with open(file, 'rb') as f:
        return [chunk for _ in iter(int, 1)
                if (chunk := f.read(size))]
```

### Walrus in Regular Loops

```python
# Reading input until empty
inputs = []
while (user_input := input("Enter value (empty to quit): ")):
    inputs.append(user_input)

# Processing until condition
results = []
while (result := process_next()) is not None:
    results.append(result)
```

---

## Performance

### Speed Comparison

```python
import timeit

# List comprehension vs loop
def using_loop():
    result = []
    for i in range(1000):
        result.append(i ** 2)
    return result

def using_comprehension():
    return [i ** 2 for i in range(1000)]

# Comprehension is faster
loop_time = timeit.timeit(using_loop, number=10000)
comp_time = timeit.timeit(using_comprehension, number=10000)

print(f"Loop: {loop_time:.4f}s")
print(f"Comprehension: {comp_time:.4f}s")
# Comprehension is typically 20-30% faster
```

### Memory Usage

```python
import sys

# List comprehension - all in memory
list_comp = [x for x in range(10000)]
print(f"List: {sys.getsizeof(list_comp)} bytes")  # ~85KB

# Generator expression - lazy
gen_expr = (x for x in range(10000))
print(f"Generator: {sys.getsizeof(gen_expr)} bytes")  # ~128 bytes

# Choose based on use case:
# - Multiple iterations? Use list
# - One-time iteration? Use generator
# - Need indexing? Use list
# - Processing pipeline? Use generator
```

### When to Use What

```python
# ✅ List comprehension - small data, multiple iterations
small_data = [x ** 2 for x in range(100)]
print(small_data[50])  # Random access
print(sum(small_data))  # Reuse

# ✅ Generator expression - large data, single pass
large_data = (x ** 2 for x in range(1000000))
result = sum(large_data)  # Process once

# ✅ Set comprehension - unique values needed
unique_values = {x % 10 for x in range(100)}

# ✅ Dict comprehension - key-value mapping
mapping = {x: x ** 2 for x in range(10)}
```

---

## Best Practices

### ✅ DO

```python
# 1. Use comprehensions for simple transformations
squares = [x ** 2 for x in range(10)]

# 2. Use filter conditions for readability
evens = [x for x in range(20) if x % 2 == 0]

# 3. Use generator expressions for large datasets
total = sum(x ** 2 for x in range(1000000))

# 4. Keep comprehensions simple and readable
# One line is ideal, two lines max
result = [
    process(item)
    for item in items
    if is_valid(item)
]

# 5. Use comprehensions for functional operations
# map equivalent
doubled = [x * 2 for x in numbers]

# filter equivalent
positives = [x for x in numbers if x > 0]

# map + filter
result = [x * 2 for x in numbers if x > 0]
```

### ❌ DON'T

```python
# 1. Don't use comprehensions with side effects
# ❌ BAD
[print(x) for x in items]  # Use regular loop instead

# ✅ GOOD
for x in items:
    print(x)

# 2. Don't make them too complex
# ❌ BAD - unreadable
result = [[[(i+j+k) for k in range(3)] for j in range(3)] for i in range(3)]

# ✅ GOOD - use functions or loops
def create_3d_matrix():
    result = []
    for i in range(3):
        matrix = []
        for j in range(3):
            row = []
            for k in range(3):
                row.append(i + j + k)
            matrix.append(row)
        result.append(matrix)
    return result

# 3. Don't use when you need the intermediate state
# ❌ BAD
items = []
[items.append(x) if condition else items.append(0) for x in data]

# ✅ GOOD
items = [x if condition else 0 for x in data]

# 4. Don't use comprehension if you don't need the result
# ❌ BAD
[process_and_save(item) for item in items]  # Creating unused list

# ✅ GOOD
for item in items:
    process_and_save(item)

# Or if you need consumption:
from collections import deque
deque((process(item) for item in items), maxlen=0)

# 5. Don't nest more than 2 levels
# ❌ BAD
result = [[[z for z in range(3)] for y in range(3)] for x in range(3)]

# ✅ GOOD (if needed)
def create_matrix():
    # Use descriptive variable names and functions
    pass
```

### Readability Guidelines

```python
# If it takes more than 3 seconds to understand, use a loop

# ✅ Clear
evens = [x for x in numbers if x % 2 == 0]

# ⚠️ Getting complex
result = [x * 2 for x in numbers if x > 0 if x < 100]

# ❌ Too complex
result = [x if x > 0 else -x for x in [y * 2 for y in numbers] if x != 0]

# Better as:
doubled = [y * 2 for y in numbers]
result = [x if x > 0 else -x for x in doubled if x != 0]

# Or just use a loop:
result = []
for y in numbers:
    doubled = y * 2
    if doubled != 0:
        result.append(doubled if doubled > 0 else -doubled)
```

---

## Quick Reference

### Syntax Summary

```python
# List comprehension
[expression for item in iterable if condition]

# Set comprehension
{expression for item in iterable if condition}

# Dict comprehension
{key: value for item in iterable if condition}

# Generator expression
(expression for item in iterable if condition)

# With if-else (ternary)
[expr_if_true if condition else expr_if_false for item in iterable]

# Nested
[expr for item1 in iterable1 for item2 in iterable2]

# Walrus operator (Python 3.8+)
[y for x in items if (y := func(x)) > threshold]
```

### Common Patterns

| Operation | Comprehension | Equivalent |
|-----------|---------------|------------|
| Map | `[f(x) for x in items]` | `map(f, items)` |
| Filter | `[x for x in items if pred(x)]` | `filter(pred, items)` |
| Map + Filter | `[f(x) for x in items if pred(x)]` | `map(f, filter(pred, items))` |
| Flatten | `[x for sublist in lists for x in sublist]` | `itertools.chain.from_iterable()` |
| Zip | `[(x, y) for x, y in zip(a, b)]` | `list(zip(a, b))` |

### Performance Guide

| Scenario | Use |
|----------|-----|
| Small data, multiple passes | List comprehension |
| Large data, single pass | Generator expression |
| Need unique values | Set comprehension |
| Key-value mapping | Dict comprehension |
| Side effects needed | Regular loop |
| Complex logic | Regular loop or function |

---

## Summary

**Key Takeaways:**

1. **Comprehensions are concise and Pythonic** for creating collections
2. **Use `[]` for lists, `{}` for sets/dicts, `()` for generators**
3. **Generator expressions save memory** for large datasets
4. **Keep comprehensions simple** - readability matters!
5. **Walrus operator `:=`** avoids redundant computations
6. **Don't use comprehensions for side effects** - use loops

**Basic Template:**
```python
# [what_to_do for item in collection if include_item]
result = [x * 2 for x in numbers if x > 0]
```

**When in doubt:**
- Simple transformation? → Comprehension
- Complex logic? → Regular loop
- Large data, one pass? → Generator expression
- Need side effects? → Regular loop

🎯 Master comprehensions for cleaner, faster, more Pythonic code!
