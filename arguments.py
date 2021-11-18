import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Data Minecraft')
    parser.add_argument('-v', '--version', type=str, nargs=1, default='1.16.1')
    parser.add_argument('-s', '--seed', type=list, nargs='?', default=[])
    parser.add_argument('-j', '--json', type=bool, nargs=1, default='true')
    parser.add_argument('-o', '--output', type=str, nargs=1, default=' ')
    parser.add_argument('-w', '--world-type', type=str, default='Default')
    parser.add_argument('-t', '--threads', type=int, nargs=1, default='8')
    return parser
