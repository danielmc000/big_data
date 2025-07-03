import sqlite3
import json
import os
import glob

DATA_LAKE_DIR = 'data_lake'
DB_NAME = 'crypto.db'
TABLE_NAME = 'crypto_prices'

def inicializar_db():
    """Crea la tabla en la base de datos si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id TEXT,
            symbol TEXT,
            name TEXT,
            current_price REAL,
            market_cap REAL,
            total_volume REAL,
            last_updated TEXT,
            ingestion_time TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def procesar_y_almacenar():
    """Lee archivos del data lake, los transforma y los carga en SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    json_files = glob.glob(os.path.join(DATA_LAKE_DIR, '*.json'))

    for file_path in json_files:
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                ingestion_time = os.path.basename(file_path).replace('coingecko_data_', '').replace('.json', '')

                # --- INICIO DE LA CORRECCIÓN ---
                # 1. Verificar si 'data' es una lista antes de iterar
                if not isinstance(data, list):
                    print(f"ADVERTENCIA: El archivo '{os.path.basename(file_path)}' no contiene una lista. Se omitirá.")
                    continue # Salta al siguiente archivo

                for crypto in data:
                    # 2. Asegurarse que 'crypto' es un diccionario
                    if not isinstance(crypto, dict):
                        print(f"ADVERTENCIA: Se encontró un elemento que no es un diccionario en '{os.path.basename(file_path)}'. Se omitirá.")
                        continue # Salta al siguiente elemento en la lista

                    # Se mantiene el bloque try-except para otros posibles errores
                    try:
                        record = (
                            crypto.get('id'),
                            crypto.get('symbol'),
                            crypto.get('name'),
                            crypto.get('current_price'),
                            crypto.get('market_cap'),
                            crypto.get('total_volume'),
                            crypto.get('last_updated'),
                            f"{ingestion_time}_{crypto.get('id')}" # Clave primaria única
                        )
                        cursor.execute(f'''
                            INSERT OR IGNORE INTO {TABLE_NAME}
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', record)
                    except Exception as e:
                        # Usar una forma segura de obtener el 'id' para el mensaje de error
                        crypto_id = crypto.get('id', 'desconocido')
                        print(f"No se pudo insertar el registro {crypto_id}: {e}")
                # --- FIN DE LA CORRECCIÓN ---

            except json.JSONDecodeError:
                print(f"ERROR: El archivo '{os.path.basename(file_path)}' no es un JSON válido. Se omitirá.")
            except Exception as e:
                print(f"Ocurrió un error inesperado procesando el archivo {os.path.basename(file_path)}: {e}")


    conn.commit()
    conn.close()
    print(f"Proceso de almacenamiento finalizado.")

if __name__ == "__main__":
    inicializar_db()
    procesar_y_almacenar()