import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Gestión de Proyectos", layout="wide")

# 2. Tu enlace de Google Sheets
SHEET_URL = "https://google.com"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    # Ajustamos los nombres a como están en tu imagen
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
    return df

st.title("📊 Panel de Control: Gastos y Proyectos")

try:
    df = cargar_datos()

    # --- FILTROS LATERALES (Ajustados a tus nombres reales) ---
    st.sidebar.header("Filtros")
    
    # Filtro por Proyecto
    proyectos = df["Proyecto"].unique()
    sel_proy = st.sidebar.multiselect("Selecciona Proyecto:", proyectos, default=proyectos)

    # Filtro por PROOVEDOR (En tu imagen está en MAYÚSCULAS)
    proveedores = df["PROOVEDOR"].unique()
    sel_prov = st.sidebar.multiselect("Selecciona Proveedor:", proveedores, default=proveedores)

    # Filtrado de datos
    df_filtrado = df[df["Proyecto"].isin(sel_proy) & df["PROOVEDOR"].isin(sel_prov)]

    # --- MÉTRICAS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Costo Total", f"${df_filtrado['COSTO'].sum():,.2f}")
    c2.metric("Total Recibido (Registros)", len(df_filtrado))
    c3.metric("Stock Promedio", f"{df_filtrado['STOCK'].mean():.2f}")

    # --- GRÁFICOS ---
    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Costo por Proyecto")
        fig1 = px.bar(df_filtrado, x="Proyecto", y="COSTO", color="Proyecto")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Inversión por Proveedor")
        fig2 = px.pie(df_filtrado, values="COSTO", names="PROOVEDOR")
        st.plotly_chart(fig2, use_container_width=True)

    # --- TABLA ---
    st.subheader("Detalle de la Hoja de Cálculo")
    st.dataframe(df_filtrado)

except Exception as e:
    st.error(f"Error: Revisa que los nombres de las columnas coincidan. Detalle: {e}")
