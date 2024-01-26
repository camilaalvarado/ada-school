import requests


def ej_4_descargar_datos(url: str) -> None:
    # Realiza un GET request para descargarlos y escribe la respuesta como un archivo de texto plano con extensión csv (no necesitas pandas para esto, sólo manipulación de archivos nativa de Python)
    response = requests.get(url)
    # se guarda el archivo en la carpeta data
    with open('./heart_failure_clinical_records_dataset.csv', 'w') as f:
        f.write(response.text)
    # se lee el archivo csv
    df = pd.read_csv('./heart_failure_clinical_records_dataset.csv')
    # se guarda el DataFrame en un archivo csv
    df.to_csv('./heart_failure_clinical_records_dataset.csv', index=False)
    
   
# se llama a la funcion
ej_4_descargar_datos('https://huggingface.co/datasets/mstz/heart_failure/raw/main/heart_failure_clinical_records_dataset.csv')