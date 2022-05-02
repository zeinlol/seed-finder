from core.config.minecraft_config import game, gen_opts
from core.game_classes.seeds import Seed


class GameInstance:
    _game_package = None
    _game_installation = None
    game_versions = []

    def __init__(self):
        self._game_package = game
        self._game_installation = \
            self._game_package.mojangapi.file.MinecraftInstallation.newLocalMinecraftInstallation()
        self.game_versions = list(self._game_installation.readInstalledVersionsAsLauncherProfiles())

    @property
    def get_biomes_list(self):
        return self._game_package.mojangapi.world.BiomeList.iterable()

    @property
    def default_world(self):
        return self._game_package.mojangapi.world.WorldType.DEFAULT

    @property
    def gen_opts(self):
        return gen_opts

    def create_silent_player_class(self):
        return self._game_package.mojangapi.world.WorldBuilder.createSilentPlayerless()

    def create_game(self, *args):
        try:
            return self._game_package.mojangapi.minecraftinterface.MinecraftInterfaces.fromLocalProfile(*args)
        except Exception as error:
            print(f'Java error:\n{error}')
            exit(1)

    def generate_random_seed(self):
        return self._game_package.mojangapi.world.WorldSeed.random()

    def convert_seeds(self, seeds: list) -> list[Seed]:
        return [self.convert_seed(seed) for seed in seeds]

    def convert_seed(self, seed) -> Seed:
        return Seed(game_value=self._game_package.mojangapi.world.WorldSeed.fromUserInput(seed), user_seed=seed)

    def get_world_options(self, seed, world_type=None, gen_options=None):
        if gen_options is None:
            gen_options = self.gen_opts
        if world_type is None:
            world_type = self.default_world
        return self._game_package.mojangapi.world.WorldOptions(seed, world_type, gen_options)
