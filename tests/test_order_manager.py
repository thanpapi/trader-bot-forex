import unittest
from unittest.mock import patch
from bot.order_manager import OrderManager

class TestOrderManager(unittest.TestCase):
    @patch('MetaTrader5.order_send')
    @patch('MetaTrader5.symbol_info_tick')
    def test_place_order(self, mock_symbol_info_tick, mock_order_send):
        mock_symbol_info_tick.return_value.ask = 1.1825
        mock_symbol_info_tick.return_value.bid = 1.1824
        mock_order_send.return_value.retcode = 10009
        
        order_manager = OrderManager(mt5=None)
        result = order_manager.place_order("EURUSD", 1.0, 0, 1.1800, 1.1850)
        
        self.assertEqual(result.retcode, 10009)
        mock_order_send.assert_called_once()

if __name__ == '__main__':
    unittest.main()