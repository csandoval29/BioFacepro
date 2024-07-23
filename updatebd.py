import  requests
import json

def update_appstate(url, state):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.put(url, data=json.dumps({"state": state}), headers=headers)
        if response.status_code == 200:
            print('App state updated successfully:', response.json())
        else:
            print('Failed to update app state:', response.status_code, response.text)
    except Exception as e:
        print('Exception in update_appstate:', e)

def update_database_with_log(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Datos almacenados correctamente en la base de datos.")
    else:
        print(f"Error al almacenar datos en la base de datos: {response.status_code}, {response.text}")