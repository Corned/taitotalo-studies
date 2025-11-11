# Python Magic Methods Cheatsheet

## Table of Contents

- [What are Magic Methods?](#what-are-magic-methods)
- [Object Initialization](#object-initialization)
- [String Representation](#string-representation)
- [Comparison Operators](#comparison-operators)
- [Arithmetic Operators](#arithmetic-operators)
- [Unary Operators](#unary-operators)
- [Augmented Assignment](#augmented-assignment)
- [Type Conversion](#type-conversion)
- [Attribute Access](#attribute-access)
- [Container Methods](#container-methods)
- [Callable Objects](#callable-objects)
- [Context Managers](#context-managers)
- [Iteration](#iteration)
- [Copying](#copying)
- [Pickling](#pickling)
- [Best Practices](#best-practices)

---

## What are Magic Methods?

**Magic methods** (also called **dunder methods** - double underscore) are special methods that Python calls internally. They allow you to define behavior for built-in operations.

**Key Benefits:**

- 🎭 Make objects behave like built-in types
- 🔧 Enable operator overloading
- 📝 Define custom behavior for standard operations
- 🐍 Write more Pythonic code

```python
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        """Define behavior for + operator"""
        return Number(self.value + other.value)

    def __str__(self):
        """Define behavior for str()"""
        return f"Number({self.value})"

n1 = Number(5)
n2 = Number(3)
result = n1 + n2  # Calls __add__
print(result)     # Calls __str__
```

---

## Object Initialization

### **new** and **init**

```python
class Point:
    def __new__(cls, x, y):
        """Create instance (called first)"""
        print(f"Creating instance of {cls}")
        instance = super().__new__(cls)
        return instance

    def __init__(self, x, y):
        """Initialize instance (called after __new__)"""
        print("Initializing instance")
        self.x = x
        self.y = y

point = Point(10, 20)
# Output:
# Creating instance of <class '__main__.Point'>
# Initializing instance
```

### **del**

```python
class Resource:
    def __init__(self, name):
        self.name = name
        print(f"Resource {name} acquired")

    def __del__(self):
        """Called when object is garbage collected"""
        print(f"Resource {self.name} released")

resource = Resource("file")
# ... use resource ...
del resource  # Triggers __del__
# Output: Resource file released
```

---

## String Representation

### **str** and **repr**

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        """User-friendly string (for print())"""
        return f"{self.name}, {self.age} years old"

    def __repr__(self):
        """Developer-friendly string (for debugging)"""
        return f"Person(name={self.name!r}, age={self.age!r})"

person = Person("Alice", 30)

print(str(person))   # Alice, 30 years old
print(repr(person))  # Person(name='Alice', age=30)
print(person)        # Calls __str__ (falls back to __repr__ if not defined)

# In REPL/debugger
>>> person
Person(name='Alice', age=30)  # Uses __repr__
```

### **format**

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __format__(self, format_spec):
        """Custom format behavior"""
        if format_spec == 'polar':
            r = (self.x**2 + self.y**2)**0.5
            theta = math.atan2(self.y, self.x)
            return f"(r={r:.2f}, θ={theta:.2f})"
        elif format_spec == 'cartesian' or not format_spec:
            return f"({self.x}, {self.y})"
        else:
            raise ValueError(f"Unknown format: {format_spec}")

point = Point(3, 4)
print(f"{point}")              # (3, 4)
print(f"{point:cartesian}")    # (3, 4)
print(f"{point:polar}")        # (r=5.00, θ=0.93)
```

### **bytes**

```python
class ByteString:
    def __init__(self, text):
        self.text = text

    def __bytes__(self):
        """Convert to bytes"""
        return self.text.encode('utf-8')

bs = ByteString("Hello")
print(bytes(bs))  # b'Hello'
```

---

## Comparison Operators

### Rich Comparison Methods

```python
class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other):
        """Equal: =="""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == \
               (other.major, other.minor, other.patch)

    def __ne__(self, other):
        """Not equal: !="""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other):
        """Less than: <"""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < \
               (other.major, other.minor, other.patch)

    def __le__(self, other):
        """Less than or equal: <="""
        return self == other or self < other

    def __gt__(self, other):
        """Greater than: >"""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) > \
               (other.major, other.minor, other.patch)

    def __ge__(self, other):
        """Greater than or equal: >="""
        return self == other or self > other

v1 = Version(1, 2, 3)
v2 = Version(1, 2, 4)
v3 = Version(2, 0, 0)

print(v1 < v2)   # True
print(v2 < v3)   # True
print(v1 == v1)  # True
print(v1 >= v2)  # False
```

### Using functools.total_ordering

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade == other.grade

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade < other.grade

    # __le__, __gt__, __ge__ automatically generated!

s1 = Student("Alice", 85)
s2 = Student("Bob", 92)

print(s1 < s2)   # True
print(s1 <= s2)  # True (auto-generated)
print(s2 > s1)   # True (auto-generated)
```

---

## Arithmetic Operators

### Binary Operators

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Addition: +"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtraction: -"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Multiplication: *"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __truediv__(self, scalar):
        """Division: /"""
        return Vector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar):
        """Floor division: //"""
        return Vector(self.x // scalar, self.y // scalar)

    def __mod__(self, scalar):
        """Modulo: %"""
        return Vector(self.x % scalar, self.y % scalar)

    def __pow__(self, power):
        """Power: **"""
        return Vector(self.x ** power, self.y ** power)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(10, 20)
v2 = Vector(5, 8)

print(v1 + v2)   # Vector(15, 28)
print(v1 - v2)   # Vector(5, 12)
print(v1 * 2)    # Vector(20, 40)
print(v1 / 2)    # Vector(5.0, 10.0)
print(v1 // 3)   # Vector(3, 6)
print(v1 % 3)    # Vector(1, 2)
print(v2 ** 2)   # Vector(25, 64)
```

### Reflected Operators

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, scalar):
        """self * scalar"""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """scalar * self (reflected)"""
        return self.__mul__(scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(3, 4)
print(v * 5)   # Vector(15, 20) - calls __mul__
print(5 * v)   # Vector(15, 20) - calls __rmul__
```

---

## Unary Operators

```python
class Number:
    def __init__(self, value):
        self.value = value

    def __neg__(self):
        """Negation: -obj"""
        return Number(-self.value)

    def __pos__(self):
        """Positive: +obj"""
        return Number(+self.value)

    def __abs__(self):
        """Absolute value: abs(obj)"""
        return Number(abs(self.value))

    def __invert__(self):
        """Bitwise NOT: ~obj"""
        return Number(~self.value)

    def __repr__(self):
        return f"Number({self.value})"

num = Number(-5)
print(-num)      # Number(5)
print(+num)      # Number(-5)
print(abs(num))  # Number(5)

num2 = Number(5)
print(~num2)     # Number(-6)
```

---

## Augmented Assignment

```python
class Counter:
    def __init__(self, value=0):
        self.value = value

    def __iadd__(self, other):
        """+="""
        self.value += other
        return self  # Must return self!

    def __isub__(self, other):
        """-="""
        self.value -= other
        return self

    def __imul__(self, other):
        """*="""
        self.value *= other
        return self

    def __itruediv__(self, other):
        """/="""
        self.value /= other
        return self

    def __repr__(self):
        return f"Counter({self.value})"

counter = Counter(10)
counter += 5   # Calls __iadd__
print(counter)  # Counter(15)

counter -= 3   # Calls __isub__
print(counter)  # Counter(12)

counter *= 2   # Calls __imul__
print(counter)  # Counter(24)
```

---

## Type Conversion

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __int__(self):
        """Convert to int: int(obj)"""
        return int(self.celsius)

    def __float__(self):
        """Convert to float: float(obj)"""
        return float(self.celsius)

    def __bool__(self):
        """Convert to bool: bool(obj)"""
        return self.celsius != 0

    def __str__(self):
        return f"{self.celsius}°C"

    def __complex__(self):
        """Convert to complex: complex(obj)"""
        return complex(self.celsius, 0)

temp = Temperature(25.5)
print(int(temp))      # 25
print(float(temp))    # 25.5
print(bool(temp))     # True
print(complex(temp))  # (25.5+0j)

temp_zero = Temperature(0)
print(bool(temp_zero))  # False
```

---

## Attribute Access

### **getattr** and **setattr**

```python
class DynamicAttributes:
    def __init__(self):
        self._data = {}

    def __getattr__(self, name):
        """Called when attribute not found normally"""
        print(f"Getting {name}")
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No attribute '{name}'")

    def __setattr__(self, name, value):
        """Called on every attribute assignment"""
        print(f"Setting {name} = {value}")
        if name == '_data':
            # Allow _data to be set normally
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def __delattr__(self, name):
        """Called when deleting attribute"""
        print(f"Deleting {name}")
        if name in self._data:
            del self._data[name]
        else:
            raise AttributeError(f"No attribute '{name}'")

obj = DynamicAttributes()
obj.x = 10        # Setting x = 10
print(obj.x)      # Getting x -> 10
del obj.x         # Deleting x
```

### **getattribute**

```python
class LoggedAccess:
    def __init__(self, value):
        self.value = value

    def __getattribute__(self, name):
        """Called for EVERY attribute access"""
        print(f"Accessing: {name}")
        return super().__getattribute__(name)

obj = LoggedAccess(42)
print(obj.value)
# Output:
# Accessing: value
# 42
```

### Property-like Behavior

```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __getattr__(self, name):
        if name == 'full_name':
            return f"{self.first_name} {self.last_name}"
        raise AttributeError(f"No attribute '{name}'")

person = Person("John", "Doe")
print(person.full_name)  # John Doe (computed dynamically)
```

---

## Container Methods

### **len**, **getitem**, **setitem**

```python
class MyList:
    def __init__(self):
        self._items = []

    def __len__(self):
        """len(obj)"""
        return len(self._items)

    def __getitem__(self, index):
        """obj[index]"""
        return self._items[index]

    def __setitem__(self, index, value):
        """obj[index] = value"""
        self._items[index] = value

    def __delitem__(self, index):
        """del obj[index]"""
        del self._items[index]

    def __contains__(self, item):
        """item in obj"""
        return item in self._items

    def append(self, item):
        self._items.append(item)

my_list = MyList()
my_list.append(10)
my_list.append(20)
my_list.append(30)

print(len(my_list))     # 3
print(my_list[1])       # 20
my_list[1] = 25
print(my_list[1])       # 25
print(20 in my_list)    # False
print(25 in my_list)    # True
del my_list[0]
print(len(my_list))     # 2
```

### Slicing Support

```python
class SliceableList:
    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, key):
        """Support both indexing and slicing"""
        if isinstance(key, slice):
            return SliceableList(self._items[key])
        return self._items[key]

    def __repr__(self):
        return f"SliceableList({self._items})"

sl = SliceableList([1, 2, 3, 4, 5])
print(sl[2])       # 3
print(sl[1:4])     # SliceableList([2, 3, 4])
print(sl[::2])     # SliceableList([1, 3, 5])
```

---

## Callable Objects

### **call**

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        """Make instance callable like a function"""
        return value * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# Check if callable
print(callable(double))  # True
```

### Stateful Callable

```python
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        """Each call increments and returns count"""
        self.count += 1
        return self.count

counter = Counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

---

## Context Managers

### **enter** and **exit**

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

        # Return False to propagate exceptions
        # Return True to suppress exceptions
        return False

with FileManager('test.txt', 'w') as f:
    f.write('Hello, World!')
# Output:
# Opening test.txt
# Closing test.txt
```

### Exception Handling in Context Manager

```python
class ErrorHandler:
    def __enter__(self):
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exc_type: Exception class (or None)
        exc_val: Exception instance (or None)
        exc_tb: Traceback object (or None)
        """
        if exc_type is None:
            print("No exception occurred")
        else:
            print(f"Handling {exc_type.__name__}: {exc_val}")
            return True  # Suppress exception

with ErrorHandler():
    print("Inside context")
    raise ValueError("Something went wrong")
    print("This won't execute")

print("Program continues")
# Output:
# Entering context
# Inside context
# Handling ValueError: Something went wrong
# Program continues
```

---

## Iteration

### **iter** and **next**

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        """Return iterator object (self)"""
        return self

    def __next__(self):
        """Return next value or raise StopIteration"""
        if self.current <= 0:
            raise StopIteration

        value = self.current
        self.current -= 1
        return value

# Use in for loop
for num in Countdown(5):
    print(num)
# Output: 5, 4, 3, 2, 1

# Manual iteration
countdown = Countdown(3)
print(next(countdown))  # 3
print(next(countdown))  # 2
print(next(countdown))  # 1
# next(countdown)       # StopIteration
```

### Separate Iterator

```python
class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        """Return separate iterator object"""
        return RangeIterator(self.start, self.end)

class RangeIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

# Can iterate multiple times
r = Range(1, 5)
print(list(r))  # [1, 2, 3, 4]
print(list(r))  # [1, 2, 3, 4] (works again!)
```

### **reversed**

```python
class MyList:
    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        """Support reversed() function"""
        return reversed(self._items)

my_list = MyList([1, 2, 3, 4, 5])
print(list(my_list))            # [1, 2, 3, 4, 5]
print(list(reversed(my_list)))  # [5, 4, 3, 2, 1]
```

---

## Copying

### **copy** and **deepcopy**

```python
import copy

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __copy__(self):
        """Shallow copy"""
        print("Creating shallow copy")
        return Point(self.x, self.y)

    def __deepcopy__(self, memo):
        """Deep copy"""
        print("Creating deep copy")
        return Point(
            copy.deepcopy(self.x, memo),
            copy.deepcopy(self.y, memo)
        )

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

original = Point(10, 20)
shallow = copy.copy(original)
deep = copy.deepcopy(original)

print(original)  # Point(10, 20)
print(shallow)   # Point(10, 20)
print(deep)      # Point(10, 20)
```

---

## Pickling

### **getstate** and **setstate**

```python
import pickle

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None  # Non-picklable

    def connect(self):
        self.socket = f"Socket({self.host}:{self.port})"

    def __getstate__(self):
        """Return state for pickling"""
        state = self.__dict__.copy()
        # Remove non-picklable attribute
        state['socket'] = None
        return state

    def __setstate__(self, state):
        """Restore state from pickle"""
        self.__dict__.update(state)
        # Reconnect
        self.connect()

conn = Connection("localhost", 8080)
conn.connect()
print(f"Original: {conn.socket}")

# Pickle and unpickle
data = pickle.dumps(conn)
restored = pickle.loads(data)
print(f"Restored: {restored.socket}")
```

---

## Best Practices

### ✅ DO

```python
# 1. Implement __repr__ for debugging
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

# 2. Return NotImplemented for unsupported operations
class Vector:
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented  # Let Python try other.__eq__(self)
        return self.data == other.data

# 3. Use @functools.total_ordering when implementing comparisons
from functools import total_ordering

@total_ordering
class Student:
    def __eq__(self, other):
        return self.grade == other.grade

    def __lt__(self, other):
        return self.grade < other.grade

# 4. Make __hash__ consistent with __eq__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

# 5. Use __slots__ for memory efficiency
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### ❌ DON'T

```python
# 1. Don't forget to return self in augmented assignment
class Bad:
    def __iadd__(self, other):
        self.value += other
        # Missing return self!

# ✓ Correct
class Good:
    def __iadd__(self, other):
        self.value += other
        return self  # Must return self!

# 2. Don't modify __eq__ without considering __hash__
class Bad:
    def __eq__(self, other):
        return self.value == other.value
    # __hash__ inherited, but now inconsistent!

# ✓ Make unhashable or define __hash__
class Good:
    def __eq__(self, other):
        return self.value == other.value

    __hash__ = None  # Explicitly unhashable
    # OR implement __hash__ correctly

# 3. Don't raise exceptions directly in comparison methods
class Bad:
    def __lt__(self, other):
        if not isinstance(other, Bad):
            raise TypeError("Cannot compare")  # Don't do this

# ✓ Return NotImplemented
class Good:
    def __lt__(self, other):
        if not isinstance(other, Good):
            return NotImplemented  # Let Python handle it

# 4. Don't forget __iter__ returns iterator
class Bad:
    def __iter__(self):
        return self._items  # List, not iterator!

# ✓ Return proper iterator
class Good:
    def __iter__(self):
        return iter(self._items)  # Iterator object

# 5. Don't access attributes directly in __setattr__
class Bad:
    def __setattr__(self, name, value):
        self.name = value  # Infinite recursion!

# ✓ Use super().__setattr__ or __dict__
class Good:
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        # OR: self.__dict__[name] = value
```

---

## Quick Reference

### Common Magic Methods

| Method         | Purpose               | Example                  |
| -------------- | --------------------- | ------------------------ |
| `__init__`     | Constructor           | `obj = MyClass()`        |
| `__str__`      | String representation | `str(obj)`, `print(obj)` |
| `__repr__`     | Developer string      | `repr(obj)`              |
| `__len__`      | Length                | `len(obj)`               |
| `__getitem__`  | Index access          | `obj[key]`               |
| `__setitem__`  | Index assignment      | `obj[key] = value`       |
| `__delitem__`  | Index deletion        | `del obj[key]`           |
| `__contains__` | Membership test       | `item in obj`            |
| `__call__`     | Callable              | `obj()`                  |
| `__iter__`     | Iterator              | `for x in obj`           |
| `__next__`     | Next value            | `next(obj)`              |
| `__enter__`    | Context enter         | `with obj:`              |
| `__exit__`     | Context exit          | `with obj:`              |

### Arithmetic Operators

| Operator | Method         | Reflected       | Augmented       |
| -------- | -------------- | --------------- | --------------- |
| `+`      | `__add__`      | `__radd__`      | `__iadd__`      |
| `-`      | `__sub__`      | `__rsub__`      | `__isub__`      |
| `*`      | `__mul__`      | `__rmul__`      | `__imul__`      |
| `/`      | `__truediv__`  | `__rtruediv__`  | `__itruediv__`  |
| `//`     | `__floordiv__` | `__rfloordiv__` | `__ifloordiv__` |
| `%`      | `__mod__`      | `__rmod__`      | `__imod__`      |
| `**`     | `__pow__`      | `__rpow__`      | `__ipow__`      |

### Comparison Operators

| Operator | Method   |
| -------- | -------- |
| `==`     | `__eq__` |
| `!=`     | `__ne__` |
| `<`      | `__lt__` |
| `<=`     | `__le__` |
| `>`      | `__gt__` |
| `>=`     | `__ge__` |

---

## Summary

**Key Takeaways:**

1. **Magic methods** enable operator overloading and custom behavior
2. **Always implement `__repr__`** for debugging
3. **`__str__` for users, `__repr__` for developers**
4. **Return `NotImplemented`** for unsupported operations
5. **Make `__hash__` consistent with `__eq__`**
6. **Use `@total_ordering`** to reduce boilerplate
7. **`__enter__` and `__exit__`** for context managers
8. **`__iter__` and `__next__`** for iteration

**Basic Template:**

```python
class MyClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"MyClass({self.value!r})"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if not isinstance(other, MyClass):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
```

🎭 Master magic methods to create Pythonic, intuitive classes!
