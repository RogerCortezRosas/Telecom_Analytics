import streamlit as st
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import pymysql

st.title('Analisis del Internet en Argentina')

st.image("imagenes/telecom.jpg",caption="imagen" , use_column_width=True)

st.markdown('***')
###########################################################
st.markdown('## Contexto ##')

contexto = """Las telecomunicaciones se refieren a la transmisión de información a través de medios electrónicos, como la telefonía, la televisión, la radio y, más recientemente, el internet. Estos medios de comunicación permiten la transmisión de información entre personas, organizaciones y dispositivos a largas distancias.

            \nEl internet, por su parte, es una red global de computadoras interconectadas que permite el intercambio de información en tiempo real. Desde su creación, ha tenido un impacto significativo en la vida de las personas, transformando la manera en que nos comunicamos, trabajamos, aprendemos y nos entretenemos.

            \nLa industria de las telecomunicaciones ha jugado un papel vital en nuestra sociedad, facilitando la información a escala internacional y permitiendo la comunicación continua incluso en medio de una pandemia mundial. La transferencia de datos y comunicación se realiza en su mayoría a través de internet, líneas telefónicas fijas, telefonía móvil, y en casi cualquier lugar del mundo.

            \nEn comparación con la media mundial, Argentina está a la vanguardia en el desarrollo de las telecomunicaciones, teniendo para el 2020 un total de 62,12 millones de conexiones"""

st.markdown(contexto)
###############################################################
st.markdown('## Telefonia movil e Internet en Argentina ##')

tel = """En comparación con la media mundial, Argentina está a la vanguardia del desarrollo de las telecomunicaciones. Bajo el código de país +54 había un total de 67,85 millones conexiones en 2022. Entre ellos había 60,24 millones teléfonos móviles, lo que corresponde a un promedio de 1,3 por persona. En todo el mundo, esta cifra es de 1,1 teléfonos móviles por persona."""
st.markdown(tel)
##################################################################
st.markdown('## Velocidad de Internet para moviles y red fija ##')

inter = """Con una velocidad media de descarga de 84,20 Mbit/segundo para la Internet de banda ancha de la red fija, Argentina ocupa el puesto 69° en una comparación internacional. Sin embargo, la velocidad de subida fue significativamente menor, de sólo 36,57 Mbit/segundo (puesto 74°).
        \nEn Internet móvil, es decir, en tabletas y smartphones, Argentina alcanza el puesto 91 con 28,76 Mbit/segundo en descarga. La velocidad de subida, de unos 7 Mbit sólo alcanzó el puesto 127.

        \nEl Speedtest Global Index (en inglés) publicado regularmente por Ookla se basa en varios millones de mediciones individuales realizadas en abril de 2024 en 181 países."""
st.markdown(inter)

st.sidebar.image("imagenes/Argentina-removebg-preview.png")


""" Bjar una tabla de my sql a un df

# Conectar a la base de datos

conexion = pymysql.connect(
                                host = "localhost",
                                user = "root",
                                password = "root1234",
                                database = "telecom_argentina"
                          )

query = "SELECT * FROM totales_accesos_por_tecnología"

df = pd.read_sql(query,conexion) # Extraccion de una tabla en especifico
st.session_state.df = df

conexion.close()

st.dataframe(df) """

# Funcion para cargar tablas desde MySQL

def load_table ( connection , table_name):
    
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query,connection)
    return df


if 'dataframes_dict' not in st.session_state:
    connection = pymysql.connect(
                                host = "localhost",
                                user = "root",
                                password = "root1234",
                                database = "telecom_argentina"
                          )
    
# Obtener los nombres de todas las tablas en la base de datos
    table_names_query = "SHOW TABLES"
    tables = pd.read_sql(table_names_query, connection)

# Cargar todas las tablas en un diccionario de DataFrames
    st.session_state.dataframes_dict = {
        table_name: load_table(connection, table_name)
        for table_name in tables.iloc[:, 0]
    }

    connection.close()