# Python Decorators Cheatsheet

## Table of Contents
- [What are Decorators?](#what-are-decorators)
- [Basic Function Decorators](#basic-function-decorators)
- [Decorators with Arguments](#decorators-with-arguments)
- [Class Decorators](#class-decorators)
- [Built-in Decorators](#built-in-decorators)
- [functools.wraps](#functoolswraps)
- [Practical Examples](#practical-examples)
- [Advanced Patterns](#advanced-patterns)
- [Common Use Cases](#common-use-cases)
- [Best Practices](#best-practices)

---

## What are Decorators?

Decorators are a **design pattern** that allows you to modify or extend the behavior of functions/classes without permanently modifying them.

**Key Concept:** Decorators are functions that take a function as input and return a modified function.

```python
# Decorator syntax sugar
@decorator
def function():
    pass

# Is equivalent to:
def function():
    pass
function = decorator(function)
```

**Why use decorators?**
- 🔄 Code reuse (DRY principle)
- 🎯 Separation of concerns
- 📝 Clean, readable code
- 🔧 Modify behavior without changing source
- 🏭 Factory pattern for functions

---

## Basic Function Decorators

### Simple Decorator

```python
def my_decorator(func):
    """Basic decorator template"""
    def wrapper(*args, **kwargs):
        # Do something before
        print(f"Calling {func.__name__}")

        result = func(*args, **kwargs)

        # Do something after
        print(f"Finished {func.__name__}")
        return result

    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Calling greet
# Hello, Alice!
# Finished greet
```

### Decorator Without Arguments

```python
def timer(func):
    """Measure execution time"""
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"

slow_function()  # slow_function took 1.0001 seconds
```

### Multiple Decorators (Stacking)

```python
def decorator1(func):
    def wrapper(*args, **kwargs):
        print("Decorator 1 - Before")
        result = func(*args, **kwargs)
        print("Decorator 1 - After")
        return result
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("Decorator 2 - Before")
        result = func(*args, **kwargs)
        print("Decorator 2 - After")
        return result
    return wrapper

@decorator1
@decorator2
def my_function():
    print("Function executed")

my_function()
# Output:
# Decorator 1 - Before
# Decorator 2 - Before
# Function executed
# Decorator 2 - After
# Decorator 1 - After
```

**Order matters!** Decorators are applied **bottom-to-top**:
```python
@decorator1
@decorator2
def func():
    pass

# Equivalent to:
func = decorator1(decorator2(func))
```

---

## Decorators with Arguments

### Decorator Factory Pattern

To create decorators that accept arguments, you need **three levels** of functions:

```python
def repeat(times):
    """Decorator factory - returns decorator"""
    def decorator(func):
        """Decorator - returns wrapper"""
        def wrapper(*args, **kwargs):
            """Wrapper - calls original function"""
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Bob")
# Output:
# Hello, Bob!
# Hello, Bob!
# Hello, Bob!
```

### Optional Arguments Decorator

```python
def smart_decorator(arg=None):
    """Decorator that works with or without arguments"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Argument: {arg}")
            return func(*args, **kwargs)
        return wrapper

    # If called without arguments: @smart_decorator
    if callable(arg):
        return decorator(arg)

    # If called with arguments: @smart_decorator(value)
    return decorator

# Without arguments
@smart_decorator
def func1():
    print("func1")

# With arguments
@smart_decorator(arg="custom")
def func2():
    print("func2")

func1()  # Argument: None
func2()  # Argument: custom
```

### Parameterized Decorator Examples

```python
def log_to(file):
    """Log function calls to file"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with open(file, 'a') as f:
                f.write(f"Called {func.__name__} with {args}, {kwargs}\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_to('app.log')
def process_data(data):
    return data.upper()

# ---

def retry(max_attempts, delay=1):
    """Retry function on failure"""
    import time

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unstable_api_call():
    import random
    if random.random() < 0.7:
        raise Exception("API Error")
    return "Success"
```

---

## Class Decorators

### Decorating Classes

```python
def add_methods(cls):
    """Add methods to a class"""
    cls.greet = lambda self: f"Hello from {self.name}"
    return cls

@add_methods
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Alice")
print(p.greet())  # Hello from Alice
```

### Class as Decorator

```python
class CountCalls:
    """Decorator class to count function calls"""
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # Call #1 of say_hello
say_hello()  # Call #2 of say_hello
say_hello()  # Call #3 of say_hello
```

### Decorator for Class Methods

```python
def method_decorator(method):
    """Decorator for class methods"""
    def wrapper(self, *args, **kwargs):
        print(f"Calling {method.__name__} on {self.__class__.__name__}")
        return method(self, *args, **kwargs)
    return wrapper

class MyClass:
    @method_decorator
    def my_method(self):
        print("Method executed")

obj = MyClass()
obj.my_method()
# Output:
# Calling my_method on MyClass
# Method executed
```

---

## Built-in Decorators

### @property

Convert a method into a read-only attribute.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """Get radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set radius with validation"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @radius.deleter
    def radius(self):
        """Delete radius"""
        del self._radius

    @property
    def area(self):
        """Computed property (read-only)"""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.radius)      # 5 (calls getter)
print(c.area)        # 78.54 (computed)

c.radius = 10        # calls setter
# c.area = 100       # AttributeError: can't set attribute

del c.radius         # calls deleter
```

### @staticmethod

Method that doesn't receive implicit first argument (no `self` or `cls`).

```python
class MathOperations:
    @staticmethod
    def add(a, b):
        """Can be called without instance"""
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

# Call without instance
print(MathOperations.add(5, 3))      # 8
print(MathOperations.multiply(4, 2)) # 8

# Can also call with instance (but not common)
math = MathOperations()
print(math.add(1, 2))  # 3
```

### @classmethod

Method that receives the class as implicit first argument.

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_string):
        """Alternative constructor"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        """Factory method"""
        import datetime
        today = datetime.date.today()
        return cls(today.year, today.month, today.day)

    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

# Regular constructor
d1 = Date(2024, 1, 15)

# Alternative constructor
d2 = Date.from_string("2024-01-15")

# Factory method
d3 = Date.today()

print(d1)  # 2024-01-15
```

### @abstractmethod

Define abstract methods (requires ABC).

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        """Must be implemented by subclasses"""
        pass

    @abstractmethod
    def move(self):
        """Must be implemented by subclasses"""
        pass

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

    def move(self):
        return "Running"

# animal = Animal()  # TypeError: Can't instantiate abstract class
dog = Dog()  # OK
print(dog.make_sound())  # Woof!
```

---

## functools.wraps

**Problem:** Decorators lose original function metadata.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone"""
    print(f"Hello, {name}")

print(greet.__name__)  # wrapper (WRONG!)
print(greet.__doc__)   # Wrapper docstring (WRONG!)
```

**Solution:** Use `functools.wraps`

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
    print(f"Hello, {name}")

print(greet.__name__)  # greet (CORRECT!)
print(greet.__doc__)   # Greet someone (CORRECT!)
print(greet.__wrapped__)  # Access original function
```

**Always use @wraps in production decorators!**

---

## Practical Examples

### 1. Debugging Decorator

```python
from functools import wraps

def debug(func):
    """Print function signature and return value"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")

        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@debug
def add(a, b):
    return a + b

add(3, 5)
# Output:
# Calling add(3, 5)
# add returned 8
```

### 2. Memoization (Caching)

```python
from functools import wraps

def memoize(func):
    """Cache function results"""
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            print(f"Computed {func.__name__}{args}")
        else:
            print(f"Cached {func.__name__}{args}")
        return cache[args]

    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(5))
# Much faster than without memoization!

# Better: Use functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

### 3. Authorization/Authentication

```python
from functools import wraps

def require_auth(func):
    """Check if user is authenticated"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get('user')
        if not user or not user.get('authenticated'):
            raise PermissionError("Authentication required")
        return func(*args, **kwargs)
    return wrapper

def require_role(role):
    """Check if user has required role"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if not user or user.get('role') != role:
                raise PermissionError(f"Role '{role}' required")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_auth
def view_profile(user=None):
    return f"Profile of {user['name']}"

@require_role('admin')
def delete_user(user_id, user=None):
    return f"Deleted user {user_id}"

# Usage
admin_user = {'name': 'Alice', 'authenticated': True, 'role': 'admin'}
regular_user = {'name': 'Bob', 'authenticated': True, 'role': 'user'}

print(view_profile(user=admin_user))  # OK
# delete_user(123, user=regular_user)  # PermissionError
```

### 4. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(max_calls, time_window):
    """Limit function calls within time window"""
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside time window
            calls[:] = [c for c in calls if c > now - time_window]

            if len(calls) >= max_calls:
                raise Exception(f"Rate limit exceeded: {max_calls} calls per {time_window}s")

            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=3, time_window=10)
def api_call():
    print("API called")
    return "Data"

# Can call 3 times, then must wait
for i in range(5):
    try:
        api_call()
    except Exception as e:
        print(e)
```

### 5. Validation Decorator

```python
from functools import wraps

def validate_types(**type_kwargs):
    """Validate function argument types"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)

            # Check types
            for name, expected_type in type_kwargs.items():
                if name in bound_args.arguments:
                    value = bound_args.arguments[name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{name} must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )

            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_user(name, age):
    return f"User {name}, age {age}"

create_user("Alice", 30)  # OK
# create_user("Bob", "30")  # TypeError: age must be int, got str
```

### 6. Context Manager Decorator

```python
from functools import wraps

def suppress_errors(func):
    """Suppress exceptions and log them"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None
    return wrapper

@suppress_errors
def risky_operation():
    return 1 / 0

result = risky_operation()  # Prints error, returns None
print(f"Result: {result}")
```

---

## Advanced Patterns

### 1. Decorator with Optional Arguments

```python
from functools import wraps

def repeat(times=2):
    """Flexible decorator with optional arguments"""
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper

    # Handle both @repeat and @repeat()
    if callable(times):
        func = times
        times = 2
        return decorator_repeat(func)

    return decorator_repeat

@repeat
def greet1():
    print("Hello!")

@repeat()
def greet2():
    print("Hi!")

@repeat(times=3)
def greet3():
    print("Hey!")

greet1()  # Prints Hello! twice
greet2()  # Prints Hi! twice
greet3()  # Prints Hey! three times
```

### 2. Chainable Decorators

```python
class DecoratorsChain:
    """Chainable decorator class"""
    def __init__(self, func):
        self.func = func
        self.middlewares = []

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)
        return self

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        for middleware in self.middlewares:
            result = middleware(result)
        return result

def uppercase(text):
    return text.upper()

def exclaim(text):
    return f"{text}!"

@DecoratorsChain
def greet(name):
    return f"Hello, {name}"

# Chain decorators
greet.add_middleware(uppercase).add_middleware(exclaim)
print(greet("alice"))  # HELLO, ALICE!
```

### 3. Context-Aware Decorators

```python
import contextvars
from functools import wraps

# Context variable
request_id = contextvars.ContextVar('request_id', default=None)

def with_request_id(func):
    """Add request ID to logs"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        req_id = request_id.get()
        print(f"[Request {req_id}] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[Request {req_id}] Finished {func.__name__}")
        return result
    return wrapper

@with_request_id
def process_request():
    print("Processing...")

# Set context
request_id.set("ABC-123")
process_request()
# Output:
# [Request ABC-123] Calling process_request
# Processing...
# [Request ABC-123] Finished process_request
```

### 4. Decorator Registry Pattern

```python
# Plugin system using decorators
_registry = {}

def register(name):
    """Register function in global registry"""
    def decorator(func):
        _registry[name] = func
        return func
    return decorator

@register('add')
def add(a, b):
    return a + b

@register('multiply')
def multiply(a, b):
    return a * b

# Use registered functions
print(_registry['add'](5, 3))       # 8
print(_registry['multiply'](4, 2))  # 8

# Useful for plugin systems, command handlers, etc.
```

---

## Common Use Cases

### Web Framework Decorators

```python
# Flask-style routing
routes = {}

def route(path):
    """Register route handler"""
    def decorator(func):
        routes[path] = func
        return func
    return decorator

@route('/')
def home():
    return "Home Page"

@route('/about')
def about():
    return "About Page"

# Simulate request
def handle_request(path):
    handler = routes.get(path)
    if handler:
        return handler()
    return "404 Not Found"

print(handle_request('/'))      # Home Page
print(handle_request('/about')) # About Page
```

### Testing Decorators

```python
from functools import wraps
import time

def test_performance(threshold):
    """Test if function executes within threshold"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start

            if duration > threshold:
                print(f"⚠️  {func.__name__} took {duration:.4f}s (> {threshold}s)")
            else:
                print(f"✓ {func.__name__} passed ({duration:.4f}s)")

            return result
        return wrapper
    return decorator

@test_performance(threshold=0.1)
def fast_function():
    time.sleep(0.05)

@test_performance(threshold=0.1)
def slow_function():
    time.sleep(0.2)

fast_function()  # ✓ fast_function passed (0.0501s)
slow_function()  # ⚠️ slow_function took 0.2001s (> 0.1s)
```

### Async Decorators

```python
import asyncio
from functools import wraps

def async_timer(func):
    """Time async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.4f}s")
        return result
    return wrapper

@async_timer
async def fetch_data():
    await asyncio.sleep(1)
    return "Data"

# asyncio.run(fetch_data())  # fetch_data took 1.0001s
```

---

## Best Practices

### ✅ DO

```python
# 1. Always use @wraps
from functools import wraps

def my_decorator(func):
    @wraps(func)  # ✓
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# 2. Accept *args, **kwargs for flexibility
def flexible_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):  # ✓ Handles any signature
        return func(*args, **kwargs)
    return wrapper

# 3. Document your decorators
def logged(func):
    """
    Decorator that logs function calls.

    Example:
        @logged
        def my_func():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # ...
        return func(*args, **kwargs)
    return wrapper

# 4. Keep decorators simple and focused
def single_responsibility(func):
    """Do one thing well"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Single, clear purpose
        return func(*args, **kwargs)
    return wrapper

# 5. Make decorators composable
@decorator1
@decorator2
@decorator3
def my_function():
    pass
```

### ❌ DON'T

```python
# 1. Don't forget @wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):  # ✗ Loses metadata
        return func(*args, **kwargs)
    return wrapper

# 2. Don't modify arguments unexpectedly
def surprising_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = tuple(str(a) for a in args)  # ✗ Surprising!
        return func(*args, **kwargs)
    return wrapper

# 3. Don't create side effects without clear documentation
def hidden_side_effects(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # ✗ Writes to file without clear indication
        with open('secret.log', 'a') as f:
            f.write('Something')
        return func(*args, **kwargs)
    return wrapper

# 4. Don't make decorators too complex
def overly_complex(func):
    # ✗ Too much logic, hard to understand
    # ... 100 lines of code ...
    pass

# 5. Don't ignore return values
def bad_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        # ✗ Doesn't return result!
    return wrapper
```

---

## Quick Reference

### Decorator Templates

```python
# Basic decorator
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper

# Decorator with arguments
def decorator(arg):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # use arg
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator

# Class decorator
class Decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # before
        result = self.func(*args, **kwargs)
        # after
        return result

# Decorator for methods
def method_decorator(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # before
        result = method(self, *args, **kwargs)
        # after
        return result
    return wrapper
```

### Common Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Timing | Measure execution time | `@timer` |
| Logging | Log function calls | `@log` |
| Caching | Memoize results | `@lru_cache` |
| Validation | Check inputs | `@validate` |
| Authorization | Check permissions | `@require_auth` |
| Retry | Retry on failure | `@retry(3)` |
| Rate limiting | Throttle calls | `@rate_limit` |
| Deprecation | Mark as deprecated | `@deprecated` |

---

## Summary

**Key Takeaways:**

1. **Decorators modify functions without changing their source code**
2. **Use `@wraps` to preserve function metadata**
3. **Pattern:** `function -> decorator -> wrapper -> modified function`
4. **Three levels for arguments:** factory -> decorator -> wrapper
5. **Common uses:** logging, timing, caching, validation, authorization

**Basic Structure:**
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Your code here
        result = func(*args, **kwargs)
        return result
    return wrapper
```

**With Arguments:**
```python
def my_decorator(param):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use param
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

🎨 Master decorators to write clean, reusable, and elegant Python code!
