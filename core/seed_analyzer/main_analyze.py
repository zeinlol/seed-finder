from io import BytesIO

import numpy as np
import peewee

import database
from config.minecraft_config import gen_opts, game
from config.variables import screen_width, screen_height
from serialyzer import filter_mesa


async def analyze_seed(seed, game_profile, game_interface, game_world_builder) -> None:
    print(f'analyze seed: {seed.getLong()}')
    world_type = game.mojangapi.world.WorldType.DEFAULT
    opts = game.mojangapi.world.WorldOptions(seed, world_type, gen_opts)
    world = game_world_builder.from_(game_interface, opts)
    # biome_oracle = world.getOceanMonumentProducer()
    biome_oracle = world.getOverworldBiomeDataOracle()
    # biome_oracle = world.getBiomeDataOracle()  # 4.5.beta3

    def biome_val(x, y):
        return np.uint8(int(biome_oracle.getBiomeAt(x, y, True).getId()))

    biome_data = np.fromfunction(np.vectorize(biome_val), (screen_width, screen_height), dtype=np.int64)

    if not filter_mesa(biome_data):
        bin_data = None
        with BytesIO() as tmp_file:
            np.save(tmp_file, biome_data)
            bin_data = tmp_file.getvalue()
        try:
            world = database.World.create(seed=seed.getLong(), biome_data=bin_data)
        except peewee.IntegrityError:
            print(f'ERROR: {seed.getLong()} already created')
        print(f'Something found! Seed: {seed.getLong()}')
        return
    print(f'Nothing found.')
