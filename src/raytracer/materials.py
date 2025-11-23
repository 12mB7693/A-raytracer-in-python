from __future__ import annotations
from dataclasses import dataclass, field

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lights import PointLight

from .tuples import Color, Vector, Point, Colors
from .matrix import create_identity_matrix
from . import shapes


import math


class StripePattern:
    def __init__(self, c1: Color, c2: Color):
        self.c1 = c1
        self.c2 = c2
        self.transform = create_identity_matrix()

    def stripe_at(self, point: Point) -> Color:
        if math.floor(point.x) % 2 == 0:
            return self.c1
        else:
            return self.c2

    def stripe_at_object(self, object: shapes.Shape, world_point: Point) -> Color:
        object_point = object.transform.inverse().multiply(world_point)
        pattern_point = self.transform.inverse().multiply(object_point)
        return self.stripe_at(pattern_point)




@dataclass
class Material:
    color: Color = field(default_factory=lambda: Color(1, 1, 1)) #TODO: ensure that either pattern or color is None
    ambient: float = 0.1
    diffuse: float = 0.9
    specular: float = 0.9
    shininess: float = 200.0
    pattern: StripePattern = None
    def __eq__(self, other):
        if isinstance(other, Material):
            return (
                self.color == other.color
                and math.isclose(self.ambient, other.ambient, abs_tol=1e-5)
                and math.isclose(self.diffuse, other.diffuse, abs_tol=1e-5)
                and math.isclose(self.specular, other.specular, abs_tol=1e-5)
                and math.isclose(self.shininess, other.shininess, abs_tol=1e-5)
            )
        else:
            return False

    def __repr__(self):
        return f"Material({self.color}, {self.ambient}, {self.diffuse}, {self.specular, {self.shininess}})"


def lighting(
    light: PointLight,
    intersectionInfo: shapes.IntersectionInfo,
    in_shadow: bool = False,
) -> Color:
    shape = intersectionInfo.intersection.shape
    m = shape.material

    if m.pattern is None:
        color = m.color
    else:
        color = m.pattern.stripe_at_object(shape, intersectionInfo.point)

    effective_color = color.hadamard_product(light.intensity)
    lightv = (light.position - intersectionInfo.point).normalize()
    ambient = effective_color * m.ambient

    if in_shadow:
        return ambient

    light_dot_normal = lightv.dot(intersectionInfo.normalv)
    if light_dot_normal < 0:
        diffuse = Color(0, 0, 0)
        specular = Color(0, 0, 0)
    else:
        diffuse = effective_color * m.diffuse * light_dot_normal
        reflectv = -lightv.reflect(intersectionInfo.normalv)
        reflect_dot_eye = reflectv.dot(intersectionInfo.eyev)

        if reflect_dot_eye <= 0:
            specular = Color(0, 0, 0)
        else:
            factor = reflect_dot_eye**m.shininess
            specular = light.intensity * m.specular * factor

    return ambient + diffuse + specular
