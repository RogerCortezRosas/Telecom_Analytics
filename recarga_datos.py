import pymysql
import pandas as pd
import streamlit as st


def load_table ( connection , table_name):
    
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query,connection)
    return df

def reload_table ():
    
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
   


   connection.close() #para evitar problemas de rendimiento y bloqueo de recursos.
