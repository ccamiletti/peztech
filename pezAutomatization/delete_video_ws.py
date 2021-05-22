import sched
import time

from pezAutomatization import automatization_delete_video_stream
from pezInterface.models import Centro
from pezTech.settings import BASE_DIR

s = sched.scheduler(time.time, time.sleep)
json_properties = BASE_DIR + "/static/properties.json"


def process_ws():
    print("En delete_video: process_ws...")

    centro_data = Centro.objects.all()

    if centro_data:
        dias_tope_almacenamiento_ms = centro_data[0].diasAlmacenamientoStream
        email_ms = centro_data[0].smtpUsuario
        password_ms = centro_data[0].smtpContrasena

        if dias_tope_almacenamiento_ms:
            print("DIAS DE ALMACENAMIENTO: " + str(dias_tope_almacenamiento_ms))
            automatization_delete_video_stream.delete_video_ms_stream(int(dias_tope_almacenamiento_ms), email_ms, password_ms)
        else:
            print("NO VIENE DIAS DE ALMACENAMIENTO MS")
    else:
        print("NO VIENE DATO DEL CENTRO")
