# Python Context Managers Cheatsheet

## Table of Contents
- [What are Context Managers?](#what-are-context-managers)
- [The with Statement](#the-with-statement)
- [Creating Context Managers with Classes](#creating-context-managers-with-classes)
- [Creating Context Managers with contextlib](#creating-context-managers-with-contextlib)
- [Multiple Context Managers](#multiple-context-managers)
- [Nested Context Managers](#nested-context-managers)
- [Exception Handling](#exception-handling)
- [Common Use Cases](#common-use-cases)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)

---

## What are Context Managers?

Context managers are objects that define **setup** and **teardown** actions to be executed when entering and exiting a runtime context.

**Key Benefits:**
- 🔒 Automatic resource management
- 🧹 Guaranteed cleanup (even with exceptions)
- 📝 Cleaner, more readable code
- 🛡️ Prevention of resource leaks

**The Protocol:**
```python
# Context manager protocol
class ContextManager:
    def __enter__(self):
        # Setup code
        return resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup code
        return False  # Don't suppress exceptions
```

---

## The with Statement

### Basic Syntax

```python
# Without context manager
file = open('data.txt', 'r')
try:
    content = file.read()
finally:
    file.close()  # Must remember to close!

# With context manager ✓
with open('data.txt', 'r') as file:
    content = file.read()
# File automatically closed, even if exception occurs
```

### How it Works

```python
# This code:
with expression as variable:
    # Body
    pass

# Is equivalent to:
manager = expression
variable = manager.__enter__()
try:
    # Body
    pass
finally:
    manager.__exit__(exc_type, exc_val, exc_tb)
```

### Multiple Resources

```python
# Multiple files
with open('input.txt') as infile, open('output.txt', 'w') as outfile:
    content = infile.read()
    outfile.write(content.upper())
# Both files automatically closed
```

---

## Creating Context Managers with Classes

### Basic Class-Based Context Manager

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """Called when entering 'with' block"""
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block"""
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions

# Usage
with FileManager('test.txt', 'w') as f:
    f.write('Hello, World!')
# Output:
# Opening test.txt
# Closing test.txt
```

### Returning Values

```python
class Timer:
    def __enter__(self):
        """Return self to access attributes"""
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end = time.time()
        self.duration = self.end - self.start
        print(f"Elapsed time: {self.duration:.4f}s")
        return False

# Access timer object
with Timer() as timer:
    # Do some work
    import time
    time.sleep(1)
# Elapsed time: 1.0001s

print(f"Duration was: {timer.duration:.4f}s")
```

### Database Connection Manager

```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    def __enter__(self):
        print("Connecting to database...")
        self.connection = self._connect(self.connection_string)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()
        return False

    def _connect(self, conn_str):
        # Simulated connection
        return {'connected': True, 'conn_str': conn_str}

# Usage
with DatabaseConnection('localhost:5432') as conn:
    # Execute queries
    print("Executing queries...")
# Connection automatically committed and closed
```

---

## Creating Context Managers with contextlib

### @contextmanager Decorator

```python
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    """Simple file manager using generator"""
    print(f"Opening {filename}")
    file = open(filename, mode)
    try:
        yield file  # Value returned to 'as' variable
    finally:
        print(f"Closing {filename}")
        file.close()

# Usage
with file_manager('test.txt', 'w') as f:
    f.write('Hello!')
```

### How @contextmanager Works

```python
from contextlib import contextmanager

@contextmanager
def my_context():
    # Setup (before yield)
    print("Entering context")
    resource = "Resource"

    yield resource  # __enter__ returns this

    # Teardown (after yield)
    print("Exiting context")

# Equivalent to:
with my_context() as res:
    print(f"Using {res}")
# Output:
# Entering context
# Using Resource
# Exiting context
```

### Timer with @contextmanager

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name):
    """Measure execution time"""
    start = time.time()
    print(f"[{name}] Starting...")

    yield

    duration = time.time() - start
    print(f"[{name}] Finished in {duration:.4f}s")

# Usage
with timer("Database Query"):
    time.sleep(1)
    # Do work
# [Database Query] Starting...
# [Database Query] Finished in 1.0001s
```

### Temporary Directory

```python
from contextlib import contextmanager
import tempfile
import shutil
import os

@contextmanager
def temporary_directory():
    """Create and cleanup temporary directory"""
    temp_dir = tempfile.mkdtemp()
    print(f"Created temp dir: {temp_dir}")

    try:
        yield temp_dir
    finally:
        print(f"Removing temp dir: {temp_dir}")
        shutil.rmtree(temp_dir)

# Usage
with temporary_directory() as tmpdir:
    # Create files in temp directory
    filepath = os.path.join(tmpdir, 'test.txt')
    with open(filepath, 'w') as f:
        f.write('Temporary data')
# Directory automatically deleted
```

---

## Multiple Context Managers

### Sequential Context Managers

```python
# Method 1: Nested with statements
with open('input.txt') as infile:
    with open('output.txt', 'w') as outfile:
        outfile.write(infile.read())

# Method 2: Single with statement (Python 2.7+)
with open('input.txt') as infile, open('output.txt', 'w') as outfile:
    outfile.write(infile.read())
```

### ExitStack for Dynamic Context Managers

```python
from contextlib import ExitStack

# Dynamic number of files
def process_files(filenames):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f)) for f in filenames]

        # All files are open here
        for file in files:
            print(file.read())

        # All files automatically closed on exit

# Usage
process_files(['file1.txt', 'file2.txt', 'file3.txt'])
```

### Conditional Context Managers

```python
from contextlib import ExitStack, nullcontext

def process_data(data, use_transaction=True):
    # Conditionally use transaction
    context = begin_transaction() if use_transaction else nullcontext()

    with context:
        # Process data
        save_data(data)

# Or with ExitStack
def process_with_optional_lock(data, use_lock=True):
    with ExitStack() as stack:
        if use_lock:
            stack.enter_context(acquire_lock())

        # Process data
        process(data)
```

---

## Nested Context Managers

### Manual Nesting

```python
from contextlib import contextmanager
import time

@contextmanager
def operation(name, level=0):
    indent = "  " * level
    print(f"{indent}Starting {name}")
    start = time.time()

    yield

    duration = time.time() - start
    print(f"{indent}Finished {name} ({duration:.4f}s)")

# Nested operations
with operation("Outer", 0):
    time.sleep(0.5)

    with operation("Inner 1", 1):
        time.sleep(0.2)

    with operation("Inner 2", 1):
        time.sleep(0.3)

# Output:
# Starting Outer
#   Starting Inner 1
#   Finished Inner 1 (0.2001s)
#   Starting Inner 2
#   Finished Inner 2 (0.3001s)
# Finished Outer (1.0002s)
```

### Nested Resource Management

```python
from contextlib import contextmanager

@contextmanager
def database_transaction(db):
    """Database transaction context"""
    print("BEGIN TRANSACTION")
    try:
        yield db
        print("COMMIT")
    except Exception as e:
        print(f"ROLLBACK due to {e}")
        raise

@contextmanager
def database_savepoint(db, name):
    """Savepoint within transaction"""
    print(f"  SAVEPOINT {name}")
    try:
        yield db
        print(f"  RELEASE SAVEPOINT {name}")
    except Exception as e:
        print(f"  ROLLBACK TO SAVEPOINT {name}")
        raise

# Usage
class DB:
    pass

db = DB()

with database_transaction(db):
    # Do some work

    with database_savepoint(db, "SP1"):
        # More work
        pass

    with database_savepoint(db, "SP2"):
        # Even more work
        pass
```

---

## Exception Handling

### Suppressing Exceptions

```python
class SuppressException:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"Suppressed ValueError: {exc_val}")
            return True  # Suppress exception
        return False  # Don't suppress other exceptions

# Usage
with SuppressException():
    raise ValueError("This will be suppressed")

print("Program continues...")

# with SuppressException():
#     raise TypeError("This will NOT be suppressed")
```

### contextlib.suppress

```python
from contextlib import suppress

# Ignore specific exceptions
with suppress(FileNotFoundError):
    import os
    os.remove('nonexistent.txt')

print("File deletion attempted, error ignored")

# Multiple exception types
with suppress(ValueError, TypeError, KeyError):
    risky_operation()

# Traditional way (for comparison)
try:
    os.remove('nonexistent.txt')
except FileNotFoundError:
    pass
```

### Exception Information

```python
from contextlib import contextmanager

@contextmanager
def error_handler():
    try:
        yield
    except Exception as e:
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        print(f"Handling error gracefully...")
        # Don't re-raise, exception is handled

# Usage
with error_handler():
    result = 1 / 0  # ZeroDivisionError

print("Program continues after error")
```

---

## Common Use Cases

### File Operations

```python
# Reading files
with open('data.txt') as f:
    content = f.read()

# Writing files
with open('output.txt', 'w') as f:
    f.write('Hello, World!')

# Binary files
with open('image.png', 'rb') as f:
    data = f.read()

# Append mode
with open('log.txt', 'a') as f:
    f.write('New log entry\n')
```

### Lock Management

```python
import threading

lock = threading.Lock()

# Automatic lock acquisition and release
with lock:
    # Critical section
    shared_resource += 1
# Lock automatically released

# Even with exceptions
try:
    with lock:
        if error_condition:
            raise ValueError("Error!")
        shared_resource += 1
except ValueError:
    pass
# Lock still released!
```

### Timing Code Blocks

```python
from contextlib import contextmanager
import time

@contextmanager
def benchmark(name):
    """Benchmark code execution"""
    start = time.perf_counter()

    yield

    duration = time.perf_counter() - start
    print(f"{name}: {duration:.6f} seconds")

# Usage
with benchmark("List comprehension"):
    result = [x**2 for x in range(100000)]

with benchmark("Generator expression"):
    result = list(x**2 for x in range(100000))
```

### Changing Working Directory

```python
from contextlib import contextmanager
import os

@contextmanager
def working_directory(path):
    """Temporarily change working directory"""
    old_dir = os.getcwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(old_dir)

# Usage
print(f"Current dir: {os.getcwd()}")

with working_directory('/tmp'):
    print(f"Inside context: {os.getcwd()}")
    # Do work in /tmp

print(f"Back to: {os.getcwd()}")
```

### Redirecting stdout

```python
from contextlib import contextmanager, redirect_stdout
import sys
import io

@contextmanager
def capture_output():
    """Capture stdout to string"""
    output = io.StringIO()
    with redirect_stdout(output):
        yield output

# Usage
with capture_output() as output:
    print("This goes to string buffer")
    print("Not to console")

captured = output.getvalue()
print(f"Captured: {captured}")

# Built-in redirect
with open('output.txt', 'w') as f:
    with redirect_stdout(f):
        print("This goes to file")
```

### Database Transactions

```python
from contextlib import contextmanager

@contextmanager
def transaction(connection):
    """Database transaction with automatic commit/rollback"""
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
        print("Transaction committed")
    except Exception as e:
        connection.rollback()
        print(f"Transaction rolled back: {e}")
        raise
    finally:
        cursor.close()

# Usage (pseudo-code)
# with transaction(db_connection) as cursor:
#     cursor.execute("INSERT INTO users VALUES (?)", (user_data,))
#     cursor.execute("UPDATE stats SET count = count + 1")
```

---

## Advanced Patterns

### Reentrant Context Manager

```python
import threading

class ReentrantLock:
    """Lock that can be acquired multiple times by same thread"""
    def __init__(self):
        self.lock = threading.RLock()
        self.count = 0

    def __enter__(self):
        self.lock.acquire()
        self.count += 1
        print(f"Lock acquired (count: {self.count})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.count -= 1
        print(f"Lock released (count: {self.count})")
        self.lock.release()
        return False

# Can be nested
lock = ReentrantLock()

with lock:
    print("Outer context")
    with lock:
        print("Inner context")
        with lock:
            print("Innermost context")
```

### Context Manager for Setup/Teardown

```python
from contextlib import contextmanager

@contextmanager
def test_environment():
    """Setup and teardown test environment"""
    # Setup
    print("Setting up test environment...")
    test_db = create_test_database()
    test_data = populate_test_data(test_db)

    try:
        yield test_db
    finally:
        # Teardown (always runs)
        print("Tearing down test environment...")
        cleanup_test_data(test_db)
        destroy_test_database(test_db)

# Usage in tests
def test_user_creation():
    with test_environment() as db:
        # Run test with clean database
        user = create_user(db, "testuser")
        assert user.name == "testuser"
    # Database automatically cleaned up
```

### Attribute Context Manager

```python
from contextlib import contextmanager

@contextmanager
def temporary_attribute(obj, attr, value):
    """Temporarily change an object's attribute"""
    old_value = getattr(obj, attr)
    setattr(obj, attr, value)

    try:
        yield obj
    finally:
        setattr(obj, attr, old_value)

# Usage
class Config:
    debug = False

config = Config()

with temporary_attribute(config, 'debug', True):
    print(f"Debug mode: {config.debug}")  # True

print(f"Debug mode: {config.debug}")  # False (restored)
```

### Callback Context Manager

```python
from contextlib import contextmanager

@contextmanager
def callbacks(on_enter=None, on_exit=None):
    """Execute callbacks on enter and exit"""
    if on_enter:
        on_enter()

    try:
        yield
    finally:
        if on_exit:
            on_exit()

# Usage
def start():
    print("Starting operation...")

def finish():
    print("Finishing operation...")

with callbacks(on_enter=start, on_exit=finish):
    print("Doing work...")
```

### State Machine Context Manager

```python
from contextlib import contextmanager
from enum import Enum

class State(Enum):
    IDLE = 1
    PROCESSING = 2
    COMPLETE = 3

class StateMachine:
    def __init__(self):
        self.state = State.IDLE

    @contextmanager
    def processing(self):
        """Ensure proper state transitions"""
        if self.state != State.IDLE:
            raise RuntimeError(f"Cannot start processing from {self.state}")

        self.state = State.PROCESSING
        print(f"State: {self.state}")

        try:
            yield
            self.state = State.COMPLETE
            print(f"State: {self.state}")
        except Exception:
            self.state = State.IDLE
            print(f"State: {self.state} (error)")
            raise

# Usage
sm = StateMachine()

with sm.processing():
    # Do processing
    print("Processing data...")
```

---

## Best Practices

### ✅ DO

```python
from contextlib import contextmanager

# 1. Always use context managers for resources
with open('file.txt') as f:  # ✓
    content = f.read()

# 2. Use @contextmanager for simple cases
@contextmanager
def simple_context():
    print("Setup")
    yield
    print("Cleanup")

# 3. Return False from __exit__ to propagate exceptions
def __exit__(self, exc_type, exc_val, exc_tb):
    self.cleanup()
    return False  # ✓ Don't suppress exceptions

# 4. Use try-finally in @contextmanager
@contextmanager
def robust_context():
    resource = acquire()
    try:
        yield resource
    finally:  # ✓ Guaranteed cleanup
        release(resource)

# 5. Use ExitStack for dynamic contexts
from contextlib import ExitStack

def process_multiple_files(filenames):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f)) for f in filenames]
        # Process files

# 6. Use contextlib.suppress for expected exceptions
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove('optional_file.txt')

# 7. Document what your context manager does
@contextmanager
def my_context():
    """
    Context manager that does X.

    Ensures Y is properly cleaned up.
    """
    pass
```

### ❌ DON'T

```python
# 1. Don't forget to close resources manually
f = open('file.txt')  # ✗
content = f.read()
# f.close()  # Easy to forget!

# Use context manager instead
with open('file.txt') as f:  # ✓
    content = f.read()

# 2. Don't suppress exceptions without good reason
def __exit__(self, exc_type, exc_val, exc_tb):
    self.cleanup()
    return True  # ✗ Silently suppresses all exceptions!

# 3. Don't forget try-finally in @contextmanager
@contextmanager
def bad_context():
    resource = acquire()
    yield resource
    release(resource)  # ✗ Won't run if exception occurs!

# Correct:
@contextmanager
def good_context():
    resource = acquire()
    try:
        yield resource
    finally:
        release(resource)  # ✓ Always runs

# 4. Don't use context managers for non-resource cleanup
@contextmanager
def bad_use():  # ✗ Overkill for simple logging
    print("Starting")
    yield
    print("Ending")

# Just use regular functions
def operation():
    print("Starting")
    do_work()
    print("Ending")

# 5. Don't mix setup and business logic
@contextmanager
def confusing():  # ✗ Hard to understand
    setup()
    yield
    business_logic()  # Wrong place!
    cleanup()

# Keep cleanup code only in cleanup section
@contextmanager
def clear():  # ✓
    setup()
    try:
        yield
        # Business logic happens here (in with block)
    finally:
        cleanup()
```

---

## Quick Reference

### Basic Patterns

```python
# Class-based context manager
class MyContext:
    def __enter__(self):
        # Setup
        return resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup
        return False

# Generator-based context manager
from contextlib import contextmanager

@contextmanager
def my_context():
    # Setup
    try:
        yield resource
    finally:
        # Cleanup
        pass
```

### Common Context Managers

| Context Manager | Use Case |
|----------------|----------|
| `open()` | File operations |
| `threading.Lock()` | Thread synchronization |
| `contextlib.suppress()` | Ignore specific exceptions |
| `contextlib.redirect_stdout()` | Redirect output |
| `tempfile.TemporaryDirectory()` | Temporary directories |
| `decimal.localcontext()` | Decimal precision |
| `ExitStack()` | Dynamic context managers |

### When to Use

| Use Context Manager When | Don't Use When |
|-------------------------|----------------|
| ✅ Managing resources (files, locks, connections) | ❌ Simple function calls |
| ✅ Setup/teardown required | ❌ No cleanup needed |
| ✅ Exception safety matters | ❌ One-line operations |
| ✅ Temporary state changes | ❌ Permanent changes |

---

## Summary

**Key Takeaways:**

1. **Context managers ensure cleanup** - resources always released
2. **Two ways to create:** class with `__enter__`/`__exit__` or `@contextmanager`
3. **`with` statement** provides automatic setup and teardown
4. **Exceptions are propagated** unless `__exit__` returns `True`
5. **Use for resources:** files, locks, database connections, etc.
6. **`ExitStack`** for dynamic number of context managers
7. **Always use try-finally** in `@contextmanager` generators

**Basic Template:**

```python
from contextlib import contextmanager

@contextmanager
def my_resource():
    # Setup
    resource = acquire_resource()

    try:
        yield resource  # Provide to with block
    finally:
        # Cleanup (always runs)
        release_resource(resource)

# Usage
with my_resource() as res:
    use(res)
```

**Best Use Cases:**
- File I/O
- Database transactions
- Lock acquisition
- Temporary state changes
- Resource pooling
- Timer/profiling
- Logging contexts

🔒 Master context managers for robust, leak-free Python code!
