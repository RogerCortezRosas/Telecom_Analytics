import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#Extraccion info
hojas = pd.read_excel("Internet.xlsx",sheet_name=None)

#Diccionario de DataFrames
data_frames = {}
for hoja, df in hojas.items():
  data_frames[hoja] = df



st.title("Penetracion por habitantes/hogares")


penetracion_total = data_frames['Penetracion-totales']


# Crear subplots (como en el paso anterior)
fig = make_subplots(rows=1, cols=2,subplot_titles=('Penetracion por hogares','Penetracion por habitantes'))


fig.add_trace(go.Scatter(x = penetracion_total['Año'] , y = penetracion_total['Accesos por cada 100 hogares']),row = 1 , col = 1)
fig.add_trace(go.Scatter(x = penetracion_total['Año'] , y = penetracion_total['Accesos por cada 100 hab']),row = 1 , col = 2)


fig.update_layout(height=600, width=900,title="Penetracion por hogares/habitantes totales")
fig.update_xaxes(range=[2014,2025],tickangle=90,tickvals=[2014,2019,2020,2022,2024])

st.plotly_chart(fig)

######################################################################################################################################

#Obtenemos un Dataframe  de la hoja Penetración-poblacion
penetracion_provincias = data_frames['Penetración-poblacion']
#Agregamos una nueva columna al DataFrame y leagregamos la columna de Accesos por cada 100 hogares de la hoja hogares
penetracion_provincias['Accesos por cada 100 hogares'] = data_frames['Penetracion-hogares']['Accesos por cada 100 hogares']
lista_provincias = penetracion_provincias['Provincia'].unique().tolist()
lista_pen = penetracion_provincias.columns[:][-2:].tolist()

def taza_crecimiento_penetracion_total(data):
  """Funcion que obtiene un dataframe con las taza de crecimientode de la penetracion por hogar y por habitante por provincia"""
  
  df_general = pd.DataFrame(columns=['Provincia','Accesos por cada 100 hab','Accesos por cada 100 hogares'])
  df_general['Provincia'] = lista_provincias
  taza_pen = {}
  contador = 0
  
  for provincia in lista_provincias:
    val_prov = data[data['Provincia'] == provincia]
    val_prov = val_prov.sort_values(by=['Año','Trimestre'],ascending=True)
    
    for i in lista_pen:
      
      val = val_prov[i].pct_change() * 100
      taza_pen[i] = val.mean()

    df_taza_pen = pd.DataFrame.from_dict(taza_pen,orient='index',columns=['Taza'])
    df_general.iloc[contador,1:] = df_taza_pen.T.iloc[0, :df_general.shape[1]]

    contador +=1
    

  return df_general

taza_penetracion_total = taza_crecimiento_penetracion_total(penetracion_provincias)
hogares = taza_penetracion_total.sort_values(by='Accesos por cada 100 hogares',ascending=False)
habitantes = taza_penetracion_total.sort_values(by='Accesos por cada 100 hab',ascending=False)

paleta_colores = sns.color_palette("colorblind",len(taza_penetracion_total['Provincia'].tolist())).as_hex()
paletas_colores = sns.color_palette("deep",len(taza_penetracion_total['Provincia'].tolist())).as_hex()


# Crear subplots (como en el paso anterior)
figura = make_subplots(rows=1, cols=2,subplot_titles=('Penetracion por hogares','Penetracion por habitantes'))


figura.add_trace(go.Bar(x = hogares['Provincia'] , y = hogares['Accesos por cada 100 hogares'],marker=dict(color=paleta_colores)),row = 1 , col = 1)
figura.add_trace(go.Bar(x = habitantes['Provincia'] , y = habitantes['Accesos por cada 100 hab'],marker=dict(color=paletas_colores)),row = 1 , col = 2)


figura.update_layout(height=600, width=900,title="Taza promedio de crecimiento de penetracion por hogares/habitantes totales")


st.plotly_chart(figura)

st.sidebar.image("imagenes/poblacion.png")
