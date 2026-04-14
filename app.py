import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Control de Inventario", layout="wide")

# REEMPLAZA ESTO CON TU ENLACE REAL (Debe terminar en /export?format=csv)
URL = "https://google.com"

@st.cache_data
def cargar_datos():
    # Leemos el CSV y forzamos a que todo sea texto primero para evitar errores de puntos/comas
    df = pd.read_csv(URL, dtype=str)
    
    # Limpiamos nombres de columnas (quita espacios y pone minúsculas)
    df.columns = df.columns.str.strip().str.lower()
    
    # Convertimos a números las columnas importantes, ignorando puntos raros
    cols_num = ['precio', 'costo', 'stock', 'salida pz']
    for col in cols_num:
        if col in df.columns:
            # Quitamos puntos de miles si existen y convertimos a número
            df[col] = pd.to_numeric(df[col].str.replace('.', '', regex=False), errors='coerce').fillna(0)
    
    return df

st.title("📊 Mi Dashboard de Inventario")

try:
    df = cargar_datos()

    # --- FILTROS ---
    st.sidebar.header("Opciones")
    
    # Filtro de Proyecto (Columna A)
    lista_proyectos = df["proyecto"].unique()
    sel_proy = st.sidebar.multiselect("Proyecto:", lista_proyectos, default=lista_proyectos)

    # Filtro de Proveedor (Columna C)
    lista_prov = df["proveedor"].unique()
    sel_prov = st.sidebar.multiselect("Proveedor:", lista_prov, default=lista_prov)

    # Aplicar filtros
    df_filtrado = df[df["proyecto"].isin(sel_proy) & df["proveedor"].isin(sel_prov)]

    # --- MÉTRICAS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Inversión Total", f"${df_filtrado['costo'].sum():,.2f}")
    m2.metric("Stock en Almacén", int(df_filtrado['stock'].sum()))
    m3.metric("Movimientos", len(df_filtrado))

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Gasto por Proyecto")
        fig1 = px.bar(df_filtrado, x="proyecto", y="costo", color="proyecto")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.subheader("Top Productos (Stock)")
        fig2 = px.pie(df_filtrado, values="stock", names="descripcion")
        st.plotly_chart(fig2, use_container_width=True)

    # --- TABLA ---
    st.subheader("Detalle de la Hoja")
    st.dataframe(df_filtrado)

except Exception as e:
    st.error(f"Error en los datos: {e}")
    st.info("Asegúrate de que el enlace en el código sea el correcto.")
