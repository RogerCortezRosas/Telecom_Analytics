import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import recarga_datos as reload



st.title('Accesos a Internet por Region')

if st.button('Actualizar Datos'):
   reload.reload_table()
   st.success('Datos actualizados')


dataframes_dict = st.session_state.dataframes_dict # Acceder al diccionario de DataFrames

st.title('Analisis del comportamiento en el tiempo')# Titulo __________________________________________________________________________________________________


vel_totales = dataframes_dict['totales_vmd'] # Creacion DF vel_totales

#Graficamos un lineplot por año ________________________________________________

fig = px.line(vel_totales, x='Año', y='Mbps (Media de bajada)', title='Velocidad de bajada por año totales')

st.plotly_chart(fig)


st.subheader('Taza de crecimiento en el tiempo') # __________________________________________________________________


vel_totales = vel_totales.sort_values(by=['Año','Trimestre']) # ordenamos el data set vel_totales por año
vel_totales['Taza crecimiento'] = vel_totales['Mbps (Media de bajada)'].pct_change() * 100 # Obtenemos la taza y lo asignamos en la columna Taza crecimiento
vel_totales_tabla = vel_totales.groupby('Año')['Taza crecimiento'].mean() # obtenemos la media por año

opcion = st.radio("Seleccione una opcion: ",['Tabla','Grafica'],horizontal=True) # Selecciona __________________________________________________________

if opcion == 'Tabla':
   st.write(vel_totales_tabla) # Muestra tabla
else:
    #Grafica ________________________________________________________________________________________________________________________
    fig = go.Figure(data = go.Scatter( x=vel_totales['Año'], y=vel_totales['Taza crecimiento'],mode ='lines+markers'))
    # Configuración del layout
    fig.update_layout(
    title='Taza crecimiento',
    xaxis_title='Años',
    yaxis_title='Taza'
)
                    

    st.plotly_chart(fig)
   
   


st.subheader('Velocidad promedio por año y provincia') # ____________________________________________________________________________________________





lista_provincias = dataframes_dict['velocidad_por_prov']['Provincia'].unique().tolist() # Obtencion lista de provinicas __________________________________________________

provincias = st.multiselect("Elije las provincias",lista_provincias,max_selections=6,default=['Buenos Aires','Capital Federal','Córdoba','Tierra Del Fuego','Formosa','Catamarca']) # Selecionar provinica _________________________________________________________________________

lista_df = [] # Creacion lista de dataframes
for prov in provincias: # Cicloque crea una lista de DF
    lista_df.append( dataframes_dict['velocidad_por_prov'][dataframes_dict['velocidad_por_prov']['Provincia'] == prov])

# Graficas ______________________________________________________________________________________________________________________________________________
fig = make_subplots(rows=2, cols=3,subplot_titles=(provincias[0],provincias[1],provincias[2],provincias[3],provincias[4],provincias[5]))

fig.add_trace(go.Scatter(x = lista_df[0]['Año'] , y = lista_df[0]['Mbps (Media de bajada)']),row = 1 , col = 1)

fig.add_trace(go.Scatter(x = lista_df[1]['Año'] , y = lista_df[1]['Mbps (Media de bajada)']),row = 1 , col = 2)
fig.add_trace(go.Scatter(x = lista_df[2]['Año'] , y = lista_df[2]['Mbps (Media de bajada)']),row = 1 , col = 3)
fig.add_trace(go.Scatter(x = lista_df[3]['Año'] , y = lista_df[3]['Mbps (Media de bajada)']),row = 2 , col = 1)
fig.add_trace(go.Scatter(x = lista_df[4]['Año'] , y = lista_df[4]['Mbps (Media de bajada)']),row = 2 , col = 2)
fig.add_trace(go.Scatter(x = lista_df[5]['Año'] , y = lista_df[5]['Mbps (Media de bajada)']),row = 2 , col = 3)



fig.update_layout(height=600, width=900, title_text="Velocidades por provincias")
fig.update_xaxes(range=[2014,2025],tickangle=90,tickvals=[2014,2019,2020,2022,2024])





st.plotly_chart(fig) # Mostrar en Streamlit


st.subheader('Taza de crecimiento promedio de velocidad por año y provincia') # ___________________________________________________________________________________________________________

dataframes_dict['velocidad_por_prov']['Mbps (Media de bajada)'] = dataframes_dict['velocidad_por_prov']['Mbps (Media de bajada)'].astype('double') # conversiondela columna Mbps (Media de bajada) a tipo double

lis_prov = dataframes_dict['velocidad_por_prov']['Provincia'].unique() # lista de provincias
data_tazas_crecimiento = pd.DataFrame(columns=['Provincia', 'Taza Crecimiento']) # Creacion de df data_tazas_crecimiento

data_tazas_crecimiento['Provincia'] = lis_prov # Se le asigna la lista de provinicas en la columna Provincia
lista_tazas = [] # Creaciondelista vacia

for provincia in lis_prov:# Ciclo que obtieneuna lista del promedio de velocidades por año de las diferentes provinicas
   val_prov =  dataframes_dict['velocidad_por_prov'][dataframes_dict['velocidad_por_prov']['Provincia'] == provincia]
   val_prov = val_prov.sort_values(by=['Año','Trimestre'],ascending=True)
   val_prov['taza'] = val_prov['Mbps (Media de bajada)'].pct_change() * 100
   taza = val_prov.groupby('Año')['taza'].mean().reset_index()
   lista_tazas.append(taza['taza'].mean())



data_tazas_crecimiento['Taza Crecimiento'] = lista_tazas # Asinacion de lista de tazas promedio a la columna Taza Crecimiento
data_tazas_crecimiento.sort_values(by='Taza Crecimiento',ascending=False,inplace=True) # Ordenacion DF de forma descendente





if st.button('Tabla'):
   st.write(data_tazas_crecimiento)

# Grafica ___________________________________________________________________________________________________________
paleta_colores = sns.color_palette("viridis",len(data_tazas_crecimiento['Provincia'].tolist())).as_hex()

figura = go.Figure()

figura.add_trace(go.Bar( x = data_tazas_crecimiento['Provincia'] , y = data_tazas_crecimiento['Taza Crecimiento'],marker=dict(color=paleta_colores)))
figura.update_layout(title='Taza crecimiento' )

st.plotly_chart(figura)

st.subheader('Accesos a tecnologias por provincia a traves del tiempo') # _________________________________________________________________________________

tec_provincia = dataframes_dict['accesos_por_tecnología'] # Creacion de DF tec_provincia

dataframes_dict['accesos_por_tecnología']['Año'] = dataframes_dict['accesos_por_tecnología']['Año'].replace('2019 *','2019')#convertimos las filas 2019 * de la columna año en solo 2019

dataframes_dict['accesos_por_tecnología'] = dataframes_dict['accesos_por_tecnología'].dropna(subset=['Año']) #eliminamos valores nulos de la columna Año

dataframes_dict['accesos_por_tecnología'] = dataframes_dict['accesos_por_tecnología'].drop(dataframes_dict['accesos_por_tecnología'].index[-1]) #eliinamos la ultima fila

dataframes_dict['accesos_por_tecnología']['Año'] = dataframes_dict['accesos_por_tecnología']['Año'].astype(int) #convertimos el tipo de dato Año a entero

tec_totales = dataframes_dict['totales_accesos_por_tecnología'] # Creacion de DF tec_totales
list_tec = tec_totales.columns[2:7] # lista de tecnologias

def taza_crecimiento(data):
  """Funcion que devuelve un dataframe con las taza de crecimiento promedio por año de cada tecnologia"""
  data = data.sort_values(by=['Año','Trimestre'],ascending=True)
  taza_tec = {}
  for i in list_tec:
    data['taza'] = data[i].pct_change() * 100
    taza = data.groupby('Año')['taza'].mean().reset_index()
    taza_tec[i] = taza['taza'].mean()
  df_taza_tec = pd.DataFrame.from_dict(taza_tec,orient='index',columns=['Taza'])
  return df_taza_tec

# Definir la función que se ejecutará al cambiar la selección
def actualizar_mensaje():
    st.session_state['mensaje'] = f"Has seleccionado {len(st.session_state['num'])} provincias."

Provincia = st.multiselect("Elije las provincias",lista_provincias,max_selections=1,default='Buenos Aires',key='num', on_change=actualizar_mensaje) # Seleccionar__________________________________________________________

st.write(st.session_state.get('mensaje', "Aún no has seleccionado ninguna provincia.")) # Mostrar el mensaje actualizado


if len(Provincia) != 0:
  tec_provincia = dataframes_dict['accesos_por_tecnología'][dataframes_dict['accesos_por_tecnología']['Provincia']==Provincia[0]] # Filtracion DF por provinica seleccionada
  tec_provincia = tec_provincia.replace(0,1) # remplazar los valores 0 por 1 en todo el DF
  taza_prov = taza_crecimiento(tec_provincia) #Obtencion del DF de las tazas portecnologia 



# Grfica __________________________________________________________________________________________________________________________________

  paletas_colores = sns.color_palette("BuPu",len(taza_prov.index.tolist())).as_hex()

 
  Fig = make_subplots(rows=2, cols=3,subplot_titles=(list_tec[0],list_tec[1],list_tec[2],list_tec[3],list_tec[4]))

  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['ADSL']),row = 1 , col = 1)

  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Cablemodem']),row = 1 , col = 2)
  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Fibra_Optica']),row = 1 , col = 3)
  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Wireless']),row = 2 , col = 1)
  Fig.add_trace(go.Scatter(x = tec_provincia['Año'] , y = tec_provincia['Otros']),row = 2 , col = 2)
  Fig.add_trace(go.Bar(x = taza_prov.index , y = taza_prov['Taza'],marker=dict(color=paletas_colores)),row = 2 , col = 3)


  st.plotly_chart(Fig)




st.sidebar.image("imagenes/tiempo.jpg")