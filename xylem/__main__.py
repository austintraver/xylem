"""
Xylem. A backtesting platform...

Usage:
  xylem run -a ALGORITHM
  xylem (-h | --help)
  xylem --version

Options:
  -h --help                     Show this screen.
  -v --version                  Show version.
  -a --algorithm ALGORITHM      Path to algorithm configuration file.

"""
from docopt import docopt
from .backtest import Backtest

def run(args):
    """ Main routine. """
    Backtest(args['--algorithm'])

def main():
    args = docopt(__doc__, version='Xylem Version 0.0.1')

    modes = {
        'run': run
    }

    func = [modes[mode] for mode in modes if args[mode]][0]

    func(args)

if __name__ == "__main__":
    main()
