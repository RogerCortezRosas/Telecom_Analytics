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

# Eliminamos las filas que tienen en provincia valores nulos
data_frames['Accesos_tecnologia_localidad'] = data_frames['Accesos_tecnologia_localidad'].dropna(subset=['Provincia'])

#Hacemos la sumatoria de accesos de internet por tecnologia

dicc_tecnologias ={
    'ADSL':0,
    'CABLEMODEM':0,
    'DIAL UP':0,
    'FIBRA OPTICA':0,
    'OTROS':0,
    'SATELITAL':0,
    'WIMAX':0,
    'WIRELESS':0,


}

for i in dicc_tecnologias.keys():
  dicc_tecnologias[i] = data_frames['Accesos_tecnologia_localidad'][i].sum()

#Hacemos un dataframe con la cantidad y el porcentaje de accesos a internet por cada tecnologia
df_tecnologias = pd.DataFrame.from_dict(dicc_tecnologias,orient = 'index' , columns = ['Total Access'])
df_tecnologias['% Total'] = df_tecnologias['Total Access'] / df_tecnologias['Total Access'].sum() * 100
df_tecnologias.sort_values(by='% Total',ascending=False)

st.title('Accesos a Internet por Tecnologias')
st.markdown("---")

if st.button('Tabla'):
  st.write(df_tecnologias.sort_values(by='% Total',ascending=False))

if st.button('Graficas'):

  #Hacemos un grafico tipo pie para observar la ditribucion de los acceos a internet las diferentees tecnologias


    colors = ['Red','Green','Blue','Orange','Brown','Black','White','Pink']

    figura= px.pie(df_tecnologias,values=dicc_tecnologias.values() , names = dicc_tecnologias.keys() , color = dicc_tecnologias.keys() ,
                   color_discrete_sequence=colors , title='Distribucion de los accesos a internet por tecnologia')
    st.plotly_chart(figura)



st.markdown(" ## Graficas de acceso a Tecnologias por provincia")
st.markdown("---")
lista_tec = df_tecnologias.index.tolist()

tecnologia = st.multiselect('Seleccione tecnologia',lista_tec,max_selections=1)

data_tec_loc = data_frames['Accesos_tecnologia_localidad'].groupby('Provincia')[['ADSL','CABLEMODEM','DIAL UP','FIBRA OPTICA','OTROS','SATELITAL','WIMAX','WIRELESS']].sum()





col1 , col2 = st.columns(2)

with col1:
    data_top_10 = data_tec_loc.sort_values(by=tecnologia,ascending=False)[:10]

    fig = plt.figure(figsize=(10,6))
    
    

    
    sns.barplot(x='Provincia', y = data_top_10[tecnologia].to_numpy().flatten(), data = data_top_10, palette = 'viridis',hue = 'Provincia')
    plt.title(f'Top 10 Provincias con mayor demanda de {tecnologia}')
    plt.xticks(rotation = 90)
    st.pyplot(fig)

with col2:
    data_Untop_10= data_tec_loc.sort_values(by=tecnologia,ascending=True)[:10]

    fig = plt.figure(figsize=(10,6))
    sns.barplot(x='Provincia', y = data_Untop_10[tecnologia].to_numpy().flatten(), data = data_Untop_10, palette = 'PuRd',hue = 'Provincia')
    plt.title(f'Top 10 Provincias con menor demanda de {tecnologia}')
    plt.xticks(rotation = 90)
    st.pyplot(fig)