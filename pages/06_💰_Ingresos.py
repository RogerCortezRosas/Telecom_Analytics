import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#Extraccion info
hojas = pd.read_excel("Internet.xlsx",sheet_name=None)

#Diccionario de DataFrames
data_frames = {}
for hoja, df in hojas.items():
  data_frames[hoja] = df

st.title("Ingresos")

data_ingresos = data_frames['Ingresos '] 
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





