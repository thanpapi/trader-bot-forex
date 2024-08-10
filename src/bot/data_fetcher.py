import MetaTrader5 as mt5
import pandas as pd

class DataFetcher:
    def __init__(self, connector):
        self.connector = connector

    def get_historical_data(self, symbol, timeframe):
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)
        data = pd.DataFrame(rates)
        data['time'] = pd.to_datetime(data['time'], unit='s')
        data.set_index('time', inplace=True)
        return data
