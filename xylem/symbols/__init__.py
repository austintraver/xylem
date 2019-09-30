import pandas as pd
from yaml import safe_load as load
from os import environ
from posixpath import join, dirname, abspath
from alpaca_trade_api import REST as alpaca

# Constant: the S&P-500 (^GSPC) symbols
# 505 tickers, comprising of the 500 largest US-traded companies
SPX = load(open(join(dirname(abspath(__file__)), 'spx.yml'), 'r'))

# Constant: the NASDAQ-100 (^NDX) symbols
# 103 tickers, comprising of 100 largest NASDAQ-traded companies
NDX = load(open(join(dirname(abspath(__file__)), 'ndx.yml'), 'r'))

# Constant: the Dow-Jones (^DJI) symbols
DJI = load(open(join(dirname(abspath(__file__)), 'dji.yml'), 'r'))

# Only for debugging: Don't run this program directly
if __name__ == "__main__":
    print(__file__)
    print(SPX, "\n")
    print(NDX, "\n")
    print(DJI, "\n")
