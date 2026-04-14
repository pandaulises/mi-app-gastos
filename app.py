import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestión de Gastos", layout="wide")

# 2. TU ENLACE DE GOOGLE SHEETS (Asegúrate de que termine en /export?format=csv)
SHEET_URL = "https://google.com"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    # LIMPIEZA CRÍTICA: Quita espacios y pone todo en MAYÚSCULAS
    df.columns = df.columns.str.strip().str.upper()
    
    if 'FECHA' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce')
    return df

st.title("📊 Panel de Control de Gastos")

try:
    df = cargar_datos()

    # Filtros usando nombres en MAYÚSCULAS (gracias a la limpieza anterior)
    st.sidebar.header("Filtros")
    
    proyectos = df["PROYECTO"].unique()
    sel_proy = st.sidebar.multiselect("Proyecto:", proyectos, default=proyectos)

    proveedores = df["PROVEEDOR"].unique()
    sel_prov = st.sidebar.multiselect("Proveedor:", proveedores, default=proveedores)

    df_filtrado = df[df["PROYECTO"].isin(sel_proy) & df["PROVEEDOR"].isin(sel_prov)]

    # Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Costo Total", f"${df_filtrado['COSTO'].sum():,.2f}")
    c2.metric("Registros", len(df_filtrado))
    c3.metric("Stock Total", int(df_filtrado['STOCK'].sum()))

    # Gráficos
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.bar(df_filtrado, x="PROYECTO", y="COSTO", title="Costo por Proyecto")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.pie(df_filtrado, values="COSTO", names="PROVEEDOR", title="Distribución por Proveedor")
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df_filtrado)

except Exception as e:
    st.error(f"Aún hay un detalle con las columnas: {e}")
    st.write("Columnas detectadas en tu Excel:", df.columns.tolist())
