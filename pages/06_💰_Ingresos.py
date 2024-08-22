import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import recarga_datos as reload



st.title('Accesos a Internet por Region')

if st.button('Actualizar Datos'):
   reload.reload_table()
   st.success('Datos actualizados')


dataframes_dict = st.session_state.dataframes_dict # Acceder al diccionario de DataFrames

st.title("Ingresos")

data_ingresos = dataframes_dict['ingresos'] 
data_ingresos.replace(2033,2023,inplace=True)
data_ingresos.sort_values(by='Año',ascending=True,inplace=True)
taza_ingresos = data_ingresos['Ingresos (miles de pesos)'].pct_change() * 100
data_ingresos['Taza'] = taza_ingresos


# Crear subplots (como en el paso anterior)
fig = make_subplots(rows=1, cols=2,subplot_titles=('Ingresos (miles de pesos)','Taza de Ingresos'))


fig.add_trace(go.Scatter(x = data_ingresos['Año'] , y = data_ingresos['Ingresos (miles de pesos)']),row = 1 , col = 1)
fig.add_trace(go.Scatter(x = data_ingresos['Año'] , y = data_ingresos['Taza']),row = 1 , col = 2)


fig.update_layout(height=600, width=900,title="Ingresos")
fig.update_xaxes(range=[2014,2025],tickangle=90,tickvals=[2014,2019,2020,2022,2024])

st.plotly_chart(fig)






st.sidebar.image("imagenes/ingresos.jpg")


