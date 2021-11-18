from arguments import arguments
from config.variables import scan_config
from core.middleware.check_input.cpu_analyze import check_cpu
from core.middleware.check_input.seeds import get_seeds_from_cli


def check_input() -> None:
    if arguments.seed:
        scan_config.update_seeds = get_seeds_from_cli()
    check_cpu()
    if arguments.output:
        ...
        # check_output_file()
    # check_game_version()
    # check_world_type()
