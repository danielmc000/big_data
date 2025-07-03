import sqlite3
import pandas as pd
import time

DB_NAME = 'crypto.db'
TABLE_NAME = 'crypto_prices'

def detectar_eventos():
    """
    Simula streaming revisando los últimos datos para detectar
    cambios de precio significativos en Bitcoin.
    """
    conn = sqlite3.connect(DB_NAME)
    
    # Obtener los dos registros más recientes de Bitcoin
    query = f"""
        SELECT current_price, last_updated
        FROM {TABLE_NAME}
        WHERE id = 'bitcoin'
        ORDER BY last_updated DESC
        LIMIT 2;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if len(df) < 2:
        print("No hay suficientes datos para comparar.")
        return

    # Lógica de detección de eventos
    precio_actual = df.iloc[0]['current_price']
    precio_anterior = df.iloc[1]['current_price']
    
    # Evitar división por cero
    if precio_anterior == 0:
        return

    variacion_pct = ((precio_actual - precio_anterior) / precio_anterior) * 100

    # Si la variación es mayor al 1%, generar una alerta
    if abs(variacion_pct) > 1.0:
        print("🔥 ALERTA DE PRECIO (STREAMING) 🔥")
        print(f"Bitcoin ha variado un {variacion_pct:.2f}% en el último periodo.")
        print(f"Precio anterior: ${precio_anterior:,.2f}, Precio actual: ${precio_actual:,.2f}")

if __name__ == "__main__":
    # Para simular, ejecuta la ingesta varias veces con unos minutos de diferencia
    # y luego corre este script.
    print("Iniciando monitoreo de streaming...")
    detectar_eventos()