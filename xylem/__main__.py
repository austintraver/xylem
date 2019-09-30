from argparse import ArgumentParser
from .backtest import TestAlgorithm


def run(args):
    """ Main routine. """


def main():
    parser = ArgumentParser(
        prog="\x1b[32;1mxylem\x1b[0m",
        usage="%(prog)s -a \x1b[1;34m<algo.yml>\x1b[0m",
        description="%(prog)s: a backtesting platform"
    )

    parser.add_argument(
        "-a",
        "--algorithm",
        dest="algorithm",
        metavar="\x1b[34;1m<algo.yml>\x1b[0m",
        required=True,
        help="path to the algorithm configuration file"
    )

    args = parser.parse_args()

    TestAlgorithm(args.algorithm)

if __name__ == "__main__":
    main()
