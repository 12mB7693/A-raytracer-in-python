from src.raytracer import Material, Color, Colors, StripePattern
from src.raytracer import Point, Vector, PointLight, lighting
from src.raytracer import Sphere, scaling, translation

import math

def test_material_constructor():
    m = Material()
    assert m.color == Color(1, 1, 1)
    assert m.ambient == 0.1
    assert m.diffuse == 0.9
    assert m.specular == 0.9
    assert m.shininess == 200.0

def test_lighting_eye_btw_light_and_surface():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.9, 1.9, 1.9)


def test_lighting_eye_btw_light_and_surface_eye_offset_45():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 1/math.sqrt(2), -1/math.sqrt(2))
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.0, 1.0, 1.0)

def test_lighting_eye_opposite_surface_light_offset_45():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(0.7364, 0.7364, 0.7364)

def test_lighting_eye_in_path_of_reflection_vector():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, -1/math.sqrt(2), -1/math.sqrt(2))
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.6364, 1.6364, 1.6364)

def test_lighting_with_light_behind_surface():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(0.1, 0.1, 0.1)

def test_lighting_with_surface_in_shadow():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    in_shadow = True
    result = lighting(m, light, pos, eyev, normalv, in_shadow)
    assert result == Color(0.1, 0.1, 0.1)

def test_lighting_with_a_pattern():
    m = Material(ambient=1, diffuse=0, specular=0, pattern=StripePattern(Colors.white, Colors.black))
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))

    c1 = lighting(m, light, Point(0.9, 0, 0), eyev, normalv, False)
    c2 = lighting(m, light, Point(1.1, 0, 0), eyev, normalv, False)

    assert c1 == Colors.white
    assert c2 == Colors.black

def test_stripe_pattern():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.c1 == Colors.white
    assert pattern.c2 == Colors.black

def test_stripe_pattern_constant_in_y():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.stripe_at(Point(0, 0, 0)) == Colors.white
    assert pattern.stripe_at(Point(0, 1, 0)) == Colors.white
    assert pattern.stripe_at(Point(0, 2, 0)) == Colors.white

def test_stripe_pattern_constant_in_z():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.stripe_at(Point(0, 0, 0)) == Colors.white
    assert pattern.stripe_at(Point(0, 0, 1)) == Colors.white
    assert pattern.stripe_at(Point(0, 0, 2)) == Colors.white

def test_stripe_pattern_alternates_in_x():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.stripe_at(Point(0, 0, 0)) == Colors.white
    assert pattern.stripe_at(Point(0.9, 0, 0)) == Colors.white
    assert pattern.stripe_at(Point(1, 0, 0)) == Colors.black
    assert pattern.stripe_at(Point(-0.1, 0, 0)) == Colors.black
    assert pattern.stripe_at(Point(-1, 0, 0)) == Colors.black
    assert pattern.stripe_at(Point(-1.1, 0, 0)) == Colors.white

def test_stripes_with_object_transformation():
    s = Sphere()
    s.set_transform(scaling(2, 2, 2))
    pattern = StripePattern(Colors.white, Colors.black)
    c = pattern.stripe_at_object(s, Point(1.5, 0, 0))
    assert c == Colors.white

def test_stripes_with_pattern_transformation():
    s = Sphere()
    pattern = StripePattern(Colors.white, Colors.black)
    pattern.transform = scaling(2, 2, 2)
    c = pattern.stripe_at_object(s, Point(1.5, 0, 0))
    assert c == Colors.white

def test_stripes_with_both_object_and_pattern_transformation():
    s = Sphere()
    s.set_transform(scaling(2, 2, 2))
    pattern = StripePattern(Colors.white, Colors.black)
    pattern.transform = translation(0.5, 0, 0)
    c = pattern.stripe_at_object(s, Point(2.5, 0, 0))
    assert c == Colors.white
