# Arquitectura del MT5 Bot

## Visión General
Este proyecto es un bot de trading automatizado que se conecta a la plataforma MetaTrader 5 para realizar operaciones de trading basadas en ciertas estrategias y reglas de gestión de riesgos.

## Componentes Principales

### 1. `main.py`
Este es el punto de entrada del bot. Inicializa todos los componentes necesarios y ejecuta la estrategia de trading.

### 2. `config.py`
Maneja la configuración del bot, incluyendo credenciales de autenticación, parámetros de trading y otros ajustes necesarios.

### 3. `MT5Connector`
Este módulo maneja la conexión y autenticación con la plataforma MetaTrader 5.

### 4. `DataFetcher`
Se encarga de obtener datos históricos de los símbolos de trading.

### 5. `OrderManager`
Gestiona la colocación de órdenes en la plataforma MetaTrader 5.

### 6. `RiskManager`
Implementa la lógica de gestión de riesgos, incluyendo el cálculo del tamaño del lote y el monitoreo de drawdown.

### 7. `Strategy`
Contiene la lógica de la estrategia de trading, incluyendo la identificación de patrones de velas y la toma de decisiones de trading.

## Flujo de Trabajo

1. **Inicialización**
   - `main.py` inicializa el `MT5Connector` para conectar y autenticar en MetaTrader 5.
   - Se configuran los parámetros y se inicializan los componentes `DataFetcher`, `OrderManager` y `RiskManager`.

2. **Ejecución de la Estrategia**
   - `Strategy.run()` se ejecuta en un bucle infinito.
   - En cada iteración, se verifica si es un día hábil (`is_weekday`).
   - Se obtienen datos históricos para cada símbolo.
   - Se calculan indicadores técnicos y se identifican patrones de velas.
   - Si se identifica una señal de trading, se coloca una orden a través de `OrderManager`.
   - Se monitorea el drawdown y se activan medidas de seguridad si es necesario.

3. **Finalización**
   - Al finalizar, el bot cierra la conexión con MetaTrader 5.

## Registro de Logs
El bot utiliza el módulo `logger` para registrar eventos importantes, errores y acciones. Los logs se almacenan en un archivo `mt5_bot.log`.

## Configuración
El archivo `.env` contiene las configuraciones necesarias, como las credenciales de la cuenta y los parámetros de trading.

## Pruebas
Las pruebas se encuentran en el directorio `tests` y verifican la funcionalidad de los componentes individuales.

## Conclusión
Esta arquitectura modular facilita la mantenibilidad y escalabilidad del bot, permitiendo añadir nuevas estrategias y gestionar riesgos de manera eficiente.