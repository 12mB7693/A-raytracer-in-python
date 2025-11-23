from .tuples import Point, Vector


class Ray:
    def __init__(self, origin: Point, direction: Vector) -> None:
        self.origin = origin
        self.direction = direction

    def position(self, t: float) -> Point:
        return self.origin + t * self.direction
