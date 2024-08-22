import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import recarga_datos as reload



st.title('Accesos a Internet por Region') #  TITULO ______________________________________________________________________________________________________________

if st.button('Actualizar Datos'): #  BOTON __________________________________________________________________
   reload.reload_table()
   st.success('Datos actualizados')


dataframes_dict = st.session_state.dataframes_dict # Acceder al diccionario de DataFrames


dataframes_dict['accesos_tecnologia_localidad'] = dataframes_dict['accesos_tecnologia_localidad'].dropna(subset=['Provincia']) # Eliminamos las filas que tienen en provincia valores nulos

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


for i in dicc_tecnologias.keys(): # Ciclo que asigna valores(numero de accesos por cada tecnologia) en el diccionario dicc_tecnologia{}
  dicc_tecnologias[i] = dataframes_dict['accesos_tecnologia_localidad'][i].sum()

#Hacemos un dataframe con la cantidad y el porcentaje de accesos a internet por cada tecnologia
df_tecnologias = pd.DataFrame.from_dict(dicc_tecnologias,orient = 'index' , columns = ['Total Access']) # Creacion de dataframe a partir del diccionario dicc_tecnologias en donde la columna Total Acces tendra los valores del diccionario 
df_tecnologias['% Total'] = df_tecnologias['Total Access'] / df_tecnologias['Total Access'].sum() * 100 # Creacion de columna %Total donde se  asinga el % del numero de accesos por cada tecnologia
df_tecnologias.sort_values(by='% Total',ascending=False, inplace=True) # Se ordenan de forma descendiente por % Total 

st.title('Accesos a Internet por Tecnologias') # ____________________________________________________________________________________________________________
st.markdown("---")

if st.button('Tabla'):# Muetra de tabla _____________________________________________
  st.write(df_tecnologias)

if st.button('Grafica'):# Muestra de grafica pie ______________________________________________________________________

  #Hacemos un grafico tipo pie para observar la ditribucion de los acceos a internet las diferentees tecnologias


    colors = ['Red','Green','Blue','Orange','Brown','Black','White','Pink']

    figura= px.pie(df_tecnologias,values=dicc_tecnologias.values() , names = dicc_tecnologias.keys() , color = dicc_tecnologias.keys() ,
                   color_discrete_sequence=colors , title='Distribucion de los accesos a internet por tecnologia')
    st.plotly_chart(figura)






st.markdown(" ### Graficas de acceso a Tecnologias en el tiempo") # __________________________________________________________________________________
st.markdown("---")

tec_totales = dataframes_dict['totales_accesos_por_tecnología'] # Creacion df tec_totales
list_tec = tec_totales.columns[2:7] # lista de las tecnologias


# Graficas _____________________________________________________________________________________________________________
fig = make_subplots(rows=2, cols=3,subplot_titles=(list_tec[0],list_tec[1],list_tec[2],list_tec[3],list_tec[4]))

fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['ADSL']),row = 1 , col = 1)

fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Cablemodem']),row = 1 , col = 2)
fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Fibra_Optica']),row = 1 , col = 3)
fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Wireless']),row = 2 , col = 1)
fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Otros']),row = 2 , col = 2)


st.plotly_chart(fig)



st.markdown(" ### Taza promedio de crecimiento por año") # ________________________________________________________________________________
st.markdown("---")

tec_totales.sort_values(by=['Año','Trimestre'],ascending=True,inplace=True) # Ordenamiento del dataframe por año y trimestre



taza_tec = {} # Creacion de diccionario vacio
for i in list_tec:# ciclo que crea el diccionario donde el key el el nombre de la tecnologia y el valor la taza promedio por Año
  tec_totales['taza'] = tec_totales[i].pct_change() * 100
  taza = tec_totales.groupby('Año')['taza'].mean().reset_index()
  taza_tec[i] = taza['taza'].mean()



df_taza_tec = pd.DataFrame.from_dict(taza_tec,orient='index',columns=['Taza']) # Conversion del diccionario al DF



# Grafica __________________________________________________________________________________________
paleta_colores = sns.color_palette("coolwarm",len(df_taza_tec.index.tolist())).as_hex()
figura = go.Figure()

figura.add_trace(go.Bar( x = df_taza_tec.index , y = df_taza_tec['Taza'],marker=dict(color=paleta_colores)))
figura.update_layout(title='Taza crecimiento' )

st.plotly_chart(figura)


st.markdown(" ### Graficas de acceso a Tecnologias por provincia")#______________________________________________________________________________________________
st.markdown("---")

lista_tec = df_tecnologias.index.tolist() # Obtencio de lsita de tecnologias
data_tec_loc = dataframes_dict['accesos_tecnologia_localidad'].groupby('Provincia')[['ADSL','CABLEMODEM','DIAL UP','FIBRA OPTICA','OTROS','SATELITAL','WIMAX','WIRELESS']].sum() # Grupacion por provinica y se hace la sumatoria de cada tecnologia



tecnologia = st.multiselect('Seleccione tecnologia',lista_tec,max_selections=1,default="ADSL")#Seleccionar tecnologia _________________________________________________________________





col1 , col2 = st.columns(2)

with col1: #Grafica 1 _________________________________________________________________________________________________________________________
    data_top_10 = data_tec_loc.sort_values(by=tecnologia,ascending=False)[:10]
    data_top_10 = data_top_10[tecnologia]
    data_top_10 =data_top_10.reset_index()
    paleta_colores = sns.color_palette("Set2",len(data_top_10.index.to_list())).as_hex()
   

  

    figura = go.Figure()

    figura.add_trace(go.Bar( x = data_top_10['Provincia'] , y = data_top_10[tecnologia[0]] ,marker=dict(color=paleta_colores)))
    figura.update_layout(title='Top 10 Provincias con MAYOR demanda ' )

    st.plotly_chart(figura)



with col2: # Grafica 2 ________________________________________________________________________________________________________________________
    
    data_Untop_10= data_tec_loc.sort_values(by=tecnologia,ascending=True)[:10]
    data_Untop_10 =data_Untop_10.reset_index()
    paleta_colores = sns.color_palette("PuRd",len(data_Untop_10.index.tolist())).as_hex()

    figura = go.Figure()

    figura.add_trace(go.Bar( x =data_Untop_10['Provincia'], y = data_Untop_10[tecnologia[0]],marker=dict(color=paleta_colores)))
    figura.update_layout(title='Top 10 Provincias con MENOR demanda' )

    st.plotly_chart(figura)


st.sidebar.image("imagenes/satelite.png")