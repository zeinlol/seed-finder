import asyncio
from datetime import datetime
from itertools import count

import jpype.imports

import database
from config.main_classes import scan_config
from config.minecraft_config import game
from core.middleware import check_input
from core.middleware.utils.amidst_setup import get_newest_asset
from core.middleware.utils.game_utils import generate_random_seed
from core.seed_analyzer.main_analyze import analyze_seed
from core.utils.Installed_versions import get_minecraft_versions


async def main():
    seeds_to_analyse = scan_config.seeds_to_analyse
    database.initialize_db()
    jpype.startJVM(classpath=get_newest_asset())
    print('JVM started')
    game_versions = get_minecraft_versions()
    # TODO add cli output for installed versions
    print('installed versions:')
    installed_versions = [version.getVersionId() for version in game_versions]
    for version in installed_versions:
        print(version)
    # TODO add cli version support
    game_profile = ''
    try:
        game_profile = next(filter(lambda ver: ver.getVersionId() == '1.16.5', game_versions))
    except StopIteration:
        print('This version is not installed or unsupported!')
        exit()
    game_interface = game.mojangapi.minecraftinterface.MinecraftInterfaces.fromLocalProfile(game_profile)
    game_world_builder = game.mojangapi.world.WorldBuilder.createSilentPlayerless()

    start_time = datetime.now()
    print(f'Start analyzing at {start_time}')

    world_type = game.mojangapi.world.WorldType.DEFAULT

    if not seeds_to_analyse:
        for iteration in count():
            seed = generate_random_seed()
            # print(f'Analyse random seed: {seed.getLong()}')
            await analyze_seed(seed=seed,
                               game_profile=game_profile,
                               game_interface=game_interface,
                               game_world_builder=game_world_builder)
    else:
        seeds = [game.mojangapi.world.WorldSeed.fromUserInput(seed) for seed in seeds_to_analyse]
        # profiles = [game_profile for _ in seeds]
        # interfaces = [game_interface for _ in seeds]
        # builders = [game_world_builder for _ in seeds]

        await asyncio.gather(*(analyze_seed(seed=seed,
                                            game_profile=game_profile,
                                            game_interface=game_interface,
                                            game_world_builder=game_world_builder) for seed in seeds))
        # for iteration, seed in enumerate(seeds_to_analyse):
        #     print(f'analyze seed: {seed}')
        #     seed = game.mojangapi.world.WorldSeed.fromUserInput(seed)
        #     analyze_seed(seed=seed, game=game, game_profile=game_profile, game_interface=game_interface,
        #                  game_world_builder=game_world_builder, counter=iteration)

    end_time = datetime.now()
    print(f'Finish analyzing at {end_time}')
    total_time = str(end_time - start_time)
    print(f"Total scan time is: {total_time} seconds.")


if __name__ == '__main__':
    check_input()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    # main()
