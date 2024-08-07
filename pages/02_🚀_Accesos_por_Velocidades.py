import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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


st.markdown(" ## Grafica numero de accesos por velocidades")
st.markdown("---")

numero = st.number_input('Selecciona un número', min_value=1, max_value=24, value="min")


data_v = data_v.iloc[:numero]
fig = px.bar(data_v,data_v.index,data_v['Total Access'])

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

  # Graficas por provinciascon las velocidades de mayoracceso
  #hacemos un subplot para visulaizar las graficas de barras data_top_10 y data_Untop_10
  fig , axs = plt.subplots(2,3,figsize = (20 ,20)) 
  


  plt.suptitle('Provincias con mayor accesoa internet', fontsize=20)


  ax = axs[0,0]
  ax.set_title("Velocidades de bajada de la provincia de BUENOS AIRES")
  sns.barplot(x=data_Buenos_Aires_v.index, y='Total Access', data=data_Buenos_Aires_v, palette = 'Reds',hue = data_Buenos_Aires_v.index ,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[0,1]
  ax.set_title("Velocidades de bajada de la provincia de CABA")
  sns.barplot(x=data_CABA_vel.index, y='Total Access', data=data_CABA_vel, palette = 'Reds',hue = data_CABA_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[0,2]
  ax.set_title("Velocidades de bajada de la provincia de CORDOBA")
  sns.barplot(x=data_CORDOBA_vel.index, y='Total Access', data=data_CORDOBA_vel, palette = 'Reds',hue = data_CORDOBA_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[1,0]
  ax.set_title("Velocidades de bajada de la provincia de SANTA FE")
  sns.barplot(x=data_SANTA_FE_vel.index, y='Total Access', data=data_SANTA_FE_vel,palette = 'Reds',hue = data_SANTA_FE_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[1,1]
  ax.set_title("Velocidades de bajada de la provincia de MENDOZA")
  sns.barplot(x=data_MENDOZA_vel.index, y='Total Access', data=data_MENDOZA_vel,palette = 'Reds',hue = data_MENDOZA_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[1,2]
  ax.set_title("Velocidades de bajada de la provincia de ENTRE RIOS")
  sns.barplot(x=data_ENTRE_RIOS_vel.index, y='Total Access', data=data_ENTRE_RIOS_vel,palette = 'Reds',hue = data_ENTRE_RIOS_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  st.pyplot(fig)
    
if dim == 'Menor Acceso':
  data_TF_v=vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'TIERRA DEL FUEGO')
  data_FOR_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'FORMOSA')
  data_CAT_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'CATAMARCA')
  data_SC_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'SANTA CRUZ')
  data_RIOJA_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'LA RIOJA')
  data_SJ_vel = vel_provincia(data_frames['Acc_vel_loc_sinrangos'],'SAN JUAN')

  # Graficas por provinciascon las velocidades de mayoracceso
  #hacemos un subplot para visulaizar las graficas de barras data_top_10 y data_Untop_10
  fig , axs = plt.subplots(2,3,figsize = (30 ,20)) 



  plt.suptitle('Provincias con menor Acceso a Internet', fontsize=20)

  ax = axs[0,0]
  ax.set_title("Velocidades de bajada de la provincia de TIERRA DEL FUEGO")
  sns.barplot(x=data_TF_v.index, y='Total Access', data=data_TF_v, palette = 'Blues',hue = data_TF_v.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[0,1]
  ax.set_title("Velocidades de bajada de la provincia de FORMOSA")
  sns.barplot(x=data_FOR_vel.index, y='Total Access', data=data_FOR_vel, palette = 'Blues',hue = data_FOR_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[0,2]
  ax.set_title("Velocidades de bajada de la provincia de CATAMARCA")
  sns.barplot(x=data_CAT_vel.index, y='Total Access', data=data_CAT_vel, palette = 'Blues',hue = data_CAT_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[1,0]
  ax.set_title("Velocidades de bajada de la provincia de SANTA CRUZ")
  sns.barplot(x=data_SC_vel.index, y='Total Access', data=data_SC_vel,palette = 'Blues',hue = data_SC_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[1,1]
  ax.set_title("Velocidades de bajada de la provincia de LA RIOJA")
  sns.barplot(x=data_RIOJA_vel.index, y='Total Access', data=data_RIOJA_vel,palette = 'Blues',hue = data_RIOJA_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  ax = axs[1,2]
  ax.set_title("Velocidades de bajada de la provincia de SAN JUAN")
  sns.barplot(x=data_SJ_vel.index, y='Total Access', data=data_SJ_vel,palette = 'Blues',hue = data_SJ_vel.index,ax=ax)
  ax.set_xlabel('Velocidades')
  ax.set_ylabel('Numero de Accesos')

  # Ajustar layout
  plt.tight_layout()

  st.pyplot(fig)