import alpaca_trade_api as tapi
import os
import pandas as pd

class Fetcher:
    def __init__(self):
        self.__api = tapi.REST(os.environ['APCA_API_KEY_ID'],
                               os.environ['APCA_API_SECRET_KEY'])
        
    def fetch_barset(self, ticker, timespan, start, stop):
        barset = self.__api.polygon.historic_agg_v2(timespan=timespan, multiplier='1', symbol=ticker, _from=start, to=stop).df
        barset.index = pd.to_datetime(barset.index, unit='ms', origin="unix")

        return barset