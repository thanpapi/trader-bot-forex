import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MT5_PATH = os.getenv("MT5_PATH", "C:\\Program Files\\MetaTrader 5\\terminal64.exe")
    ACCOUNT = int(os.getenv("ACCOUNT"))
    PASSWORD = os.getenv("PASSWORD")
    SERVER = os.getenv("SERVER")
    
    # Límite de pérdida diaria (en porcentaje del balance actual)

    DAILY_LOSS_LIMIT_PERCENTAGE = 5  # 2% del balance actual
    
    # Límite de pérdida máxima total (en porcentaje del balance actual)

    MAX_LOSS_LIMIT_PERCENTAGE = 5  # 2% del balance actual
    
    # Porcentaje de riesgo por operación (porcentaje del balance)

    RISK_PERCENTAGE = 3 # 1% del balance por operación


    #parametros para operar
    TAKE_PROFIT_PIPS = 80 # Ajustado a pips para hacer el % en una operación
    STOP_LOSS_PIPS = 200 # Ajustado a pips para mantener el stop loss en línea con el take profit
    MAX_OPERATIONS =  5 # aqui van los numeros de operaciones 
    MAX_LOT_SIZE = 0.2 #LOTES


    # ["BTCUSD"] SOLO FINES DE SEMANA TEMP 4H/15M
    # ["GBPUSD", "USDCAD"] pares 8AM /12PM
    # ["USDJPY", "AUDUSD", "NZDJPY", "AUDJPY"] PARES 8PM/10PM asia 
    # Lista de símbolos Forex (sin criptomonedas) 
     # ["XAUUSD"]
    SYMBOLS_FOREX = ["EURUSD"] 
    # Periodo para el cálculo de la media móvil simple (SMA)
    SMA_PERIOD = 50
    
    # Periodo para la identificación de soportes y resistencias
    SUPPORT_RESISTANCE_PERIOD = 40
   
    # Porcentaje máximo de riesgo en comparación con el balance de la cuenta (en total)
    MAX_RISK_PERCENTAGE = 50  # Alineado con el objetivo de ganancia del 10%
    
    # Balance inicial de la cuenta (en unidades monetarias de la cuenta)
    INITIAL_BALANCE = 10150 
    
    # Deslizamiento permitido (en pips)
    SLIPPAGE = 0  # Configurado para permitir hasta 10 pips de deslizamiento en las órdenes
    

    SUPPORT_RESISTANCE_PERIOD = 40
    SMA_PERIOD = 50
    
    
    