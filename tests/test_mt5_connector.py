import unittest
from unittest.mock import patch
from bot.mt5_connector import MT5Connector
import MetaTrader5 as mt5

class TestMT5Connector(unittest.TestCase):
    @patch('MetaTrader5.initialize')
    @patch('MetaTrader5.login')
    @patch('MetaTrader5.shutdown')
    def test_initialize_success(self, mock_initialize, mock_login, mock_shutdown):
        mock_initialize.return_value = True
        connector = MT5Connector("C:\\Program Files\\MetaTrader 5\\terminal64.exe")
        self.assertIsNone(connector.initialize())
        mock_initialize.assert_called_once()

    @patch('MetaTrader5.initialize')
    @patch('MetaTrader5.login')
    @patch('MetaTrader5.shutdown')
    def test_initialize_failure(self, mock_initialize, mock_login, mock_shutdown):
        mock_initialize.return_value = False
        mock_initialize.last_error.return_value = 1
        connector = MT5Connector("C:\\Program Files\\MetaTrader 5\\terminal64.exe")
        with self.assertRaises(Exception):
            connector.initialize()
        mock_initialize.assert_called_once()

    @patch('MetaTrader5.login')
    def test_login_success(self, mock_login):
        mock_login.return_value = True
        connector = MT5Connector("C:\\Program Files\\MetaTrader 5\\terminal64.exe")
        connector.login(10003281620, "EdPsC+1g", "MetaQuotes-Demo")
        mock_login.assert_called_once_with(10003281620, password="EdPsC+1g", server="MetaQuotes-Demo")

    @patch('MetaTrader5.login')
    def test_login_failure(self, mock_login):
        mock_login.return_value = False
        connector = MT5Connector("C:\\Program Files\\MetaTrader 5\\terminal64.exe")
        with self.assertRaises(Exception):
            connector.login(10003281620, "EdPsC+1g", "MetaQuotes-Demo")
        mock_login.assert_called_once_with(10003281620, password="EdPsC+1g", server="MetaQuotes-Demo")

if __name__ == '__main__':
    unittest.main()