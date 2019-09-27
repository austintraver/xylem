import alpaca_trade_api as tapi
import os
import pandas as pd
from pendulum import duration, datetime

class Fetcher:
    def __init__(self):
        self.__api = tapi.REST(os.environ['APCA_API_KEY_ID'],
                               os.environ['APCA_API_SECRET_KEY'],
                               api_version='v2')

    def fetch_barset(self, symbol, timespan, start, stop=None, limit=None):
        start = start.format('YYYY-M-D')
        stop = stop.format('YYYY-M-D')
        barset = self.__api.polygon.historic_agg_v2(symbol=symbol, multiplier=1, timespan=timespan, _from=start, to=stop).df
        barset.index = pd.to_datetime(barset.index, unit='ms', origin="unix")
        return barset

    def fetch_price(self, symbol, date):
        date = date.format('YYYY-M-D')
        barset = self.__api.polygon.historic_trades(symbol,date,limit=1).df
        price = barset["price"][0]
        # price = barset[1]
        return price

    def last_price(self, symbol, date):
        try:
            return self.fetch_price(symbol, date)
        except TypeError as error:
            print(error)
            # change date back a day
            date = date - duration(days=1)
            print("Error: New date is ", date)
            return self.last_price(symbol, date)
