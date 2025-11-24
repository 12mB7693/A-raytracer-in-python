from src.raytracer import *
from math import sqrt

def test_normal_at_x_axis():
    """
    Test the normal on a sphere at a point on the x axis
    """
    s = Sphere()
    normal = s.normal_at(Point(1, 0, 0))
    assert normal == Vector(1, 0 , 0)

def test_normal_at_y_axis():
    s = Sphere()
    normal = s.normal_at(Point(0, 1, 0))
    assert normal == Vector(0, 1 , 0)

def test_normal_at_z_axis():
    s = Sphere()
    normal = s.normal_at(Point(0, 0, 1))
    assert normal == Vector(0, 0 , 1)

def test_normal_at_nonaxial_point():
    s = Sphere()
    normal = s.normal_at(Point(1/sqrt(3), 1/sqrt(3), 1/sqrt(3)))
    assert normal == Vector(1/sqrt(3), 1/sqrt(3), 1/sqrt(3))

def test_normal_is_normalized_vector():
    s = Sphere()
    normal = s.normal_at(Point(1/sqrt(3), 1/sqrt(3), 1/sqrt(3)))
    assert normal == normal.normalize()

def test_normal_on_translated_sphere():
    s = Sphere()
    s.set_transform(translation(0, 1, 0))
    normal = s.normal_at(Point(0, 1.70711, -0.70711))
    print(normal.z)
    assert normal == Vector(0, 0.70711, -0.70711)

def test_normal_on_transformed_sphere():
    s = Sphere()
    s.set_transform(scaling(1, 0.5, 1).multiply(rotation_z(math.pi/5)))
    normal = s.normal_at(Point(0, 1/sqrt(2), - 1/sqrt(2)))
    assert normal == Vector(0, 0.97014, -0.24254)

def test_default_material_of_sphere():
    s = Sphere()
    m = Material()
    assert m == s.material

def test_set_material_of_sphere():
    s = Sphere()
    m = Material()
    m.ambient = 1
    s.material = m
    assert s.material == m

def test_computation_preparation():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    info = prepare_computations(i, r)
    assert info.intersection.t == i.t
    assert info.intersection.shape == i.shape
    assert info.point == Point(0, 0, -1)
    assert info.eyev == Vector(0, 0, -1)
    assert info.normalv == Vector(0, 0, -1)

def test_intersection_occurs_on_the_outside():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = prepare_computations(i, r)
    assert comps.inside == False

def test_intersection_occurs_on_the_inside():
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = prepare_computations(i, r)
    assert comps.point == Point(0, 0, 1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.inside == True
    assert comps.normalv == Vector(0, 0, -1)

def test_hit_should_offset_the_point():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    s.set_transform(translation(0, 0, 1))
    i = Intersection(5, s)
    comps = prepare_computations(i, r)
    assert comps.over_point.z < -ABS_TOL/2
    assert comps.point.z > comps.over_point.z

def test_plane_normal_at():
    p = Plane()
    n1 = p.shape_specific_normal_at(Point(0, 0, 0))
    n2 = p.shape_specific_normal_at(Point(10, 0, -10))
    n3 = p.shape_specific_normal_at(Point(-5, 0, 150))
    assert n1 == Vector(0, 1, 0)
    assert n2 == Vector(0, 1, 0)
    assert n3 == Vector(0, 1, 0)

def test_intersect_ray_parallel_to_plane():
    p = Plane()
    r = Ray(Point(0, 10, 0), Vector(0, 0, 1))
    xs = p.shape_specific_intersect(r)
    assert xs == []

def test_intersect_ray_coplanar_to_plane():
    p = Plane()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = p.shape_specific_intersect(r)
    assert xs == []

def test_intersect_plane_from_above():
    p = Plane()
    r = Ray(Point(0, 1, 0), Vector(0, -1, 0))
    xs = p.shape_specific_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].shape == p

def test_intersect_plane_from_below():
    p = Plane()
    r = Ray(Point(0, -1, 0), Vector(0, 1, 0))
    xs = p.shape_specific_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].shape == p

def test_texture_transform():
    s = Sphere()
    assert s.texture_transform(Point(0, 0, 1)) == (0.75, 0.5)
    assert s.texture_transform(Point(0, 0, -1)) == (0.25, 0.5)
