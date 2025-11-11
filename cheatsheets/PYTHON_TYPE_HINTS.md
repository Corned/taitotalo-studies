# Python Type Hints Cheatsheet

## Table of Contents
- [What are Type Hints?](#what-are-type-hints)
- [Basic Type Hints](#basic-type-hints)
- [Built-in Types](#built-in-types)
- [Collections](#collections)
- [Optional and Union](#optional-and-union)
- [Functions](#functions)
- [Classes](#classes)
- [Generics](#generics)
- [Type Aliases](#type-aliases)
- [Protocol and Structural Subtyping](#protocol-and-structural-subtyping)
- [TypeVar and Constraints](#typevar-and-constraints)
- [Literal and Final](#literal-and-final)
- [Type Checking with mypy](#type-checking-with-mypy)
- [Best Practices](#best-practices)

---

## What are Type Hints?

**Type hints** (PEP 484) allow you to specify expected types for variables, function parameters, and return values. They improve code readability, enable better IDE support, and catch bugs early with type checkers.

**Key Benefits:**
- 🔍 Early bug detection with type checkers
- 💡 Better IDE autocomplete and suggestions
- 📖 Self-documenting code
- 🛡️ Refactoring safety
- 👥 Team collaboration

**Important:** Type hints are **optional** and don't affect runtime behavior!

```python
# Type hints don't prevent runtime errors
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet(123)  # Type checker warns, but runs fine at runtime
```

---

## Basic Type Hints

### Variable Annotations

```python
# Basic type hints
name: str = "Alice"
age: int = 30
height: float = 5.8
is_active: bool = True

# Type hints without assignment
user_id: int
user_id = 12345

# Multiple variables
x: int
y: int
x, y = 1, 2
```

### Type Inference

```python
# Python can infer types
name = "Alice"  # Inferred as str
age = 30        # Inferred as int

# Explicit is better when it's not obvious
data = load_data()  # What type is data?
data: dict[str, Any] = load_data()  # Clear!
```

---

## Built-in Types

### Simple Types

```python
# Primitives
integer: int = 42
floating: float = 3.14
text: str = "Hello"
flag: bool = True
nothing: None = None

# Bytes
binary: bytes = b"hello"
byte_array: bytearray = bytearray(b"hello")
```

### Any Type

```python
from typing import Any

# Any accepts any type (disables type checking)
data: Any = "string"
data = 123  # OK
data = [1, 2, 3]  # OK

# Use sparingly - defeats purpose of type hints!
def process(value: Any) -> Any:
    return value
```

---

## Collections

### Lists

```python
from typing import List  # Python 3.9+: can use list directly

# List of specific type
numbers: list[int] = [1, 2, 3, 4, 5]
names: list[str] = ["Alice", "Bob", "Charlie"]

# Nested lists
matrix: list[list[int]] = [[1, 2], [3, 4], [5, 6]]

# Empty list with type hint
items: list[str] = []

# Old style (Python 3.8 and earlier)
from typing import List
numbers: List[int] = [1, 2, 3]
```

### Tuples

```python
# Fixed-length tuple with specific types
coordinates: tuple[int, int] = (10, 20)
person: tuple[str, int, bool] = ("Alice", 30, True)

# Variable-length tuple (all same type)
numbers: tuple[int, ...] = (1, 2, 3, 4, 5)

# Empty tuple
empty: tuple[()] = ()

# Old style
from typing import Tuple
coords: Tuple[int, int] = (10, 20)
```

### Sets

```python
# Set of specific type
unique_numbers: set[int] = {1, 2, 3, 4, 5}
tags: set[str] = {"python", "coding", "types"}

# Empty set with type hint
ids: set[int] = set()

# Frozenset (immutable set)
frozen: frozenset[str] = frozenset({"a", "b", "c"})

# Old style
from typing import Set
numbers: Set[int] = {1, 2, 3}
```

### Dictionaries

```python
# Dictionary with key and value types
scores: dict[str, int] = {"Alice": 90, "Bob": 85}
config: dict[str, str] = {"host": "localhost", "port": "8080"}

# Nested dictionaries
data: dict[str, dict[str, int]] = {
    "user1": {"age": 30, "score": 100},
    "user2": {"age": 25, "score": 95}
}

# Empty dict with type hint
cache: dict[int, str] = {}

# Old style
from typing import Dict
scores: Dict[str, int] = {"Alice": 90}
```

### Sequences and Mappings

```python
from typing import Sequence, Mapping, Iterable

# Sequence (list, tuple, etc.)
def process_sequence(items: Sequence[int]) -> int:
    return sum(items)

process_sequence([1, 2, 3])  # OK
process_sequence((1, 2, 3))  # OK

# Mapping (dict, etc.)
def process_mapping(data: Mapping[str, int]) -> list[int]:
    return list(data.values())

# Iterable (anything you can iterate over)
def process_items(items: Iterable[str]) -> list[str]:
    return [item.upper() for item in items]
```

---

## Optional and Union

### Optional

```python
from typing import Optional

# Optional[X] is shorthand for Union[X, None]
def find_user(user_id: int) -> Optional[str]:
    """Returns username or None if not found"""
    if user_id == 1:
        return "Alice"
    return None

# Modern syntax (Python 3.10+)
def find_user(user_id: int) -> str | None:
    if user_id == 1:
        return "Alice"
    return None

# Function parameter can be None
def greet(name: Optional[str] = None) -> str:
    if name is None:
        return "Hello, stranger!"
    return f"Hello, {name}!"
```

### Union

```python
from typing import Union

# Union type - can be one of several types
def process(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return str(value * 2)
    return value.upper()

process(5)        # OK - int
process("hello")  # OK - str

# Modern syntax (Python 3.10+)
def process(value: int | str) -> str:
    if isinstance(value, int):
        return str(value * 2)
    return value.upper()

# Multiple types
ID = Union[int, str, bytes]
user_id: ID = 12345
```

---

## Functions

### Function Signatures

```python
# Basic function type hints
def add(a: int, b: int) -> int:
    return a + b

# No return value (returns None)
def log_message(message: str) -> None:
    print(message)

# Multiple parameters with defaults
def create_user(name: str, age: int = 0, active: bool = True) -> dict[str, Any]:
    return {"name": name, "age": age, "active": active}

# *args and **kwargs
def sum_numbers(*args: int) -> int:
    return sum(args)

def create_config(**kwargs: str) -> dict[str, str]:
    return kwargs
```

### Callable

```python
from typing import Callable

# Callable[[arg_types], return_type]
def execute(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

def add(x: int, y: int) -> int:
    return x + y

result = execute(add, 5, 3)  # Returns 8

# Callable with no arguments
callback: Callable[[], None]

# Callable with any arguments
processor: Callable[..., int]

# Function that returns a function
def create_multiplier(factor: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:
        return x * factor
    return multiply
```

### Overload

```python
from typing import overload, Union

# Multiple signatures for same function
@overload
def process(value: int) -> int: ...

@overload
def process(value: str) -> str: ...

def process(value: Union[int, str]) -> Union[int, str]:
    """Actual implementation"""
    if isinstance(value, int):
        return value * 2
    return value.upper()

# Type checker knows:
result1: int = process(5)       # Returns int
result2: str = process("hello") # Returns str
```

---

## Classes

### Class Type Hints

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age
        self.email: str | None = None

    def greet(self) -> str:
        return f"Hello, I'm {self.name}"

    def set_email(self, email: str) -> None:
        self.email = email

    def get_info(self) -> dict[str, str | int]:
        return {"name": self.name, "age": self.age}
```

### Class Variables vs Instance Variables

```python
from typing import ClassVar

class Config:
    # Class variable
    app_name: ClassVar[str] = "MyApp"
    version: ClassVar[str] = "1.0.0"

    # Instance variable
    def __init__(self, env: str) -> None:
        self.env: str = env
        self.debug: bool = False
```

### Self Type

```python
from typing import Self  # Python 3.11+

class Builder:
    def __init__(self) -> None:
        self.value: int = 0

    def add(self, n: int) -> Self:
        """Returns self for chaining"""
        self.value += n
        return self

    def multiply(self, n: int) -> Self:
        self.value *= n
        return self

# Type checker knows chaining works
builder = Builder().add(5).multiply(2)  # OK
```

### Forward References

```python
# Forward reference using string
class Node:
    def __init__(self, value: int, next_node: "Node | None" = None) -> None:
        self.value = value
        self.next = next_node

# Or use from __future__ import annotations (Python 3.7+)
from __future__ import annotations

class Node:
    def __init__(self, value: int, next_node: Node | None = None) -> None:
        self.value = value
        self.next = next_node
```

---

## Generics

### Generic Functions

```python
from typing import TypeVar

T = TypeVar('T')

def first(items: list[T]) -> T | None:
    """Returns first item or None"""
    return items[0] if items else None

# Type checker knows the return type matches input
numbers: list[int] = [1, 2, 3]
first_num: int | None = first(numbers)  # Returns int | None

strings: list[str] = ["a", "b", "c"]
first_str: str | None = first(strings)  # Returns str | None
```

### Generic Classes

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def peek(self) -> T | None:
        return self.items[-1] if self.items else None

# Type-safe stack
int_stack: Stack[int] = Stack[int]()
int_stack.push(1)
int_stack.push(2)
# int_stack.push("string")  # Type error!

value: int = int_stack.pop()
```

### Multiple Type Parameters

```python
from typing import Generic, TypeVar

K = TypeVar('K')
V = TypeVar('V')

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

    def get_key(self) -> K:
        return self.key

    def get_value(self) -> V:
        return self.value

# Usage
pair: Pair[str, int] = Pair("age", 30)
key: str = pair.get_key()
value: int = pair.get_value()
```

---

## Type Aliases

### Simple Aliases

```python
# Type alias for readability
UserId = int
UserName = str
Score = float

def get_user_score(user_id: UserId) -> Score:
    return 95.5

# Complex type alias
JSON = dict[str, Any]
Headers = dict[str, str]

def parse_response(data: JSON) -> list[str]:
    return list(data.keys())
```

### NewType

```python
from typing import NewType

# NewType creates distinct types for type checker
UserId = NewType('UserId', int)
PostId = NewType('PostId', int)

def get_user(user_id: UserId) -> str:
    return f"User {user_id}"

def get_post(post_id: PostId) -> str:
    return f"Post {post_id}"

user_id = UserId(123)
post_id = PostId(456)

get_user(user_id)   # OK
# get_user(post_id) # Type error! PostId != UserId
# get_user(123)     # Type error! int != UserId
```

### TypeAlias (Python 3.10+)

```python
from typing import TypeAlias

# Explicit type alias
Vector: TypeAlias = list[float]
ConnectionOptions: TypeAlias = dict[str, str | int | bool]

def calculate_magnitude(vector: Vector) -> float:
    return sum(x**2 for x in vector) ** 0.5
```

---

## Protocol and Structural Subtyping

### Protocol

```python
from typing import Protocol

# Define protocol (structural typing)
class Drawable(Protocol):
    def draw(self) -> None: ...

# Any class with draw() method satisfies protocol
class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

def render(shape: Drawable) -> None:
    shape.draw()

# Both work without explicit inheritance!
render(Circle())  # OK
render(Square())  # OK
```

### Runtime Checkable Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

class File:
    def close(self) -> None:
        print("Closing file")

# Runtime check
file = File()
if isinstance(file, Closeable):
    file.close()
```

### Generic Protocol

```python
from typing import Protocol, TypeVar

T_co = TypeVar('T_co', covariant=True)

class SupportsRead(Protocol[T_co]):
    def read(self, size: int = -1) -> T_co: ...

def read_data(reader: SupportsRead[str]) -> str:
    return reader.read()
```

---

## TypeVar and Constraints

### Basic TypeVar

```python
from typing import TypeVar

T = TypeVar('T')

def identity(value: T) -> T:
    return value

# Preserves type
x: int = identity(5)
y: str = identity("hello")
```

### Constrained TypeVar

```python
from typing import TypeVar

# Can only be int or str
NumberOrString = TypeVar('NumberOrString', int, str)

def double(value: NumberOrString) -> NumberOrString:
    if isinstance(value, int):
        return value * 2
    return value * 2  # Repeats string

result1: int = double(5)      # OK
result2: str = double("hi")   # OK
# result3 = double(3.14)      # Type error! float not allowed
```

### Bounded TypeVar

```python
from typing import TypeVar

class Animal:
    def make_sound(self) -> str:
        return "Some sound"

class Dog(Animal):
    def make_sound(self) -> str:
        return "Woof!"

# T must be Animal or subclass
T = TypeVar('T', bound=Animal)

def make_noise(animal: T) -> T:
    print(animal.make_sound())
    return animal

dog: Dog = Dog()
same_dog: Dog = make_noise(dog)  # Returns Dog, not Animal
```

### Variance

```python
from typing import TypeVar

# Covariant (can return subtype)
T_co = TypeVar('T_co', covariant=True)

class Producer(Generic[T_co]):
    def produce(self) -> T_co: ...

# Contravariant (can accept supertype)
T_contra = TypeVar('T_contra', contravariant=True)

class Consumer(Generic[T_contra]):
    def consume(self, item: T_contra) -> None: ...

# Invariant (default - must be exact type)
T = TypeVar('T')
```

---

## Literal and Final

### Literal

```python
from typing import Literal

# Accept only specific values
def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Mode: {mode}")

set_mode("read")   # OK
set_mode("write")  # OK
# set_mode("delete")  # Type error!

# Multiple literals
def set_flag(flag: Literal[0, 1, True, False]) -> None:
    pass

# Use with Union
Status = Literal["pending", "active", "completed"]
Priority = Literal[1, 2, 3, 4, 5]

def update_status(status: Status, priority: Priority) -> None:
    pass
```

### Final

```python
from typing import Final

# Final variable (cannot be reassigned)
MAX_CONNECTIONS: Final = 100
# MAX_CONNECTIONS = 200  # Type error!

# Final in class
class Config:
    API_KEY: Final[str] = "secret_key"

    def __init__(self) -> None:
        self.timeout: Final[int] = 30
        # self.timeout = 60  # Type error!

# Final method (cannot be overridden)
from typing import final

class Base:
    @final
    def important_method(self) -> None:
        pass

class Derived(Base):
    # def important_method(self) -> None:  # Type error!
    #     pass
    pass
```

---

## Type Checking with mypy

### Installing mypy

```bash
pip install mypy

# Run type checker
mypy script.py
mypy project/

# With specific Python version
mypy --python-version 3.11 script.py

# Strict mode
mypy --strict script.py
```

### Configuration (mypy.ini)

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_generics = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
check_untyped_defs = True
strict_equality = True

# Per-module options
[mypy-tests.*]
disallow_untyped_defs = False

[mypy-third_party_lib.*]
ignore_missing_imports = True
```

### Type Comments (Legacy)

```python
# For Python < 3.6 or when annotations aren't possible
x = []  # type: list[int]

def old_style(x, y):
    # type: (int, str) -> bool
    return len(y) > x

# With statement
with open("file.txt") as f:  # type: IO[str]
    content = f.read()
```

### Ignoring Type Errors

```python
# Ignore type error on specific line
result = some_function()  # type: ignore

# Ignore specific error code
value = dict["key"]  # type: ignore[index]

# Ignore entire file
# mypy: ignore-errors

# Better: Fix the issue or use proper types!
```

---

## Best Practices

### ✅ DO

```python
# 1. Use type hints for function signatures
def calculate_total(items: list[float]) -> float:
    return sum(items)

# 2. Use Optional for values that can be None
def find_user(user_id: int) -> Optional[str]:
    return user_dict.get(user_id)

# 3. Use type aliases for complex types
JSONResponse = dict[str, Any]
Headers = dict[str, str]

def fetch_data() -> tuple[JSONResponse, Headers]:
    return {}, {}

# 4. Use Protocol for structural typing
from typing import Protocol

class Printable(Protocol):
    def __str__(self) -> str: ...

def print_item(item: Printable) -> None:
    print(str(item))

# 5. Use TypeVar for generic functions
T = TypeVar('T')

def first_or_none(items: list[T]) -> T | None:
    return items[0] if items else None

# 6. Use Literal for specific values
def set_log_level(level: Literal["DEBUG", "INFO", "ERROR"]) -> None:
    pass

# 7. Use Final for constants
MAX_RETRIES: Final = 3

# 8. Gradual typing - start with important functions
def critical_function(data: dict[str, Any]) -> bool:
    # Type hint critical functions first
    pass
```

### ❌ DON'T

```python
from typing import Any

# 1. Don't overuse Any
def bad_function(x: Any) -> Any:  # ✗ Defeats purpose of type hints
    return x

def good_function(x: int | str) -> str:  # ✓ Be specific
    return str(x)

# 2. Don't use mutable defaults
def bad(items: list[int] = []) -> list[int]:  # ✗ Dangerous!
    items.append(1)
    return items

def good(items: list[int] | None = None) -> list[int]:  # ✓
    if items is None:
        items = []
    items.append(1)
    return items

# 3. Don't forget return type
def missing_return(x: int):  # ✗ What does it return?
    return x * 2

def with_return(x: int) -> int:  # ✓
    return x * 2

# 4. Don't use bare except with type hints
def bad_error_handling(x: int) -> int:
    try:
        return x / 0
    except:  # ✗ Too broad
        return 0

def good_error_handling(x: int) -> int:
    try:
        return x // 1
    except ZeroDivisionError:  # ✓ Specific
        return 0

# 5. Don't ignore type checker warnings
result = might_be_none()  # type: ignore  # ✗
# Fix the issue instead!

result = might_be_none()
if result is not None:  # ✓
    use(result)
```

### Type Hint Patterns

```python
# Pattern 1: Factory functions
def create_user(name: str) -> dict[str, str | int]:
    return {"name": name, "age": 0}

# Pattern 2: Callback types
Callback = Callable[[int, str], None]

def register_callback(callback: Callback) -> None:
    pass

# Pattern 3: Return multiple types
def parse_value(s: str) -> int | float | str:
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

# Pattern 4: Context managers
from types import TracebackType

class DatabaseConnection:
    def __enter__(self) -> "DatabaseConnection":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        pass
```

---

## Quick Reference

### Common Type Hints

| Type | Example |
|------|---------|
| `int` | `x: int = 5` |
| `str` | `name: str = "Alice"` |
| `float` | `pi: float = 3.14` |
| `bool` | `flag: bool = True` |
| `list[T]` | `numbers: list[int] = [1, 2, 3]` |
| `tuple[T, ...]` | `coords: tuple[int, int] = (0, 0)` |
| `dict[K, V]` | `scores: dict[str, int] = {}` |
| `set[T]` | `ids: set[int] = {1, 2, 3}` |
| `None` | `def f() -> None:` |
| `Any` | `data: Any = anything` |
| `Optional[T]` | `result: Optional[str] = None` |
| `Union[X, Y]` | `id: Union[int, str]` |
| `Callable[[Args], Return]` | `func: Callable[[int], str]` |

### Modern Syntax (Python 3.10+)

```python
# Union with |
def process(x: int | str) -> str: ...

# Optional with |
def find(id: int) -> str | None: ...

# Multiple unions
def handle(value: int | str | float | None) -> bool: ...
```

### Import Locations

```python
# Python 3.9+
from typing import (
    Any, Optional, Union, Callable,
    TypeVar, Generic, Protocol,
    Literal, Final, ClassVar, Self
)

# Use built-in types for collections (Python 3.9+)
list[int], dict[str, int], set[str], tuple[int, ...]

# Python 3.8 and earlier
from typing import List, Dict, Set, Tuple
List[int], Dict[str, int], Set[str], Tuple[int, ...]
```

---

## Summary

**Key Takeaways:**

1. **Type hints are optional** - but highly recommended
2. **Start gradually** - add types to new code first
3. **Use mypy** - catch errors before runtime
4. **Be specific** - avoid `Any` when possible
5. **Use modern syntax** - `|` instead of `Union` (Python 3.10+)
6. **Protocol for duck typing** - structural subtyping
7. **Generics for reusability** - `TypeVar` and `Generic`
8. **Type aliases for clarity** - document complex types

**Basic Pattern:**
```python
from typing import Optional

def process_user(
    user_id: int,
    name: str,
    email: Optional[str] = None
) -> dict[str, str | int]:
    return {
        "id": user_id,
        "name": name,
        "email": email or "no-email"
    }
```

**Check Your Code:**
```bash
mypy --strict your_module.py
```

📘 Master type hints for safer, more maintainable Python code!
