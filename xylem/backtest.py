import yaml
import os
from six import exec_
from .Utils.Fetcher import Fetcher
from .Utils.Result import Result

class TestAlgorithm:
    def __init__(self, algo):
        
        self.__config = {}
        with open(algo, "r") as yml:
            try:
                self.__config = yaml.safe_load(yml)
            except yaml.YAMLError as e:
                print(e)

        algo = self.__load_algorithm()

        tests = self.__parse_tests()

        i = 1
        for test in tests:
            t = ExecuteTest(self.__config["equity"], test, self.__config["context"],
                            self.__config["statistics"], algo)
            t.execute()
            t.save_result_set(self.__config["output"], "test_" + str(i) + ".json")

            i += 1


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
                single_test["tickers"] = ['MMM', 'ABT', 'ABBV', 'ACN', 'ATVI', 'AYI', 'ADBE', 'AMD', 'AAP', 'AES', 'AET', 'AMG', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'AGN', 'ADS', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'ANDV', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'AIV', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ARNC', 'AJG', 'AIZ', 'T', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BHGE', 'BLL', 'BAC', 'BK', 'BAX', 'BBT', 'BDX', 'BRK.B', 'BBY', 'BIIB', 'BLK', 'HRB', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BHF', 'BMY', 'AVGO', 'BF.B', 'CHRW', 'CA', 'COG', 'CDNS', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CAT', 'CBOE', 'CBRE', 'CBS', 'CELG', 'CNC', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CXO', 'COP', 'ED', 'STZ', 'COO', 'GLW', 'COST', 'COTY', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DOV', 'DWDP', 'DPS', 'DTE', 'DRE', 'DUK', 'DXC', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ETR', 'EVHC', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FL', 'F', 'FTV', 'FBHS', 'BEN', 'FCX', 'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GS', 'GT', 'GWW', 'HAL', 'HBI', 'HOG', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HP', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HPQ', 'HUM', 'HBAN', 'HII', 'IDXX', 'INFO', 'ITW', 'ILMN', 'IR', 'INTC', 'ICE', 'IBM', 'INCY', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JEC', 'JBHT', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KHC', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LEG', 'LEN', 'LUK', 'LLY', 'LNC', 'LKQ', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MTD', 'MGM', 'KORS', 'MCHP', 'MU', 'MSFT', 'MAA', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NKTR', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'PCAR', 'PKG', 'PH', 'PAYX', 'PYPL', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RJF', 'RTN', 'O', 'RHT', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RCL', 'CRM', 'SBAC', 'SCG', 'SLB', 'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SPGI', 'SWK', 'SBUX', 'STT', 'SRCL', 'SYK', 'STI', 'SIVB', 'SYMC', 'SYF', 'SNPS', 'SYY', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'FTI', 'TXN', 'TXT', 'TMO', 'TIF', 'TWX', 'TJX', 'TMK', 'TSS', 'TSCO', 'TDG', 'TRV', 'TRIP', 'FOXA', 'FOX', 'TSN', 'UDR', 'ULTA', 'USB', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']
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
            "before_exit": namespace.get("before_exit", nofunc)
        }

    def __read_algo(self, algo):
        algo_str = ""
        
        # Support for windows paths??
        algo_list = algo.strip().split("/")
        algo_name = algo_list[len(algo_list) - 1]

        with open(algo, "r") as f:
            algo_str = f.read()

        return algo_str, algo_name

class ExecuteTest:
    def __init__(self, equity, test_config, context, stats, algo):
        self.__test_config = test_config
        self.__context = context
        self.__stats = stats
        self.__algo = algo
        self.__equity = equity

        # Test Data
        self.__wallet = equity
        self.__buys = []
        self.__sells = []

        # Result Set 
        self.__result_set = []

    def execute(self):
        for symb in self.__test_config["tickers"]:
            context = self.__context

            stats = self.__get_data_with_stats(symb)

            f_stats = {}
            for index, row in stats.iterrows():
                self.__current_candle = row

                for stat in self.__stats:
                    f_stats[stat] = row[stat]

                self.__algo["compute"](context, f_stats, self.order)

            # Run Before Exit
            self.__algo["before_exit"](context, f_stats, self.order)

            # Save Result
            r = Result(symb, self.__buys, self.__sells, self.__equity, self.__wallet)
            self.__result_set.append(r)
            r.printResult()

            # Reset for next symbol
            self.__wallet = self.__equity
            self.__buys = []
            self.__sells = []

    def __get_data_with_stats(self, symb):
        barset = self.__fetch_data(symb)

        if "EMA12" in self.__stats:
            barset["EMA12"] = barset["o"].ewm(span=12).mean()
        
        if "EMA26" in self.__stats:
            barset["EMA26"] = barset["o"].ewm(span=26).mean()
        
        return barset

    def __fetch_data(self, symb):
        f  = Fetcher()
        s = self.__test_config["date_range_start"]
        e = self.__test_config["date_range_end"]
        
        return f.fetch_barset(ticker=symb, timespan='minute', start=s, stop=e)

    def save_result_set(self, output, file_name):
        if not output.strip().endswith("/"):
            output += ("/")
        
        if not os.path.exists(output):
            os.makedirs(output)
        
        with open(output + file_name, 'w') as f:
            json_str = "["
            for res in self.__result_set:
                json_str += res.json()
                json_str += ","
            
            json_str = json_str[:-1]
            json_str += "]"

            f.write(json_str)

    def order(self, amount):
        self.__wallet += (amount * self.__current_candle["o"])

        if amount > 0:
            self.__buys.append(self.__current_candle)
        elif amount < 0:
            self.__sells.append(self.__current_candle)
        
        