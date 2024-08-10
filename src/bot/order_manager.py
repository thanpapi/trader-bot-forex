import MetaTrader5 as mt5

class OrderManager:
    def __init__(self, connector):
        self.connector = connector

    def place_order(self, symbol, lot_size, order_type, stop_loss, take_profit):
        # Verifica la información del símbolo
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            print(f"Symbol info for {symbol} not found")
            return None

        # Verifica el tick de información del símbolo
        symbol_tick = mt5.symbol_info_tick(symbol)
        if symbol_tick is None:
            print(f"No tick data available for {symbol}")
            return None

        # Verifica el volumen mínimo y el paso de volumen
        volume_min = symbol_info.volume_min
        volume_step = symbol_info.volume_step

        # Ajusta el tamaño del lote
        lot_size = round(lot_size / volume_step) * volume_step
        if lot_size < volume_min:
            lot_size = volume_min

        # Determina el precio según el tipo de orden
        price = symbol_tick.ask if order_type == mt5.ORDER_TYPE_BUY else symbol_tick.bid
        if price == 0:
            print(f"Invalid price (zero) for {symbol}")
            return None

        deviation = 10

        # Define la solicitud de orden
        order_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": order_type,
            "price": price,
            "sl": stop_loss,
            "tp": take_profit,
            "deviation": deviation,
            "magic": 234000,
            "comment": "Order by bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

        print(f"Placing order: {order_request}")
        result = mt5.order_send(order_request)
        
        # Verifica si el resultado es válido y tiene atributos esperados
        if result is None:
            print(f"Order failed for {symbol}, result is None")
            print(f"MetaTrader 5 error code: {mt5.last_error()}")
            return None
        
        if hasattr(result, 'retcode'):
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Order failed for {symbol}, retcode={result.retcode}, comment={result.comment}")
                print(f"MetaTrader 5 error code: {mt5.last_error()}")
            else:
                print(f"Order placed successfully for {symbol}")
        else:
            print(f"Unexpected result format for {symbol}: {result}")
        
        return result

    def close_position(self, symbol, volume, order_type):
        # Obtener la posición abierta
        positions = mt5.positions_get(symbol=symbol)
        if not positions:
            print(f"No open positions found for {symbol}.")
            return None

        pos = positions[0]  # Suponiendo que hay solo una posición abierta por símbolo

        # Preparar el pedido de cierre
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).bid if pos.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
            "deviation": 10,
            "magic": 234000,
            "comment": "Position closed by strategy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            "position": pos.ticket
        }
        
        result = mt5.order_send(close_request)
        if result is None:
            print(f"Failed to close position for {symbol}, result is None")
            print(f"MetaTrader 5 error code: {mt5.last_error()}")
        elif hasattr(result, 'retcode') and result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to close position for {symbol}, retcode={result.retcode}")
            print(f"MetaTrader 5 error code: {mt5.last_error()}")
        else:
            print(f"Position closed successfully for {symbol}")
        
        return result
