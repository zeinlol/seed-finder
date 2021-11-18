from arguments import arguments
from config.main_classes import scan_config
from core.middleware.check_input.cpu_analyze import check_cpu
from core.middleware.check_input.seeds import get_seeds_from_cli


def check_input() -> None:
    check_cpu()
    if arguments.output:
        ...
        # check_output_file()
    # check_game_version()
    # check_world_type()
