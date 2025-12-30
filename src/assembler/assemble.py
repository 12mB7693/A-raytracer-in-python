import os
from PIL import Image

def assemble(job_id, width, height, tile_size):
    final_img = Image.new("RGB", (width, height))
    tile_dir = "tiles"

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            tile_path = f"{tile_dir}/{job_id}_{x}_{y}.png"
            if not os.path.exists(tile_path):
                print(f"Missing: {tile_path}")
                continue

            tile = Image.open(tile_path)
            final_img.paste(tile, (x, y))

    output_path = f"{job_id}_final.png"
    final_img.save(output_path)
    print(f"Done! Saved as: {output_path}")
    return output_path

if __name__ == "__main__":
    # insert job id here
    assemble("2b894fc0-0906-4723-989d-5baa1f50ee59", 700, 700, 64)
