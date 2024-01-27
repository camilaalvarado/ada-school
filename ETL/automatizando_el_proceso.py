import requests
import pandas as pd
import numpy as np
url = 'URL_de_tu_dataset_actualizado'

def descargar_y_procesar_datos(url):
    try:
        # Realizar un GET request a la URL
        response = requests.get(url)
        response.raise_for_status()  # Verificar si la respuesta es exitosa

        # Escribir la respuesta en un archivo CSV
        with open('datos_descargados.csv', 'w') as archivo_csv:
            archivo_csv.write(response.text)

        print("Datos descargados y guardados en 'datos_descargados.csv'")

        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv('datos_descargados.csv')

        # Verificar valores faltantes, filas repetidas, eliminar valores atípicos y categorizar por edades
        procesar_dataframe(df)

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar los datos: {e}")
    except Exception as e:
        print(f"Error al procesar el DataFrame: {e}")

def procesar_dataframe(df):
    # Verificar valores faltantes
    if df.isnull().values.any():
        print("Existen valores faltantes.")
        # Eliminar valores faltantes
        df = df.dropna()
        print("Valores faltantes eliminados.")

    # Verificar filas repetidas
    if df.duplicated().any():
        print("Existen filas repetidas.")
        # Eliminar filas repetidas
        df = df.drop_duplicates()
        print("Filas repetidas eliminadas.")

    # Verificar y eliminar valores atípicos
    # (Ajusta esta parte según la forma en que identificas y manejas los valores atípicos)

    # Crear columna que categorice por edades
    df['Categoria_Edad'] = pd.cut(df['Edad'], bins=[0, 12, 19, 39, 59, np.inf], labels=['Niño', 'Adolescente', 'Jóvenes adulto', 'Adulto', 'Adulto mayor'])

    # Guardar el resultado como CSV
    df.to_csv('datos_procesados.csv', index=False)
    print("Resultados guardados como 'datos_procesados.csv'.")

# Llamar a la función con la URL proporcionada
url_datos = "URL_de_tu_dataset_actualizado"
descargar_y_procesar_datos(url_datos)