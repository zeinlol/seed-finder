from arguments import arguments
from core.middleware.check_input.cpu_analyze import check_cpu


def check_input() -> None:
    check_cpu()
    if arguments.output:
        ...
        # check_output_file()
    # check_game_version()
    # check_world_type()
