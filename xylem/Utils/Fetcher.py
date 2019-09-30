import alpaca_trade_api
from os import getenv
import pandas as pd
from pendulum import duration, datetime

public_key = getenv("APCA_API_KEY_ID")
private_key = getenv("APCA_API_SECRET_KEY")

if type(public_key) is None or type(private_key) is None:
    raise KeyError("Alpaca API keys not found in shell environment")

api = alpaca_trade_api.REST(
    public_key,
    private_key,
    api_version='v2')


def fetch_barset(symbol, timespan, start, stop=None, limit=None):
    start = start.format('YYYY-M-D')
    stop = stop.format('YYYY-M-D')

    barset = api.polygon.historic_agg_v2(
        symbol=symbol,
        multiplier=1,
        timespan=timespan,
        _from=start,
        to=stop).df

    barset.index = pd.to_datetime(barset.index, unit='ms', origin="unix")
    return barset


def fetch_price(symbol, date):
    date = date.format('YYYY-M-D')
    barset = api.polygon.historic_trades(symbol, date, limit=1).df
    price = barset["price"][0]
    # price = barset[1]
    return price


def last_price(symbol, date):
    try:
        return fetch_price(symbol, date)
    except TypeError as error:
        print(error)
        # change date back a day
        date -= duration(days=1)
        print("Error: New date is ", date)
        return last_price(symbol, date)

__all__ = ["fetch_barset", "fetch_price", "last_price"]
