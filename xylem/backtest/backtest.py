import os
import random
import time
import yaml
import json
from six import exec_
from ..tickers import *

class Backtest:
    def __init__(self, algo):

        self.__algo = algo
        self.__current_candle = None
        self.__current_time = None

        # Test Data
        self.__portfolio = 0 # Value of all stocks held
        self.__buys = []
        self.__sells = []
        self.__orders = []

        # Result Set 
        self.__result_set = []

        self.__config = yaml.load(open(algo, "r"))

        self.__equity = self.__config["equity"]
        self.__context = self.__config["context"]
        self.__stats = self.__config["statistics"]

        test = self.__parse_tests()

        for i in range(len(test)):
            result = self.execute(test[i])
            print(result)
            json.dump(result, 'test_{0:d}.yml'.format(str(i)))


    def __parse_tests(self):
        
        tests = []
        for test in self.__config["tests"]:
            test_list = test.strip().split(" ")

            single_test = {}
            # Evaluate tickers
            tickers = test_list[test_list.index("TEST") + 1]
            
            if "," in tickers:
                tickers = tickers.strip().split(",")
                single_test["tickers"] = tickers
            elif tickers == "*":
              # Pull the S&P 500 stock tickers
                single_test["tickers"] = gspc
            else:
                single_test["tickers"] = [tickers]

            # Check if we should select dates randomly
            if "RANDOM" in test_list:
                single_test["random_selection"] = True
            else:
                single_test["random_selection"] = False
            
            # Find date range
            single_test["date_range_start"] = test_list[test_list.index("FROM") + 1]
            single_test["date_range_end"] = test_list[test_list.index("TO") + 1]

            # Find duration
            single_test["duration_number"] = test_list[test_list.index("DURATION") + 1]
            single_test["duration_type"] = test_list[test_list.index("DURATION") + 2]

            # Find attempts
            single_test["attempts"] = test_list[test_list.index("ATTEMPT") + 1]

            tests.append(single_test)

        return tests

    def __load_algorithm(self):
        algo_string, algo_name = self.__read_algo(self.__config["algorithm"])

        code = compile(algo_string, algo_name, 'exec')

        namespace = {}
        exec_(code, namespace)

        def nofunc(*args, **kwargs): pass
        
        return {
            "compute": namespace.get("compute", nofunc),
            "before_exit": namespace.get("before_exit", nofunc),
            "analyze": namespace.get("analyze", nofunc)
        }

    def __read_algo(self, algo):
        algo_str = ""
        
        # Support for windows paths??
        algo_list = algo.strip().split("/")
        algo_name = algo_list[len(algo_list) - 1]

        algo_str = open(algo, "r").read()
        return algo_str, algo_name


    def execute(self, test):

        # TODO Add support for multiple attempts
        for symb in gspc: 

            buys = []
            sells = []

             # Reset for next symbol
            self.__wallet = self.__equity

            stats = self.__get_data_with_stats(symb)

            f_stats = {}
            for index, row in stats.iterrows():
                self.__current_candle = row
                self.__current_time = index
                for stat in stats:
                    f_stats[stat] = row[stat]

                self.__algo["compute"](self.__context, f_stats, self.order)

            # Run Before Exit
            self.__algo["before_exit"](self.__context, f_stats, self.order)

            # Save Result
            result = {
                "ticker": symb,
                "buys": buys,
                "sells": sells, 
                "orders": self.__orders, 
                "wallet": self.__wallet,
                "portfolio": self.__equity,
            }

            self.__result_set.append(result)

            return(get_stats(result))


        # End of all symbol tests    
        self.__algo["analyze"](self.__result_set)

    def __get_data_with_stats(self, symb):
        barset = self.__fetch_data(symb)

        if "EMA12" in self.__stats:
            barset["EMA12"] = barset["o"].ewm(span=12).mean()
        
        if "EMA26" in self.__stats:
            barset["EMA26"] = barset["o"].ewm(span=26).mean()
        
        return barset

    def __fetch_data(self, symb):
        s = self.__config["date_range_start"]
        e = self.__config["date_range_end"]

        # TODO Regardless of config it always selects randomly
        # TODO Add support for durations longer than a month
        rand_s, rand_e = self.__random_date(s, e, random.random())
        
        return get_barset(ticker=symb, timespan='minute', start=rand_s, stop=rand_e)

    def __random_date(self, start, end, prop):
        format_str = "%Y-%m-%d"
        seconds_in_month = 2592000

        stime = time.mktime(time.strptime(start, format_str))
        etime = time.mktime(time.strptime(end, format_str))

        sptime = stime + prop * (etime - stime)
        eptime = sptime + seconds_in_month

        return time.strftime(format_str, time.localtime(sptime)), time.strftime(format_str, time.localtime(eptime))


    def order(self, order_size=0, *, all_in=False, liquidate=False):

        current_price = self.__current_candle["o"]

        if all_in:
            # Ensure that the order_size for all_in() is +/- 1
            if order_size in [-1, 1]:
                # Calculate max # of stocks we can long/short @ current price...
                order_size *= self.__wallet // current_price
                
            else:
                raise ValueError("Order is all_in but != +/- 1")
            
        elif liquidate:
            # Order size should be the opposite of our current position
            order_size = self.__portfolio * -1
        
        # Catch an invalid set of arguments passed to order()
        elif order_size == 0:
            raise ValueError("Order placed for 0 stocks")
            
        # Subtract the cost of this order from the wallet
        self.__wallet -= (order_size * current_price)
        
        # Adjust balance +/- amount of stocks owned
        self.__portfolio += order_size
        
        # Add to the list of total orders
        order = {
            "time": str(self.__current_time),
            "amount": order_size,
            "price": current_price
        }
        
        self.__orders.append(order)
