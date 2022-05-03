from pathlib import Path

BASE_DIR = Path(__file__).parents[3]

DATABASE_DIR = BASE_DIR.joinpath('data')
BIOME_PROFILE = BASE_DIR.joinpath('core', 'config', 'default_biome_profile.json')
DEFAULT_IMAGE_PATH = BASE_DIR.joinpath('images')
