import MetaTrader5 as mt5


class MT5Connector:
    def __init__(self, config):
        self.config = config

    def initialize(self):
        if not mt5.initialize():
            print("initialize() failed")
            return False
        print("MetaTrader5 initialized successfully")
        return True

    def shutdown(self):
        mt5.shutdown()