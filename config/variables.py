from os import path

screen_width = 1400
screen_height = 650
database_file = path.join('data', 'worlds.sqlite3')
amidst_file = 'amidst-v4-5-beta3.jar'


class ScanConfig:

    seeds_to_analyse = []

    def __init__(self):
        self.seeds_to_analyse = []
        self.game_version = ''

    @classmethod
    def update_seeds(cls, seeds):
        cls.seeds_to_analyse = cls.seeds_to_analyse.append(seeds)
        print(f'seeds for scanning: {cls.seeds_to_analyse}')


scan_config = ScanConfig()
