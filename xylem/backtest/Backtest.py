from os import makedirs
from json import *
from ..utils.fetcher import *
from posixpath import *
from importlib.util import *


class Backtest:
    def __init__(self, *,
    config, context, stats, equity, algorithm, output, filename):

        # Load algorithm to backtest into the namespace "algo"
        spec = spec_from_file_location("algorithm", algorithm)
        self.algorithm = module_from_spec(spec)
        spec.loader.exec_module(self.algorithm)

        self.config = config
        self.context = context
        self.stats = stats
        self.equity = equity

        self.current_candle = None
        self.current_time = None
        self.start = None
        self.stop = None

        self.portfolio = 0  # Value of all stocks held
        self.wallet = self.equity
        self.orders = list()
        self.results = list()

        self.execute()

        self.save_results(
            directory=output,
            filename=filename)

    def execute(self):
        barsets = list()
        for symb in self.config["symbols"]:
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

                self.algorithm.compute(context, f_stats, self.order)

            # Run Before Exit
            self.algorithm.before_exit(context, f_stats, self.order)

            result = dict({
                "symbol": symb,
                "orders": self.orders,
                "starting_balance": self.equity,
                "ending_balance": self.wallet,
                "start": self.start,
                "stop": self.stop,
            })

            self.results.append(result)
            print("=======================================")
            print(f"Summary Statistics ({symb})")
            print("=======================================")
            print(f"Start Time: {self.start}")
            print(f"Stop Time: {self.stop}")
            print(f"Starting Balance: ${self.equity:.2f}")
            print(f"Ending Balance: ${self.wallet:.2f}")
            print("=======================================\n")

            # Reset for next symbol
            self.wallet = self.equity
            self.buys = list()
            self.sells = list()
        # End of all symbol tests
        self.algorithm.analyze(self.results, barsets)

    def get_data_with_stats(self, symbol):
        barset = self.fetch_data(
            symbol=symbol,
            start=self.config["start"],
            stop=self.config["stop"])

        if "EMA12" in self.stats:
            barset["EMA12"] = barset["o"].ewm(span=12).mean()

        if "EMA26" in self.stats:
            barset["EMA26"] = barset["o"].ewm(span=26).mean()

        return barset

    def fetch_data(self, *, symbol, start, stop):

        self.start = start
        self.stop = stop

        return fetch_barset(
            symbol=symbol,
            timespan='minute',
            start=start,
            stop=stop)

    def save_results(self, *, directory, filename):

        if not exists(directory):
            makedirs(directory)

        ofile = open(join(directory, filename), 'w')

        dump(self.results, ofile)

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
