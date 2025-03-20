# Usar una imagen base con python
FROM python:3.11-bookworm

#Crear un directorio dentro de mi contenedor y es donde todos los archivos de mi aplicacion se van a alojar

WORKDIR /dashboard

#Copiar mis librerias dentro de mi entorno de trabajo (contenedor de docker)
#mi archivo local requirements copia con el mismo nombre al contenedro 
COPY requirements.txt requirements.txt

#Instalar las librerias para ejecutar mi aplicacion
RUN pip install -r requirements.txt

#Segundo copy para copiar ahora todo el resto del directorio
COPY . .

#Especificar que use el entorno virtual antes de ejecutar Streamlit
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]