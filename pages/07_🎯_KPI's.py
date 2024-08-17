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


st.title("KPI's")


st.subheader('Aumento 2% al acceso al servicio de internet para el proximo trimestre , cada 100 hogares , por provincia')

penetracion_provincias = data_frames['Penetración-poblacion']

#Agregamos una nueva columna al DataFrame y lea gregamos la columna de Accesos por cada 100 hogares de la hoja hogares
penetracion_provincias['Accesos por cada 100 hogares'] = data_frames['Penetracion-hogares']['Accesos por cada 100 hogares']



lista_provinicias =  penetracion_provincias['Provincia'].unique().tolist() # lista de provincias
lista_pen = penetracion_provincias.columns[:][-2:].tolist() # lista de penetracion provincias

def taza_crecimiento_penetracion_total(data):
  """Funcion que obtiene un dataframe con las taza de crecimientode de la penetracion por hogar y por habitante por provincia"""
  
  df_general = pd.DataFrame(columns=['Provincia','Accesos por cada 100 hab','Accesos por cada 100 hogares'])
  df_general['Provincia'] = lista_provinicias
  taza_pen = {}
  contador = 0
  
  for provincia in lista_provinicias:
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


# Definir la función que se ejecutará al cambiar la selección
def actualizar_mensaje():
    st.session_state['mensaje'] = f"Has seleccionado {len(st.session_state['num'])} provincias."

 

Provincia = st.multiselect("Elije las provincias",lista_provinicias,max_selections=1,default='Buenos Aires',key='num', on_change=actualizar_mensaje)
# Mostrar el mensaje actualizado
st.write(st.session_state.get('mensaje', "Aún no has seleccionado ninguna provincia."))


if len(Provincia) != 0:

    df_provincia = penetracion_provincias[penetracion_provincias['Provincia']==Provincia[0]] # Obtenemos el  dataframe por provincia seleccionada
    df_provincia = df_provincia[df_provincia['Año'] == 2024]
    df_provincia.sort_values(by=['Año','Trimestre'] , ascending=True , inplace=True) # Ordenamos de menor a mayor
    df_provincia.drop(columns='Accesos por cada 100 hab',inplace=True) # Eliminamos columna inecesaria
    df_provincia.reset_index(inplace=True)
    df_provincia.drop(columns='index',inplace=True) # Eliminamos columna inecesaria

    val = df_provincia.iloc[len(df_provincia)-1]['Accesos por cada 100 hogares'] #Obtenemos el valor del ultimo trimestre 2024
    taza = taza_penetracion_total[taza_penetracion_total['Provincia'] == Provincia[0]]['Accesos por cada 100 hogares'] # valor dela taza de crecimiento de la provincia
    suma = val + taza.iloc[0] # suma del valor del ultimo trimestre mas la taza
    
    
    kpi = df_provincia.iloc[len(df_provincia)-1]['Accesos por cada 100 hogares'] * 1.02 # valor que es el 2% de crecimiento respecto al ultimo trimestre

   

    graf_kpi = df_provincia.copy() # Obtenemos nuevo df y lo llamamos graf_kpi
    graf_taza = df_provincia.copy()
    
    graf_kpi.loc[len(graf_kpi)] = ['2024-1',2,Provincia[0],kpi ] # agrgamos ultima fila que representa el valor en el ultimo semestre al calculo del kpi
    graf_taza.loc[len(graf_taza)] = ['2024-1',2,Provincia[0],suma ] # agregamos ultima fila que representa el valor en el ultimo semestre al calculo de la taza

    # Crear la gráfica de línea
    figure = go.Figure()

    figure.add_trace(go.Bar(
        x=graf_taza['Año'],
        y=graf_taza['Accesos por cada 100 hogares'],
        marker_color = 'darkgreen',
        name='Accesos taza',
        
    ))

    figure.add_trace(go.Bar(
        x=graf_kpi['Año'],
        y=graf_kpi['Accesos por cada 100 hogares'],
        marker_color = 'mediumseagreen',
        name='Accesos kpi',
        
    ))

    st.plotly_chart(figure)


    col1 , col2 = st.columns(2)

    with col1:
       st.write(graf_kpi)
    with col2:
       st.write(graf_taza)


st.subheader('Aumento 5% del numero de accesos de fibra optica para el proximo trimestre , para todas las provinicias ')

data_tec_loc = data_frames['Accesos_tecnologia_localidad'].groupby('Provincia')[['FIBRA OPTICA']].sum()
data_tec_loc['Nuevo_Acceso'] = data_tec_loc['FIBRA OPTICA'] * 1.05

figura = go.Figure()

# Grafica del trimestre actual

figura.add_trace(go.Bar(
                      x = data_tec_loc.index , 
                      y = data_tec_loc['FIBRA OPTICA'] ,
                      name = 'Acceso Actual',
                      marker_color = 'darkgreen'
))


figura.add_trace(go.Bar(
                      x = data_tec_loc.index , 
                      y = data_tec_loc['Nuevo_Acceso'] ,
                      name = 'Acceso Aumento 5 %',
                      marker_color = 'mediumseagreen'
))

st.plotly_chart(figura)

st.subheader(" Acceso de 0 % a la tecnologia de ADSL en 2 años ( tomando la taza de crecimiento)")

# Eliminamos las filas que tienen en provincia valores nulos
data_frames['Accesos_tecnologia_localidad'] = data_frames['Accesos_tecnologia_localidad'].dropna(subset=['Provincia'])

#Hacemos la sumatoria de accesos de internet por tecnologia

dicc_tecnologias ={
    'ADSL':0,

}

dicc_tecnologias['ADSL'] = data_frames['Accesos_tecnologia_localidad']['ADSL'].sum()

trimestres_totales = 9


decremento_trimestral = dicc_tecnologias['ADSL'] / trimestres_totales

# Crear DataFrame con la proyección de accesos por trimestre
data = {
        'Trimestre' : ['2024','2024/1','2024/2','2024/3','2025','2025/1','2025/2','2025/3','2026','2026/1'] ,
    
        'Accesos_ADSL': [dicc_tecnologias['ADSL'] - decremento_trimestral * i for i in range(trimestres_totales + 1)]
}



df = pd.DataFrame.from_dict(data)



# Crear la gráfica de línea
figure = go.Figure()

figure.add_trace(go.Scatter(
    x=df['Trimestre'],
    y=df['Accesos_ADSL'],
    mode='lines+markers',
    name='Accesos ADSL',
    line=dict(color='red', width=4),
    marker=dict(size=10)
))

# Añadir título y etiquetas
figure.update_layout(
    title='Decrecimiento del Número de Accesos ADSL por Trimestre',
    xaxis_title='Trimestre',
    yaxis_title='Número de Accesos ADSL',
    xaxis=dict(tickmode='linear', dtick=1),
    yaxis=dict(tickformat='~s')  # Para formato simplificado de números grandes
)

# Mostrar la gráfica
st.plotly_chart(figure)