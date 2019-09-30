import os
import random
import time
from six import exec_
from ..utils.fetcher import *
import yaml
import json


class TestAlgorithm:
    def __init__(self, algo):

        self.config = dict()
        with open(algo, "r") as yml:
            try:
                self.config = yaml.safe_load(yml)
            except yaml.YAMLError as error:
                print(error)

        algo = self.load_algorithm()
        tests = self.parse_tests()

        for i in range(0, len(tests)):
            t = ExecuteTest(
                self.config["equity"],
                tests[i],
                self.config["context"],
                self.config["statistics"],
                algo)
            t.execute()
            t.save_result_set(
                self.config["output"],
                f"test_{str(i+1)}.json")

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
            single_test["date_range_start"] = test_list[test_list.index(
                "FROM") + 1]
            single_test["date_range_end"] = test_list[test_list.index(
                "TO") + 1]

            tests.append(single_test)

        return tests

    def load_algorithm(self):
        algo_string, algo_name = self.read_algo(self.config["algorithm"])

        code = compile(algo_string, algo_name, 'exec')

        namespace = dict()
        exec_(code, namespace)

        def nofunc(*args, **kwargs):
            pass

        return {
            "compute": namespace.get("compute", nofunc),
            "before_exit": namespace.get("before_exit", nofunc),
            "analyze": namespace.get("analyze", nofunc)
        }

    def read_algo(self, algo):
        algo_str = ""

        # Support for windows paths??
        algo_list = algo.strip().split("/")
        algo_name = algo_list[len(algo_list) - 1]

        with open(algo, "r") as f:
            algo_str = f.read()

        return algo_str, algo_name


class ExecuteTest:
    def __init__(self, equity, test_config, context, stats, algo):
        self.test_config = test_config
        self.context = context
        self.stats = stats
        self.algo = algo
        self.equity = equity
        self.current_candle = None
        self.current_time = None
        self.start_time = None
        self.stop_time = None

        # Test Data
        self.portfolio = 0  # Value of all stocks held
        self.wallet = equity
        self.orders = list()

        # Result Set
        self.result_set = list()

    def execute(self):
        barsets = list()
        for symb in self.test_config["symbols"]:
            context = self.context

            # NOTE look at how we're generating statistics
            stats = self.get_data_with_stats(symb)
            barsets.append(stats)

            f_stats = dict()
            for index, row in stats.iterrows():
                self.current_candle = row
                self.current_time = index
                for stat in self.stats:
                    if stat != "CANDLE":
                        f_stats[stat] = row[stat]
                    else:
                        f_stats["CANDLE"] = row

                self.algo["compute"](context, f_stats, self.order)

            # Run Before Exit
            self.algo["before_exit"](context, f_stats, self.order)

            result = dict({
                "symbol": symb,
                "orders": self.orders,
                "starting_balance": self.equity,
                "ending_balance": self.wallet,
                "start_time": self.start_time,
                "stop_time": self.stop_time
            })

            self.result_set.append(result)
            print("=======================================")
            print(f"Summary Statistics ({symb})")
            print("=======================================")
            print(f"Start Time: {self.start_time}")
            print(f"Stop Time: {self.stop_time}")
            print(f"Starting Balance: ${self.equity:.2f}")
            print(f"Ending Balance: ${self.wallet:.2f}")
            print("=======================================\n")

            # Reset for next symbol
            self.wallet = self.equity
            self.buys = list()
            self.sells = list()
        # End of all symbol tests
        self.algo["analyze"](self.result_set, barsets)

    def get_data_with_stats(self, symb):
        barset = self.fetch_data(symb)

        if "EMA12" in self.stats:
            barset["EMA12"] = barset["o"].ewm(span=12).mean()

        if "EMA26" in self.stats:
            barset["EMA26"] = barset["o"].ewm(span=26).mean()

        return barset

    def fetch_data(self, symbol):
        start = self.test_config["date_range_start"]
        stop = self.test_config["date_range_end"]

        self.start_time = start
        self.stop_time = stop

        return fetch_barset(
            symbol=symbol,
            timespan='minute',
            start=start,
            stop=stop)

    def save_result_set(self, output, file_name):

        if not os.path.exists(output):
            os.makedirs(output)

        ofile = open(os.path.join(output, file_name), 'w')
        # yaml.dump(self.result_set, ofile, default_flow_style=false)
        json.dump(self.result_set, ofile)

    def order(self, order_size=0, *, liquidate=False):

        current_price = self.current_candle["o"]

        if liquidate:
            # Order size should be the opposite of our current position
            order_size = self.portfolio * -1

        # Catch an invalid set of arguments passed to order()
        elif order_size == 0:
            raise ValueError("Order placed for 0 stocks")

        # Subtract the cost of this order from the wallet
        self.wallet -= (order_size * current_price)

        # Adjust balance +/- amount of stocks owned
        self.portfolio += order_size

        # Add to the list of total orders
        order = {
            "time": str(self.current_time),
            "amount": order_size,
            "price": current_price
        }

        self.orders.append(order)
