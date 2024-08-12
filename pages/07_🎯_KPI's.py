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
                      marker_color = 'blue'
))


fig.add_trace(go.Bar(
                      x = penetracion_2024['Provincia'] , 
                      y = penetracion_2024['Nuevo_Acceso'] ,
                      name = 'Acceso Aumento 2 %',
                      marker_color = 'red'
))

st.plotly_chart(fig)