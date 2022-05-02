import argparse

from core.config.variables import minecraft_version, amidst_file


def create_parser():
    parser = argparse.ArgumentParser(description='Seed finder')
    parser.add_argument('-gv', '--game-version', type=str, default=minecraft_version,
                        help='Minecraft version. Use --show-versions to see installed. Default is 1.16.1')
    parser.add_argument('-src', '--sources', type=str, default=amidst_file,
                        help='Amidst sources path. You can put them in assets folder or specify path to file. '
                             f'Default: {amidst_file}')
    parser.add_argument('-s', '--seeds', type=str, nargs='*', default=[],
                        help='Seeds to analyze world')
    parser.add_argument('-b', '--biomes', type=str, nargs='*', default=['Badlands'],
                        help="Search for biome name. Case doesn't matter. Can be more than one."
                             " Can search by part of name.\n"
                             "If 'Badlands' than search for 'Eroded Badlands', 'Modified Badlands Plateau'...\n"
                             'Default is Badlands. Run --show-biomes to see all possible values.')
    # parser.add_argument('-w', '--world-type', type=str, default='Default',
    #                     help='World type')
    parser.add_argument('-a', '--amount', type=int, default=-1,
                        help='Amount of seeds to find. Default: infinity')
    #    parser.add_argument('-j', '--json', default=False, action='store_true',
    #                        help='show data as json')
    #    parser.add_argument('-o', '--output', type=Path, default=None,
    #                        help='File to save data')
    parser.add_argument('-sv', '--show-versions', default=False, action='store_true',
                        help='See installed minecraft and sources versions and exit')
    parser.add_argument('-sb', '--show-biomes', default=False, action='store_true',
                        help='See possible minecraft biomes and exit')
    return parser.parse_args()


cli_arguments = create_parser()
