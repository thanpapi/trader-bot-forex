import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime
from telegram_utils import send_telegram_message
import requests 

class Strategy:
    def __init__(self, data_fetcher, order_manager, risk_manager, config):
        self.data_fetcher = data_fetcher
        self.order_manager = order_manager
        self.risk_manager = risk_manager
        self.config = config
        self.initial_balance = config.INITIAL_BALANCE
        self.target_balance = self.initial_balance * 1.50  # % objetivo de ganancia
        self.operations_count = 0  # Contador de operaciones realizadas
        self.open_positions = set()  # Conjunto para registrar los símbolos de las posiciones abiertas

    def is_weekday(self):
        return datetime.now().weekday() < 7

    def calculate_bollinger_bands(self, data, period, std_dev):
        data['sma'] = data['close'].rolling(window=period).mean()
        data['std_dev'] = data['close'].rolling(window=period).std()
        data['upper_band'] = data['sma'] + std_dev * data['std_dev']
        data['lower_band'] = data['sma'] - std_dev * data['std_dev']
        return data

    def identify_order_blocks(self, data):
        order_blocks = []
        for i in range(2, len(data) - 2):
            # Condición para identificar un Order Block alcista
            if data['close'].iloc[i] < data['open'].iloc[i] and \
               data['close'].iloc[i-1] > data['open'].iloc[i-1] and \
               data['close'].iloc[i+1] > data['open'].iloc[i+1]:
                order_blocks.append((data['high'].iloc[i], 'bullish'))

            # Condición para identificar un Order Block bajista
            if data['close'].iloc[i] > data['open'].iloc[i] and \
               data['close'].iloc[i-1] < data['open'].iloc[i-1] and \
               data['close'].iloc[i+1] < data['open'].iloc[i+1]:
                order_blocks.append((data['low'].iloc[i], 'bearish'))

        return order_blocks

    def run(self):
        while True:
            print("Strategy loop started")
            if self.is_weekday():
                account_info = mt5.account_info()
                balance = account_info.balance
                profit = account_info.profit
                print(f"Current balance: {balance}, Profit: {profit}")

                if balance >= self.target_balance:
                    print(f"Target balance achieved: {balance}, stopping the bot.")
                    break

                print(f"Bot running, balance={balance}")
                all_symbols = self.config.SYMBOLS_FOREX
                for symbol in all_symbols:
                    
                    higher_timeframe_data = self.data_fetcher.get_historical_data(symbol, mt5.TIMEFRAME_M15)
                    lower_timeframe_data = self.data_fetcher.get_historical_data(symbol, mt5.TIMEFRAME_M3)

                    if higher_timeframe_data.empty or lower_timeframe_data.empty:
                        print(f"Skipping {symbol} due to empty data.")
                        continue

                    min_required_length = max(self.config.SMA_PERIOD, self.config.SUPPORT_RESISTANCE_PERIOD)
                    if len(higher_timeframe_data) < min_required_length:
                        print(f"Skipping {symbol} due to insufficient higher timeframe data.")
                        continue

                    if len(lower_timeframe_data) < min_required_length:
                        print(f"Skipping {symbol} due to insufficient lower timeframe data.")
                        continue

                    higher_timeframe_data['close'] = higher_timeframe_data['close'].astype(float)
                    lower_timeframe_data['close'] = lower_timeframe_data['close'].astype(float)

                    # Indicadores en la temporalidad mayor 
                    higher_timeframe_data['sma'] = higher_timeframe_data['close'].rolling(window=self.config.SMA_PERIOD).mean()
                    higher_timeframe_data['macd'], higher_timeframe_data['macd_signal'], higher_timeframe_data['macd_hist'] = self.calculate_macd(higher_timeframe_data)

                    # Indicadores en la temporalidad menor 
                    lower_timeframe_data['sma'] = lower_timeframe_data['close'].rolling(window=self.config.SMA_PERIOD).mean()
                    lower_timeframe_data['macd'], lower_timeframe_data['macd_signal'], lower_timeframe_data['macd_hist'] = self.calculate_macd(lower_timeframe_data)

                    # Identificación de Order Blocks en la temporalidad menor
                    order_blocks = self.identify_order_blocks(lower_timeframe_data)

                    # Señales en la temporalidad mayor 
                    higher_timeframe_signal = (higher_timeframe_data['close'].iloc[-1] > higher_timeframe_data['sma'].iloc[-1]) and (higher_timeframe_data['macd_hist'].iloc[-1] > 0)

                    # Señales en la temporalidad menor 
                    lower_timeframe_signal = (lower_timeframe_data['close'].iloc[-1] > lower_timeframe_data['sma'].iloc[-1]) and (lower_timeframe_data['macd_hist'].iloc[-1] > 0)

                    # Confirmación de la señal con Order Block
                    valid_order_block = False
                    for block_price, block_type in order_blocks:
                        if block_type == 'bullish' and lower_timeframe_data['close'].iloc[-1] > block_price:
                            valid_order_block = True
                            break
                        if block_type == 'bearish' and lower_timeframe_data['close'].iloc[-1] < block_price:
                            valid_order_block = True
                            break

                    signal = None
                    order_type = None
                    stop_loss = None

                    # Decisiones basadas en ambas temporalidades y la validación del Order Block
                    if higher_timeframe_signal and lower_timeframe_signal and valid_order_block:
                        signal = True
                        order_type = mt5.ORDER_TYPE_BUY
                        stop_loss = lower_timeframe_data['close'].iloc[-1] - (self.config.STOP_LOSS_PIPS * mt5.symbol_info(symbol).point)
                    elif not higher_timeframe_signal and not lower_timeframe_signal and valid_order_block:
                        signal = True
                        order_type = mt5.ORDER_TYPE_SELL
                        stop_loss = lower_timeframe_data['close'].iloc[-1] + (self.config.STOP_LOSS_PIPS * mt5.symbol_info(symbol).point)

                    if signal and not self.is_symbol_in_opposite_direction(symbol, order_type):
                        price = lower_timeframe_data['close'].iloc[-1]
                        take_profit = (price + self.config.TAKE_PROFIT_PIPS * mt5.symbol_info(symbol).point) if order_type == mt5.ORDER_TYPE_BUY else (price - self.config.TAKE_PROFIT_PIPS * mt5.symbol_info(symbol).point)
                        lot_size = self.risk_manager.calculate_lot_size(balance, self.config.RISK_PERCENTAGE, abs(price - stop_loss) / mt5.symbol_info(symbol).point, symbol)
                        max_lot_size = self.config.MAX_LOT_SIZE
                        lot_size = min(lot_size, max_lot_size)
                        lot_size_formatted = round(lot_size, 2)

                        if lot_size_formatted <= 0:
                            print(f"Invalid lot size calculated: {lot_size_formatted} for symbol {symbol}. Skipping order.")
                            continue

                        print(f"Placing order: symbol={symbol}, lot_size={lot_size_formatted}, order_type={order_type}, stop_loss={stop_loss}, take_profit={take_profit}")
                        result = self.order_manager.place_order(symbol, lot_size_formatted, order_type, stop_loss, take_profit)

                        if result is None:
                            print(f"Order failed for {symbol}, result is None")
                        elif result.retcode != mt5.TRADE_RETCODE_DONE:
                            print(f"Order failed for {symbol}, retcode={result.retcode}, comment={result.comment}")
                        else:
                            print(f"Order placed successfully for {symbol}")
                            
                            # Enviar mensaje a Telegram
                            message = (f"Abrir operación para {symbol}:\n"
                                       f"Precio de Entrada alrededor de: {price}\n"
                                       f"Opero: 0.25% riesgo\n" 
                                       f"Tipo de Orden: {'Buy' if order_type == mt5.ORDER_TYPE_BUY else 'Sell'}\n"
                                       f"Stop Loss: {stop_loss}\n"
                                       f"Take Profit: {take_profit}\n")
                            print(f"Enviando mensaje: {message}")
                            send_telegram_message(message)

                            self.operations_count += 1
                            print(f"Operation {self.operations_count} placed successfully for {symbol}")

                            # Verificar si se han realizado suficientes operaciones
                            if self.operations_count >= self.config.MAX_OPERATIONS:
                                print(f"Target number of operations reached: {self.operations_count}, stopping the bot.")
                                return

                time.sleep(3)
            else:
                print("Market is closed. Waiting...")
                time.sleep(3600)

    def is_symbol_in_opposite_direction(self, symbol, order_type):
        for pos in mt5.positions_get():
            if pos.symbol == symbol:
                if (order_type == mt5.ORDER_TYPE_BUY and pos.type == mt5.ORDER_TYPE_SELL) or (order_type == mt5.ORDER_TYPE_SELL and pos.type == mt5.ORDER_TYPE_BUY):
                    return True
        return False

    def identify_support_resistance(self, data, period):
        data['max'] = data['high'].rolling(window=period).max()
        data['min'] = data['low'].rolling(window=period).min()
        return data

    def detect_candle_pattern(self, data):
        patterns = {
            'hammer': (data['close'] > data['open']) & ((data['high'] - data['low']) > 3 * (data['close'] - data['open'])),
            'shooting_star': (data['close'] < data['open']) & ((data['high'] - data['low']) > 3 * (data['open'] - data['close'])),
            'bullish_engulfing': (data['close'].shift(1) < data['open'].shift(1)) & (data['close'] > data['open']) & (data['close'] > data['open'].shift(1)) & (data['open'] < data['close'].shift(1)),
            'bearish_engulfing': (data['close'].shift(1) > data['open'].shift(1)) & (data['close'] < data['open']) & (data['close'] < data['open'].shift(1)) & (data['open'] > data['close'].shift(1)),
            'doji': (abs(data['close'] - data['open']) <= 0.1 * (data['high'] - data['low'])),
            # Más patrones según sea necesario
        }

        patterns_detected = pd.DataFrame({key: patterns[key] for key in patterns}, index=data.index)
        return patterns_detected

    def add_indicators(self, data):
        # Agregar indicadores adicionales como RSI, ATR, MACD, etc.
        data['rsi'] = self.calculate_rsi(data, 14)
        data['atr'] = self.calculate_atr(data, 14)
        data['macd'], data['macd_signal'], data['macd_hist'] = self.calculate_macd(data)
        return data

    def calculate_rsi(self, data, period):
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_atr(self, data, period):
        data['tr'] = data[['high', 'low', 'close']].max(axis=1) - data[['high', 'low', 'close']].min(axis=1)
        atr = data['tr'].rolling(window=period).mean()
        return atr

    def calculate_macd(self, data, short_period=12, long_period=26, signal_period=9):
        short_ema = data['close'].ewm(span=short_period, adjust=False).mean()
        long_ema = data['close'].ewm(span=long_period, adjust=False).mean()
        macd = short_ema - long_ema
        macd_signal = macd.ewm(span=signal_period, adjust=False).mean()
        macd_hist = macd - macd_signal
        return macd, macd_signal, macd_hist

    def additional_filters(self, data):
        # Agregar filtros adicionales basados en indicadores, por ejemplo, RSI, MACD, ATR, etc.
        if data['rsi'].iloc[-1] > 70 or data['rsi'].iloc[-1] < 30:
            return False
        if data['macd_hist'].iloc[-1] > 0 and data['macd_hist'].iloc[-2] < 0:
            return True
        if data['macd_hist'].iloc[-1] < 0 and data['macd_hist'].iloc[-2] > 0:
            return True
        return True
