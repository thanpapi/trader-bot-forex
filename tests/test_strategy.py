import unittest
import MetaTrader5 as mt5
from unittest.mock import patch, MagicMock
from src.bot import DataFetcher, OrderManager, RiskManager, Strategy
from src.config.config import Config

class TestStrategy(unittest.TestCase):
    @patch('MetaTrader5.account_info')
    @patch('MetaTrader5.positions_get')
    @patch('MetaTrader5.symbol_info')
    @patch('MetaTrader5.symbol_info_tick')
    def test_run(self, mock_account_info, mock_positions_get, mock_symbol_info, mock_symbol_info_tick):
        config = Config()
        data_fetcher = DataFetcher(mt5=None)
        order_manager = OrderManager(mt5=None)
        risk_manager = RiskManager(mt5=None, config=config)
        
        strategy = Strategy(data_fetcher, order_manager, risk_manager, config, mt5=None)

        mock_account_info.return_value.balance = 1000
        mock_positions_get.return_value = []
        mock_symbol_info_tick.return_value.ask = 1.1825
        mock_symbol_info_tick.return_value.bid = 1.1824
        mock_symbol_info.return_value.trade_tick_value = 10.0
        
        with patch.object(strategy, 'is_weekday', return_value=True):
            with patch.object(data_fetcher, 'get_historical_data') as mock_get_data:
                mock_get_data.return_value = MagicMock()
                mock_get_data.return_value.empty = False
                mock_get_data.return_value.__len__.return_value = max(config.SMA_PERIOD, config.SUPPORT_RESISTANCE_PERIOD)
                mock_get_data.return_value.iloc[-1].close = 1.1825
                mock_get_data.return_value.iloc[-1].sma = 1.1820
                mock_get_data.return_value.iloc[-1].hammer = True
                
                with patch.object(strategy, 'identify_support_resistance', return_value=MagicMock()):
                    with patch.object(strategy, 'detect_candle_pattern', return_value={'hammer': [True], 'shooting_star': [False]}):
                        strategy.run()

if __name__ == '__main__':
    unittest.main()
    
    
    
    