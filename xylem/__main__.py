from argparse import ArgumentParser
from .backtest import *


# def run(args):
# """ Main routine. """


def main():
    parser = ArgumentParser(
        prog="\x1b[32;1mxylem\x1b[0m",
        usage="%(prog)s -a \x1b[1;34m<algo.yml>\x1b[0m",
        description="%(prog)s: a backtesting platform"
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        metavar="\x1b[34;1m<config.yml>\x1b[0m",
        required=True,
        help="path to the config file"
    )

    parser.add_argument(
        "-a",
        "--algorithm",
        dest="algorithm",
        metavar="\x1b[34;1m<algorithm.py>\x1b[0m",
        required=True,
        help="path to the algorithm file"
    )

    parser.add_argument(
        "-e",
        "--equity",
        dest="equity",
        metavar="\x1b[34;1m<9001>\x1b[0m",
        type=int,
        required=False,
        help="starting amount of equity in the portfolio"
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        metavar="\xc1b[34;1m</path/to/output/dir>\x1b[0m",
        required=False,
        help="path to directory to output xylem results")

    args = parser.parse_args()

    Algorithm(
        config=args.config,
        algorithm=args.algorithm,
        equity=args.equity,
        output=args.output)


if __name__ == "__main__":
    main()
