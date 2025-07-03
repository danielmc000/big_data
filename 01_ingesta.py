import requests
import json
from datetime import datetime
import os

# Directorio para el Data Lake local
DATA_LAKE_DIR = 'data_lake'
os.makedirs(DATA_LAKE_DIR, exist_ok=True)

# URL de la API de CoinGecko
API_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'

def ingerir_datos():
    """
    Realiza una solicitud a la API de CoinGecko y guarda los datos en el data lake.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa (código 2xx)
        data = response.json()

        # Generar un nombre de archivo único con la fecha y hora actual
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join(DATA_LAKE_DIR, f'coingecko_data_{timestamp}.json')

        # Guardar los datos crudos en un archivo JSON
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Datos ingeridos y guardados exitosamente en: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")

if __name__ == "__main__":
    ingerir_datos()