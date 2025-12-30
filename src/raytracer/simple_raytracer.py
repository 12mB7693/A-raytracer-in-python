from PIL import Image
import time
import raytracer as rt
import math

def render_tile2(x0, x1, y0, y1, width, height):
    """
    Example of how to render tiles with a color gradient
    """
    tile_width = x1 - x0
    tile_height = y1 - y0

    img = Image.new("RGB", (tile_width, tile_height))

    for y in range(tile_height):
        for x in range(tile_width):
            r = int(255 * (x0 + x) / width)
            g = int(255 * (y0 + y) / height)
            b = 128
            img.putpixel((x, y), (r, g, b))
    time.sleep(1)

    return img


def render_tile(x0, x1, y0, y1, width, height):
    middle = rt.Sphere()
    pattern = rt.Texture(rt.TexturePath.earthTexture)
    middle.set_transform(rt.translation(0, 0.5, 0))
    middle.material = rt.Material(pattern=pattern, diffuse=0.7, specular=0.3)

    floor = rt.Plane()
    floor.transform = rt.translation(0, -4, 10)
    floor.material = rt.Material(pattern=rt.ConstantPattern(rt.Colors.white), specular=0)

    world = rt.World()
    world.objects = [floor, middle]
    world.lightSource = rt.PointLight(rt.Point(-10, 10, -10), rt.Color(1, 1, 1))

    camera = rt.Camera(700, 700, math.pi / 3)
    camera.transform = rt.view_transform(
        rt.Point(0, 1.5, -5), rt.Point(0, 1, 0), rt.Vector(0, 1, 0)
    )
    img = camera.render_tile(world, x0, x1, y0, y1, width, height)
    return img
