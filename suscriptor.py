# consumoApi.py
import requests

def obtener_datos(url):
    try:
        # Realizando la solicitud GET
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo algún error en la solicitud

        # Parseando el contenido de la respuesta a formato JSON
        data = response.json()

        # Extraer las claves específicas
        estado = data.get('appstate', {}).get('state', None)
        faceid = data.get('appstate', {}).get('faceid', None)


        # Imprimir los valores extraídos
        print(f"Estado: {estado}")
        print(f"FaceID: {faceid}")

        return estado, faceid

    except requests.exceptions.RequestException as e:
        # Manejo de errores en la solicitud
        print(f"Error al realizar la solicitud: {e}")
        return None, None
