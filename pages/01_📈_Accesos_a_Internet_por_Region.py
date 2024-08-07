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
            



# Figuras

suma_accesos = data_frames['Acc_vel_loc_sinrangos'].groupby('Provincia')['Suma_Acceso_Internet'].sum()
suma_accesos = pd.DataFrame(suma_accesos)
suma_accesos.reset_index(inplace=True)

num  = st.slider('Definir numero de provincias',5,10,15)

fig = plt.figure(figsize=(10,6))

sns.barplot(x='Provincia', y='Suma_Acceso_Internet', data=suma_accesos.iloc[:num],palette = 'Set3',hue = 'Provincia')
plt.title('Cantidad de accesos a internet por provincia')
plt.xticks(rotation=90)
st.pyplot(fig)




#lista provincias
lista_provincias = data_frames['Acc_vel_loc_sinrangos']['Provincia'].unique().tolist()

#variablequealmacena las provincias seleccionadas porelusuario
provincias = st.multiselect('Seleccione las provincias a analizar: ',lista_provincias)

#Dataframe con slasprovincias seleccionadas
def_provinicas = suma_accesos[suma_accesos['Provincia'].isin(provincias)]
#Grafica de las provincias seleccionadas
fig = plt.figure(figsize=(10,6))

sns.barplot(x='Provincia', y='Suma_Acceso_Internet', data=def_provinicas,palette = 'Set3',hue = 'Provincia')
plt.title('Cantidad de accesos a internet por provincia')
plt.xticks(rotation=90)
st.pyplot(fig)



col1 , col2 = st.columns(2)

with col1:
    def_provinicas =def_provinicas[def_provinicas['Provincia']=='CABA']

    fig = plt.figure(figsize=(10,6))
    sns.barplot(x='Provincia', y='Suma_Acceso_Internet', data=def_provinicas,palette = 'Set3',hue = 'Provincia')
    plt.title('Cantidad de accesos a internet CABA')
    plt.xticks(rotation=90)
    st.pyplot(fig)

with col2:
    def_provinicass =def_provinicas[def_provinicas['Provincia']=='CORDOBA']

    fig = plt.figure(figsize=(10,6))
    sns.barplot(x='Provincia', y='Suma_Acceso_Internet', data=def_provinicass,palette = 'Set3',hue = 'Provincia')
    plt.title('Cantidad de accesos a CORDOBA')
    plt.xticks(rotation=90)
    st.pyplot(fig)