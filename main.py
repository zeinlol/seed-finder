# noinspection PyPackageRequirements
import jpype.imports

import numpy as np
import database
from itertools import count
from io import BytesIO

from config.minecraft_config import gen_opts, game
from core.middleware import check_input
from core.middleware.utils.amidst_setup import get_newest_asset
from core.middleware.utils.game_utils import generate_random_seed
from serialyzer import filter_mesa

from config.variables import screen_width, screen_height
from config.main_classes import scan_config


def main():
    seeds_to_analyse = scan_config.seeds_to_analyse
    database.initialize_db()
    jpype.startJVM(classpath=get_newest_asset())
    print('JVM started')
    new_minecraft_instance = game.mojangapi.file.MinecraftInstallation.newLocalMinecraftInstallation()
    game_versions = list(new_minecraft_instance.readInstalledVersionsAsLauncherProfiles())
    # TODO add cli output for installed versions
    print('installed versions:')
    for version in game_versions:
        print(version.getVersionId())

    # TODO add cli version support
    game_profile = next(filter(lambda version: version.getVersionId() == '1.16.1', game_versions))
    game_interface = game.mojangapi.minecraftinterface.MinecraftInterfaces.fromLocalProfile(game_profile)
    game_world_builder = game.mojangapi.world.WorldBuilder.createSilentPlayerless()

    if not seeds_to_analyse:
        for i in count():
            seed = generate_random_seed()
            print(f'Analyse random seed: {seed.getLong()}')
            world_type = game.mojangapi.world.WorldType.DEFAULT
            opts = game.mojangapi.world.WorldOptions(seed, world_type, gen_opts)
            world = game_world_builder.from_(game_interface, opts)
            biome_oracle = world.getBiomeDataOracle()

            def biome_val(x, y):
                return np.uint8(int(biome_oracle.getBiomeAt(x, y, True).getId()))

            biome_data = np.fromfunction(np.vectorize(biome_val), (screen_width, screen_height), dtype=np.int64)

            if not filter_mesa(biome_data):
                bin_data = None
                with BytesIO() as tmp_file:
                    np.save(tmp_file, biome_data)
                    bin_data = tmp_file.getvalue()
                world = database.World.create(seed=seed.getLong(), biome_data=bin_data)

            print(i, seed.getLong())
    else:
        for seed in scan_config.seeds_to_analyse:
            print(f'analyze seed: {seed}')
            seed = game.mojangapi.world.WorldSeed.fromUserInput(seed)
            world_type = game.mojangapi.world.WorldType.DEFAULT
            opts = game.mojangapi.world.WorldOptions(seed, world_type, gen_opts)
            world = game_world_builder.from_(game_interface, opts)
            biome_oracle = world.getBiomeDataOracle()

            def biome_val(x, y):
                return np.uint8(int(biome_oracle.getBiomeAt(x, y, True).getId()))

            biome_data = np.fromfunction(np.vectorize(biome_val), (screen_width, screen_height), dtype=np.int64)

            if not filter_mesa(biome_data):
                bin_data = None
                with BytesIO() as tmp_file:
                    np.save(tmp_file, biome_data)
                    bin_data = tmp_file.getvalue()
                world = database.World.create(seed=seed.getLong(), biome_data=bin_data)

            print(seed, seed.getLong())

if __name__ == '__main__':
    check_input()
    # TODO if seeds as list (123, 123, 123) parser.seed = ['123,', '123,', '123']. Clean input if needed
    # print(arguments.seed)
    main()
