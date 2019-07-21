import pandas as pd
from json import load
from os import environ, path
from alpaca_trade_api import REST as alpaca

# Constant: the S&P-500 (^GSPC) tickers
# 505 tickers, comprising of the 500 largest US-traded companies
gspc = load(open(path.join(path.dirname(path.abspath(__file__)),'gspc.json'), 'r'))

# Constant: the NASDAQ-100 (^NDX) tickers
# 103 tickers, comprising of 100 largest NASDAQ-traded companies
ndx = load(open(path.join(path.dirname(path.abspath(__file__)), 'ndx.json'), 'r'))

# Constant: the Dow-Jones (^DJI) tickers
dji = load(open(path.join(path.dirname(path.abspath(__file__)), 'dji.json'), 'r'))

def get_barset(ticker, timespan, start, stop):

    api = alpaca(environ['APCA_API_KEY_ID'], environ['APCA_API_SECRET_KEY'])
    barset = api.polygon.historic_agg_v2(timespan=timespan, multiplier='1', symbol=ticker, _from=start, to=stop).df
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
