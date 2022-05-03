import json
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image

import database
from core.config.constants.core import BIOME_PROFILE, DEFAULT_IMAGE_PATH

color_map = dict(json.load(open(BIOME_PROFILE))["colorMap"])
biome_num = 256
color_arr = np.zeros((biome_num, 3), dtype=np.uint8)
for i in range(biome_num):
    if i in color_map:
        color = color_map[i]
        color_arr[i, 0] = color["r"]
        color_arr[i, 1] = color["g"]
        color_arr[i, 2] = color["b"]


def generate_images():
    for world in database.World.select().where(database.World.image.is_null(True)):
        biome_arr = np.load(BytesIO(world.biome_data))
        rgb = color_arr[biome_arr]
        rgb = rgb.transpose((1, 0, 2))
        f = BytesIO()
        Image.fromarray(rgb).save(f, format="png")
        database.World.update(image=f.getvalue()).where(database.World.seed == world.seed).execute()


def export_images():
    for world in database.World.select().where(database.World.image.is_null(False)):
        export_image_from_world(world)


def export_image_from_world(world: database.World, out_path: Path = DEFAULT_IMAGE_PATH):
    image = Image.open(BytesIO(world.image))
    image.save(out_path.joinpath(f'world_{world.seed}.png'))


generate_images()
export_images()
