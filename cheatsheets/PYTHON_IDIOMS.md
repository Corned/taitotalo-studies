# Python Idioms Cheatsheet

## Table of Contents

- [What are Python Idioms?](#what-are-python-idioms)
- [Pythonic Code Principles](#pythonic-code-principles)
- [String Operations](#string-operations)
- [Lists and Sequences](#lists-and-sequences)
- [Dictionaries](#dictionaries)
- [Loops and Iteration](#loops-and-iteration)
- [Functions and Callables](#functions-and-callables)
- [Context Managers](#context-managers)
- [Classes and Objects](#classes-and-objects)
- [File Operations](#file-operations)
- [Error Handling](#error-handling)
- [Common Anti-Patterns](#common-anti-patterns)

---

## What are Python Idioms?

**Python idioms** are coding patterns that are considered "Pythonic" - natural, readable, and efficient in Python. They follow the philosophy described in PEP 20 (The Zen of Python).

```python
import this
# The Zen of Python
# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Readability counts.
```

**Benefits:**

- 🎯 More readable code
- ⚡ Better performance
- 🐍 Following Python conventions
- 👥 Easier collaboration

---

## Pythonic Code Principles

### Explicit is Better Than Implicit

```python
# ❌ Implicit (Anti-pattern)
def process(data, flag=[]):  # Dangerous! Mutable default argument
    flag.append(data)
    return flag

# ✅ Explicit
def process(data, flag=None):
    if flag is None:
        flag = []  # Creates new list each time
    # ...

# ✅ Even better
def process(data, flag=None):
    flag = flag if flag is not None else []
    # ...
```

### Simple is Better Than Complex

```python
# ❌ Complex
result = []
for item in items:
    if item > 0:
        result.append(item * 2)

# ✅ Simple
result = [item * 2 for item in items if item > 0]
```

### Readability Counts

```python
# ❌ Hard to read
x=lambda a,b:a+b if a>0 and b>0 else 0

# ✅ Readable
def add_positive(a, b):
    """Add two numbers if both are positive."""
    return a + b if a > 0 and b > 0 else 0
```

---

## String Operations

### String Concatenation

```python
# ❌ Don't use + for many strings
result = ""
for s in strings:
    result += s  # Creates new string each time

# ✅ Use join()
result = "".join(strings)

# ✅ Use f-strings for formatting
name = "Alice"
age = 30
message = f"{name} is {age} years old"

# ❌ Old style
message = "%s is %d years old" % (name, age)
message = "{} is {} years old".format(name, age)
```

### String Checking

```python
# ✅ Check for empty string
if not string:  # Pythonic
    pass

# ❌ Don't compare to empty string
if string == "":
    pass

# ✅ Check prefix/suffix
if filename.startswith("test_"):
    pass

if filename.endswith(".py"):
    pass

# ❌ Don't use slicing
if filename[:5] == "test_":
    pass
```

### String Building

```python
# ❌ Multiple concatenations
html = "<html>"
html += "<body>"
html += "<h1>Title</h1>"
html += "</body>"
html += "</html>"

# ✅ Use list and join
parts = [
    "<html>",
    "<body>",
    "<h1>Title</h1>",
    "</body>",
    "</html>"
]
html = "".join(parts)

# ✅ Or use f-strings
html = f"""
<html>
<body>
<h1>{title}</h1>
</body>
</html>
"""
```

---

## Lists and Sequences

### List Comprehensions

```python
# ❌ Verbose
squares = []
for x in range(10):
    squares.append(x ** 2)

# ✅ Pythonic
squares = [x ** 2 for x in range(10)]

# ✅ With condition
evens = [x for x in range(20) if x % 2 == 0]

# ✅ Nested
matrix = [[i + j for j in range(3)] for i in range(3)]
```

### Unpacking

```python
# ✅ Multiple assignment
a, b = 1, 2
x, y, z = [1, 2, 3]

# ✅ Swap variables
a, b = b, a

# ✅ Extended unpacking
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5

# ✅ Ignore values
x, _, z = (1, 2, 3)  # Ignore middle value
```

### Slicing

```python
# ✅ Copy list
new_list = old_list[:]  # Shallow copy
new_list = old_list.copy()  # Also good

# ✅ Reverse
reversed_list = items[::-1]

# ✅ Get every nth element
every_third = items[::3]

# ✅ Negative indexing
last = items[-1]
second_last = items[-2]
```

### List Operations

```python
# ✅ Check membership
if item in items:  # O(n) for lists
    pass

# ✅ Use set for frequent lookups
items_set = set(items)
if item in items_set:  # O(1) average
    pass

# ✅ Remove duplicates (preserving order)
seen = set()
unique = [x for x in items if not (x in seen or seen.add(x))]

# ✅ Flatten list
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]

# Or use itertools
from itertools import chain
flat = list(chain.from_iterable(nested))
```

---

## Dictionaries

### Dictionary Creation

```python
# ✅ Dict comprehension
squares = {x: x ** 2 for x in range(10)}

# ✅ From keys and values
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = dict(zip(keys, values))

# ✅ Default values
from collections import defaultdict
word_count = defaultdict(int)
word_count['apple'] += 1  # No KeyError
```

### Dictionary Access

```python
# ❌ Check key existence
if 'key' in d:
    value = d['key']
else:
    value = default

# ✅ Use get()
value = d.get('key', default)

# ✅ Use setdefault()
d.setdefault('key', []).append(item)

# ❌ Don't do this
if 'key' not in d:
    d['key'] = []
d['key'].append(item)
```

### Dictionary Iteration

```python
# ✅ Iterate over keys
for key in d:
    print(key)

# ✅ Iterate over values
for value in d.values():
    print(value)

# ✅ Iterate over items
for key, value in d.items():
    print(f"{key}: {value}")

# ❌ Don't do this
for key in d.keys():  # .keys() is unnecessary
    print(key)
```

### Dictionary Merging

```python
# ✅ Python 3.9+
merged = d1 | d2

# ✅ Python 3.5+
merged = {**d1, **d2}

# ✅ Update in place
d1.update(d2)

# ❌ Don't do this
merged = d1.copy()
for key, value in d2.items():
    merged[key] = value
```

---

## Loops and Iteration

### enumerate()

```python
# ❌ Manual counter
i = 0
for item in items:
    print(f"{i}: {item}")
    i += 1

# ✅ Use enumerate()
for i, item in enumerate(items):
    print(f"{i}: {item}")

# ✅ Start from different index
for i, item in enumerate(items, start=1):
    print(f"{i}: {item}")
```

### zip()

```python
# ❌ Manual indexing
for i in range(len(names)):
    print(f"{names[i]}: {ages[i]}")

# ✅ Use zip()
for name, age in zip(names, ages):
    print(f"{name}: {age}")

# ✅ Multiple iterables
for a, b, c in zip(list1, list2, list3):
    print(a, b, c)

# ✅ Create dictionary from two lists
d = dict(zip(keys, values))
```

### List Iteration

```python
# ❌ Index-based iteration
for i in range(len(items)):
    item = items[i]
    process(item)

# ✅ Direct iteration
for item in items:
    process(item)

# ✅ When you need index
for i, item in enumerate(items):
    print(f"Item {i}: {item}")
```

### Reverse Iteration

```python
# ✅ Use reversed()
for item in reversed(items):
    print(item)

# ❌ Don't create reversed copy
for item in items[::-1]:  # Creates new list
    print(item)
```

### Sorting

```python
# ✅ Sort by key
students = [("Alice", 90), ("Bob", 85), ("Charlie", 95)]
sorted_by_grade = sorted(students, key=lambda x: x[1])

# ✅ Multiple criteria
sorted_students = sorted(students, key=lambda x: (-x[1], x[0]))
# Sort by grade desc, then name asc

# ✅ Sort in place
items.sort()

# ✅ Sort with reverse
items.sort(reverse=True)
```

---

## Functions and Callables

### Function Arguments

```python
# ✅ Default arguments
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# ✅ Keyword arguments
def create_user(name, email, *, age=None, active=True):
    # * forces keyword-only arguments after it
    pass

create_user("Alice", "alice@example.com", age=30)

# ✅ Variable arguments
def sum_all(*args):
    return sum(args)

def process(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
```

### Lambda Functions

```python
# ✅ Simple operations
square = lambda x: x ** 2

# ✅ With sorted/filter/map
sorted_items = sorted(items, key=lambda x: x.value)
evens = list(filter(lambda x: x % 2 == 0, numbers))

# ❌ Don't use for complex logic
# Bad: lambda x: x if x > 0 else -x if x < 0 else 0

# ✅ Use named function instead
def absolute_value(x):
    if x > 0:
        return x
    elif x < 0:
        return -x
    else:
        return 0
```

### Returning Multiple Values

```python
# ✅ Return tuple
def get_coordinates():
    return x, y  # Returns tuple

# ✅ Unpack returned values
x, y = get_coordinates()

# ✅ Named tuple for clarity
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

def get_point():
    return Point(10, 20)

point = get_point()
print(point.x, point.y)
```

---

## Context Managers

### The with Statement

```python
# ❌ Manual resource management
f = open('file.txt')
try:
    content = f.read()
finally:
    f.close()

# ✅ Use with statement
with open('file.txt') as f:
    content = f.read()

# ✅ Multiple context managers
with open('input.txt') as infile, open('output.txt', 'w') as outfile:
    outfile.write(infile.read())
```

### Custom Context Managers

```python
from contextlib import contextmanager

# ✅ Create context manager
@contextmanager
def timer():
    import time
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")

with timer():
    # Code to time
    pass
```

---

## Classes and Objects

### Properties

```python
# ❌ Direct attribute access with getters/setters
class Person:
    def __init__(self):
        self._age = 0

    def get_age(self):
        return self._age

    def set_age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

# ✅ Use @property
class Person:
    def __init__(self):
        self._age = 0

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

person = Person()
person.age = 30  # Calls setter
print(person.age)  # Calls getter
```

### String Representation

```python
# ✅ Implement __repr__ and __str__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # For developers (recreatable)
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        # For end users (readable)
        return f"({self.x}, {self.y})"
```

### Comparison Methods

```python
from functools import total_ordering

# ✅ Use @total_ordering
@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        return self.grade == other.grade

    def __lt__(self, other):
        return self.grade < other.grade

# Now has __le__, __gt__, __ge__ automatically
```

---

## File Operations

### Reading Files

```python
# ✅ Read entire file
with open('file.txt') as f:
    content = f.read()

# ✅ Read lines
with open('file.txt') as f:
    lines = f.readlines()

# ✅ Iterate over lines (memory efficient)
with open('file.txt') as f:
    for line in f:
        process(line.strip())

# ✅ Read specific number of lines
with open('file.txt') as f:
    first_line = f.readline()
```

### Writing Files

```python
# ✅ Write to file
with open('output.txt', 'w') as f:
    f.write('Hello, World!\n')

# ✅ Write multiple lines
lines = ['Line 1\n', 'Line 2\n', 'Line 3\n']
with open('output.txt', 'w') as f:
    f.writelines(lines)

# ✅ Append to file
with open('log.txt', 'a') as f:
    f.write('New log entry\n')
```

### Path Operations

```python
# ✅ Use pathlib (modern)
from pathlib import Path

path = Path('data/file.txt')
if path.exists():
    content = path.read_text()

# ✅ Join paths
path = Path('data') / 'subfolder' / 'file.txt'

# ✅ Get file parts
print(path.name)      # file.txt
print(path.stem)      # file
print(path.suffix)    # .txt
print(path.parent)    # data/subfolder

# ❌ Old way (os.path)
import os
path = os.path.join('data', 'subfolder', 'file.txt')
```

---

## Error Handling

### Exception Handling

```python
# ✅ Catch specific exceptions
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except KeyError as e:
    print(f"Key error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# ✅ Use else clause
try:
    result = operation()
except ValueError:
    handle_error()
else:
    # Runs if no exception
    process_result(result)
finally:
    # Always runs
    cleanup()

# ❌ Don't catch all exceptions
try:
    operation()
except:  # Catches KeyboardInterrupt, SystemExit, etc.
    pass

# ✅ Be specific
try:
    operation()
except (ValueError, TypeError) as e:
    handle_error(e)
```

### EAFP vs LBYL

```python
# LBYL: Look Before You Leap (not Pythonic)
if key in d:
    value = d[key]
else:
    value = default

# ✅ EAFP: Easier to Ask for Forgiveness than Permission (Pythonic)
try:
    value = d[key]
except KeyError:
    value = default

# ✅ Or use get()
value = d.get(key, default)
```

### Custom Exceptions

```python
# ✅ Create custom exceptions
class ValidationError(ValueError):
    """Raised when validation fails"""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

# ✅ Use them
def validate_age(age):
    if age < 0:
        raise ValidationError(f"Age cannot be negative: {age}")
    if age > 150:
        raise ValidationError(f"Age seems unrealistic: {age}")
```

---

## Common Anti-Patterns

### Don't Use Mutable Default Arguments

```python
# ❌ WRONG - dangerous!
def append_to_list(item, lst=[]):
    lst.append(item)
    return lst

# Each call shares the same list!
print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - NOT [2]!

# ✅ CORRECT
def append_to_list(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Don't Modify List While Iterating

```python
# ❌ WRONG - skips elements
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # Modifying while iterating!

# ✅ CORRECT - create new list
items = [1, 2, 3, 4, 5]
items = [item for item in items if item % 2 != 0]

# ✅ CORRECT - iterate over copy
items = [1, 2, 3, 4, 5]
for item in items[:]:
    if item % 2 == 0:
        items.remove(item)
```

### Don't Use == for None

```python
# ❌ WRONG
if value == None:
    pass

# ✅ CORRECT - use 'is'
if value is None:
    pass

# ✅ Check for not None
if value is not None:
    pass
```

### Don't Use type() for Type Checking

```python
# ❌ WRONG - doesn't work with subclasses
if type(obj) == list:
    pass

# ✅ CORRECT - works with subclasses
if isinstance(obj, list):
    pass

# ✅ Check multiple types
if isinstance(obj, (list, tuple)):
    pass
```

### Don't Compare to True/False

```python
# ❌ WRONG
if flag == True:
    pass

if length == 0:
    pass

# ✅ CORRECT
if flag:
    pass

if not length:  # Pythonic - empty sequences are falsy
    pass
```

### Don't Reinvent the Wheel

```python
# ❌ Manual implementation
def get_unique_items(items):
    unique = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique

# ✅ Use built-in
unique_items = list(set(items))

# ✅ Or preserve order
from collections import OrderedDict
unique_items = list(OrderedDict.fromkeys(items))
```

---

## Quick Reference

### Pythonic Patterns

| Instead of                                        | Use                               |
| ------------------------------------------------- | --------------------------------- |
| `for i in range(len(items))`                      | `for item in items`               |
| `for i in range(len(items)): print(i, items[i])`  | `for i, item in enumerate(items)` |
| `if len(items) == 0`                              | `if not items`                    |
| `if x == True`                                    | `if x`                            |
| `if x == None`                                    | `if x is None`                    |
| `result = []; for x in items: result.append(x*2)` | `result = [x*2 for x in items]`   |

### Best Practices

```python
# ✅ Use comprehensions
squares = [x**2 for x in range(10)]

# ✅ Use enumerate()
for i, item in enumerate(items):
    pass

# ✅ Use zip()
for a, b in zip(list1, list2):
    pass

# ✅ Use with statement
with open('file.txt') as f:
    content = f.read()

# ✅ Use get() for dicts
value = d.get(key, default)

# ✅ Use is for None
if value is None:
    pass

# ✅ Use isinstance() for type checking
if isinstance(obj, str):
    pass
```

### Common Functions

| Function      | Purpose                    | Example                                |
| ------------- | -------------------------- | -------------------------------------- |
| `enumerate()` | Get index and value        | `for i, x in enumerate(items)`         |
| `zip()`       | Iterate multiple sequences | `for a, b in zip(list1, list2)`        |
| `sorted()`    | Return sorted copy         | `sorted(items, key=lambda x: x.value)` |
| `reversed()`  | Iterate in reverse         | `for item in reversed(items)`          |
| `any()`       | Check if any is true       | `any(x > 0 for x in numbers)`          |
| `all()`       | Check if all are true      | `all(x > 0 for x in numbers)`          |
| `map()`       | Apply function to all      | `list(map(str.upper, words))`          |
| `filter()`    | Filter by condition        | `list(filter(lambda x: x>0, nums))`    |

---

## Summary

**Key Principles:**

1. **Beautiful is better than ugly** - Write clean, readable code
2. **Explicit is better than implicit** - Be clear about intent
3. **Simple is better than complex** - Use built-in features
4. **Readability counts** - Code is read more than written
5. **There should be one obvious way** - Follow conventions

**Core Idioms:**

- Use list comprehensions for simple transformations
- Use `enumerate()` and `zip()` for iteration
- Use `with` for resource management
- Use `is None` not `== None`
- Use `isinstance()` for type checking
- Use `get()` for dictionary access
- Avoid mutable default arguments
- Follow EAFP (Easier to Ask Forgiveness than Permission)

**Remember:**

```python
import this  # Read The Zen of Python
```

🐍 Write Pythonic code that's elegant, efficient, and easy to maintain!
