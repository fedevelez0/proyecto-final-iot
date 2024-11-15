
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Análisis de Sensores - Mi Ciudad", page_icon="📊", layout="wide")

# CSS personalizado
st.markdown("""
    <style>
    .main { padding: 2rem; background-color: #f4f4f9; }
    .stAlert, .stDataframe, .stMetric { background-color: #ffffff; padding: 10px; border-radius: 5px; }
    h1, h2, h3, h4, h5, h6 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title('📊 Análisis de datos de Sensores en Mi Ciudad')
st.markdown("Esta aplicación permite analizar datos de temperatura y humedad recolectados por sensores en diferentes puntos de la ciudad.")

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
uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

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
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "📅 Rango de Tiempo"])

        # Pestaña de visualización de datos
        with tab1:
            st.subheader('Visualización de Datos')
            variable = st.selectbox("Seleccione variable a visualizar", ["temperatura", "humedad", "Ambas variables"])
            chart_type = st.selectbox("Seleccione tipo de gráfico", ["Línea", "Área", "Barra"])

            # Mostrar gráficos de la variable seleccionada
            if variable == "Ambas variables":
                st.write("### Temperatura")
                fig_temp = px.line(df1, x=df1.index, y='temperatura', title="Temperatura en el Tiempo") if chart_type == "Línea" else \
                    px.area(df1, x=df1.index, y='temperatura', title="Temperatura en el Tiempo") if chart_type == "Área" else \
                    px.bar(df1, x=df1.index, y='temperatura', title="Temperatura en el Tiempo")
                st.plotly_chart(fig_temp)

                st.write("### Humedad")
                fig_hum = px.line(df1, x=df1.index, y='humedad', title="Humedad en el Tiempo") if chart_type == "Línea" else \
                    px.area(df1, x=df1.index, y='humedad', title="Humedad en el Tiempo") if chart_type == "Área" else \
                    px.bar(df1, x=df1.index, y='humedad', title="Humedad en el Tiempo")
                st.plotly_chart(fig_hum)
            else:
                fig = px.line(df1, x=df1.index, y=variable, title=f"{variable.capitalize()} en el Tiempo") if chart_type == "Línea" else \
                    px.area(df1, x=df1.index, y=variable, title=f"{variable.capitalize()} en el Tiempo") if chart_type == "Área" else \
                    px.bar(df1, x=df1.index, y=variable, title=f"{variable.capitalize()} en el Tiempo")
                st.plotly_chart(fig)

            # Gráfico de distribución y box plot
            st.write("### Distribución de Datos")
            fig_hist = px.histogram(df1, x=variable, title=f"Distribución de {variable.capitalize()}")
            st.plotly_chart(fig_hist)

            st.write("### Box Plot de Datos")
            fig_box = px.box(df1, y=variable, title=f"Box Plot de {variable.capitalize()}")
            st.plotly_chart(fig_box)

            # Mostrar datos crudos
            if st.checkbox('Mostrar datos crudos'):
                st.write(df1)

        # Pestaña de estadísticas
        with tab2:
            st.subheader('Análisis Estadístico')
            stat_variable = st.radio("Seleccione variable para estadísticas", ["temperatura", "humedad"])
            stats_df = df1[stat_variable].describe()

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(stats_df)

            with col2:
                if stat_variable == "temperatura":
                    st.metric("Temperatura Promedio", f"{stats_df['mean']:.2f}°C")
                    st.metric("Temperatura Máxima", f"{stats_df['max']:.2f}°C")
                    st.metric("Temperatura Mínima", f"{stats_df['min']:.2f}°C")
                else:
                    st.metric("Humedad Promedio", f"{stats_df['mean']:.2f}%")
                    st.metric("Humedad Máxima", f"{stats_df['max']:.2f}%")
                    st.metric("Humedad Mínima", f"{stats_df['min']:.2f}%")

        # Pestaña de filtros de datos
        with tab3:
            st.subheader('Filtros de Datos')
            filter_variable = st.selectbox("Seleccione variable para filtrar", ["temperatura", "humedad"])

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
                st.write(f"Registros con {filter_variable} superior a {min_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
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
                st.write(f"Registros con {filter_variable} inferior a {max_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_max)

            # Descarga de datos filtrados
            if st.button('Descargar datos filtrados'):
                csv = filtrado_df_min.to_csv().encode('utf-8')
                st.download_button(label="Descargar CSV", data=csv, file_name='datos_filtrados.csv', mime='text/csv')

        # Pestaña de filtro de rango de tiempo
        with tab4:
            st.subheader("Filtro de Rango de Tiempo")
            start_date = st.date_input("Fecha inicial", value=df1.index.min())
            end_date = st.date_input("Fecha final", value=df1.index.max())
            
            if start_date <= end_date:
                df_filtered = df1.loc[start_date:end_date]
                st.write(f"Datos desde {start_date} hasta {end_date}")
                st.line_chart(df_filtered[variable])
            else:
                st.error("La fecha de inicio debe ser anterior o igual a la fecha final.")

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')
else:
    st.warning('Por favor, cargue un archivo CSV para comenzar el análisis.')

# Footer
st.markdown("""
    ---
    Desarrollado para el análisis de datos de sensores urbanos.
    Ubicación: Universidad EAFIT, Medellín, Colombia
""")

