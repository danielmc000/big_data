import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh


# Título del Dashboard
st.set_page_config(layout="wide")
# Recarga automática cada 30 segundos (30000 ms)
st_autorefresh(interval=30000, key="auto_refresh")

st.title("📊 Dashboard de Análisis de Criptomonedas")

# Cargar los datos del reporte batch
try:
    df_reporte = pd.read_csv('reporte_batch.csv')
    df_full = pd.read_sql_query('SELECT name, symbol, current_price, market_cap FROM crypto_prices', 'sqlite:///crypto.db')
    # Tomar el precio más reciente por moneda
    df_full = df_full.loc[df_full.groupby('name')['current_price'].idxmax()]

except FileNotFoundError:
    st.error("El archivo 'reporte_batch.csv' no fue encontrado. Por favor, ejecuta el script de procesamiento batch primero.")
    st.stop()
except Exception as e:
    st.error(f"Error al leer la base de datos: {e}")
    st.stop()


# --- Mostrar métricas clave ---
st.header("Resultados del Procesamiento Batch")
st.write("Análisis de precios promedio y máximos registrados.")
st.dataframe(df_reporte)


# --- Gráficos ---
st.header("Visualizaciones")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras de capitalización de mercado
    st.subheader("Top 10 Criptomonedas por Capitalización de Mercado")
    df_top10_market_cap = df_full.nlargest(10, 'market_cap')
    fig_bar = px.bar(
        df_top10_market_cap,
        x='name',
        y='market_cap',
        title='Market Cap (USD)',
        labels={'name': 'Criptomoneda', 'market_cap': 'Capitalización de Mercado'},
        color='name'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Gráfico de pie de precios
    st.subheader("Distribución de Precios (Top 10)")
    df_top10_price = df_full.nlargest(10, 'current_price')
    fig_pie = px.pie(
        df_top10_price,
        names='name',
        values='current_price',
        title='Precio Actual (USD)',
        hole=.3,
        color='name'
    )
    st.plotly_chart(fig_pie, use_container_width=True)
# --- Log del proceso ---
st.header("📝 Registro de Ejecución del Flujo")

try:
    with open("log.txt", "r", encoding="utf-8") as f:
        log = f.read()
    st.text_area("Log del flujo Big Data", value=log, height=400)
except FileNotFoundError:
    st.warning("El archivo 'log.txt' aún no existe. Ejecuta el flujo para generar registros.")