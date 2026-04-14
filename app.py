import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inventario y Gastos", layout="wide")

# SUSTITUYE POR TU ENLACE REAL
SHEET_URL = "https://google.com"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    # Limpieza automática de nombres de columnas
    df.columns = df.columns.str.strip().str.lower()
    return df

st.title("📊 Dashboard de Inventario y Gastos")

try:
    df = cargar_datos()

    # Filtros laterales usando los nombres exactos de tu imagen
    st.sidebar.header("Filtros")
    
    # Filtro por Proyecto
    proyectos = df["proyecto"].unique()
    sel_proy = st.sidebar.multiselect("Proyecto:", proyectos, default=proyectos)

    # Filtro por Proveedor
    proveedores = df["proveedor"].unique()
    sel_prov = st.sidebar.multiselect("Proveedor:", proveedores, default=proveedores)

    df_filtrado = df[df["proyecto"].isin(sel_proy) & df["proveedor"].isin(sel_prov)]

    # Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Costo Total", f"${df_filtrado['costo'].sum():,.2f}")
    c2.metric("Stock Actual", f"{df_filtrado['stock'].sum():.0f}")
    c3.metric("Registros", len(df_filtrado))

    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Costo por Proyecto")
        fig1 = px.bar(df_filtrado, x="proyecto", y="costo", color="proyecto")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("Gasto por Proveedor")
        fig2 = px.pie(df_filtrado, values="costo", names="proveedor")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Detalle del Inventario")
    st.dataframe(df_filtrado)

except Exception as e:
    st.error(f"Error detectado: {e}")
    st.info("Revisa que los encabezados de tu Excel no tengan celdas vacías al inicio.")
