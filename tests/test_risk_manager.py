import unittest
from unittest.mock import patch
from bot.risk_manager import RiskManager
from config.config import Config

class TestRiskManager(unittest.TestCase):
    @patch('MetaTrader5.symbol_info')
    def test_calculate_lot_size(self, mock_symbol_info):
        mock_symbol_info.return_value.trade_tick_value = 10.0
        risk_manager = RiskManager(mt5=None, config=Config())
        
        lot_size = risk_manager.calculate_lot_size(1000, 1, 15, "EURUSD")
        
        expected_lot_size = 1000 * (1 / 100) / (15 * 10.0)
        self.assertAlmostEqual(lot_size, expected_lot_size)

if __name__ == '__main__':
    unittest.main()