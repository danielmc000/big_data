Paso 0: ejecucion del entorno virtual de python venv
Activa tu entorno virtual del proyecto

comando:

Set-ExecutionPolicy RemoteSigned -Scope Process
myenv\Scripts\activate



pip install -r requirements.txt
🔹 Paso 1: Ingesta de Datos
Obtiene datos actuales del mercado desde la API de CoinGecko y los guarda en archivos .json en el directorio data_lake/.

Comando: python 01_ingesta.py
Qué hace:

Crea archivos como coingecko_data_YYYY-MM-DD_HH-MM-SS.json.
Ejecuta este script varias veces para simular el paso del tiempo.

🔹 Paso 2: Almacenamiento en Base de Datos
Procesa los archivos JSON y los convierte en registros estructurados guardados en crypto.db.

Comando: python 02_almacenamiento.py

🔹 Paso 3: Procesamiento Batch
Realiza análisis por lotes y genera un reporte CSV con promedios y máximos por criptomoneda.

Comando: python 03_procesamiento_batch.py

🔹 Paso 4: Procesamiento en Streaming (Simulado)
Simula eventos en tiempo real comparando las últimas dos ingestas.

Comando: python 04_procesamiento_streaming.py

🔹 Paso 5: Visualización de Resultados
Inicia un dashboard interactivo con gráficos y tablas.

Comando: streamlit run 05_visualizacion.py

🔹 Paso Opcional: Ejecutar Todo el Flujo Automáticamente
Si deseas automatizar los pasos 1 a 5 (sin la visualización)

Comando: python run_all.py
Qué hace:

Ejecuta en secuencia: 01_ingesta.py, 02_almacenamiento.py, 03_procesamiento_batch.py, 04_procesamiento_streaming.py y streamlit run 05_visualizacion.py