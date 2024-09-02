from __future__ import annotations
import math


class Tuple:
    def __init__(self, x, y, z, w) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, value: object) -> bool:
        return (
            math.isclose(self.x, value.x)
            and math.isclose(self.y, value.y)
            and math.isclose(self.z, value.z)
            and math.isclose(self.w, value.w)
        )

    def __add__(self, other):
        # if isinstance(self, Tuple):
        return Tuple(
            self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w
        )

    def __sub__(self, other):
        return Tuple(
            self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w
        )

    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, scalar):
        return Tuple(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return Tuple(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)


class Vector(Tuple):
    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y, z, 0)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        return Vector(
            self.x / self.magnitude(),
            self.y / self.magnitude(),
            self.z / self.magnitude(),
        )

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector) -> Vector:
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


class Point(Tuple):
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y, z, 1)


def create_tuple(x, y, z, w):
    if w == 0:
        return Vector(x, y, z)
    elif w == 1:
        return Point(x, y, z)
    else:
        return None
