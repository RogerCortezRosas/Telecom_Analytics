import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots


#Extraccion info
hojas = pd.read_excel("Internet.xlsx",sheet_name=None)

#Diccionario de DataFrames
data_frames = {}
for hoja, df in hojas.items():
  data_frames[hoja] = df


st.title("KPI's")


st.subheader('Aumento 2% al acceso al servicio de internet para el proximo trimestre , cada 100 hogares , por provincia')

penetracion_provincias = data_frames['Penetración-poblacion']

#Agregamos una nueva columna al DataFrame y lea gregamos la columna de Accesos por cada 100 hogares de la hoja hogares
penetracion_provincias['Accesos por cada 100 hogares'] = data_frames['Penetracion-hogares']['Accesos por cada 100 hogares']

penetracion_2024 = penetracion_provincias[penetracion_provincias['Año']==2024] # Tomamaos solo la info del ultimo año del ultimo trimestre

penetracion_2024['Nuevo_Acceso'] = penetracion_2024['Accesos por cada 100 hogares'] *1.02 # Agregamos una nueva columna con el calculo del 2% respecto al ultmo trimestre

fig = go.Figure()

# Grafica del trimestre actual

fig.add_trace(go.Bar(
                      x = penetracion_2024['Provincia'] , 
                      y = penetracion_2024['Accesos por cada 100 hogares'] ,
                      name = 'Acceso Actual',
                      marker_color = 'darkred'
))


fig.add_trace(go.Bar(
                      x = penetracion_2024['Provincia'] , 
                      y = penetracion_2024['Nuevo_Acceso'] ,
                      name = 'Acceso Aumento 2 %',
                      marker_color = 'lightcoral'
))

st.plotly_chart(fig)

st.subheader('Aumento 5% del numero de accesos de fibra optica para el proximo trimestre , para todas las provinicias ')

data_tec_loc = data_frames['Accesos_tecnologia_localidad'].groupby('Provincia')[['FIBRA OPTICA']].sum()
data_tec_loc['Nuevo_Acceso'] = data_tec_loc['FIBRA OPTICA'] * 1.05

figura = go.Figure()

# Grafica del trimestre actual

figura.add_trace(go.Bar(
                      x = data_tec_loc.index , 
                      y = data_tec_loc['FIBRA OPTICA'] ,
                      name = 'Acceso Actual',
                      marker_color = 'darkgreen'
))


figura.add_trace(go.Bar(
                      x = data_tec_loc.index , 
                      y = data_tec_loc['Nuevo_Acceso'] ,
                      name = 'Acceso Aumento 5 %',
                      marker_color = 'mediumseagreen'
))

st.plotly_chart(figura)

st.subheader(" Acceso de 0 % a la tecnologia de ADSL en 2 años ( tomando la taza de crecimiento)")

# Eliminamos las filas que tienen en provincia valores nulos
data_frames['Accesos_tecnologia_localidad'] = data_frames['Accesos_tecnologia_localidad'].dropna(subset=['Provincia'])

#Hacemos la sumatoria de accesos de internet por tecnologia

dicc_tecnologias ={
    'ADSL':0,

}

dicc_tecnologias['ADSL'] = data_frames['Accesos_tecnologia_localidad']['ADSL'].sum()

trimestres_totales = 9


decremento_trimestral = dicc_tecnologias['ADSL'] / trimestres_totales

# Crear DataFrame con la proyección de accesos por trimestre
data = {
    
    'Accesos_ADSL': [dicc_tecnologias['ADSL'] - decremento_trimestral * i for i in range(trimestres_totales + 1)]
}

list_años = ['2024','','','','2025','','','','2026']

df = pd.DataFrame.from_dict(data,orient = 'index',columns = [list_años,'Accesos_ADSL'])



# Crear la gráfica de línea
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list_años,
    y=df['Accesos_ADSL'],
    mode='lines+markers',
    name='Accesos ADSL',
    line=dict(color='red', width=4),
    marker=dict(size=10)
))

# Añadir título y etiquetas
fig.update_layout(
    title='Decrecimiento del Número de Accesos ADSL por Trimestre',
    xaxis_title='Trimestre',
    yaxis_title='Número de Accesos ADSL',
    xaxis=dict(tickmode='linear', dtick=1),
    yaxis=dict(tickformat='~s')  # Para formato simplificado de números grandes
)

# Mostrar la gráfica
fig.show()