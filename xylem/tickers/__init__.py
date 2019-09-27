import pandas as pd
from yaml import safe_load as load
from os import environ
from posixpath import join, dirname, abspath
from alpaca_trade_api import REST as alpaca

# Constant: the S&P-500 (^GSPC) tickers
# 505 tickers, comprising of the 500 largest US-traded companies
SPX = load(open(join(dirname(abspath(__file__)), 'spx.yml'), 'r'))

# Constant: the NASDAQ-100 (^NDX) tickers
# 103 tickers, comprising of 100 largest NASDAQ-traded companies
NDX = load(open(join(dirname(abspath(__file__)), 'ndx.yml'), 'r'))

# Constant: the Dow-Jones (^DJI) tickers
DJI = load(open(join(dirname(abspath(__file__)), 'dji.yml'), 'r'))

def get_barset(ticker, timespan, start, stop):

    api = alpaca(environ['APCA_API_KEY_ID'], environ['APCA_API_SECRET_KEY'], api_version='v2')
    barset = api.polygon.historic_agg(timespan=timespan, multiplier='1', symbol=ticker, _from=start, to=stop).df
    barset.index = pd.to_datetime(barset.index, unit='ms', origin="unix")
    return barset

def get_stats(result):
        summary = ("\
        =======================================\
        Summary Statistics [{ticker}]:\
        =======================================\
        Number of Buys: {buys}\
        Number of Sells: {sells}\
        Starting Balance: {starting_balance:.2f}\
        Ending Balance: {ending_balance:.2f}\
        =======================================")
        # Replace any templated variables with those in the supplied dictionary
        return(summary.format(**result))

# Only for debugging: Don't run this program directly
if __name__ == '__main__':
    print(__file__)
    print(gspc,"\n")
    print(ndx,"\n")
    print(dji,"\n")
