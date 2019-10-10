from yaml import safe_load as load
from six import exec_
from .Backtest import Backtest
from posixpath import *
from importlib.util import *


class Algorithm:
    def __init__(self, *, config, algorithm, equity, output):
        ifile = open(config, "r")
        self.config = load(ifile)

        tests = self.parse_tests()

        for i in range(0, len(tests)):
            Backtest(
                equity=equity,
                config=tests[i],
                context=self.config["context"],
                stats=self.config["statistics"],
                algorithm=algorithm,
                output=output,
                filename=f"test_{str(i+1)}.json")

    def parse_tests(self):

        tests = list()
        for test in self.config["tests"]:
            test_list = test.strip().split(" ")

            single_test = dict()
            # Evaluate tickers
            symbols = test_list[test_list.index("TEST") + 1]

            if "," in symbols:
                symbols = symbols.strip().split(",")
                single_test["symbols"] = symbols
            elif symbols == "*":
                from ..symbols import SPX
                single_test["symbols"] = SPX
            else:
                single_test["symbols"] = [symbols]

            # Find date range
            single_test["start"] = test_list[test_list.index(
                "FROM") + 1]
            single_test["stop"] = test_list[test_list.index(
                "TO") + 1]

            tests.append(single_test)

        return tests
