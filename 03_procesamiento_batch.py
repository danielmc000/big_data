import sqlite3
import pandas as pd

DB_NAME = 'crypto.db'
TABLE_NAME = 'crypto_prices'
OUTPUT_CSV = 'reporte_batch.csv'

def procesar_batch():
    """
    Calcula el precio promedio y máximo por criptomoneda
    y lo guarda en un CSV.
    """
    conn = sqlite3.connect(DB_NAME)
    # Cargar datos a un DataFrame de Pandas
    df = pd.read_sql_query(f'SELECT * FROM {TABLE_NAME}', conn)
    conn.close()

    if df.empty:
        print("No hay datos para procesar.")
        return

    # Lógica de agregación
    # Convierte la columna de precio a numérico, forzando errores a NaN
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    
    # Agrupar por nombre y calcular agregados
    reporte = df.groupby('name').agg(
        precio_promedio=('current_price', 'mean'),
        precio_maximo=('current_price', 'max')
    ).reset_index()

    # Guardar el resultado en un archivo CSV
    reporte.to_csv(OUTPUT_CSV, index=False)
    print(f"Procesamiento batch completado. Reporte guardado en: {OUTPUT_CSV}")

if __name__ == "__main__":
    procesar_batch()