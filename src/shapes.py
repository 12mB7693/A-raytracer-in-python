from .ray import Ray
from .tuples import Point
import math


class Shape:
    pass


class Intersection:
    def __init__(self, t, shape: Shape) -> None:
        self.t = t
        self.shape = shape


def hit(intersections: list[Intersection]):
    pos_intersections = [i for i in intersections if i.t > 0]
    if len(pos_intersections) == 0:
        return None
    else:
        return min(pos_intersections, key=lambda intersection: intersection.t)
    # return min(intersections, key=lambda intersection : intersection.t)


class Sphere(Shape):
    def intersect(self, ray: Ray) -> list[Intersection]:
        sphere_to_ray = ray.origin - Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return []

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return [Intersection(t1, self), Intersection(t2, self)]
