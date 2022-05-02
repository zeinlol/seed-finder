from io import BytesIO
from itertools import count

import numpy as np

import database
from core import cli_arguments
from core.assets_classes.abstract_asset import AbstractAssetClass
from core.config.typing import T_BIOME_IDS
from core.config.variables import screen_width, screen_height
from core.game_classes.biome_class import GameBiome
from core.game_classes.game_data import GameInstance
from core.middleware.amidst_setup import get_assets_list
from core.middleware.filters.biom_lifters import filter_mesa


class BaseAsset(AbstractAssetClass):
    amidst_sources = None
    _game_instance = None
    game_versions: list = []
    game_version: str = ''
    _game_profile = None
    _game_interface = None
    _biomes_list: list[GameBiome] = []
    _seed = None
    _world = []

    def __init__(self, amidst_sources, game_version: str):
        try:
            self.amidst_sources = amidst_sources
            self._game_instance = GameInstance()
            self.game_version = game_version
            self.game_versions = self._game_instance.game_versions
            self.check_versions()
            self._game_interface = self._game_instance.create_game(self.get_game_profile())
        except (AttributeError, TypeError):
            print('Unsupported amidst version or error in sources')
            exit(1)

    @property
    def biomes_list(self):
        return self._biomes_list

    @property
    def seed(self):
        return self._seed

    def check_versions(self):
        try:
            self._game_profile = next(
                filter(lambda game_version: game_version.getVersionId() == self.game_version, self.game_versions))
        except StopIteration:
            print(f'Version {self.game_version} is not installed. You can use one of {self.game_versions}')

    def print_versions(self):
        print('Installed minecraft versions:')
        for version in self.game_versions:
            print(f'\t{version.getVersionId()}')

        print(f'\nInstalled amidst versions:')
        for asset in get_assets_list():
            print(f'\t{asset}')

    def get_game_profile(self):
        return self._game_profile

    def get_biomes_ids(self) -> T_BIOME_IDS:
        return [biome.biome_id for biome in self._biomes_list]

    def fill_biomes(self, biomes: list):
        for biome in biomes:
            self._biomes_list.append(GameBiome(biome_name=biome.getName(), biome_id=int(biome.getId())))

    def generate_new_world(self):
        self._seed = self._game_instance.generate_random_seed()
        options = self._game_instance.get_world_options(seed=self._seed)
        self._world = self._game_instance.create_silent_player_class().from_(self._game_interface, options)

        self.fill_biomes(self._world.getBiomeList().iterable())
        return self._world

    def get_biomes_data(self):
        try:  # for 4-5-beta3
            return self._world.getBiomeDataOracle()
        except AttributeError:  # for 4-5 and above
            return self._world.getOverworldBiomeDataOracle()

    def search_seeds(self):
        print('Found seeds:')
        for i in count():
            if i == cli_arguments.amount:
                break
            self.generate_new_world()
            try:
                biomes_info = self.get_biomes_data()  # v4-5-beta3
            except AttributeError as error:
                print(f'Incompatible game and asset version.'
                      f'\nGame version: {self.game_version}'
                      f'\nAsset version: {self.amidst_sources}')
                print(error)
                exit(1)

            def biome_val(x, y):
                return np.uint8(int(biomes_info.getBiomeAt(x, y, True).getId()))

            biome_data = np.fromfunction(np.vectorize(biome_val), (screen_width, screen_height), dtype=np.int64)

            if not filter_mesa(biome_data):
                with BytesIO() as tmp_file:
                    np.save(tmp_file, biome_data)
                    bin_data = tmp_file.getvalue()
                database.World.create(seed=self._seed.getLong(), biome_data=bin_data)

            print(i, self._seed.getLong())
