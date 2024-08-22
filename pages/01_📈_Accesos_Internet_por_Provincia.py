import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import pymysql
import recarga_datos as reload



st.title('Accesos a Internet por Region') #______________________________________________________________________________________________________________

if st.button('Actualizar Datos'):# _________________________________________________________________________
   reload.reload_table() # llamada a ala funcion para actualizar la informacion
   st.success('Datos actualizados')


dataframes_dict = st.session_state.dataframes_dict # Acceder al diccionario de DataFrames



dataframes_dict['acc_vel_loc_sinrangos'] = dataframes_dict['acc_vel_loc_sinrangos'].fillna(0) #ELiminacion de nulos de acc_vel_loc_sinrangos


dataframes_dict['acc_vel_loc_sinrangos']['Suma_Acceso_Internet'] = dataframes_dict['acc_vel_loc_sinrangos'].iloc[:, 4:].sum(axis=1) #Agregamos columna Suma_Acceso_Internet



suma_accesos = dataframes_dict['acc_vel_loc_sinrangos'].groupby('Provincia')['Suma_Acceso_Internet'].sum().sort_values(ascending=False) # Agrupacio por provinicas y hace la sumatoria de todos los accesos y se lo asigna a la variable suma_accesos

suma_accesos = pd.DataFrame(suma_accesos)# convertimos de tipo series a dataframe

suma_accesos.reset_index(inplace=True) #Reset de indices 




if st.checkbox('Accesos a Internet por Provincias'):# _________________________________________________________________________________________________



   if st.button('Tabla'):
      st.write( suma_accesos)

   if st.button('Mostrar Grafica'):

      paleta_colores = sns.color_palette("coolwarm",len(suma_accesos.index.tolist())).as_hex()

      figura = go.Figure()

      figura.add_trace(go.Bar( x = suma_accesos['Provincia'] , y = suma_accesos['Suma_Acceso_Internet'],marker=dict(color=paleta_colores)))
      figura.update_layout(title='Cantidad de accesos a internet por provincia' )

      st.plotly_chart(figura)




if st.checkbox('Accesos a Internet por Partido'): # ___________________________________________________________________________________________________
   
   
   lista_provincias = dataframes_dict['acc_vel_loc_sinrangos']['Provincia'].unique().tolist() #lista provincias

  
   provincia = st.multiselect('Seleccione las provincia a analizar: ',lista_provincias)  #variable que almacena las provincias seleccionadas por el usuario

   data_provincia = dataframes_dict['acc_vel_loc_sinrangos'][dataframes_dict['acc_vel_loc_sinrangos']['Provincia'].isin(provincia)] # obtencion de dataframe filtrando solo la informacion de la provinica seleccionada por el usuario
   data_provincia = data_provincia.groupby('Partido')['Suma_Acceso_Internet'].sum().sort_values(ascending=False)[:10].reset_index() # Agrupacion por Partido y sumando los accesos de ese partido despues se filtran de manera edscndiemte las primeras 10 filas y se reinicia los indices

   paleta_colores = sns.color_palette("bright",len(data_provincia.index.tolist())).as_hex()

   figura = go.Figure()

   figura.add_trace(go.Bar( x = data_provincia['Partido'] , y = data_provincia['Suma_Acceso_Internet'],marker=dict(color=paleta_colores)))
   figura.update_layout(title='Cantidad de accesos a internet por partido' )

   st.plotly_chart(figura)


st.image("imagenes/mapa-removebg-preview.png")

