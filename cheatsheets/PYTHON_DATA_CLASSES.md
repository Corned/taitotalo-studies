# Python Data Classes Cheatsheet

## Table of Contents
- [What are Data Classes?](#what-are-data-classes)
- [Basic Data Classes](#basic-data-classes)
- [Field Options](#field-options)
- [Default Values](#default-values)
- [Post-Init Processing](#post-init-processing)
- [Inheritance](#inheritance)
- [Immutability](#immutability)
- [Comparison and Ordering](#comparison-and-ordering)
- [Converting to Dict/Tuple](#converting-to-dicttuple)
- [Alternative: attrs](#alternative-attrs)
- [Alternative: NamedTuple](#alternative-namedtuple)
- [Alternative: TypedDict](#alternative-typeddict)
- [Best Practices](#best-practices)

---

## What are Data Classes?

**Data classes** (PEP 557, Python 3.7+) are a decorator and functions for automatically adding special methods to classes that primarily store data.

**Key Benefits:**
- 🎯 Less boilerplate code
- 📝 Automatic `__init__`, `__repr__`, `__eq__`
- 🔒 Immutability support with `frozen=True`
- 🏷️ Type hints built-in
- ⚡ Fast and clean

**Without dataclass:**
```python
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age}, email={self.email})"

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return (self.name, self.age, self.email) == (other.name, other.age, other.email)
```

**With dataclass:**
```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str
```

---

## Basic Data Classes

### Simple Data Class

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

# Automatic __init__
point = Point(10.0, 20.0)

# Automatic __repr__
print(point)  # Point(x=10.0, y=20.0)

# Automatic __eq__
p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1 == p2)  # True
```

### With Type Hints

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class User:
    username: str
    email: str
    age: int
    is_active: bool = True
    tags: List[str] = None
    bio: Optional[str] = None

user = User("alice", "alice@example.com", 30)
print(user)
# User(username='alice', email='alice@example.com', age=30,
#      is_active=True, tags=None, bio=None)
```

### Accessing Attributes

```python
@dataclass
class Product:
    name: str
    price: float
    quantity: int

product = Product("Laptop", 999.99, 5)

# Access attributes
print(product.name)      # Laptop
print(product.price)     # 999.99

# Modify attributes
product.quantity = 10
print(product.quantity)  # 10
```

---

## Field Options

### field() Function

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    # Field with default value
    grade: int = field(default=0)

    # Field with default_factory (for mutable defaults)
    courses: list[str] = field(default_factory=list)

    # Field excluded from __repr__
    password: str = field(default="", repr=False)

    # Field excluded from comparison
    last_login: str = field(default="", compare=False)

    # Field excluded from __init__
    student_id: int = field(init=False)

student = Student("Alice")
print(student)
# Student(name='Alice', grade=0, courses=[], last_login='')
```

### Field Parameters

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    # default: default value
    host: str = field(default="localhost")

    # default_factory: callable that returns default
    ports: list[int] = field(default_factory=list)

    # init: include in __init__ (default: True)
    computed: str = field(init=False)

    # repr: include in __repr__ (default: True)
    secret: str = field(default="", repr=False)

    # compare: include in comparison (default: True)
    timestamp: float = field(default=0.0, compare=False)

    # hash: include in __hash__ (default: None)
    id: int = field(default=0, hash=True)

    # metadata: dictionary for custom use
    version: str = field(default="1.0", metadata={"deprecated": False})

config = Config()
```

### Mutable Default Values

```python
from dataclasses import dataclass, field

# ❌ WRONG - Don't use mutable defaults directly
@dataclass
class BadExample:
    items: list = []  # This will cause issues!

# ✅ CORRECT - Use default_factory
@dataclass
class GoodExample:
    items: list[str] = field(default_factory=list)
    data: dict[str, int] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)

# Each instance gets its own list
user1 = GoodExample()
user2 = GoodExample()

user1.items.append("item1")
print(user1.items)  # ['item1']
print(user2.items)  # []  ✓ Separate lists!
```

### Custom Default Factory

```python
from dataclasses import dataclass, field
from datetime import datetime

def get_timestamp():
    return datetime.now().isoformat()

def generate_id():
    return id(object())

@dataclass
class Event:
    name: str
    timestamp: str = field(default_factory=get_timestamp)
    event_id: int = field(default_factory=generate_id)

event1 = Event("login")
event2 = Event("logout")

print(event1.event_id != event2.event_id)  # True - unique IDs
```

---

## Default Values

### Simple Defaults

```python
from dataclasses import dataclass

@dataclass
class Rectangle:
    width: float = 1.0
    height: float = 1.0
    color: str = "black"

# Use defaults
rect1 = Rectangle()
print(rect1)  # Rectangle(width=1.0, height=1.0, color='black')

# Override some defaults
rect2 = Rectangle(width=5.0)
print(rect2)  # Rectangle(width=5.0, height=1.0, color='black')

# Override all
rect3 = Rectangle(10.0, 20.0, "red")
print(rect3)  # Rectangle(width=10.0, height=20.0, color='red')
```

### Required Fields First

```python
from dataclasses import dataclass

@dataclass
class Book:
    # Required fields (no default) must come first
    title: str
    author: str

    # Optional fields (with default) come after
    year: int = 2024
    pages: int = 0
    isbn: str = ""

# ❌ This would cause an error:
# @dataclass
# class BadBook:
#     title: str = "Unknown"  # Has default
#     author: str             # No default - ERROR!
```

---

## Post-Init Processing

### __post_init__ Method

```python
from dataclasses import dataclass, field

@dataclass
class Temperature:
    celsius: float
    fahrenheit: float = field(init=False)
    kelvin: float = field(init=False)

    def __post_init__(self):
        """Called after __init__"""
        self.fahrenheit = self.celsius * 9/5 + 32
        self.kelvin = self.celsius + 273.15

temp = Temperature(25.0)
print(temp.fahrenheit)  # 77.0
print(temp.kelvin)      # 298.15
```

### Validation in __post_init__

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str

    def __post_init__(self):
        """Validate data after initialization"""
        if self.age < 0:
            raise ValueError("Age cannot be negative")

        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")

        # Transform data
        self.name = self.name.strip().title()

# Valid
person = Person("alice smith", 30, "alice@example.com")
print(person.name)  # "Alice Smith"

# Invalid - raises ValueError
# person = Person("Bob", -5, "bob@example.com")
```

### InitVar - Init-Only Variables

```python
from dataclasses import dataclass, field, InitVar

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    # InitVar: only available in __post_init__, not stored
    calculate_area: InitVar[bool] = True

    def __post_init__(self, calculate_area: bool):
        if calculate_area:
            self.area = self.width * self.height
        else:
            self.area = 0.0

rect1 = Rectangle(10, 20)
print(rect1.area)  # 200.0

rect2 = Rectangle(10, 20, calculate_area=False)
print(rect2.area)  # 0.0

# calculate_area is not an attribute
# print(rect1.calculate_area)  # AttributeError
```

---

## Inheritance

### Basic Inheritance

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    species: str

@dataclass
class Dog(Animal):
    breed: str

    def bark(self) -> str:
        return f"{self.name} says woof!"

dog = Dog("Buddy", "Canis familiaris", "Golden Retriever")
print(dog)
# Dog(name='Buddy', species='Canis familiaris', breed='Golden Retriever')
print(dog.bark())  # Buddy says woof!
```

### Inheritance with Defaults

```python
from dataclasses import dataclass

@dataclass
class Base:
    required_field: str
    optional_field: int = 0

@dataclass
class Derived(Base):
    # New fields with defaults can be added
    extra_field: str = "extra"

    # Cannot add required fields after inherited optional fields!
    # new_required: str  # This would cause an error!

derived = Derived("test")
print(derived)
# Derived(required_field='test', optional_field=0, extra_field='extra')
```

### Overriding Fields

```python
from dataclasses import dataclass, field

@dataclass
class Base:
    name: str
    value: int = 0

@dataclass
class Derived(Base):
    # Override with different default
    value: int = 10

    # Add new field
    extra: str = field(default="", repr=False)

obj = Derived("test")
print(obj.value)  # 10 (overridden default)
```

---

## Immutability

### Frozen Data Classes

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

point = ImmutablePoint(10.0, 20.0)
print(point.x)  # 10.0

# Cannot modify
# point.x = 30.0  # FrozenInstanceError!

# Can use as dict key (if frozen)
points_dict = {point: "origin"}
print(points_dict[ImmutablePoint(10.0, 20.0)])  # "origin"
```

### Frozen with Mutable Fields

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Config:
    name: str
    # The list itself can't be reassigned, but can be modified
    values: list[int] = field(default_factory=list)

config = Config("test")
# config.name = "new"  # FrozenInstanceError!

# But this works (modifying list contents)
config.values.append(1)  # OK
print(config.values)  # [1]

# To make truly immutable, use tuple
@dataclass(frozen=True)
class TrulyImmutable:
    name: str
    values: tuple[int, ...] = ()
```

---

## Comparison and Ordering

### Equality Comparison

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
p3 = Point(2.0, 3.0)

print(p1 == p2)  # True (values are equal)
print(p1 == p3)  # False
print(p1 is p2)  # False (different objects)
```

### Ordering

```python
from dataclasses import dataclass

@dataclass(order=True)
class Student:
    name: str
    grade: float
    age: int

students = [
    Student("Alice", 85.5, 20),
    Student("Bob", 92.0, 19),
    Student("Charlie", 85.5, 21)
]

# Sort by all fields (lexicographic order)
sorted_students = sorted(students)
for student in sorted_students:
    print(student)
# Student(name='Alice', grade=85.5, age=20)
# Student(name='Bob', grade=92.0, age=19)
# Student(name='Charlie', grade=85.5, age=21)

# Comparison operators
print(students[0] < students[1])  # True
```

### Custom Sort Order

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    # Field used for sorting
    sort_index: int = field(init=False, repr=False)

    # Actual fields
    priority: int
    name: str

    def __post_init__(self):
        # Sort by priority (descending), then name
        self.sort_index = (-self.priority, self.name)

tasks = [
    Task(1, "Low priority task"),
    Task(3, "High priority task"),
    Task(2, "Medium priority task"),
    Task(3, "Another high priority")
]

for task in sorted(tasks):
    print(f"{task.priority}: {task.name}")
# 3: Another high priority
# 3: High priority task
# 2: Medium priority task
# 1: Low priority task
```

---

## Converting to Dict/Tuple

### asdict() and astuple()

```python
from dataclasses import dataclass, asdict, astuple

@dataclass
class Person:
    name: str
    age: int
    email: str

person = Person("Alice", 30, "alice@example.com")

# Convert to dictionary
person_dict = asdict(person)
print(person_dict)
# {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}

# Convert to tuple
person_tuple = astuple(person)
print(person_tuple)
# ('Alice', 30, 'alice@example.com')
```

### Nested Data Classes

```python
from dataclasses import dataclass, asdict

@dataclass
class Address:
    street: str
    city: str
    zip_code: str

@dataclass
class Person:
    name: str
    age: int
    address: Address

person = Person(
    "Alice",
    30,
    Address("123 Main St", "New York", "10001")
)

# asdict recursively converts nested dataclasses
person_dict = asdict(person)
print(person_dict)
# {
#     'name': 'Alice',
#     'age': 30,
#     'address': {
#         'street': '123 Main St',
#         'city': 'New York',
#         'zip_code': '10001'
#     }
# }
```

### replace() - Create Modified Copy

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Point:
    x: float
    y: float

point1 = Point(10.0, 20.0)

# Create new instance with modified values
point2 = replace(point1, x=30.0)
print(point1)  # Point(x=10.0, y=20.0)
print(point2)  # Point(x=30.0, y=20.0)

# Works with unfrozen classes too
@dataclass
class MutablePoint:
    x: float
    y: float

mp1 = MutablePoint(1.0, 2.0)
mp2 = replace(mp1, y=5.0)
print(mp2)  # MutablePoint(x=1.0, y=5.0)
```

---

## Alternative: attrs

### Basic attrs

```python
import attr

@attr.s(auto_attribs=True)
class Point:
    x: float
    y: float

# Or with define
from attrs import define

@define
class Point:
    x: float
    y: float

point = Point(10.0, 20.0)
print(point)  # Point(x=10.0, y=20.0)
```

### attrs Features

```python
from attrs import define, field, validators

@define
class User:
    name: str = field(validator=validators.instance_of(str))
    age: int = field(validator=validators.and_(
        validators.instance_of(int),
        validators.ge(0)
    ))
    email: str = field()

    @email.validator
    def check_email(self, attribute, value):
        if "@" not in value:
            raise ValueError("Invalid email")

# Validators run automatically
user = User("Alice", 30, "alice@example.com")  # OK
# user = User("Bob", -5, "bob@example.com")  # ValueError!
```

### attrs vs dataclasses

```python
# attrs advantages:
# - More features (validators, converters)
# - Older, more mature
# - More customization options
# - Better performance in some cases

# dataclasses advantages:
# - Built into Python 3.7+
# - Standard library
# - Simpler API
# - Better IDE support
```

---

## Alternative: NamedTuple

### Basic NamedTuple

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

point = Point(10.0, 20.0)
print(point.x)  # 10.0
print(point[0])  # 10.0 (tuple indexing works)

# Immutable by default
# point.x = 30.0  # AttributeError!

# Unpack like tuple
x, y = point
print(x, y)  # 10.0 20.0
```

### NamedTuple with Methods

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def translate(self, dx: float, dy: float) -> 'Point':
        return Point(self.x + dx, self.y + dy)

point = Point(3.0, 4.0)
print(point.distance_from_origin())  # 5.0

new_point = point.translate(1.0, 1.0)
print(new_point)  # Point(x=4.0, y=5.0)
```

### NamedTuple vs dataclass

```python
# NamedTuple advantages:
# - Immutable by default
# - Memory efficient (tuple subclass)
# - Can use tuple features (indexing, unpacking)
# - Slightly faster

# dataclass advantages:
# - Mutable by default (can be frozen)
# - More flexible (field options)
# - Better for complex scenarios
# - Can use __post_init__
```

---

## Alternative: TypedDict

### Basic TypedDict

```python
from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int
    email: str

# Used for type checking dictionaries
def process_person(person: Person) -> None:
    print(person["name"], person["age"])

# Regular dict with correct structure
person: Person = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}

process_person(person)  # Type checker validates structure
```

### Optional Keys

```python
from typing import TypedDict, NotRequired

# Python 3.11+
class User(TypedDict):
    username: str
    email: str
    age: NotRequired[int]  # Optional key

# Python 3.8-3.10
class User(TypedDict, total=False):
    age: int  # Optional

class User(TypedDict):
    username: str
    email: str  # Required

user1: User = {"username": "alice", "email": "alice@example.com"}
user2: User = {"username": "bob", "email": "bob@example.com", "age": 25}
```

### TypedDict vs dataclass

```python
# TypedDict:
# - For type-checking dicts (no runtime class)
# - Used with JSON, APIs, configs
# - Lighter weight
# - Only for dictionaries

# dataclass:
# - Creates actual class
# - Methods, inheritance, validation
# - Better for OOP
# - More features
```

---

## Best Practices

### ✅ DO

```python
from dataclasses import dataclass, field

# 1. Use type hints
@dataclass
class Product:
    name: str
    price: float
    quantity: int

# 2. Use field() for mutable defaults
@dataclass
class ShoppingCart:
    items: list[str] = field(default_factory=list)

# 3. Use frozen for immutable data
@dataclass(frozen=True)
class Coordinate:
    x: float
    y: float

# 4. Use __post_init__ for validation
@dataclass
class User:
    age: int

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age must be positive")

# 5. Use repr=False for sensitive data
@dataclass
class Account:
    username: str
    password: str = field(repr=False)

# 6. Use order=True for sortable data
@dataclass(order=True)
class Priority:
    level: int
    name: str

# 7. Use slots for memory efficiency (Python 3.10+)
@dataclass(slots=True)
class Point:
    x: float
    y: float
```

### ❌ DON'T

```python
from dataclasses import dataclass

# 1. Don't use mutable defaults directly
@dataclass
class Bad:
    items: list = []  # ✗ Will be shared!

# ✓ Use default_factory
@dataclass
class Good:
    items: list = field(default_factory=list)

# 2. Don't put optional fields before required
# @dataclass
# class Bad:
#     name: str = "default"  # ✗
#     age: int               # Required after optional!

# ✓ Required fields first
@dataclass
class Good:
    age: int
    name: str = "default"

# 3. Don't forget frozen when using as dict key
@dataclass
class Bad:
    x: int
    y: int

# d = {Bad(1, 2): "value"}  # ✗ TypeError: unhashable type

# ✓ Use frozen
@dataclass(frozen=True)
class Good:
    x: int
    y: int

d = {Good(1, 2): "value"}  # ✓ Works

# 4. Don't overuse dataclasses for complex logic
# If you need lots of methods and complex behavior,
# use regular classes instead

# 5. Don't mix dataclass with manual __init__
@dataclass
class Bad:
    name: str

    # def __init__(self, name):  # ✗ Don't override!
    #     self.name = name
```

### Common Patterns

```python
from dataclasses import dataclass, field
from typing import ClassVar

# Pattern 1: Class-level constants
@dataclass
class Config:
    VERSION: ClassVar[str] = "1.0.0"
    instance_id: int

# Pattern 2: Computed fields
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        self.area = self.width * self.height

# Pattern 3: Factory methods
@dataclass
class Point:
    x: float
    y: float

    @classmethod
    def origin(cls) -> 'Point':
        return cls(0.0, 0.0)

    @classmethod
    def from_tuple(cls, coords: tuple[float, float]) -> 'Point':
        return cls(*coords)

# Pattern 4: JSON serialization
import json
from dataclasses import asdict

@dataclass
class User:
    name: str
    age: int

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> 'User':
        return cls(**json.loads(json_str))
```

---

## Quick Reference

### Decorator Options

```python
@dataclass(
    init=True,           # Generate __init__
    repr=True,           # Generate __repr__
    eq=True,             # Generate __eq__
    order=False,         # Generate comparison methods
    unsafe_hash=False,   # Generate __hash__
    frozen=False,        # Make immutable
    match_args=True,     # Enable pattern matching (3.10+)
    kw_only=False,       # Keyword-only __init__ (3.10+)
    slots=False          # Use __slots__ (3.10+)
)
class MyClass:
    pass
```

### Field Options

```python
from dataclasses import field

field(
    default=MISSING,           # Default value
    default_factory=MISSING,   # Callable for default
    init=True,                 # Include in __init__
    repr=True,                 # Include in __repr__
    hash=None,                 # Include in __hash__
    compare=True,              # Include in comparisons
    metadata=None,             # Custom metadata dict
    kw_only=False              # Keyword-only (3.10+)
)
```

### Functions

| Function | Purpose |
|----------|---------|
| `asdict(obj)` | Convert to dict |
| `astuple(obj)` | Convert to tuple |
| `replace(obj, **changes)` | Create modified copy |
| `fields(obj)` | Get field definitions |
| `is_dataclass(obj)` | Check if dataclass |

---

## Summary

**Key Takeaways:**

1. **@dataclass** - reduces boilerplate for data-holding classes
2. **field()** - customize field behavior and defaults
3. **frozen=True** - create immutable instances
4. **__post_init__** - post-initialization processing
5. **order=True** - enable sorting/comparison
6. **Use default_factory** - for mutable defaults
7. **Consider alternatives** - attrs, NamedTuple, TypedDict

**Basic Template:**
```python
from dataclasses import dataclass, field

@dataclass
class Person:
    name: str
    age: int
    email: str
    hobbies: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age must be positive")
```

**When to Use:**
- Data containers (DTOs, configuration, etc.)
- Value objects
- Simple domain models
- API request/response objects

**When NOT to Use:**
- Complex business logic
- Need for __init__ customization
- Heavy inheritance hierarchies

🎯 Master dataclasses for clean, maintainable Python code!
