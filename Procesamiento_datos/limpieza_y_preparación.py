import requests
from io import StringIO
import pandas as pd


# URL del archivo CSV
url = "https://huggingface.co/datasets/mstz/heart_failure/raw/main/heart_failure_clinical_records_dataset.csv"

# Realizar la solicitud GET para obtener los datos
response = requests.get(url)

# verificar respueste la respuesta es positiva o = 200 
if response.status_code == 200:
    data = response.content.decode('utf-8')
    df = pd.read_csv(StringIO(data))


    print(df.head())
else:
    print("Error al descargar los datos:", response.status_code)

import pandas as pd

def procesar_dataframe(df):
    # Verificar valores faltantes
    if df.isnull().values.any():
        print("Existen valores faltantes. Tratando de manejarlos...")
        df = df.dropna()
        print("Valores faltantes eliminados.")

    # Verificar filas duplicadas
    if df.duplicated().any():
        print("Existen filas duplicadas. Tratando de manejarlas...")
        df = df.drop_duplicates()
        print("Filas duplicadas eliminadas.")

    # Verificar valores atípicos y eliminarlos
    Q1 = df['age'].quantile(0.25)
    Q3 = df['age'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = (df['age'] < lower_bound) | (df['age'] > upper_bound)
    if outliers.any():
        print("Existen valores atípicos. Tratando de manejarlos...")
        df = df[~outliers]
        print("Valores atípicos eliminados.")

    # Crear columna de categorías por edades
    bins = [0, 12, 19, 39, 59, float('inf')]
    labels = ['Niño', 'Adolescente', 'Jóvenes adulto', 'Adulto', 'Adulto mayor']
    df['Categoria_Edad'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Guardar el resultado como CSV
    df.to_csv('resultado.csv', index=False)
    print("Proceso completado. Resultado guardado como 'resultado.csv'.")


procesar_dataframe(df)