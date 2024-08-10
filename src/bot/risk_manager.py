import MetaTrader5 as mt5

class RiskManager:
    def __init__(self, connector, config):
        self.connector = connector
        self.config = config
        self.daily_loss_limit = config.DAILY_LOSS_LIMIT_PERCENTAGE 
        self.max_loss_limit = config.MAX_LOSS_LIMIT_PERCENTAGE
        self.risk_percentage = config.RISK_PERCENTAGE
        self.initial_balance = mt5.account_info().balance
        self.daily_loss = 0

    def update_daily_loss(self, current_balance):
        self.daily_loss = self.initial_balance - current_balance

    def check_limit(self, current_balance):
        self.update_daily_loss(current_balance)
        if self.daily_loss >= self.daily_loss_limit or (self.initial_balance - current_balance) >= self.max_loss_limit:
            return True
        return False

    def calculate_lot_size(self, balance, risk_percentage, stop_loss_distance, symbol):
        adjusted_risk_percentage = min(self.risk_percentage, self.config.MAX_RISK_PERCENTAGE)
        risk_amount = balance * (adjusted_risk_percentage / 100)
        
        reduction_factor = 0.02  # Puedes ajustar este valor según tus necesidades
        lot_size = (risk_amount * reduction_factor) / (stop_loss_distance * mt5.symbol_info(symbol).point)
        
        min_lot_size = mt5.symbol_info(symbol).volume_min
        max_lot_size = mt5.symbol_info(symbol).volume_max
        
        if lot_size < min_lot_size:
            lot_size = min_lot_size
        elif lot_size > max_lot_size:
            lot_size = max_lot_size
        
        return lot_size


