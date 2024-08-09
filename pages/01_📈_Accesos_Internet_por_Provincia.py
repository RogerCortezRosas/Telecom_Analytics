import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objs as go



st.title('Accesos a Internet por Region')


#Extraccion info
hojas = pd.read_excel("Internet.xlsx",sheet_name=None)

#Diccionario de DataFrames
data_frames = {}
for hoja, df in hojas.items():
  data_frames[hoja] = df

#ELiminacion de nulos de Acc_vel_loc_sinrangos
data_frames['Acc_vel_loc_sinrangos'] = data_frames['Acc_vel_loc_sinrangos'].fillna(0)

#Agregamos columna Suma_Acceso_Internet
data_frames['Acc_vel_loc_sinrangos']['Suma_Acceso_Internet'] = data_frames['Acc_vel_loc_sinrangos'].iloc[:, 4:].sum(axis=1)

#Provincias
data_frames['Acc_vel_loc_sinrangos'].groupby('Provincia')['Suma_Acceso_Internet'].sum().sort_values(ascending=False)


# Figuras

suma_accesos = data_frames['Acc_vel_loc_sinrangos'].groupby('Provincia')['Suma_Acceso_Internet'].sum()
suma_accesos = pd.DataFrame(suma_accesos)
suma_accesos.reset_index(inplace=True)




if st.checkbox('Accesos a Internet por Provincias'):



   if st.button('Tabla'):
      st.write( data_frames['Acc_vel_loc_sinrangos'].groupby('Provincia')['Suma_Acceso_Internet'].sum().sort_values(ascending=False))

   if st.button('Mostrar Grafica'):

      paleta_colores = sns.color_palette("coolwarm",len(suma_accesos.index.tolist())).as_hex()

      figura = go.Figure()

      figura.add_trace(go.Bar( x = suma_accesos['Provincia'] , y = suma_accesos['Suma_Acceso_Internet'],marker=dict(color=paleta_colores)))
      figura.update_layout(title='Cantidad de accesos a internet por provincia' )

      st.plotly_chart(figura)




if st.checkbox('Accesos a Internet por Partido'):
   
   #lista provincias
   lista_provincias = data_frames['Acc_vel_loc_sinrangos']['Provincia'].unique().tolist()

   #variablequealmacena las provincias seleccionadas porelusuario
   provincia = st.multiselect('Seleccione las provincia a analizar: ',lista_provincias)

   data_provincia = data_frames['Acc_vel_loc_sinrangos'][data_frames['Acc_vel_loc_sinrangos']['Provincia'].isin(provincia)]
   data_provincia = data_provincia.groupby('Partido')['Suma_Acceso_Internet'].sum().sort_values(ascending=False)[:10].reset_index()

   paleta_colores = sns.color_palette("bright",len(data_provincia.index.tolist())).as_hex()

   figura = go.Figure()

   figura.add_trace(go.Bar( x = data_provincia['Partido'] , y = data_provincia['Suma_Acceso_Internet'],marker=dict(color=paleta_colores)))
   figura.update_layout(title='Cantidad de accesos a internet por partido' )

   st.plotly_chart(figura)


st.image("imagenes/mapa-removebg-preview.png")

