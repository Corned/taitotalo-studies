# Python Late Binding Cheatsheet

## Table of Contents
- [What is Late Binding?](#what-is-late-binding)
- [The Core Problem](#the-core-problem)
- [Common Scenarios](#common-scenarios)
- [Solutions](#solutions)
- [Understanding the Mechanics](#understanding-the-mechanics)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)

---

## What is Late Binding?

**Late Binding** (lazy binding) means Python captures **variable names** in closures, not their **values**. The variable is looked up when the function **executes**, not when it's **created**.

### The Key Concept

```python
x = 1
f = lambda: x  # Captures reference to 'x', not value 1

print(f())  # 1

x = 2  # Change x
print(f())  # 2 (uses new value!)
```

**Why this happens:**
- Python uses **lexical scoping**
- Closures remember **variable names**, not values
- Lookup happens at **execution time**, not definition time

---

## The Core Problem

### Classic Loop Problem

```python
❌ # WRONG - All functions use final value
functions = []
for i in range(5):
    functions.append(lambda: i)

# Expected: 0, 1, 2, 3, 4
# Actual:
print(functions[0]())  # 4
print(functions[1]())  # 4
print(functions[2]())  # 4
print(functions[3]())  # 4
print(functions[4]())  # 4
```

**Why?** All lambdas reference the **same** variable `i`. When executed, they all see `i`'s **final value** (4).

### Visual Explanation

```
Step 1: i=0  →  lambda: i  ┐
Step 2: i=1  →  lambda: i  ├─→ All reference same 'i'
Step 3: i=2  →  lambda: i  │
Step 4: i=3  →  lambda: i  │
Step 5: i=4  →  lambda: i  ┘

When called: i = 4 (final value)
All lambdas return: 4
```

---

## Common Scenarios

### 1. Lambdas in Loops

```python
❌ # PROBLEM
funcs = [lambda x: x * i for i in range(5)]
print([f(10) for f in funcs])  # [40, 40, 40, 40, 40]

✅ # SOLUTION: Default argument
funcs = [lambda x, i=i: x * i for i in range(5)]
print([f(10) for f in funcs])  # [0, 10, 20, 30, 40]
```

### 2. Generator Expressions

```python
❌ # PROBLEM
generators = []
for i in range(3):
    generators.append((x + i for x in range(3)))

for gen in generators:
    print(list(gen))
# Output: [2,3,4], [2,3,4], [2,3,4] - all use i=2

✅ # SOLUTION: Factory function
def make_gen(i):
    return (x + i for x in range(3))

generators = [make_gen(i) for i in range(3)]
for gen in generators:
    print(list(gen))
# Output: [0,1,2], [1,2,3], [2,3,4]
```

### 3. Event Handlers / Callbacks

```python
❌ # PROBLEM
buttons = []
for i in range(5):
    buttons.append(lambda: print(f"Button {i} clicked"))

buttons[0]()  # Button 4 clicked (expected: Button 0)
buttons[2]()  # Button 4 clicked (expected: Button 2)

✅ # SOLUTION: Default argument
buttons = []
for i in range(5):
    buttons.append(lambda i=i: print(f"Button {i} clicked"))

buttons[0]()  # Button 0 clicked ✓
buttons[2]()  # Button 2 clicked ✓
```

### 4. Nested Functions

```python
❌ # PROBLEM
def create_multipliers(n):
    multipliers = []
    for i in range(1, n + 1):
        def multiply(x):
            return x * i  # References i
        multipliers.append(multiply)
    return multipliers

funcs = create_multipliers(5)
print(funcs[0](10))  # Expected: 10, Actual: 50
print(funcs[2](10))  # Expected: 30, Actual: 50

✅ # SOLUTION: Factory function
def create_multipliers(n):
    def make_multiplier(factor):
        def multiply(x):
            return x * factor
        return multiply

    return [make_multiplier(i) for i in range(1, n + 1)]

funcs = create_multipliers(5)
print(funcs[0](10))  # 10 ✓
print(funcs[2](10))  # 30 ✓
```

### 5. Class Methods

```python
❌ # PROBLEM
class Calculator:
    def setup_wrong(self):
        self.ops = {}
        for op in ['+', '-', '*', '/']:
            self.ops[op] = lambda a, b: f"{a} {op} {b}"

calc = Calculator()
calc.setup_wrong()
print(calc.ops['+'](5, 3))  # "5 / 3" (uses final op)

✅ # SOLUTION: Default argument
class Calculator:
    def setup_correct(self):
        self.ops = {}
        for op in ['+', '-', '*', '/']:
            self.ops[op] = lambda a, b, op=op: f"{a} {op} {b}"

calc = Calculator()
calc.setup_correct()
print(calc.ops['+'](5, 3))  # "5 + 3" ✓
```

### 6. Decorators

```python
❌ # PROBLEM
decorators = {}
for name in ['debug', 'info', 'warn']:
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{name}] {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    decorators[name] = decorator

@decorators['debug']
def add(a, b):
    return a + b

add(2, 3)  # [warn] add (should be [debug])

✅ # SOLUTION: Factory function
decorators = {}
for name in ['debug', 'info', 'warn']:
    def make_decorator(level):
        def decorator(func):
            def wrapper(*args, **kwargs):
                print(f"[{level}] {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    decorators[name] = make_decorator(name)

@decorators['debug']
def multiply(a, b):
    return a * b

multiply(2, 3)  # [debug] multiply ✓
```

---

## Solutions

### Solution 1: Default Arguments (Most Common) ⭐

Default arguments are evaluated at **function definition time**, capturing the current value.

```python
# Basic usage
funcs = [lambda i=i: i for i in range(5)]
print([f() for f in funcs])  # [0, 1, 2, 3, 4]

# With parameters
funcs = [lambda x, i=i: x + i for i in range(5)]
print([f(10) for f in funcs])  # [10, 11, 12, 13, 14]

# Multiple captures
funcs = [lambda a=a, b=b: a + b for a in range(3) for b in range(3)]
```

**Why it works:**
```python
def demo(i):
    f = lambda i=i: i  # i=i evaluates NOW
    return f

f = demo(5)
print(f.__defaults__)  # (5,) - value stored in function
```

### Solution 2: Factory Functions

Create a new scope that captures the value.

```python
def create_function(value):
    """Factory creates new scope"""
    return lambda: value

funcs = [create_function(i) for i in range(5)]
print([f() for f in funcs])  # [0, 1, 2, 3, 4]

# Or inline
funcs = [(lambda i: lambda: i)(i) for i in range(5)]
```

### Solution 3: functools.partial

Bind arguments early using `partial`.

```python
from functools import partial

def get_value(x):
    return x

funcs = [partial(get_value, i) for i in range(5)]
print([f() for f in funcs])  # [0, 1, 2, 3, 4]
```

### Solution 4: List Comprehension Scope (Python 3+)

List comprehensions have their own scope in Python 3.

```python
# The variable in list comprehension is local
funcs = [lambda: i for i in range(5)]
# Still has late binding issue with lambda!

# But this works
values = [i for i in range(5)]  # Each i is captured properly
```

### Solution 5: IIFE (Immediately Invoked Function Expression)

```python
funcs = [(lambda i: lambda: i)(i) for i in range(5)]
#        └─────┬─────┘└──┬──┘ └┬┘
#         outer func   inner  call outer immediately
```

---

## Understanding the Mechanics

### What Gets Captured?

```python
def demonstrate():
    x = 10

    # Captures reference to name 'x'
    f = lambda: x

    # See what variables the closure references
    print(f.__code__.co_freevars)  # ('x',)
    print(f.__closure__)  # (<cell at 0x...: int object at 0x...>,)

    # Access the actual value
    print(f.__closure__[0].cell_contents)  # 10

    x = 20  # Change x
    print(f())  # 20 (looks up current value)

demonstrate()
```

### Default Arguments vs Closures

```python
x = 1

# Closure - late binding
f1 = lambda: x
# Default argument - early binding
f2 = lambda x=x: x

print(f1.__closure__)    # (<cell ...>,) - references x
print(f2.__closure__)    # None - no closure
print(f2.__defaults__)   # (1,) - value stored

x = 2
print(f1())  # 2 (looks up x)
print(f2())  # 1 (uses stored value)
```

### When Evaluation Happens

```python
def show_timing():
    print("Creating functions...")

    # Default argument evaluated NOW
    funcs = [lambda i=i: (print(f"Using {i}"), i)[1]
             for i in range(3)]

    print("Calling functions...")
    for f in funcs:
        f()

show_timing()
# Output:
# Creating functions...
# Calling functions...
# Using 0
# Using 1
# Using 2
```

---

## Real-World Examples

### 1. Web Routes / URL Handlers

```python
from flask import Flask
app = Flask(__name__)

❌ # WRONG
routes = ['/', '/about', '/contact']
for route in routes:
    @app.route(route)
    def handler():
        return f"Page: {route}"  # All use final route!

✅ # CORRECT
def create_handler(route_name):
    def handler():
        return f"Page: {route_name}"
    return handler

for route in ['/', '/about', '/contact']:
    app.route(route)(create_handler(route))
```

### 2. Threading / Async Tasks

```python
import threading

❌ # WRONG
threads = []
for i in range(5):
    t = threading.Thread(target=lambda: print(f"Thread {i}"))
    threads.append(t)
    t.start()
# Output: Thread 4, Thread 4, Thread 4... (unpredictable)

✅ # CORRECT
threads = []
for i in range(5):
    t = threading.Thread(target=lambda i=i: print(f"Thread {i}"))
    threads.append(t)
    t.start()
# Output: Thread 0, Thread 1, Thread 2, Thread 3, Thread 4
```

### 3. Dynamic Method Creation

```python
class DynamicMethods:
    ❌ # WRONG
    def add_methods_wrong(self, names):
        for name in names:
            setattr(self, name, lambda self: f"Method {name}")

    ✅ # CORRECT
    def add_methods_correct(self, names):
        for name in names:
            # Use factory
            def make_method(method_name):
                return lambda self: f"Method {method_name}"
            setattr(self, name, make_method(name))

obj = DynamicMethods()
obj.add_methods_correct(['foo', 'bar', 'baz'])
print(obj.foo(obj))  # Method foo ✓
```

### 4. Command Pattern

```python
class CommandManager:
    def __init__(self):
        self.commands = {}

    ❌ # WRONG
    def register_commands_wrong(self, operations):
        for op, func in operations:
            self.commands[op] = lambda x: func(x, op)

    ✅ # CORRECT
    def register_commands_correct(self, operations):
        for op, func in operations:
            # Capture both func and op
            self.commands[op] = lambda x, f=func, o=op: f(x, o)

# Usage
manager = CommandManager()
ops = [
    ('add', lambda x, op: f"{x} + {op}"),
    ('sub', lambda x, op: f"{x} - {op}"),
]
manager.register_commands_correct(ops)
```

### 5. Memoization with Closures

```python
❌ # WRONG
def create_memoizers():
    cache = {}
    memoizers = []

    for key in ['func1', 'func2', 'func3']:
        def memoize(n):
            if key not in cache:  # 'key' references loop variable!
                cache[key] = expensive_computation(n)
            return cache[key]
        memoizers.append(memoize)

    return memoizers

✅ # CORRECT
def create_memoizers():
    memoizers = []

    for key in ['func1', 'func2', 'func3']:
        def make_memoizer(cache_key):
            cache = {}
            def memoize(n):
                if cache_key not in cache:
                    cache[cache_key] = expensive_computation(n)
                return cache[cache_key]
            return memoize
        memoizers.append(make_memoizer(key))

    return memoizers
```

---

## Best Practices

### ✅ DO

```python
# 1. Use default arguments for simple cases
funcs = [lambda i=i: i for i in range(5)]

# 2. Use factory functions for complex cases
def make_handler(value):
    def handler():
        return value
    return handler

# 3. Use functools.partial when appropriate
from functools import partial
funcs = [partial(func, i) for i in range(5)]

# 4. Document late binding risks in code
def create_callbacks(items):
    """
    Create callbacks for items.
    Note: Uses default argument to avoid late binding.
    """
    return [lambda item=item: process(item) for item in items]

# 5. Use list comprehensions when possible
# The iteration variable is properly scoped in Python 3
values = [func(i) for i in range(5)]
```

### ❌ DON'T

```python
# 1. Don't reference loop variables in closures without capturing
for i in range(5):
    funcs.append(lambda: i)  # BAD

# 2. Don't assume closures capture values
x = 1
f = lambda: x  # Captures reference, not value!

# 3. Don't forget to capture in nested loops
for i in range(3):
    for j in range(3):
        funcs.append(lambda: i + j)  # Both i and j need capturing!

# 4. Don't mix late and early binding without understanding
for i in range(5):
    # This captures i but not x from outer scope
    funcs.append(lambda i=i: i + x)
```

---

## Quick Reference

### Problem Detection

**Signs you have a late binding issue:**
- ✋ Functions created in loops all return the same value
- ✋ All callbacks use the last iteration value
- ✋ Variables in closures have unexpected values
- ✋ Generator expressions reference loop variables

### Solution Cheat Sheet

| Scenario | Solution | Example |
|----------|----------|---------|
| Simple lambda in loop | Default argument | `lambda i=i: i` |
| Complex function in loop | Factory function | `def make(i): return lambda: i` |
| Existing function | `functools.partial` | `partial(func, i)` |
| Generator expression | Factory or immediate use | `def make(i): return (x+i for x in range(3))` |
| Multiple variables | Capture all with defaults | `lambda i=i, j=j: i+j` |
| Class methods | Factory method | `setattr(self, name, make_method(name))` |

### Quick Fixes

```python
# Lambda in loop
❌ [lambda: i for i in range(5)]
✅ [lambda i=i: i for i in range(5)]

# Nested function
❌ def make():
     def inner(): return i
     return inner
✅ def make(i):
     def inner(): return i
     return inner

# Generator expression
❌ (x + i for x in range(3))  # in loop
✅ (x + i for x in range(3) for i in [i])  # capture i

# Two variables
❌ lambda: i + j
✅ lambda i=i, j=j: i + j
```

---

## Summary

**Key Takeaways:**

1. **Late binding = variables looked up at execution time, not definition time**
2. **Closures capture variable names, not values**
3. **Default arguments capture values immediately**
4. **Most common solution: `lambda i=i: ...`**
5. **Factory functions create new scopes**

**Remember:**
```python
# This captures reference to 'x'
f = lambda: x

# This captures value of x
f = lambda x=x: x

# When in doubt, use default arguments!
```

**The Rule:**
> If you create functions in a loop that reference loop variables, use default arguments or factory functions to capture the current value.

🎯 Master late binding to avoid subtle bugs in Python!
