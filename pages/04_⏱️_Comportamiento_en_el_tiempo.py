import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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


st.subheader('Taza de crecimiento en el tiempo')

#ordenamos el data set vel_totales por año
vel_totales = vel_totales.sort_values(by='Año')
vel_totales['Taza crecimiento'] = vel_totales['Mbps (Media de bajada)'].pct_change() * 100
vel_totales_tabla = vel_totales.groupby('Año')['Taza crecimiento'].sum()
opcion = st.radio("Seleccione una opcion: ",['Tabla','Grafica'],horizontal=True)

if opcion == 'Tabla':
   st.write(vel_totales_tabla)
else:
    fig = go.Figure(data = go.Scatter( x=vel_totales['Año'], y=vel_totales['Taza crecimiento'],mode ='lines+markers'))
    # Configuración del layout
    fig.update_layout(
    title='Taza crecimiento',
    xaxis_title='Años',
    yaxis_title='Taza'
)
                    

    st.plotly_chart(fig)
   
   


st.subheader('Velocidad promedio por año y provincia')





lista_provincias = data_frames['Velocidad % por prov']['Provincia'].unique().tolist()

provincias = st.multiselect("Elije las provincias",lista_provincias,max_selections=6,default=['Buenos Aires','Capital Federal','Córdoba','Tierra Del Fuego','Formosa','Catamarca'])

lista_df = [] # Creacion lista de dataframes
for prov in provincias:
    lista_df.append( data_frames['Velocidad % por prov'][data_frames['Velocidad % por prov']['Provincia'] == prov])

# Crear subplots (como en el paso anterior)
fig = make_subplots(rows=2, cols=3,subplot_titles=(provincias[0],provincias[1],provincias[2],provincias[3],provincias[4],provincias[5]))

fig.add_trace(go.Scatter(x = lista_df[0]['Año'] , y = lista_df[0]['Mbps (Media de bajada)']),row = 1 , col = 1)

fig.add_trace(go.Scatter(x = lista_df[1]['Año'] , y = lista_df[1]['Mbps (Media de bajada)']),row = 1 , col = 2)
fig.add_trace(go.Scatter(x = lista_df[2]['Año'] , y = lista_df[2]['Mbps (Media de bajada)']),row = 1 , col = 3)
fig.add_trace(go.Scatter(x = lista_df[3]['Año'] , y = lista_df[3]['Mbps (Media de bajada)']),row = 2 , col = 1)
fig.add_trace(go.Scatter(x = lista_df[4]['Año'] , y = lista_df[4]['Mbps (Media de bajada)']),row = 2 , col = 2)
fig.add_trace(go.Scatter(x = lista_df[5]['Año'] , y = lista_df[5]['Mbps (Media de bajada)']),row = 2 , col = 3)



fig.update_layout(height=600, width=900, title_text="Velocidades por provincias")
fig.update_xaxes(range=[2014,2025],tickangle=90,tickvals=[2014,2019,2020,2022,2024])



# Mostrar en Streamlit

st.plotly_chart(fig)


st.subheader('Taza de crecimiento promedio de velocidad por año y provincia')

data_frames['Velocidad % por prov']['Mbps (Media de bajada)'] =data_frames['Velocidad % por prov']['Mbps (Media de bajada)'].astype('double')

lis_prov = data_frames['Velocidad % por prov']['Provincia'].unique()
data_tazas_crecimiento = pd.DataFrame(columns=['Provincia', 'Taza Crecimiento'])

data_tazas_crecimiento['Provincia'] = lis_prov
lista_tazas = []

for provincia in lis_prov:
   val_prov =  data_frames['Velocidad % por prov'][data_frames['Velocidad % por prov']['Provincia'] == provincia]
   val_prov = val_prov.sort_values(by='Año',ascending=True)
   val_prov = val_prov['Mbps (Media de bajada)'].pct_change() * 100
   lista_tazas.append(val_prov.mean())

data_tazas_crecimiento['Taza Crecimiento'] = lista_tazas
data_tazas_crecimiento.sort_values(by='Taza Crecimiento',ascending=False,inplace=True)

paleta_colores = sns.color_palette("viridis",len(data_tazas_crecimiento['Provincia'].tolist())).as_hex()

if st.button('Tabla'):
   st.write(data_tazas_crecimiento)

figura = go.Figure()

figura.add_trace(go.Bar( x = data_tazas_crecimiento['Provincia'] , y = data_tazas_crecimiento['Taza Crecimiento'],marker=dict(color=paleta_colores)))
figura.update_layout(title='Taza crecimiento' )

st.plotly_chart(figura)


st.subheader('Accesos a tecnologias por provincia a traves del tiempo')

tec_provincia = data_frames['Accesos Por Tecnología']
#convertimos las filas 2019 * de la columna año
data_frames['Accesos Por Tecnología']['Año'] = data_frames['Accesos Por Tecnología']['Año'].replace('2019 *','2019')
#eliminamos valores nulos de la columna Año
data_frames['Accesos Por Tecnología'] = data_frames['Accesos Por Tecnología'].dropna(subset=['Año'])
#eliinamos la ultima fila
data_frames['Accesos Por Tecnología'] = data_frames['Accesos Por Tecnología'].drop(data_frames['Accesos Por Tecnología'].index[-1])
#convertimos el tipo de dato Año a entero
data_frames['Accesos Por Tecnología']['Año'] = data_frames['Accesos Por Tecnología']['Año'].astype(int)

tec_totales = data_frames['Totales Accesos Por Tecnología']
list_tec = tec_totales.columns[2:7]

def taza_crecimiento(data):
  """Funcion que obtiene un dataframe con las taza de crecimientode cada tecnologia"""
  data = data.sort_values(by='Año',ascending=True)
  taza_tec = {}
  for i in list_tec:
    val = data[i].pct_change() * 100
    taza_tec[i] = val.mean()
  df_taza_tec = pd.DataFrame.from_dict(taza_tec,orient='index',columns=['Taza'])
  return df_taza_tec

# Definir la función que se ejecutará al cambiar la selección
def actualizar_mensaje():
    st.session_state['mensaje'] = f"Has seleccionado {len(st.session_state['frutas'])} provinica."

Provincia = st.multiselect("Elije las provincias",lista_provincias,max_selections=1,default='Buenos Aires',key='frutas', on_change=actualizar_mensaje)
# Mostrar el mensaje actualizado
st.write(st.session_state.get('mensaje', "Aún no has seleccionado ninguna provincia."))


if len(Provincia) != 0:
  tec_provincia = data_frames['Accesos Por Tecnología'][data_frames['Accesos Por Tecnología']['Provincia']==Provincia[0]]
  tec_provincia = tec_provincia.replace(0,1)
  taza_prov = taza_crecimiento(tec_provincia)



  paletas_colores = sns.color_palette("BuPu",len(taza_prov.index.tolist())).as_hex()

  # Crear subplots (como en el paso anterior)
  Fig = make_subplots(rows=2, cols=3,subplot_titles=(list_tec[0],list_tec[1],list_tec[2],list_tec[3],list_tec[4]))

  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['ADSL']),row = 1 , col = 1)

  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Cablemodem']),row = 1 , col = 2)
  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Fibra óptica']),row = 1 , col = 3)
  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Wireless']),row = 2 , col = 1)
  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Otros']),row = 2 , col = 2)
  Fig.add_trace(go.Bar(x = taza_prov.index , y = taza_prov['Taza'],marker=dict(color=paletas_colores)),row = 2 , col = 3)


  st.plotly_chart(Fig)




st.sidebar.image("imagenes/tiempo.jpg")