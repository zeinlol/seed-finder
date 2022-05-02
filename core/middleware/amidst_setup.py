from pathlib import Path

from core import cli_arguments
from core.config.constants.core import BASE_DIR


def get_assets_list() -> list[Path]:
    main_path = BASE_DIR.joinpath('assets').glob('*')
    return [asset for asset in main_path if asset.is_file() and 'amidst-' in asset.name]


def get_target_asset(asset_name: str) -> str:
    assets_list = get_assets_list()
    if cli_arguments.sources:
        if str(Path(cli_arguments.sources).parent) == '.':
            asset_name = cli_arguments.sources
        else:
            return cli_arguments.sources
    try:
        target_asset = next(filter(lambda asset: asset.name == asset_name, assets_list))
        return target_asset.as_posix()
    except StopIteration:
        print(f'Amidst {asset_name} not found')
        exit(1)
