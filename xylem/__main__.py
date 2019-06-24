import argparse
from .backtest import TestAlgorithm

def run():
    """ Main routine. """
    # Parse CL Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algo", help="Path to the algorithm YAML file.",
                        required=True, type=str)

    args = parser.parse_args()

    TestAlgorithm(args.algo)
    
if __name__ == "__main__":
    run()