# ESTRUCTURA A USAR: [FECHA] [HILO] [ACCIÓN] [DETALLE] [RECURSO]
from datetime import datetime
import threading

mutex_log = threading.Lock()

def registrar_log(accion, detalle, recurso):
    with mutex_log:
        with open("bitacora.log", "a") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hilo = threading.current_thread().name

            linea = f"{fecha} | {hilo} | {accion} | {detalle} | {recurso}\n"
            archivo.write(linea)