# noinspection PyPackageRequirements
from datetime import datetime

import jpype.imports

import database
from core import cli_arguments
from core.assets_classes.base_amidts import BaseAsset
from core.middleware.amidst_setup import get_target_asset


def main():
    database.initialize_db()
    print(f'Used minecraft version: {cli_arguments.game_version}')
    sources = get_target_asset(cli_arguments.sources)
    jpype.startJVM(classpath=sources)
    print(f'Using sources: {sources}')
    if len(cli_arguments.seeds) > 0 and cli_arguments.amount > 0:
        print('Specify one one of arguments: seeds OR amount')
        exit(1)
    print('JVM started')
    asset_api = BaseAsset(
        amidst_sources=sources,
    )
    if cli_arguments.show_versions:
        asset_api.print_versions()
        exit(0)
    print(f'Minecraft {cli_arguments.game_version} started successfully')
    start_time = datetime.now()
    print(f'Start analyzing at {start_time}')
    asset_api.search_seeds()
    end_time = datetime.now()
    print(f'Finish analyzing at {end_time}')
    total_time = str(end_time - start_time)
    print(f"Total scan time is: {total_time} seconds.")


if __name__ == '__main__':
    main()
