from keras.models import load_model  # pip install tensorflow==2.9.0
import cv2  # pip install opencv-python==4.8.0.74
import numpy as np
import time
from suscriptor import obtener_datos
from updatebd import update_appstate, update_database_with_log
from datetime import datetime
import webbrowser
import os

# Desactivar notación científica para mayor claridad
np.set_printoptions(suppress=True)

# Cargar el modelo
model = load_model("keras_Model.h5", compile=False)

# Cargar las etiquetas
class_names = open("labels.txt", "r").readlines()

ruta_archivo = 'C:/Users/57302/PycharmProjects/RecFacial/index.html'
# Asegúrate de que la ruta sea absoluta
ruta_absoluta = os.path.abspath(ruta_archivo)
# Abre el archivo HTML en el navegador predeterminado
webbrowser.open(f'file://{ruta_absoluta}')

while True:
    time.sleep(3)  # Intervalo de 3 segundos entre llamadas a la base de datos
    url = "https://biofacepro-default-rtdb.firebaseio.com/.json"
    estado, faceid = obtener_datos(url)
    appstate_url = "https://biofacepro-default-rtdb.firebaseio.com/appstate.json?auth=blpAMq9G4AqyEPStZ5hsizUXyo8nq6lu06ZZJpzu"
    log_url = "https://biofacepro-default-rtdb.firebaseio.com/logs.json?auth=blpAMq9G4AqyEPStZ5hsizUXyo8nq6lu06ZZJpzu"

    if estado == "getfaceid":
        print("Procesando con los datos obtenidos...")
        camera = cv2.VideoCapture(0)

        contador = 0

        recognized = False
        while not recognized:
            ret, image = camera.read()
            image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            cv2.imshow("Webcam Image", image_resized)

            image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
            image_array = (image_array / 127.5) - 1

            prediction = model.predict(image_array)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            label = class_name[2:].strip()
            porcentaje = str(np.round(confidence_score * 100))[:-2].strip()

            print("Class:", label, "Confidence Score:", porcentaje, "%")
            contador += 1

            if contador == 200:
                falla = "faceidnull"
                update_appstate(appstate_url, falla)
                time.sleep(5)
                falla = "getcard"
                update_appstate(appstate_url, falla)
                break

            if label == faceid and int(porcentaje) > 92:
                recognized = True

        if recognized:
            now = datetime.now().isoformat()
            data = {
                "Pago": "confirmado",
                "faceid": faceid,
                "timestamp": now
            }
            update_database_with_log(log_url, data)
            print(f"Datos almacenados en la base de datos: {data}")

            actualizacion = "default"
            update_appstate(appstate_url, actualizacion)
            time.sleep(5)
            actualizacion = "getcard"
            update_appstate(appstate_url, actualizacion)

        camera.release()
        cv2.destroyAllWindows()
    else:
        print("No se pudieron obtener los datos necesarios.")

    print("Desconexión exitosa")
