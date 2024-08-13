import streamlit as st
import pandas as pd
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

if st.button('Grafica'):

  #Hacemos un grafico tipo pie para observar la ditribucion de los acceos a internet las diferentees tecnologias


    colors = ['Red','Green','Blue','Orange','Brown','Black','White','Pink']

    figura= px.pie(df_tecnologias,values=dicc_tecnologias.values() , names = dicc_tecnologias.keys() , color = dicc_tecnologias.keys() ,
                   color_discrete_sequence=colors , title='Distribucion de los accesos a internet por tecnologia')
    st.plotly_chart(figura)






st.markdown(" ### Graficas de acceso a Tecnologias en el tiempo")
st.markdown("---")

tec_totales = data_frames['Totales Accesos Por Tecnología']
list_tec = tec_totales.columns[2:7]


# Crear subplots (como en el paso anterior)
fig = make_subplots(rows=2, cols=3,subplot_titles=(list_tec[0],list_tec[1],list_tec[2],list_tec[3],list_tec[4]))

fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['ADSL']),row = 1 , col = 1)

fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Cablemodem']),row = 1 , col = 2)
fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Fibra óptica']),row = 1 , col = 3)
fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Wireless']),row = 2 , col = 1)
fig.add_trace(go.Scatter(x = tec_totales['Año'] , y = tec_totales['Otros']),row = 2 , col = 2)


st.plotly_chart(fig)



st.markdown(" ### Taza promedio de crecimiento")
st.markdown("---")

tec_totales_taza = tec_totales.sort_values(by=['Año','Trimestre'],ascending=True)

taza_tec = {}
for i in list_tec:
  val = tec_totales_taza[i].pct_change() * 100
  taza_tec[i] = val.mean()

df_taza_tec = pd.DataFrame.from_dict(taza_tec,orient='index',columns=['Taza'])

paleta_colores = sns.color_palette("coolwarm",len(df_taza_tec.index.tolist())).as_hex()

figura = go.Figure()

figura.add_trace(go.Bar( x = df_taza_tec.index , y = df_taza_tec['Taza'],marker=dict(color=paleta_colores)))
figura.update_layout(title='Taza crecimiento' )

st.plotly_chart(figura)


st.markdown(" ### Graficas de acceso a Tecnologias por provincia")
st.markdown("---")

lista_tec = df_tecnologias.index.tolist()
data_tec_loc = data_frames['Accesos_tecnologia_localidad'].groupby('Provincia')[['ADSL','CABLEMODEM','DIAL UP','FIBRA OPTICA','OTROS','SATELITAL','WIMAX','WIRELESS']].sum()



tecnologia = st.multiselect('Seleccione tecnologia',lista_tec,max_selections=1,default="ADSL")





col1 , col2 = st.columns(2)

with col1:
    data_top_10 = data_tec_loc.sort_values(by=tecnologia,ascending=False)[:10]
    data_top_10 = data_top_10[tecnologia]
    data_top_10 =data_top_10.reset_index()
    paleta_colores = sns.color_palette("Set2",len(data_top_10.index.to_list())).as_hex()
   

  

    figura = go.Figure()

    figura.add_trace(go.Bar( x = data_top_10['Provincia'] , y = data_top_10[tecnologia[0]] ,marker=dict(color=paleta_colores)))
    figura.update_layout(title='Top 10 Provincias con MAYOR demanda ' )

    st.plotly_chart(figura)



with col2:
    
    data_Untop_10= data_tec_loc.sort_values(by=tecnologia,ascending=True)[:10]
    data_Untop_10 =data_Untop_10.reset_index()
    paleta_colores = sns.color_palette("PuRd",len(data_Untop_10.index.tolist())).as_hex()

    figura = go.Figure()

    figura.add_trace(go.Bar( x =data_Untop_10['Provincia'], y = data_Untop_10[tecnologia[0]],marker=dict(color=paleta_colores)))
    figura.update_layout(title='Top 10 Provincias con MENOR demanda' )

    st.plotly_chart(figura)


st.sidebar.image("imagenes/satelite.png")