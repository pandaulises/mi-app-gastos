import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (esto es lo primero que ve el navegador)
st.set_page_config(page_title="Gestión de Proyectos", layout="wide")

# 2. El enlace que me pasaste (Ya integrado)
SHEET_URL = "https://google.com"

# 3. Función para leer los datos
@st.cache_data # Esto hace que la app sea rápida y no descargue todo cada segundo
def cargar_datos():
    # Leemos el CSV desde tu enlace
    df = pd.read_csv(SHEET_URL)
    
    # Limpieza básica: Aseguramos que la columna FECHA sea entendida como fecha por Python
    if 'FECHA' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
    
    return df

# 4. Título de la aplicación
st.title("📊 Panel de Control: Proyectos y Proveedores")
st.markdown("Datos extraídos en tiempo real desde Google Sheets")

try:
    # Cargamos los datos en una variable llamada 'df'
    df = cargar_datos()

    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.header("Filtros de Búsqueda")
    
    # Creamos un filtro por PROYECTO
    proyectos_disponibles = df["PROYECTO"].unique()
    seleccion_proy = st.sidebar.multiselect("Filtrar por Proyecto:", proyectos_disponibles, default=proyectos_disponibles)

    # Creamos un filtro por PROOVEDOR
    proveedores_disponibles = df["PROOVEDOR"].unique()
    seleccion_prov = st.sidebar.multiselect("Filtrar por Proveedor:", proveedores_disponibles, default=proveedores_disponibles)

    # Aplicamos los filtros a los datos
    df_filtrado = df[df["PROYECTO"].isin(seleccion_proy) & df["PROOVEDOR"].isin(seleccion_prov)]

    # --- CUADROS DE RESUMEN (MÉTRICAS) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Recibido", f"${df_filtrado['RECIBIDO'].sum():,.2f}")
    with c2:
        st.metric("Costo Total", f"${df_filtrado['COSTO'].sum():,.2f}")
    with c3:
        # Calculamos la diferencia entre Precio y Costo
        utilidad = df_filtrado['PRECIO'].sum() - df_filtrado['COSTO'].sum()
        st.metric("Margen (Precio - Costo)", f"${utilidad:,.2f}")

    # --- GRÁFICOS ---
    st.divider() # Una línea para separar
    
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Inversión por Proyecto")
        fig1 = px.bar(df_filtrado, x="PROYECTO", y="COSTO", color="PROYECTO", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col_der:
        st.subheader("Distribución por Proveedor")
        fig2 = px.pie(df_filtrado, values="COSTO", names="PROOVEDOR")
        st.plotly_chart(fig2, use_container_width=True)

    # --- TABLA FINAL ---
    st.subheader("Listado Detallado")
    st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error(f"Hubo un problema al leer los datos. Error: {e}")
