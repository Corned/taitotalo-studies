from math import pow, sqrt


class Vector:
    __slots__ = ("x", "y")

    def __init__(self, x: int | float = 0, y: int | float = 0):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __add__(self, other) -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    @property
    def length(self) -> float:
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def __mul__(self, scalar: int | float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int | float) -> "Vector":
        return self.__mul__(scalar)


v1 = Vector(2, 3)
v2 = Vector(3, 2)
print(v1 == v2)  # False
print(v2 != v1)  # True
print(v1 + v2)  # Vector(5, 5)
print(v2 + v1)  # Vector(5, 5)
print(v1 - v2)  # Vector(-1, 1)
print(v2 - v1)  # Vector(1, -1)
print(-v1)  # Vector(-2, -3)
print(-v2)  # Vector(-3, -2)
print(v1.length)  # 1.8988289221159418
print(v2.length)  # 1.8988289221159418
print(v1 * 3)  # Vector(6, 9)
print(3 * v1)  # Vector(6, 9)
print(v2 * 5.5)  # Vector(16.5, 11.0)
print(5.5 * v2)  # Vector(16.5, 11.0)


v1.extra = 2
