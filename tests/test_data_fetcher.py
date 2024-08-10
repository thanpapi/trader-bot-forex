import unittest
from unittest.mock import patch
from bot.data_fetcher import DataFetcher
import pandas as pd

class TestDataFetcher(unittest.TestCase):
    @patch('MetaTrader5.copy_rates_from_pos')
    def test_get_historical_data(self, mock_copy_rates):
        mock_copy_rates.return_value = [
            (1625097600, 1.1825, 1.1826, 1.1824, 1.1825, 100),
            (1625097700, 1.1826, 1.1827, 1.1825, 1.1826, 150),
        ]
        data_fetcher = DataFetcher(mt5=None)
        data = data_fetcher.get_historical_data("EURUSD", 15, 2)
        expected_data = pd.DataFrame({
            'time': [1625097600, 1625097700],
            'open': [1.1825, 1.1826],
            'high': [1.1826, 1.1827],
            'low': [1.1824, 1.1825],
            'close': [1.1825, 1.1826],
            'tick_volume': [100, 150],
        })
        pd.testing.assert_frame_equal(data, expected_data)

if __name__ == '__main__':
    unittest.main()