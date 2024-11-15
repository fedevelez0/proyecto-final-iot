
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Análisis de Sensores - Mi Ciudad", page_icon="📊", layout="wide")

# CSS personalizado
st.markdown("""
    <style>
    .main { padding: 2rem; background-color: #f4f4f9; }
    .stAlert, .stDataframe, .stMetric { background-color: #ffffff; padding: 10px; border-radius: 5px; }
    .stButton>button { background-color: #2c3e50; color: #ffffff; padding: 10px; font-size: 16px; }
    h1, h2, h3, h4, h5, h6 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title('📊 Análisis de Datos de Sensores en Mi Ciudad')
st.markdown("""
    Bienvenido al panel de análisis de datos. Esta aplicación permite visualizar y analizar datos de temperatura y 
    humedad recolectados por sensores en varios puntos de la ciudad. Puedes cargar tu archivo CSV para comenzar.
""")

# Ubicación en mapa para Universidad EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

# Mostrar mapa de ubicación
st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

# Subir archivo CSV
uploaded_file = st.file_uploader('Seleccione un archivo CSV con datos de temperatura y humedad', type=['csv'])

if uploaded_file:
    try:
        # Cargar y procesar datos
        df1 = pd.read_csv(uploaded_file)
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Renombrar columnas para simplicidad
        df1 = df1.rename(columns={
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        })

        # Pestañas para organizar análisis
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualización General", "📊 Análisis Estadístico", "🔍 Filtros y Comparación", "📅 Rango de Tiempo"])

        # Pestaña de visualización general
        with tab1:
            st.subheader('Visualización de Datos')

            # Selector de gráficos y variable
            variable = st.selectbox("Seleccione la variable a visualizar", ["temperatura", "humedad", "Ambas variables"])
            chart_type = st.selectbox("Seleccione el tipo de gráfico", ["Línea", "Área", "Barra", "Scatter"])

            # Generar gráficos según la selección
            if variable == "Ambas variables":
                # Gráficos combinados de temperatura y humedad
                fig_temp = px.line(df1, x=df1.index, y='temperatura', title="Temperatura en el Tiempo") if chart_type == "Línea" else \
                    px.area(df1, x=df1.index, y='temperatura', title="Temperatura en el Tiempo") if chart_type == "Área" else \
                    px.bar(df1, x=df1.index, y='temperatura', title="Temperatura en el Tiempo") if chart_type == "Barra" else \
                    px.scatter(df1, x=df1.index, y='temperatura', title="Temperatura en el Tiempo")
                fig_temp.update_traces(marker_color="tomato")
                st.plotly_chart(fig_temp)

                fig_hum = px.line(df1, x=df1.index, y='humedad', title="Humedad en el Tiempo") if chart_type == "Línea" else \
                    px.area(df1, x=df1.index, y='humedad', title="Humedad en el Tiempo") if chart_type == "Área" else \
                    px.bar(df1, x=df1.index, y='humedad', title="Humedad en el Tiempo") if chart_type == "Barra" else \
                    px.scatter(df1, x=df1.index, y='humedad', title="Humedad en el Tiempo")
                fig_hum.update_traces(marker_color="skyblue")
                st.plotly_chart(fig_hum)
            else:
                fig = px.line(df1, x=df1.index, y=variable, title=f"{variable.capitalize()} en el Tiempo") if chart_type == "Línea" else \
                    px.area(df1, x=df1.index, y=variable, title=f"{variable.capitalize()} en el Tiempo") if chart_type == "Área" else \
                    px.bar(df1, x=df1.index, y=variable, title=f"{variable.capitalize()} en el Tiempo") if chart_type == "Barra" else \
                    px.scatter(df1, x=df1.index, y=variable, title=f"{variable.capitalize()} en el Tiempo")
                fig.update_traces(marker_color="orange" if variable == "temperatura" else "lightblue")
                st.plotly_chart(fig)

            # Gráfico adicional: Distribución y Box Plot
            st.write("### Distribución de Datos")
            fig_hist = px.histogram(df1, x=variable, nbins=30, title=f"Distribución de {variable.capitalize()}")
            fig_hist.update_traces(marker_color="darkblue")
            st.plotly_chart(fig_hist)

            st.write("### Box Plot de Datos")
            fig_box = px.box(df1, y=variable, title=f"Box Plot de {variable.capitalize()}")
            fig_box.update_traces(marker_color="purple")
            st.plotly_chart(fig_box)

        # Pestaña de estadísticas
        with tab2:
            st.subheader('Análisis Estadístico')
            stat_variable = st.radio("Seleccione la variable para estadísticas", ["temperatura", "humedad"])
            stats_df = df1[stat_variable].describe()

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(stats_df)

            with col2:
                st.metric(f"Promedio de {stat_variable.capitalize()}", f"{stats_df['mean']:.2f}")
                st.metric(f"Máximo de {stat_variable.capitalize()}", f"{stats_df['max']:.2f}")
                st.metric(f"Mínimo de {stat_variable.capitalize()}", f"{stats_df['min']:.2f}")

            # Gráfico de Tendencia de Temperatura vs. Humedad
            st.write("### Gráfico de Dispersión: Temperatura vs. Humedad")
            fig_scatter = px.scatter(df1, x="temperatura", y="humedad", title="Relación entre Temperatura y Humedad")
            fig_scatter.update_traces(marker=dict(color="lightcoral", size=8))
            st.plotly_chart(fig_scatter)

        # Pestaña de filtros y comparación
        with tab3:
            st.subheader('Filtros y Comparación')
            filter_variable = st.selectbox("Seleccione la variable para filtrar", ["temperatura", "humedad"])

            col1, col2 = st.columns(2)
            with col1:
                min_val = st.slider(
                    f'Valor mínimo de {filter_variable}', 
                    float(df1[filter_variable].min()), 
                    float(df1[filter_variable].max()), 
                    float(df1[filter_variable].mean()), 
                    key="min_val"
                )
                filtrado_df_min = df1[df1[filter_variable] > min_val]
                st.write(f"Registros con {filter_variable} superior a {min_val}")
                st.dataframe(filtrado_df_min)

            with col2:
                max_val = st.slider(
                    f'Valor máximo de {filter_variable}', 
                    float(df1[filter_variable].min()), 
                    float(df1[filter_variable].max()), 
                    float(df1[filter_variable].mean()), 
                    key="max_val"
                )
                filtrado_df_max = df1[df1[filter_variable] < max_val]
                st.write(f"Registros con {filter_variable} inferior a {max_val}")
                st.dataframe(filtrado_df_max)

            # Gráfico de barras agrupadas por filtros
            st.write("### Gráfico Comparativo de Temperatura y Humedad")
            fig_bar = go.Figure(data=[
                go.Bar(name='Temperatura', x=filtrado_df_min.index, y=filtrado_df_min['temperatura'], marker_color='indianred'),
                go.Bar(name='Humedad', x=filtrado_df_min.index, y=filtrado_df_min['humedad'], marker_color='lightblue')
            ])
            fig_bar.update_layout(barmode='group', title="Comparación de Temperatura y Humedad Filtradas")
            st.plotly_chart(fig_bar)

        # Pestaña de rango de tiempo
        with tab4:
            st.subheader("Filtro de Rango de Tiempo")
            start_date = st.date_input("Fecha inicial", value=df1.index.min())
            end_date = st.date_input("Fecha final", value=df1

