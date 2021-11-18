import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Broken Minecraft seeds finder')
    parser.add_argument('-v', '--version', type=str, nargs=1, default='1.16.1',
                        help='Minecraft version for analyzing. Snapshots are not supported')
    parser.add_argument('-s', '--seed', type=str, nargs='*', default=[])
    parser.add_argument('-j', '--json', default=False, action='store_true')
    parser.add_argument('-o', '--output', type=str, nargs=1, default=' ')
    parser.add_argument('-w', '--world-type', type=str, default='Default')
    parser.add_argument('-t', '--threads', type=int, nargs=1, default='8')
    return parser.parse_args()


arguments = create_parser()
