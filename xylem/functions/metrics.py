from ..utils import Fetcher
from pendulum import duration, date
import pandas as pd
import numpy as np


# α
def alpha(ri, symbol, start, stop):
    # R𝑚: Market Return
    # R𝑓: Risk Free Rate
    # R𝑖: Realized Return
    # R𝑒: Return of an individual stock

    rm = RM(start, stop)
    rf = RF(start, stop)
    b = beta(symbol, stop)

    # α = R𝑖 - (R𝑓 + (β * (R𝑚 - R𝑓)))
    a = ri - (rf + (b * (rm - rf)))
    return a

# β
def beta(symbol, stop):
    f = Fetcher()

    start = stop - duration(months=36)

    # rm = RM(start, stop)
    # rf = RF(start, stop)
    # re = RE(symbol, start, stop)

    re = f.fetch_barset(symbol=symbol, timespan='month', start=start, stop=stop)["c"]
    re = re.pct_change()[1:]
    rm = f.fetch_barset(symbol='SPY', timespan='month', start=start, stop=stop)["c"]
    rm = rm.pct_change()[1:]

    # covariance of the security's rate of return with respect to that of the market's
    # divided by the variance of the market's rate of return
    return re.cov(rm) / rm.cov(rm)

    # Here lies the Superior Numpy Solution, refused to be used by the inferior intellect
    # Austin Traver. Saturday, August 10, 2019.
    # ------------------------------------------------------------------- #
    # X = np.array([re, rm])
    # cov_matrix = np.cov(X)
    # # var_Re = cov_matrix[0][0]
    # cov_Re_Rm = cov_matrix[0][1]
    # # cov_Rm_Re = cov_matrix[1][0]
    # var_Rm = cov_matrix[1][1]
    # return cov_Re_Rm / var_Rm


# R𝑚: the market rate of return
def RM(start, stop):
    f = Fetcher()
    print("RM")
    print("initial_price")
    initial_price = f.last_price('SPY',start)
    print("final_price")
    final_price = f.last_price('SPY',stop)

    cumulative_return = (final_price - initial_price) / initial_price
    days_held = (stop - start).days
    annualized_return = (1 + cumulative_return)**(365.2 - days_held) - 1

    return annualized_return


# R𝑓: The risk-free rate of return
def RF(start, stop):
    f = Fetcher()

    print("RF")
    print("initial_price")
    initial_price = f.last_price('^TNX',start)
    print("final_price")
    final_price = f.last_price('^TNX',stop)

    cumulative_return = (final_price - initial_price) / initial_price
    days_held = (stop - start).days
    annualized_return = (1 + cumulative_return)**(365.2 - days_held) - 1

    return annualized_return


# R𝑒: The rate of return of a single security
def RE(symbol, start, stop):
    f = Fetcher()
    print("RE")
    print("initial_price")
    initial_price = f.last_price(symbol,start)
    print("final_price")
    final_price = f.last_price(symbol,stop)

    cumulative_return = (final_price - initial_price) / initial_price
    days_held = (stop - start).days
    annualized_return = (1 + cumulative_return)**(365.2 - days_held) - 1

    return annualized_return


# Beta Function

## Input Parameters
## (Remember, we can pull these from polygon at will)
## Historic aggregation, monthly candlesticks, ^GSPC
## Historic aggregation, monthly candlesticks, current_stock

## Take the dataframe for each of those two stocks, take their opening prices for each entry
## Map the covariance

