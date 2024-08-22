import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import recarga_datos as reload



st.title('Accesos a Internet por Region')

if st.button('Actualizar Datos'):
   reload.reload_table()
   st.success('Datos actualizados')

dataframes_dict = st.session_state.dataframes_dict # Acceder al diccionario de DataFrames


st.title("Penetracion por habitantes/hogares")# Titulo _________________________________________________________________________________________________________________________


penetracion_total = dataframes_dict['penetracion_totales'] # Creacion de df 


# Grafica _____________________________________________________________________________________________________________________
fig = make_subplots(rows=1, cols=2,subplot_titles=('Penetracion por hogares','Penetracion por habitantes'))


fig.add_trace(go.Scatter(x = penetracion_total['Año'] , y = penetracion_total['Accesos por cada 100 hogares']),row = 1 , col = 1)
fig.add_trace(go.Scatter(x = penetracion_total['Año'] , y = penetracion_total['Accesos por cada 100 hab']),row = 1 , col = 2)


fig.update_layout(height=600, width=900,title="Penetracion por hogares/habitantes totales")
fig.update_xaxes(range=[2014,2025],tickangle=90,tickvals=[2014,2019,2020,2022,2024])

st.plotly_chart(fig)

######################################################################################################################################


penetracion_provincias = dataframes_dict['penetración_poblacion'] #Obtenemos un Dataframe  de la hoja penetración_poblacion

penetracion_provincias['Accesos por cada 100 hogares'] = dataframes_dict['penetracion_hogares']['Accesos por cada 100 hogares'] #Agregamos una nueva columna al DataFrame y le agregamos la columna de Accesos por cada 100 hogares de la hoja hogares
lista_provincias = penetracion_provincias['Provincia'].unique().tolist() # Creacion lista de provincias
lista_pen = penetracion_provincias.columns[:][-2:].tolist() # lista de penentracion hogares / habitantes

def taza_crecimiento_penetracion_total(data):
  """Funcion que obtiene un dataframe con las taza de crecimientode de la penetracion por hogar y por habitante por provincia"""
    
  df_general = pd.DataFrame(columns=['Provincia','Accesos por cada 100 hab','Accesos por cada 100 hogares']) # Se crea un data frame df_general
  df_general['Provincia'] = lista_provincias #Asigna la lista a la columna Provincia
  taza_pen = {}
  contador = 0

  for provincia in lista_provincias:
    provi = penetracion_provincias[penetracion_provincias['Provincia'] == provincia]
    provi = provi.sort_values(by=['Año','Trimestre'],ascending=True)
    
    for i in lista_pen:
      
      provi['taza'] = provi[i].pct_change() * 100
      taza = provi.groupby('Año')['taza'].mean().reset_index()
      taza_pen[provincia] = taza['taza'].mean()

  df_taza_pen = pd.DataFrame.from_dict(taza_pen,orient='index',columns=['Taza'])
    

  
    

  return df_taza_pen




taza_penetracion_total = taza_crecimiento_penetracion_total(penetracion_provincias) #Obtencion de df de la taza porhabitantes y por hogares


hogares = taza_penetracion_total.sort_values(by='Taza',ascending=False) # Data frame con ordenacion por hogares





paleta_colores = sns.color_palette("colorblind",len(taza_penetracion_total.index.tolist())).as_hex()



# Crear subplots (como en el paso anterior)
figura = make_subplots(rows=1, cols=2,subplot_titles=('Penetracion por hogares','Penetracion por habitantes'))


figura.add_trace(go.Bar(x = hogares.index, y = hogares['Taza'],marker=dict(color=paleta_colores)),row = 1 , col = 1)



figura.update_layout(height=600, width=900,title="Taza promedio de crecimiento de penetracion por hogares/habitantes totales")


st.plotly_chart(figura)

st.sidebar.image("imagenes/poblacion.png")
