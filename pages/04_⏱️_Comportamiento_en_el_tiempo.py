import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#Extraccion info
hojas = pd.read_excel("Internet.xlsx",sheet_name=None)

#Diccionario de DataFrames
data_frames = {}
for hoja, df in hojas.items():
  data_frames[hoja] = df

st.title('Analisis del comportamiento en el tiempo')


vel_totales = data_frames['Totales VMD']

#Graficamos un lineplot por año

fig = px.line(vel_totales, x='Año', y='Mbps (Media de bajada)', title='Velocidad de bajada por año totales')

st.plotly_chart(fig)