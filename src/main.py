from .tuples import Point, Vector, Color
from .canvas import Canvas


class Projectile:
    def __init__(self, position: Point, veloctiy: Vector) -> None:
        self.position = position
        self.velocity = veloctiy


class Environment:
    def __init__(self, gravity: Vector, wind: Vector) -> None:
        self.gravity = gravity
        self.wind = wind


def tick(env, proj):
    proj.position = proj.position + proj.velocity
    proj.velocity = proj.velocity + env.gravity + env.wind


def main():
    p = Projectile(Point(0, 1, 0), 11.25*Vector(1, 1.8, 0).normalize())
    e = Environment(Vector(0, -0.1, 0), Vector(-0.01, 0, 0))
    canvas = Canvas(900, 550)

    tick_count = 0
    while p.position.y > 0:
        canvas.write_pixel(int(p.position.x), 550-int(p.position.y), Color(1,0,0))
        tick(e, p)
        tick_count += 1
        print(f"Projectile position: ({p.position.x}, {p.position.y})")     

    print(f"Tick count: {tick_count}")
    
    ppm = canvas.convert_to_ppm()

    with open("output.ppm", "w") as text_file:
        text_file.write(ppm)


if __name__ == "__main__":
    main()
