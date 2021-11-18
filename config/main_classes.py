from core.middleware.check_input.seeds import get_seeds_from_cli


class ScanConfig:

    def __init__(self, seed_list):
        self.seeds_to_analyse = seed_list
        self.game_version = ''

    def update_seeds(self, seeds):
        seeds_to_analyse = self.seeds_to_analyse.append(seeds)
        print(f'seeds for scanning: {self.seeds_to_analyse}')

    def get_seeds(self):
        return self.seeds_to_analyse


scan_config = ScanConfig(get_seeds_from_cli())
