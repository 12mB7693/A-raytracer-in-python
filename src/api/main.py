from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from redis import Redis
from rq import Queue
import raytracer as rt
import math

app = FastAPI()
redis_conn = Redis()
queue = Queue("render_queue", connection=redis_conn)

class RenderRequest(BaseModel):
    width: int
    height: int
    tile_size: int = 64

def simple_scene_of_a_sphere():
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
    canvas = camera.render(world)
    return canvas

@app.post("/render")
def render_image(req: RenderRequest):
    job_id = str(uuid.uuid4())

    tiles = []
    for y in range(0, req.height, req.tile_size):
        for x in range(0, req.width, req.tile_size):
            x1 = min(x + req.tile_size, req.width)
            y1 = min(y + req.tile_size, req.height)

            job = queue.enqueue(
                "worker.worker.render_job",
                job_id, x, x1, y, y1, req.width, req.height
            )

            tiles.append(job.id)

    return {
        "job_id": job_id,
        "tiles": len(tiles),
        "tile_job_ids": tiles
    }
