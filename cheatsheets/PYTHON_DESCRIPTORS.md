# Python Descriptors Cheatsheet

## Table of Contents
- [What are Descriptors?](#what-are-descriptors)
- [The Descriptor Protocol](#the-descriptor-protocol)
- [Data vs Non-Data Descriptors](#data-vs-non-data-descriptors)
- [Basic Descriptors](#basic-descriptors)
- [Common Use Cases](#common-use-cases)
- [Property Decorator](#property-decorator)
- [Method Descriptors](#method-descriptors)
- [ClassMethod and StaticMethod](#classmethod-and-staticmethod)
- [Descriptor Examples](#descriptor-examples)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)

---

## What are Descriptors?

**Descriptors** are objects that define how attribute access is handled. They power Python features like properties, methods, static methods, and class methods.

**Key Benefits:**
- 🎯 Control attribute access
- 🔒 Implement validation and constraints
- 🔄 Create reusable attribute logic
- 🏗️ Build powerful abstractions

**The Magic:** When you access `obj.attr`, Python looks for a descriptor in the class hierarchy.

```python
class Descriptor:
    def __get__(self, obj, objtype=None):
        return "descriptor value"

    def __set__(self, obj, value):
        pass

    def __delete__(self, obj):
        pass

class MyClass:
    attr = Descriptor()  # Descriptor instance

obj = MyClass()
value = obj.attr  # Calls Descriptor.__get__(descriptor, obj, MyClass)
```

---

## The Descriptor Protocol

### Three Methods

```python
class DescriptorProtocol:
    def __get__(self, obj, objtype=None):
        """
        Called to get attribute value.

        obj: instance being accessed (None if accessed from class)
        objtype: type of instance (class)
        """
        return value

    def __set__(self, obj, value):
        """
        Called to set attribute value.

        obj: instance being modified
        value: new value to set
        """
        pass

    def __delete__(self, obj):
        """
        Called to delete attribute.

        obj: instance being modified
        """
        pass

# If __set__ or __delete__ is defined: Data Descriptor
# If only __get__ is defined: Non-Data Descriptor
```

### How Descriptors Work

```python
class LoggedAccess:
    def __init__(self, name):
        self.name = name
        self.value = None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # Accessed from class
        print(f"Getting {self.name}")
        return self.value

    def __set__(self, obj, value):
        print(f"Setting {self.name} = {value}")
        self.value = value

    def __delete__(self, obj):
        print(f"Deleting {self.name}")
        self.value = None

class MyClass:
    x = LoggedAccess('x')

obj = MyClass()
obj.x = 10       # Setting x = 10
print(obj.x)     # Getting x -> 10
del obj.x        # Deleting x
```

---

## Data vs Non-Data Descriptors

### Data Descriptor

Has `__set__` and/or `__delete__` - takes precedence over instance `__dict__`.

```python
class DataDescriptor:
    def __get__(self, obj, objtype=None):
        print("DataDescriptor.__get__")
        return 42

    def __set__(self, obj, value):
        print("DataDescriptor.__set__")

class MyClass:
    attr = DataDescriptor()

obj = MyClass()
obj.__dict__['attr'] = 100  # Set in instance dict
print(obj.attr)  # Still calls descriptor! -> 42

# Lookup order for data descriptors:
# 1. Data descriptors from type(obj).__mro__
# 2. obj.__dict__
# 3. Non-data descriptors and class variables
```

### Non-Data Descriptor

Only has `__get__` - instance `__dict__` takes precedence.

```python
class NonDataDescriptor:
    def __get__(self, obj, objtype=None):
        print("NonDataDescriptor.__get__")
        return 42

class MyClass:
    attr = NonDataDescriptor()

obj = MyClass()
print(obj.attr)  # NonDataDescriptor.__get__ -> 42

obj.attr = 100   # Sets in instance __dict__
print(obj.attr)  # 100 (instance dict shadows descriptor)

# Lookup order for non-data descriptors:
# 1. obj.__dict__
# 2. Data descriptors from type(obj).__mro__
# 3. Non-data descriptors and class variables from type(obj).__mro__
# 4. __getattr__ if defined
```

---

## Basic Descriptors

### Simple Descriptor

```python
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 0)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer")
        obj.__dict__[self.name] = value

class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

point = Point(10, 20)
print(point.x)  # 10

# point.x = "string"  # TypeError: x must be an integer
```

### Storing Data

```python
# Method 1: Store in instance __dict__
class Descriptor1:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

# Method 2: Store in descriptor (shared across instances!)
class Descriptor2:
    def __init__(self):
        self.value = None  # WRONG: Shared by all instances!

    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value):
        self.value = value

# Method 3: Use WeakKeyDictionary
from weakref import WeakKeyDictionary

class Descriptor3:
    def __init__(self):
        self.data = WeakKeyDictionary()

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(obj)

    def __set__(self, obj, value):
        self.data[obj] = value
```

---

## Common Use Cases

### Validation

```python
class Validated:
    def __init__(self, name, validator):
        self.name = name
        self.validator = validator

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        obj.__dict__[self.name] = value

class Person:
    name = Validated('name', lambda x: isinstance(x, str) and len(x) > 0)
    age = Validated('age', lambda x: isinstance(x, int) and 0 <= x <= 150)

    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
print(person.name)  # Alice

# person.age = -5  # ValueError: Invalid value for age: -5
# person.name = ""  # ValueError: Invalid value for name:
```

### Type Checking

```python
class TypedProperty:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value

class User:
    name = TypedProperty('name', str)
    age = TypedProperty('age', int)
    email = TypedProperty('email', str)

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

user = User("Bob", 25, "bob@example.com")
# user.age = "25"  # TypeError: age must be int, got str
```

### Lazy Evaluation

```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Compute value on first access
        value = self.func(obj)

        # Replace descriptor with computed value
        setattr(obj, self.name, value)

        return value

class DataProcessor:
    @LazyProperty
    def expensive_computation(self):
        print("Computing...")
        import time
        time.sleep(1)
        return sum(range(1000000))

processor = DataProcessor()
print("Created processor")
print(processor.expensive_computation)  # Computing... -> result
print(processor.expensive_computation)  # result (no computation)
```

---

## Property Decorator

### How @property Works

```python
# @property is implemented as a descriptor!

class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

# Using property
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

temp = Temperature(25)
print(temp.celsius)     # 25
print(temp.fahrenheit)  # 77.0

temp.fahrenheit = 32
print(temp.celsius)     # 0.0
```

---

## Method Descriptors

### How Methods Work

```python
class Function:
    """Simplified function descriptor"""
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            # Accessed from class, return unbound function
            return self.func

        # Accessed from instance, return bound method
        from types import MethodType
        return MethodType(self.func, obj)

class MyClass:
    def method(self):
        return "called method"

    # method is actually a descriptor!

obj = MyClass()

# From instance: bound method
print(obj.method)       # <bound method MyClass.method of ...>
print(obj.method())     # "called method"

# From class: unbound function
print(MyClass.method)   # <function MyClass.method at ...>
print(MyClass.method(obj))  # "called method"
```

### Custom Method Descriptor

```python
class LoggedMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func

        def wrapper(*args, **kwargs):
            print(f"Calling {self.func.__name__}")
            result = self.func(obj, *args, **kwargs)
            print(f"Finished {self.func.__name__}")
            return result

        return wrapper

class MyClass:
    @LoggedMethod
    def method(self):
        return "result"

obj = MyClass()
obj.method()
# Calling method
# Finished method
```

---

## ClassMethod and StaticMethod

### How @classmethod Works

```python
class ClassMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if objtype is None:
            objtype = type(obj)

        # Return function with class as first argument
        def wrapper(*args, **kwargs):
            return self.func(objtype, *args, **kwargs)

        return wrapper

class MyClass:
    value = 10

    @classmethod
    def get_value(cls):
        return cls.value

print(MyClass.get_value())  # 10

obj = MyClass()
print(obj.get_value())      # 10 (cls is still MyClass)
```

### How @staticmethod Works

```python
class StaticMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        # Return function without binding
        return self.func

class MyClass:
    @staticmethod
    def static_method(x, y):
        return x + y

print(MyClass.static_method(5, 3))  # 8

obj = MyClass()
print(obj.static_method(5, 3))      # 8
```

---

## Descriptor Examples

### Range Validator

```python
class RangeValidated:
    def __init__(self, name, min_value, max_value):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"{self.name} must be between {self.min_value} "
                f"and {self.max_value}"
            )

        obj.__dict__[self.name] = value

class Student:
    grade = RangeValidated('grade', 0, 100)
    age = RangeValidated('age', 0, 150)

    def __init__(self, grade, age):
        self.grade = grade
        self.age = age

student = Student(85, 20)
# student.grade = 150  # ValueError: grade must be between 0 and 100
```

### Cached Property

```python
class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Check if already cached
        cache_name = f'_cached_{self.name}'
        if not hasattr(obj, cache_name):
            # Compute and cache
            value = self.func(obj)
            setattr(obj, cache_name, value)

        return getattr(obj, cache_name)

    def __set__(self, obj, value):
        raise AttributeError("Can't set cached property")

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    @CachedProperty
    def mean(self):
        print("Computing mean...")
        return sum(self.data) / len(self.data)

    @CachedProperty
    def std_dev(self):
        print("Computing std dev...")
        mean = self.mean
        variance = sum((x - mean) ** 2 for x in self.data) / len(self.data)
        return variance ** 0.5

analyzer = DataAnalyzer([1, 2, 3, 4, 5])
print(analyzer.mean)     # Computing mean... -> 3.0
print(analyzer.mean)     # 3.0 (cached)
print(analyzer.std_dev)  # Computing std dev... -> 1.41...
```

### String Formatter

```python
class FormattedString:
    def __init__(self, name, formatter):
        self.name = name
        self.formatter = formatter

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.name, "")
        return self.formatter(value)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

class Person:
    name = FormattedString('name', str.title)
    email = FormattedString('email', str.lower)

    def __init__(self, name, email):
        self.name = name
        self.email = email

person = Person("alice smith", "Alice@EXAMPLE.COM")
print(person.name)   # Alice Smith (formatted)
print(person.email)  # alice@example.com (formatted)
```

### One-Time Descriptor

```python
class OneTime:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if self.name in obj.__dict__:
            raise AttributeError(f"{self.name} can only be set once")
        obj.__dict__[self.name] = value

class Configuration:
    api_key = OneTime('api_key')

    def __init__(self, api_key):
        self.api_key = api_key

config = Configuration("secret-key-123")
print(config.api_key)  # secret-key-123

# config.api_key = "new-key"  # AttributeError: api_key can only be set once
```

---

## Advanced Patterns

### Descriptor with __set_name__

```python
class AutoName:
    """Automatically gets attribute name (Python 3.6+)"""
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        print(f"Setting {self.name} on {obj.__class__.__name__}")
        obj.__dict__[self.name] = value

class MyClass:
    x = AutoName()  # __set_name__ called automatically
    y = AutoName()

obj = MyClass()
obj.x = 10  # Setting x on MyClass
obj.y = 20  # Setting y on MyClass
```

### Descriptor as Decorator

```python
class validate:
    def __init__(self, validator):
        self.validator = validator

    def __call__(self, func):
        """Make descriptor work as decorator"""
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not self.validator(result):
                raise ValueError("Validation failed")
            return result
        return wrapper

    def __get__(self, obj, objtype=None):
        """Also work as descriptor"""
        if obj is None:
            return self
        def bound_validator(value):
            return self.validator(value)
        return bound_validator

# As decorator
@validate(lambda x: x > 0)
def positive_number():
    return 5
```

### Descriptor Factory

```python
def typed_property(name, expected_type):
    """Factory function for typed properties"""
    storage_name = f'_{name}'

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(
                f"{name} must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(self, storage_name, value)

    return prop

class Person:
    name = typed_property('name', str)
    age = typed_property('age', int)

    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
# person.age = "30"  # TypeError: age must be int, got str
```

### Chaining Descriptors

```python
class ValidateDescriptor:
    def __init__(self, validator):
        self.validator = validator

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value: {value}")
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class TransformDescriptor:
    def __init__(self, descriptor, transform):
        self.descriptor = descriptor
        self.transform = transform

    def __get__(self, obj, objtype=None):
        value = self.descriptor.__get__(obj, objtype)
        return self.transform(value) if value is not None else None

    def __set__(self, obj, value):
        self.descriptor.__set__(obj, value)

    def __set_name__(self, owner, name):
        self.descriptor.__set_name__(owner, name)

class Person:
    name = TransformDescriptor(
        ValidateDescriptor(lambda x: isinstance(x, str) and x),
        str.title
    )

person = Person()
person.name = "alice"
print(person.name)  # Alice (validated and transformed)
```

---

## Best Practices

### ✅ DO

```python
# 1. Use __set_name__ for automatic naming (Python 3.6+)
class GoodDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

# 2. Handle None in __get__ for class access
class GoodDescriptor:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # Return descriptor when accessed from class
        return obj.__dict__.get(self.name)

# 3. Store data in instance __dict__ or WeakKeyDictionary
from weakref import WeakKeyDictionary

class GoodDescriptor:
    def __init__(self):
        self.data = WeakKeyDictionary()

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(obj)

# 4. Validate in __set__
class GoodDescriptor:
    def __set__(self, obj, value):
        if not self.validate(value):
            raise ValueError("Invalid value")
        obj.__dict__[self.name] = value

# 5. Document descriptor behavior
class GoodDescriptor:
    """
    Descriptor that validates integer values.

    Usage:
        class MyClass:
            value = GoodDescriptor()
    """
    pass
```

### ❌ DON'T

```python
# 1. Don't store instance data in descriptor without WeakKeyDictionary
class BadDescriptor:
    def __init__(self):
        self.value = None  # ✗ Shared by all instances!

# ✓ Use instance __dict__ or WeakKeyDictionary
class GoodDescriptor:
    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

# 2. Don't forget to handle obj=None
class BadDescriptor:
    def __get__(self, obj, objtype=None):
        return obj.value  # ✗ AttributeError if obj is None!

# ✓ Check for None
class GoodDescriptor:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

# 3. Don't create circular references
class BadDescriptor:
    def __get__(self, obj, objtype=None):
        return obj.other_attr  # ✗ If other_attr also uses descriptor...

# 4. Don't modify obj in __get__
class BadDescriptor:
    def __get__(self, obj, objtype=None):
        obj.accessed = True  # ✗ Side effects in getter!
        return obj.__dict__.get(self.name)

# 5. Don't forget __set_name__ manual fallback
class BadDescriptor:
    def __init__(self, name):
        self.name = name  # ✗ Required in old Python versions

# ✓ Support both
class GoodDescriptor:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
```

---

## Quick Reference

### Descriptor Protocol

```python
class Descriptor:
    def __get__(self, obj, objtype=None):
        """Get attribute value"""
        pass

    def __set__(self, obj, value):
        """Set attribute value"""
        pass

    def __delete__(self, obj):
        """Delete attribute"""
        pass

    def __set_name__(self, owner, name):
        """Called when descriptor is assigned to class attribute"""
        pass
```

### Descriptor Types

| Type | Methods | Behavior |
|------|---------|----------|
| Data Descriptor | `__get__` + `__set__` or `__delete__` | Takes precedence over instance dict |
| Non-Data Descriptor | Only `__get__` | Instance dict takes precedence |

### Lookup Order

```
For obj.attr:
1. Data descriptors from type(obj).__mro__
2. obj.__dict__ (if exists)
3. Non-data descriptors from type(obj).__mro__
4. Class variables from type(obj).__mro__
5. __getattr__() if defined
6. AttributeError
```

### Common Patterns

```python
# Validation
class Validated:
    def __set__(self, obj, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        obj.__dict__[self.name] = value

# Lazy evaluation
class Lazy:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.compute(obj)
        setattr(obj, self.name, value)
        return value

# Type checking
class Typed:
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type}")
        obj.__dict__[self.name] = value
```

---

## Summary

**Key Takeaways:**

1. **Descriptors control attribute access** via `__get__`, `__set__`, `__delete__`
2. **Data descriptors** (with `__set__`) override instance dict
3. **Non-data descriptors** (only `__get__`) are overridden by instance dict
4. **Use `__set_name__`** to automatically get attribute name (Python 3.6+)
5. **Store data** in instance `__dict__` or `WeakKeyDictionary`
6. **Handle `obj=None`** in `__get__` for class access
7. **Properties, methods, classmethod, staticmethod** are all descriptors!

**Basic Template:**

```python
class Descriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        # Validate value
        obj.__dict__[self.name] = value
```

**When to Use:**
- Custom validation and type checking
- Lazy evaluation and caching
- Reusable attribute behavior
- Framework development
- Advanced Python features

🔧 Master descriptors for powerful, reusable Python code!
