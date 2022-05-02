import jpype.imports

from core import cli_arguments
from core.assets_classes.base_amidts import BaseAsset
from core.middleware.amidst_setup import get_target_asset


def main():
    print(f'Used minecraft version: {cli_arguments.game_version}')
    sources = get_target_asset(cli_arguments.sources)
    jpype.startJVM(classpath=sources)
    print(f'Using sources: {sources}')
    print('JVM started')
    asset_api = BaseAsset(
        amidst_sources=sources,
        game_version=cli_arguments.game_version
    )
    if cli_arguments.show_versions:
        asset_api.print_versions()
        exit(0)
    print('Minecraft started successfully')
    asset_api.search_seeds()


if __name__ == '__main__':
    main()
