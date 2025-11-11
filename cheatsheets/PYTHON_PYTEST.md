# Python Pytest Cheatsheet

## Table of Contents
- [What is Pytest?](#what-is-pytest)
- [Installation and Setup](#installation-and-setup)
- [Basic Test Structure](#basic-test-structure)
- [Running Tests](#running-tests)
- [Assertions](#assertions)
- [Fixtures](#fixtures)
- [Parametrization](#parametrization)
- [Marks and Markers](#marks-and-markers)
- [Mocking](#mocking)
- [Configuration](#configuration)
- [Best Practices](#best-practices)

---

## What is Pytest?

**Pytest** is a powerful, flexible testing framework for Python that makes it easy to write simple and scalable tests.

**Key Benefits:**
- 🎯 Simple assert statements (no special methods)
- 🔧 Powerful fixtures system
- 📊 Detailed test reports
- 🔌 Rich plugin ecosystem
- 🚀 Easy to get started, scales well

---

## Installation and Setup

### Installation

```bash
# Install pytest
pip install pytest

# Install with common plugins
pip install pytest pytest-cov pytest-mock pytest-asyncio

# Check installation
pytest --version
```

### Project Structure

```
my_project/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Shared fixtures
│   ├── test_calculator.py  # Test modules start with test_
│   └── test_utils.py
├── pytest.ini              # Pytest configuration
└── requirements.txt
```

---

## Basic Test Structure

### Simple Test Function

```python
# tests/test_math.py

def test_addition():
    """Test addition operation"""
    result = 2 + 2
    assert result == 4

def test_subtraction():
    """Test subtraction operation"""
    result = 5 - 3
    assert result == 2

# Run with: pytest tests/test_math.py
```

### Test Classes

```python
# tests/test_calculator.py

class TestCalculator:
    """Group related tests in a class"""

    def test_add(self):
        result = 2 + 3
        assert result == 5

    def test_subtract(self):
        result = 5 - 2
        assert result == 3

    def test_multiply(self):
        result = 3 * 4
        assert result == 12

    def test_divide(self):
        result = 10 / 2
        assert result == 5
```

### Testing a Module

```python
# src/calculator.py

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# tests/test_calculator.py

from src.calculator import Calculator

def test_calculator_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_calculator_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_calculator.py

# Run specific test
pytest tests/test_calculator.py::test_addition

# Run tests in directory
pytest tests/

# Run tests matching pattern
pytest -k "addition"  # Runs tests with "addition" in name

# Run with verbose output
pytest -v

# Run with extra verbosity
pytest -vv

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3
```

### Useful Options

```bash
# Run last failed tests
pytest --lf

# Run failed tests first, then others
pytest --ff

# Show local variables in tracebacks
pytest -l

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Generate coverage report
pytest --cov=src --cov-report=html

# Run only tests that changed
pytest --testmon

# Disable warnings
pytest --disable-warnings

# Show slowest tests
pytest --durations=10
```

---

## Assertions

### Basic Assertions

```python
import pytest

def test_basic_assertions():
    # Equality
    assert 1 + 1 == 2
    assert "hello" == "hello"
    assert [1, 2, 3] == [1, 2, 3]

    # Inequality
    assert 5 != 3
    assert "a" != "b"

    # Boolean
    assert True
    assert not False

    # None checks
    assert None is None
    assert 0 is not None

    # Contains
    assert "hello" in "hello world"
    assert 3 in [1, 2, 3, 4]
    assert "key" in {"key": "value"}

    # Type checks
    assert isinstance(42, int)
    assert isinstance("text", str)
```

### Detailed Assertion Messages

```python
def test_with_messages():
    # Custom message
    x = 5
    assert x == 10, f"Expected 10, got {x}"

    # Pytest automatically shows useful info
    a = [1, 2, 3]
    b = [1, 2, 4]
    assert a == b  # Shows: [3] != [4] at index 2
```

### Exception Testing

```python
import pytest

def test_exceptions():
    # Test that exception is raised
    with pytest.raises(ZeroDivisionError):
        1 / 0

    # Test exception message
    with pytest.raises(ValueError, match="invalid literal"):
        int("abc")

    # Capture exception for inspection
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("Custom error")

    assert "Custom" in str(exc_info.value)

def test_no_exception():
    # Test that no exception is raised
    try:
        result = 1 + 1
        assert result == 2
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")
```

### Approximate Comparisons

```python
import pytest

def test_approximate():
    # Float comparison with tolerance
    assert 0.1 + 0.2 == pytest.approx(0.3)

    # Custom tolerance
    assert 100 == pytest.approx(105, abs=5)
    assert 100 == pytest.approx(105, rel=0.1)  # 10% tolerance

    # Lists of floats
    assert [0.1, 0.2] == pytest.approx([0.1, 0.2])
```

---

## Fixtures

### Basic Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests"""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_length(sample_data):
    assert len(sample_data) == 5

# Fixture with setup and teardown
@pytest.fixture
def database():
    """Setup database before test, cleanup after"""
    # Setup
    db = create_database()
    print("\nDatabase created")

    yield db  # Provide to test

    # Teardown
    db.close()
    print("\nDatabase closed")

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert result is not None
```

### Fixture Scopes

```python
import pytest

# Function scope (default) - runs for each test
@pytest.fixture(scope="function")
def temp_file():
    with open("temp.txt", "w") as f:
        f.write("data")
    yield "temp.txt"
    import os
    os.remove("temp.txt")

# Class scope - runs once per test class
@pytest.fixture(scope="class")
def database():
    db = create_database()
    yield db
    db.close()

# Module scope - runs once per module
@pytest.fixture(scope="module")
def api_client():
    client = APIClient()
    yield client
    client.disconnect()

# Session scope - runs once per test session
@pytest.fixture(scope="session")
def server():
    server = start_server()
    yield server
    server.stop()
```

### Fixture Dependencies

```python
import pytest

@pytest.fixture
def database():
    db = Database()
    yield db
    db.close()

@pytest.fixture
def user(database):
    """Fixture that depends on database fixture"""
    user = database.create_user("testuser")
    yield user
    database.delete_user(user.id)

def test_user_creation(user):
    assert user.name == "testuser"
```

### conftest.py - Shared Fixtures

```python
# tests/conftest.py
"""
Fixtures defined here are available to all tests
in this directory and subdirectories
"""

import pytest

@pytest.fixture
def api_client():
    """Shared API client for all tests"""
    client = APIClient(base_url="http://test.local")
    yield client
    client.close()

@pytest.fixture
def sample_user():
    """Sample user data"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30
    }

# Auto-use fixture (runs automatically)
@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    db.clear()
    yield
    # Cleanup after test
```

### Built-in Fixtures

```python
import pytest

def test_tmp_path(tmp_path):
    """tmp_path provides temporary directory"""
    file = tmp_path / "test.txt"
    file.write_text("content")
    assert file.read_text() == "content"

def test_tmp_path_factory(tmp_path_factory):
    """Create multiple temp directories"""
    dir1 = tmp_path_factory.mktemp("data1")
    dir2 = tmp_path_factory.mktemp("data2")
    # Use directories

def test_monkeypatch(monkeypatch):
    """Modify objects and environment"""
    # Patch attribute
    monkeypatch.setattr("os.getcwd", lambda: "/fake/path")

    # Set environment variable
    monkeypatch.setenv("API_KEY", "test-key")

    # Modify dict
    import sys
    monkeypatch.setitem(sys.modules, "fake_module", None)

def test_capsys(capsys):
    """Capture stdout/stderr"""
    print("Hello")
    print("Error", file=sys.stderr)

    captured = capsys.readouterr()
    assert "Hello" in captured.out
    assert "Error" in captured.err

def test_caplog(caplog):
    """Capture log messages"""
    import logging
    logger = logging.getLogger(__name__)

    logger.info("Info message")
    logger.error("Error message")

    assert "Info message" in caplog.text
    assert len(caplog.records) == 2
```

---

## Parametrization

### Basic Parametrization

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
])
def test_double(input, expected):
    assert input * 2 == expected

# Equivalent to writing 4 separate tests
```

### Multiple Parameters

```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (5, 7, 12),
    (10, 20, 30),
    (0, 0, 0),
])
def test_addition(a, b, expected):
    assert a + b == expected
```

### Named Parameters

```python
@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param(1, 2, id="one"),
        pytest.param(2, 4, id="two"),
        pytest.param(3, 6, id="three"),
    ]
)
def test_with_ids(test_input, expected):
    assert test_input * 2 == expected

# Test names: test_with_ids[one], test_with_ids[two], etc.
```

### Parametrize Multiple Times

```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_combinations(x, y):
    # Runs 4 times: (0,2), (0,3), (1,2), (1,3)
    assert x + y >= 2
```

### Parametrize with Fixtures

```python
@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param

def test_with_fixture(number):
    # Runs 3 times with number=1, 2, 3
    assert number > 0
```

---

## Marks and Markers

### Built-in Marks

```python
import pytest

# Skip test
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

# Skip conditionally
@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_modern_feature():
    pass

# Expected to fail
@pytest.mark.xfail(reason="Known bug")
def test_buggy_feature():
    assert False  # Won't cause test failure

# Mark as slow
@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(5)

# Run with: pytest -m slow (run only slow tests)
# Run with: pytest -m "not slow" (skip slow tests)
```

### Custom Markers

```python
# pytest.ini
"""
[pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    smoke: marks tests as smoke tests
    api: marks tests as API tests
"""

# Use custom markers
@pytest.mark.smoke
def test_basic_functionality():
    assert True

@pytest.mark.integration
def test_database_integration():
    # Test database integration
    pass

@pytest.mark.api
@pytest.mark.slow
def test_external_api():
    # Test external API
    pass

# Run specific marks
# pytest -m smoke
# pytest -m "smoke or integration"
# pytest -m "not slow"
```

### Marking Classes

```python
@pytest.mark.integration
class TestDatabaseOperations:
    """All tests in this class are marked as integration"""

    def test_insert(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass
```

---

## Mocking

### Using pytest-mock

```bash
pip install pytest-mock
```

```python
import pytest

# Mock function
def test_function_mock(mocker):
    mock_func = mocker.Mock(return_value=42)
    result = mock_func()
    assert result == 42
    mock_func.assert_called_once()

# Patch attribute
def test_patch_attribute(mocker):
    mocker.patch('os.getcwd', return_value='/fake/path')
    import os
    assert os.getcwd() == '/fake/path'

# Patch method
def test_patch_method(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='file content'))
    with open('test.txt') as f:
        content = f.read()
    assert content == 'file content'

# Mock class
def test_mock_class(mocker):
    MockClass = mocker.Mock()
    instance = MockClass()
    instance.method.return_value = 'mocked'

    assert instance.method() == 'mocked'
    instance.method.assert_called_once()
```

### Spy on Functions

```python
def test_spy(mocker):
    """Spy allows real function to run while tracking calls"""
    spy = mocker.spy(os.path, 'exists')

    # Real function runs
    result = os.path.exists('/tmp')

    # But we can check it was called
    spy.assert_called_once_with('/tmp')
    assert isinstance(result, bool)
```

### Mock Side Effects

```python
def test_side_effects(mocker):
    # Return different values on successive calls
    mock = mocker.Mock(side_effect=[1, 2, 3])
    assert mock() == 1
    assert mock() == 2
    assert mock() == 3

    # Raise exception
    mock = mocker.Mock(side_effect=ValueError("Error"))
    with pytest.raises(ValueError):
        mock()

    # Custom function
    def side_effect_func(x):
        return x * 2

    mock = mocker.Mock(side_effect=side_effect_func)
    assert mock(5) == 10
```

---

## Configuration

### pytest.ini

```ini
# pytest.ini
[pytest]
# Minimum pytest version
minversion = 6.0

# Test discovery patterns
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Test paths
testpaths = tests

# Add markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

# Add command line options
addopts =
    -v
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing

# Show warnings
filterwarnings =
    error
    ignore::DeprecationWarning
```

### pyproject.toml Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--cov=src",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

---

## Best Practices

### ✅ DO

```python
# 1. Use descriptive test names
def test_user_can_login_with_valid_credentials():
    pass

# 2. Follow AAA pattern (Arrange, Act, Assert)
def test_addition():
    # Arrange
    calculator = Calculator()
    a, b = 2, 3

    # Act
    result = calculator.add(a, b)

    # Assert
    assert result == 5

# 3. One assertion per test (when possible)
def test_list_length():
    data = [1, 2, 3]
    assert len(data) == 3

def test_list_contents():
    data = [1, 2, 3]
    assert data[0] == 1

# 4. Use fixtures for setup
@pytest.fixture
def user():
    return User(name="Test User")

def test_user_name(user):
    assert user.name == "Test User"

# 5. Use parametrize for similar tests
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected

# 6. Test edge cases
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# 7. Use marks to organize tests
@pytest.mark.slow
@pytest.mark.integration
def test_database_query():
    pass

# 8. Mock external dependencies
def test_api_call(mocker):
    mocker.patch('requests.get', return_value=mock_response)
    result = fetch_data()
    assert result == expected
```

### ❌ DON'T

```python
# 1. Don't test implementation details
def bad_test():
    obj = MyClass()
    assert obj._internal_cache == {}  # ✗ Testing private attribute

def good_test():
    obj = MyClass()
    assert obj.get_data() == expected  # ✓ Testing behavior

# 2. Don't write interdependent tests
# ✗ BAD
def test_part_1():
    global shared_state
    shared_state = setup()

def test_part_2():
    # Depends on test_part_1 running first
    result = use(shared_state)

# ✓ GOOD - use fixtures
@pytest.fixture
def state():
    return setup()

def test_part_1(state):
    pass

def test_part_2(state):
    pass

# 3. Don't make tests too complex
def bad_test():  # ✗ Too complex
    # 50 lines of setup
    # Multiple nested if statements
    # Testing multiple things
    pass

# 4. Don't ignore test failures
@pytest.mark.skip  # ✗ Don't just skip failing tests
def test_something():
    pass

# 5. Don't use time.sleep in tests
def bad_test():
    start_async_task()
    time.sleep(5)  # ✗ Slow and unreliable
    assert task_complete()

# Use proper async testing or mocking instead
```

### Test Organization

```python
# Organize tests by feature/module
tests/
├── conftest.py          # Shared fixtures
├── test_auth.py         # Authentication tests
├── test_users.py        # User management tests
├── test_api/
│   ├── conftest.py      # API-specific fixtures
│   ├── test_endpoints.py
│   └── test_validation.py
└── test_integration/
    ├── conftest.py
    └── test_workflows.py

# Group related tests in classes
class TestUserAuthentication:
    def test_login_success(self):
        pass

    def test_login_failure(self):
        pass

    def test_logout(self):
        pass
```

---

## Quick Reference

### Running Tests

```bash
pytest                      # Run all tests
pytest -v                   # Verbose
pytest -s                   # Show print statements
pytest -x                   # Stop on first failure
pytest -k "pattern"         # Run tests matching pattern
pytest -m "marker"          # Run tests with marker
pytest --lf                 # Run last failed
pytest --cov=src           # Coverage report
pytest -n auto             # Parallel execution
```

### Common Assertions

```python
assert x == y               # Equality
assert x != y               # Inequality
assert x                    # Truthy
assert not x                # Falsy
assert x in y               # Membership
assert x is y               # Identity
assert isinstance(x, Type)  # Type check
```

### Fixture Scopes

| Scope | Description |
|-------|-------------|
| `function` | Run for each test (default) |
| `class` | Run once per test class |
| `module` | Run once per module |
| `session` | Run once per test session |

---

## Summary

**Key Takeaways:**

1. **Simple assertions** - use plain `assert` statements
2. **Fixtures** - powerful dependency injection system
3. **Parametrization** - test multiple scenarios easily
4. **Markers** - organize and select tests
5. **Mocking** - isolate code under test
6. **Configuration** - customize pytest behavior
7. **Follow AAA pattern** - Arrange, Act, Assert

**Basic Test:**
```python
import pytest

@pytest.fixture
def data():
    return [1, 2, 3]

def test_sum(data):
    assert sum(data) == 6
```

**Run tests:**
```bash
pytest -v --cov=src
```

🧪 Master pytest for robust, maintainable test suites!
