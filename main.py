# noinspection PyPackageRequirements
import jpype.imports

import numpy as np
import database
from itertools import count
from io import BytesIO

from arguments import create_parser
from config.minecraft_config import gen_opts, game
from middleware.amidst_setup import get_newest_asset
from middleware.game_utils import generate_random_seed
from serialyzer import filter_mesa

from config.variables import screen_width, screen_height


def main():
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
    
    for i in count():
        seed = generate_random_seed()
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


if __name__ == '__main__':
    parser = create_parser()
    print(parser)
    main()
