import pandas as pd
from typing import Set
import requests

def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    url = "https://public.opendatasoft.com/explore/dataset/us-cities-demographics/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B"
    data = pd.read_csv(url, sep=';')

    # Limpiar los datos demográficos
    data.drop(columns=['Race', 'Count', 'Number of Veterans'], inplace=True)
    data.drop_duplicates(inplace=True)

    return data

def ej_2_cargar_calidad_aire(ciudades: Set[str]) -> None:
    # Inicializar un DataFrame para almacenar los datos de calidad del aire
    calidad_aire = pd.DataFrame(columns=['city', 'CO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'overall_aqi'])

    # Iterar sobre las ciudades y obtener datos de calidad del aire
    for ciudad in ciudades:
        url = f"https://api-ninjas.com/api/airquality?city={ciudad}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            calidad_aire = calidad_aire.append({
                'city': ciudad,
                'CO': data['concentration']['CO'],
                'NO2': data['concentration']['NO2'],
                'O3': data['concentration']['O3'],
                'SO2': data['concentration']['SO2'],
                'PM2.5': data['concentration']['PM2.5'],
                'PM10': data['concentration']['PM10'],
                'overall_aqi': data['overall_aqi']
            }, ignore_index=True)

    # Guardar los datos en un archivo CSV
    calidad_aire.to_csv('calidad_aire.csv', index=False)

# Tests
def test_sol_1():
    df = ej_1_cargar_datos_demograficos()
    idxs = [1995, 1360, 982, 2264, 2096, 1733, 1804, 2025, 2070, 507]

    selected_rows = df.loc[idxs].values
    assert _hash(selected_rows) == "567b67390efd8da8091f6f86da9f5e76b30d1b7dcb25bd7d9b87bcb757b2c571"


def test_sol_2():
    df = ej_1_cargar_datos_demograficos()
    ej_2_cargar_calidad_aire(set(df["City"].tolist()))

    ciudades_df = pd.read_csv("calidad_aire.csv")

    actual = ciudades_df.loc[:9].to_dict()

    expected = {
        'CO': {0: 250.34, 1: 287.06, 2: 247.0, 3: 280.38, 4: 323.77, 5: 243.66, 6: 173.57, 7: 211.95, 8: 263.69, 9: 260.35},
        'NO2': {0: 3.43, 1: 0.76, 2: 0.56, 3: 1.06, 4: 1.67, 5: 0.91, 6: 0.23, 7: 0.84, 8: 0.8, 9: 1.71},
        'O3': {0: 167.37, 1: 103.0, 2: 41.13, 3: 98.71, 4: 86.55, 5: 100.14, 6: 94.41, 7: 105.86, 8: 100.14, 9: 130.18},
        'SO2': {0: 2.92, 1: 2.3, 2: 0.19, 3: 1.1, 4: 6.32, 5: 1.27, 6: 0.38, 7: 0.24, 8: 0.4, 9: 5.36},
        'PM2.5': {0: 17.78, 1: 6.06, 2: 1.79, 3: 4.08, 4: 2.64, 5: 5.43, 6: 12.62, 7: 1.67, 8: 4.49, 9: 6.21},
        'PM10': {0: 26.26, 1: 6.37, 2: 1.85, 3: 4.47, 4: 2.95, 5: 5.68, 6: 48.06, 7: 1.79, 8: 4.66, 9: 6.76},
        'overall_aqi': {0: 220, 1: 170, 2: 34, 3: 159, 4: 128, 5: 162, 6: 148, 7: 177, 8: 162, 9: 205},
        'city': {0: 'Perris', 1: 'Mount Vernon', 2: 'Mobile', 3: 'Dale City', 4: 'Maple Grove', 5: 'Muncie', 6: 'San Clemente', 7: 'Providence', 8: 'Norman', 9: 'Hoover'}
    }

    assert expected == actual