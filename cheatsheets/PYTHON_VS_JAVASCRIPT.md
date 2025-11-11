# Python vs JavaScript: Core Comparison Guide

A quick reference guide for JavaScript developers learning Python.

## Table of Contents

- [Checking Conditions](#checking-conditions)
- [Quick Reference Table](#quick-reference-table)
- [Practical Examples](#practical-examples)
- [Chaining Operations](#chaining-operations)
- [Performance Notes](#performance-notes)

---

## Checking Conditions

### JavaScript `.every()` → Python `all()`

Check if **ALL** elements meet a condition:

```javascript
// JavaScript
const numbers = [2, 4, 6, 8, 10];
numbers.every((n) => n % 2 === 0); // true
```

```python
# Python
numbers = [2, 4, 6, 8, 10]
all(n % 2 == 0 for n in numbers)  # True
```

### JavaScript `.some()` → Python `any()`

Check if **ANY** element meets a condition:

```javascript
// JavaScript
const numbers = [2, 4, 6, 8, 10];
numbers.some((n) => n > 5); // true
```

```python
# Python
numbers = [2, 4, 6, 8, 10]
any(n > 5 for n in numbers)  # True
```

---

## Quick Reference Table

| JavaScript     | Python                           | Example                                              |
| -------------- | -------------------------------- | ---------------------------------------------------- |
| `.every()`     | `all()`                          | `all(x > 0 for x in nums)`                           |
| `.some()`      | `any()`                          | `any(x > 10 for x in nums)`                          |
| `.map()`       | `map()` or list comprehension    | `[x * 2 for x in nums]`                              |
| `.filter()`    | `filter()` or list comprehension | `[x for x in nums if x > 5]`                         |
| `.reduce()`    | `reduce()` or built-ins          | `sum(nums)`, `min(nums)`, `max(nums)`                |
| `.find()`      | `next()` with generator          | `next((x for x in nums if x > 5), None)`             |
| `.findIndex()` | `next()` with `enumerate()`      | `next((i for i, x in enumerate(nums) if x > 5), -1)` |
| `.includes()`  | `in` operator                    | `5 in nums`                                          |
| `.length`      | `len()`                          | `len(nums)`                                          |
| `.forEach()`   | `for` loop                       | `for x in nums: ...`                                 |
| `.slice()`     | slice notation                   | `nums[start:end]`                                    |
| `.concat()`    | `+` operator                     | `list1 + list2`                                      |
| `.join()`      | `str.join()`                     | `', '.join(strings)`                                 |
| `.indexOf()`   | `list.index()`                   | `nums.index(5)`                                      |
| `.push()`      | `list.append()`                  | `nums.append(5)`                                     |
| `.pop()`       | `list.pop()`                     | `nums.pop()`                                         |

---

## Practical Examples

### Example 1: Validating a Sequence

```javascript
// JavaScript
const diffs = [-1, -2, -2, -1];

// Check if ALL are negative
diffs.every((d) => d < 0); // true

// Check if ANY are zero
diffs.some((d) => d === 0); // false

// Check if ALL are in valid range
diffs.every((d) => Math.abs(d) >= 1 && Math.abs(d) <= 3); // true
```

```python
# Python
diffs = [-1, -2, -2, -1]

# Check if ALL are negative
all(d < 0 for d in diffs)  # True

# Check if ANY are zero
any(d == 0 for d in diffs)  # False

# Check if ALL are in valid range
all(1 <= abs(d) <= 3 for d in diffs)  # True
```

### Example 2: Counting and Transforming

```javascript
// JavaScript
const numbers = [1, 2, 3, 4, 5];

// Count matching elements
numbers.filter((n) => n > 3).length; // 2

// Transform and sum
numbers.map((n) => n * n).reduce((a, b) => a + b, 0); // 55
```

```python
# Python
numbers = [1, 2, 3, 4, 5]

# Count matching elements
sum(1 for n in numbers if n > 3)  # 2

# Transform and sum
sum(n * n for n in numbers)  # 55
```

### Example 3: Finding Elements

```javascript
// JavaScript
const data = [10, 20, 30, 40, 50];

// Find first element > 25
data.find((x) => x > 25); // 30

// Find index of first element > 25
data.findIndex((x) => x > 25); // 2

// Check if contains 30
data.includes(30); // true
```

```python
# Python
data = [10, 20, 30, 40, 50]

# Find first element > 25
next((x for x in data if x > 25), None)  # 30

# Find index of first element > 25
next((i for i, x in enumerate(data) if x > 25), -1)  # 2

# Check if contains 30
30 in data  # True
```

---

## Chaining Operations

### JavaScript Style

```javascript
// JavaScript
const data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

data.filter((x) => x % 2 === 0)
    .map((x) => x * x)
    .reduce((a, b) => a + b, 0); // 220
```

### Python Style

```python
# Python - Using generator expressions (memory efficient)
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

sum(x * x for x in data if x % 2 == 0)  # 220

# Or step by step
evens = [x for x in data if x % 2 == 0]     # [2, 4, 6, 8, 10]
squares = [x * x for x in evens]             # [4, 16, 36, 64, 100]
total = sum(squares)                         # 220
```

---

## Performance Notes

### 🚀 Short-Circuiting

Both `all()` and `any()` **short-circuit**, meaning they stop evaluating as soon as the result is determined:

```python
# Stops at first False
all(expensive_check(x) for x in huge_list)

# Stops at first True
any(expensive_check(x) for x in huge_list)
```

### 💾 Memory Efficiency

**Generator expressions** (round brackets) are lazy and memory-efficient:

```python
# Uses minimal memory - processes one element at a time
sum(x * 2 for x in huge_list)

# Creates full list in memory first
sum([x * 2 for x in huge_list])
```

### ⚡ Use Built-ins When Possible

Built-in functions are optimized in C and much faster than custom implementations:

```python
# Fast ✅
sum(numbers)
min(numbers)
max(numbers)
len(numbers)

# Slower ❌
from functools import reduce
from operator import add
reduce(add, numbers)  # Equivalent to sum() but slower
```

---

## Key Takeaways

1. **`all()` = `.every()`** - Check if all elements match
2. **`any()` = `.some()`** - Check if any element matches
3. **List comprehensions** are the Pythonic way to transform/filter data
4. **Generator expressions** (with `all()`, `any()`, `sum()`) are memory-efficient
5. **Built-in functions** are your friend - they're fast and readable
6. **Both `all()` and `any()` short-circuit** for better performance

---

## Additional Resources

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Python Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python itertools Module](https://docs.python.org/3/library/itertools.html)

---

_Happy coding! 🐍_
