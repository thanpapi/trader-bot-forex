import sys
import os
import MetaTrader5 as mt5
from telegram_utils import send_telegram_message  # Asegúrate de que este módulo exista
import requests 
# Asegúrate de que se pueda encontrar el paquete src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.config import Config
from src.bot import MT5Connector, DataFetcher, OrderManager, RiskManager, Strategy

def main():
    print("Bot started")
    config = Config()
    
    connector = MT5Connector(config)
    if not connector.initialize():
        print("Failed to initialize MT5Connector")
        return
    
    data_fetcher = DataFetcher(connector)
    order_manager = OrderManager(connector)
    risk_manager = RiskManager(connector, config)
    strategy = Strategy(data_fetcher, order_manager, risk_manager, config)
    
    try:
        # Llama a la estrategia
        strategy.run()
    finally:
        connector.shutdown()

    # Ejemplo de uso del bot de Telegram al final
    message = "¡!"
    send_telegram_message(message)  # Asegúrate de que send_telegram_message esté definido correctamente

if __name__ == "__main__":
    main()


