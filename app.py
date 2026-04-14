import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Control de Inventario", layout="wide")

# 2. ENLACE DE TU HOJA (Asegúrate de que termine en /export?format=csv)
# Reemplaza TODO el link de abajo por el tuyo
SHEET_URL = "https://google.com"

@st.cache_data
def cargar_datos():
    # Cargamos y limpiamos espacios invisibles
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    
    # Convertir fecha a formato real de Python
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
    
    # Asegurar que costo y precio sean números
    df['costo'] = pd.to_numeric(df['costo'], errors='coerce').fillna(0)
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce').fillna(0)
    return df

st.title("📊 Dashboard de Inventario y Gastos")

try:
    df = cargar_datos()

    # --- FILTROS LATERALES ---
    st.sidebar.header("Filtros")
    
    # Filtro por Proyecto (columna I en tu imagen)
    proyectos = df["proyecto"].unique()
    sel_proy = st.sidebar.multiselect("Filtrar por Proyecto:", proyectos, default=proyectos)

    # Filtro por Proveedor (columna B en tu imagen)
    proveedores = df["proveedor"].unique()
    sel_prov = st.sidebar.multiselect("Filtrar por Proveedor:", proveedores, default=proveedores)

    # Aplicar filtros
    df_filtrado = df[df["proyecto"].isin(sel_proy) & df["proveedor"].isin(sel_prov)]

    # --- MÉTRICAS PRINCIPALES ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gasto Total (Costo)", f"${df_filtrado['costo'].sum():,.2f}")
    m2.metric("Artículos en Stock", int(df_filtrado['stock'].sum()))
    m3.metric("Productos Distintos", len(df_filtrado))
    m4.metric("Precio Promedio", f"${df_filtrado['precio'].mean():,.2f}")

    st.divider()

    # --- GRÁFICOS ---
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Costos por Proveedor")
        fig1 = px.bar(df_filtrado, x="proveedor", y="costo", color="proveedor", text_auto='.2s')
        st.plotly_chart(fig1, use_container_width=True)

    with col_der:
        st.subheader("Distribución de Stock")
        fig2 = px.pie(df_filtrado, values="stock", names="descripcion", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    # --- TABLA DETALLADA ---
    st.subheader("📋 Detalle de Movimientos")
    st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error(f"Hubo un error al leer las columnas. Detalles: {e}")
    st.info("Asegúrate de que la primera fila de tu Excel sea exactamente: descripcion, proveedor, precio, salida pz, costo, stock, fecha, recibio, proyecto")
