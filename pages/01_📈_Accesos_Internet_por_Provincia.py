import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


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
      fig = plt.figure(figsize=(10,6))
      sns.barplot(x='Provincia', y='Suma_Acceso_Internet', data=suma_accesos,palette = 'Set3',hue = 'Provincia')
      plt.title('Cantidad de accesos a internet por provincia')
      plt.xticks(rotation=90)
      st.pyplot(fig)


if st.checkbox('Accesos a Internet por Partido'):
   
    #lista provincias
    lista_provincias = data_frames['Acc_vel_loc_sinrangos']['Provincia'].unique().tolist()

    #variablequealmacena las provincias seleccionadas porelusuario
    provincia = st.multiselect('Seleccione las provincia a analizar: ',lista_provincias)

    data_provincia = data_frames['Acc_vel_loc_sinrangos'][data_frames['Acc_vel_loc_sinrangos']['Provincia'].isin(provincia)]
    data_provincia = data_provincia.groupby('Partido')['Suma_Acceso_Internet'].sum().sort_values(ascending=False)[:10].reset_index()

    fig = plt.figure(figsize=(10,6))
    sns.barplot(x='Partido', y='Suma_Acceso_Internet', data=data_provincia,palette = 'Set3',hue = 'Partido')
    plt.title('Cantidad de accesos a internet por provincia')
    plt.xticks(rotation=90)
    st.pyplot(fig)

