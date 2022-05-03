from io import BytesIO
from itertools import count

import numpy as np
import peewee

import database
from core import cli_arguments
from core.assets_classes.abstract_asset import AbstractAssetClass
from core.config.typing import T_BIOME_IDS, T_TARGET_BIOMES_NAMES, T_TARGET_BIOME_NAME
from core.game_classes.biome_class import GameBiome
from core.game_classes.game_data import GameInstance
from core.game_classes.seeds import Seed
from core.middleware.amidst_setup import get_assets_list
from core.middleware.filters.biom_lifters import filter_biome


class BaseAsset(AbstractAssetClass):
    amidst_sources = None
    _game_instance = None
    game_versions: list = []
    game_version: str = ''
    _game_profile = None
    _game_interface = None
    _biomes_list: list[GameBiome] = []
    _target_biomes: list[GameBiome] = []
    _current_seed = None
    _seeds: list[Seed] = None
    _world = []

    def __init__(self, amidst_sources, game_version: str = None):
        try:
            self.amidst_sources = amidst_sources
            self._game_instance = GameInstance()
            self.game_version = game_version or cli_arguments.game_version
            self.game_versions = self._game_instance.game_versions
            self.check_versions()
            self._game_interface = self._game_instance.create_game(self.get_game_profile())
            if cli_arguments.seeds:
                self._seeds = self._game_instance.convert_seeds(cli_arguments.seeds)
            self.generate_idle_world()
            self.fill_target_biomes(cli_arguments.biomes)
        except (AttributeError, TypeError) as error:
            print(f'Unsupported amidst version or error in sources\n{error}')
            exit(1)

    @property
    def biomes_list(self) -> list[GameBiome]:
        return self._biomes_list

    @property
    def target_biomes_names(self) -> list[str]:
        return [biome.biome_name for biome in self._target_biomes]

    @property
    def seed_number(self):
        return self._current_seed.getLong()

    @property
    def seed(self):
        return self._current_seed

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

    def print_biomes(self):
        print(f'Biomes in minecraft {self.game_version}:')
        for biome in self.biomes_list:
            print(f'\t{biome.biome_id}: {biome.biome_name}')

    def get_game_profile(self):
        return self._game_profile

    def get_biomes_ids(self) -> T_BIOME_IDS:
        return [biome.biome_id for biome in self._biomes_list]

    def fill_biomes(self, biomes: list):
        for biome in biomes:
            self._biomes_list.append(GameBiome(biome_name=str(biome.getName()), biome_id=int(biome.getId())))

    def fill_target_biomes(self, target_names: T_TARGET_BIOMES_NAMES):
        for biome_name in target_names:
            biome_name: T_TARGET_BIOME_NAME = biome_name.lower()
            target_biomes = list(filter(lambda biome: biome_name in biome.biome_name.lower(), self._biomes_list))
            self._target_biomes.extend(target_biomes)

    def generate_idle_world(self):
        print('Generating idle world...')
        self.generate_new_world()
        print('Idle world generated')

    def generate_new_world(self, seed=None):
        if seed is None:
            seed = self._game_instance.generate_random_seed()
        self._current_seed = seed
        options = self._game_instance.get_world_options(seed=self._current_seed)
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
        if self._seeds:
            self.check_user_seeds()
            return
        for i in count():
            if i == cli_arguments.amount:
                break
            try:
                result = 'Contains looked data!' if self.check_world() else '-'
                if result != '-' and cli_arguments.silent:
                    print(f'{i} {result} Seed: {self.seed_number}')
            except Exception as error:
                print(f'Error on analyzing seed {self.seed_number}:\n{error}')

    def check_user_seeds(self):
        for key, seed in enumerate(self._seeds):
            try:
                result = 'Contains looked data!' if self.check_world(seed=seed.game_value) else '-'
                if result != '-' and cli_arguments.silent:
                    print(f'{key} {result} Seed: {seed.input_value} (was converted to {seed.game_value.getLong()})')
            except Exception as error:
                print(f'{key} Error on analyzing seed  {seed.input_value} '
                      f'(was converted to {seed.game_value.getLong()}):\n{error}')
        print('Analyze finished successfully')

    def check_world(self, seed=None):
        if seed is None:
            seed = self._game_instance.generate_random_seed()
        self.generate_new_world(seed=seed)
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

        biome_data = np.fromfunction(np.vectorize(biome_val), (cli_arguments.size_x, cli_arguments.size_y), dtype=np.int64)

        if not filter_biome(biomes_array=biome_data, target_biome=self._target_biomes):
            with BytesIO() as tmp_file:
                np.save(tmp_file, biome_data)
                bin_data = tmp_file.getvalue()
            try:
                database.World.create(seed=seed.getLong(), biome_data=bin_data)
            except peewee.IntegrityError:
                print(f'ERROR: {seed.getLong()} already created')
            return True
        return False
