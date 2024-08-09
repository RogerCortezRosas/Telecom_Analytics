import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#Extraccion info
hojas = pd.read_excel("Internet.xlsx",sheet_name=None)

#Diccionario de DataFrames
data_frames = {}
for hoja, df in hojas.items():
  data_frames[hoja] = df

#ELiminacion de nulos de Acc_vel_loc_sinrangos
data_frames['Acc_vel_loc_sinrangos'] = data_frames['Acc_vel_loc_sinrangos'].fillna(0)


st.title('Accesos a Internet por Velocidades')

velocidades = data_frames['Acc_vel_loc_sinrangos'].columns[4:len(data_frames['Acc_vel_loc_sinrangos'].columns)-1].tolist() #Lista de las velocidades

dicc_vel = {}
for velocidad in velocidades:
    dicc_vel[velocidad] = data_frames['Acc_vel_loc_sinrangos'][velocidad].sum() #Diccionario que almacena como key el texto de la velocidad y como value la suma total de accesos a esa velocidad


data_v = pd.DataFrame.from_dict(dicc_vel,orient='index',columns=['Total Access']) #Conversion deldiccionario a dataframe

data_v = data_v.sort_values(by='Total Access',ascending=False) #Ordenamos de forma descendiente (mayor -> menor) los valores




if st.button('Tabla'):
    st.write( data_v)


st.subheader("  Grafica numero de accesos por velocidades")
st.markdown("---")

numero = st.number_input('Selecciona un número', min_value=1, max_value=24, value="min")


data_v = data_v.iloc[:numero]
fig = px.bar(data_v,data_v.index,data_v['Total Access'])
fig.update_xaxes(title_text ='Velocidades' )

st.plotly_chart(fig)

st.markdown(" ## Accesos por velocidades de las regiones con mayor y menor acceso a Internet")
st.markdown("---")

dim = st.radio('Provincias:' , ('Mayor Acceso','Menor Acceso')) # Seleccionador de mayor o menor acceso

def vel_provincia(df,provincia):
  """Funcion que recibe por parametro el Dataframe data_frames['Acc_vel_loc_sinrangos'] y el nombre de una provincia y devuelve como resultado un data frame agrupado por provincia
  las 5 velocidades en donde hay la mayor cantidad de accesos"""
  df = data_frames['Acc_vel_loc_sinrangos'][data_frames['Acc_vel_loc_sinrangos']['Provincia'] == provincia]
  velocidades = df.columns[4:len(df.columns)-1].tolist()
  dicc_vel = {}
  for velocidad in velocidades:
    dicc_vel[velocidad] = df[velocidad].sum()
  df_vel = pd.DataFrame.from_dict(dicc_vel,orient='index',columns=['Total Access'])
  df_vel = df_vel.sort_values(by='Total Access',ascending=False).iloc[:5]
  return df_vel

if dim == 'Mayor Acceso':


  data_Buenos_Aires_v=vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'BUENOS AIRES')
  data_CABA_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'CABA')
  data_CORDOBA_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'CORDOBA')
  data_SANTA_FE_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'SANTA FE')
  data_MENDOZA_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'MENDOZA')
  data_ENTRE_RIOS_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'ENTRE RIOS')

  

  paleta_colores = sns.color_palette("Reds",len(data_Buenos_Aires_v.index.tolist())).as_hex()

    # Crear subplots (como en el paso anterior)
  fig = make_subplots(rows=2, cols=3,subplot_titles=('BUENOS AIRES','CABA','CORDOBA','SANTA FE','MENDOZA','ENTRE RIOS'),vertical_spacing=0.3 )

  fig.add_trace(go.Bar(x = data_Buenos_Aires_v.index , y = data_Buenos_Aires_v['Total Access'],marker=dict(color=paleta_colores)),row = 1 , col = 1)
  fig.add_trace(go.Bar(x = data_CABA_vel.index , y = data_CABA_vel['Total Access'],marker=dict(color=paleta_colores)),row = 1 , col = 2)
  fig.add_trace(go.Bar(x = data_CORDOBA_vel.index , y = data_CORDOBA_vel['Total Access'],marker=dict(color=paleta_colores)),row = 1 , col = 3)
  fig.add_trace(go.Bar(x = data_SANTA_FE_vel.index , y = data_SANTA_FE_vel['Total Access'],marker=dict(color=paleta_colores)),row = 2 , col = 1)
  fig.add_trace(go.Bar(x = data_MENDOZA_vel.index , y = data_MENDOZA_vel['Total Access'],marker=dict(color=paleta_colores)),row = 2 , col = 2)
  fig.add_trace(go.Bar(x = data_ENTRE_RIOS_vel.index , y = data_ENTRE_RIOS_vel['Total Access'],marker=dict(color=paleta_colores)),row = 2 , col = 3)

  fig.update_layout(yaxis_title = 'Numero de Accesos' )
  st.plotly_chart(fig)


  
    
if dim == 'Menor Acceso':
  data_TF_v=vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'TIERRA DEL FUEGO')
  data_FOR_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'FORMOSA')
  data_CAT_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'CATAMARCA')
  data_SC_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'SANTA CRUZ')
  data_RIOJA_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'LA RIOJA')
  data_SJ_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'SAN JUAN')


  paleta_colores = sns.color_palette("Blues",len(data_TF_v.index.tolist())).as_hex()

    # Crear subplots (como en el paso anterior)
  fig = make_subplots(rows=2, cols=3,subplot_titles=('TIERRA DEL FUEGO','FORMOSA','CATAMARCA','SANTA CRUZ','LA RIOJA','SAN JUAN'),vertical_spacing=0.3 )

  fig.add_trace(go.Bar(x = data_TF_v.index , y = data_TF_v['Total Access'],marker=dict(color=paleta_colores)),row = 1 , col = 1)
  
 
  fig.add_trace(go.Bar(x = data_FOR_vel.index , y = data_FOR_vel['Total Access'],marker=dict(color=paleta_colores)),row = 1 , col = 2)
  fig.add_trace(go.Bar(x = data_CAT_vel.index , y = data_CAT_vel['Total Access'],marker=dict(color=paleta_colores)),row = 1 , col = 3)
  fig.add_trace(go.Bar(x = data_SC_vel.index , y = data_SC_vel['Total Access'],marker=dict(color=paleta_colores)),row = 2 , col = 1)
  fig.add_trace(go.Bar(x = data_RIOJA_vel.index , y = data_RIOJA_vel['Total Access'],marker=dict(color=paleta_colores)),row = 2 , col = 2)
  fig.add_trace(go.Bar(x = data_SJ_vel.index , y = data_SJ_vel['Total Access'],marker=dict(color=paleta_colores)),row = 2 , col = 3)

  fig.update_layout(yaxis_title = 'Numero de Accesos' )

  st.plotly_chart(fig)



st.sidebar.image("imagenes/velocidad.png")