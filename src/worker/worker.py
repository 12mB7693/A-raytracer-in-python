import os
from redis import Redis
from PIL import Image
from raytracer.simple_raytracer import render_tile
from raytracer import Canvas

def render_job(job_id, x0, x1, y0, y1, width, height):
    os.makedirs("tiles", exist_ok=True)

    img = render_tile(x0, x1, y0, y1, width, height)

    tile_path = f"tiles/{job_id}_{x0}_{y0}.png"
    if isinstance(img, Image.Image):
        img.save(tile_path)
    elif isinstance(img, Canvas):
        ppm = img.convert_to_ppm()
        with open(tile_path, "w") as text_file:
            text_file.write(ppm)

    return tile_path

if __name__ == "__main__":
    from rq import Queue
    from rq.worker import Worker
    redis_conn = Redis(host="localhost", port=6379)
    queue = Queue("render_queue", connection=redis_conn)

    worker = Worker([queue]) #worker listens to jobs in the "render_queue"
    worker.work()
