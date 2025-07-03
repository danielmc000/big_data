# 📊 Proyecto Final – Big Data: Análisis de Criptomonedas

Este proyecto implementa un flujo completo de Big Data que permite obtener, procesar y visualizar datos de criptomonedas en tiempo real. Utiliza la API de CoinGecko, una base de datos SQLite, procesamiento batch y streaming simulado, y un dashboard web interactivo con Streamlit.

---

## ⚙️ Paso 0: Preparación del Entorno

### 1. Crear y activar entorno virtual (Windows):

```Terminal de comando

python -m venv myenv(para crear el entorno virutal de python)

Set-ExecutionPolicy RemoteSigned -Scope Process (cambiar la política de ejecución temporalmente a una más permisiva.
Esto te permitirá activar el entorno virtual sin problemas en caso de error. ejecutar en powershell)

myenv\Scripts\activate (para activar el entorno virtual depython)

Set-ExecutionPolicy Default -Scope Process (si quieres revertir los cambios y restaurar la política de ejecución
original, puedes cerrar la ventana de PowerShell o ejecutas el comando. ejecutar en powershell)
```
## 2. Instalar dependencias:
pip install
📦 Librerías necesarias:
```
requests
pandas
streamlit
plotly
plotly.express
streamlit-autorefresh
```

## 🔹 Paso 1: Ingesta de Datos
Obtiene datos actualizados del mercado desde la API pública de CoinGecko y los guarda en formato .json en la carpeta data_lake/.
```
python 01_ingesta.py
```
✅ Resultado: Archivos tipo coingecko_data_YYYY-MM-DD_HH-MM-SS.json.

## 🔹 Paso 2: Almacenamiento en Base de Datos
Lee los archivos JSON del data lake, los transforma y los guarda en una base de datos SQLite (crypto.db).
```
python 02_almacenamiento.py
```
## 🔹 Paso 3: Procesamiento Batch
Analiza todos los registros en la base de datos y genera un archivo reporte_batch.csv con estadísticas agregadas (precio promedio y máximo por criptomoneda).
```
 python 03_procesamiento_batch.py
```
## 🔹 Paso 4: Procesamiento en Streaming (Simulado)
Simula detección de eventos en tiempo real: compara las últimas dos ingestas y genera una alerta si el precio de Bitcoin cambia más del 1%.
```
python 04_procesamiento_streaming.py
```
## 🔹 Paso 5: Visualización de Resultados
Lanza un dashboard web usando Streamlit para visualizar los datos procesados, gráficas interactivas y el log del sistema.
```
streamlit run 05_visualizacion.py
```
## ✅ Muestra:
```
Tabla con precios promedio y máximos.

Gráfico de barras (Top 10 por capitalización).

Gráfico circular (Top 10 por precio).

Log actualizado automáticamente (log.txt).
```
## 🔁 Paso 6: Ejecución Automática del Flujo Completo
Si deseas ejecutar todo el flujo de manera automática y continua, usa:
```
python run_all.py
```
## ✅ Ejecuta en bucle:
```
01_ingesta.py

02_almacenamiento.py

03_procesamiento_batch.py

04_procesamiento_streaming.py

05_visualizacion.py 

Se repite cada 5 minutos
```
💡 El dashboard se actualiza automáticamente cada 30 segundos gracias a streamlit-autorefresh.
