# https://docs.python.org/3/library/sched.html
# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/#howto-custom-management-commands
import datetime
import json
import os
import sched
import time
import pytz
import logging

from os import scandir
from pezAutomatization import automatization_ms_stream
from pezInterface.models import Centro, RecordHistory
from pezTech.settings import BASE_DIR
from pezAutomatization import send_mail

s = sched.scheduler(time.time, time.sleep)
json_properties = BASE_DIR + "/static/properties.json"

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_ws(sc):
    logger.info("En upload_video: process_ws...")
    print("En upload_video: process_ws...")

    centro_data = Centro.objects.all()

    if centro_data:
        rango_horario_desde = centro_data[0].rangoHorarioDesde
        rango_horario_hasta = centro_data[0].rangoHorarioHasta

        if rango_horario_desde is not None and rango_horario_hasta is not None:
            logger.info("upload_video: RANGO DESDE: " + str(rango_horario_desde))
            logger.info("upload_video: RANGO HASTA: " + str(rango_horario_hasta))

            print("RANGO DESDE: " + str(rango_horario_desde))
            print("RANGO HASTA: " + str(rango_horario_hasta))

            # obtener hora actual si esta dentro del rango desde y hasta
            # now = datetime.datetime.now()
            now_cl = datetime.datetime.now(pytz.timezone('America/Santiago'))
            now_hour_format = int(now_cl.strftime("%H"))
            now_min_format = int(now_cl.strftime("%M"))

            logger.info("upload_video: Hora actual: " + str(now_hour_format) + " " + str(now_min_format))
            print("Hora actual: " + str(now_hour_format) + " " + str(now_min_format))

            if now_hour_format >= rango_horario_desde and now_hour_format <= rango_horario_hasta:
                logger.info("upload_video: Rango ok")
                print("Rango ok")
                # ejecutar task para subir video a MS stream
                process_upload_record_video()
            else:
                logger.info("upload_video: No esta dentro del rango de carga")
                logger.info("upload_video: Obteniendo el rango restante en que se ejecutara la task...")

                print("No esta dentro del rango de carga")
                print("Obteniendo el rango restante en que se ejecutara la task...")

                diff_hours = rango_horario_desde - now_hour_format - 1
                # print("Faltan "+str(diff_hours)+" Horas")

                diff_min = 60 - now_min_format
                # print("Faltan "+str(diff_min)+" Minutos")

                diff_sec = diff_hours * 3600  # se pasan las horas a segundos
                diff_sec += diff_min * 60  # se pasan los minutos a segundos

                logger.info("upload_video: Task se ejecutara en " + str(diff_sec) + " segundos")
                print("Task se ejecutara en " + str(diff_sec) + " segundos")

                s.enter(diff_sec, 1, process_ws, (sc,))  # diff_sec trae los seg. que faltan para ejecutar la task
        else:
            logger.info("upload_video: NO VIENE FECHA DESDE O HASTA")
            print("NO VIENE FECHA DESDE O HASTA")
            # s.cancel(sc)
    else:
        logger.info("upload_video: NO VIENE DATO DEL CENTRO")
        print("NO VIENE DATO DEL CENTRO")
        # s.cancel(sc)


def process_upload_record_video():
    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        folder_video_recording = data_prop['folderToUploadVideoRecording']
        folder_failed_video_recording = data_prop['folderFailedVideoRecording']

    files = ls(folder_video_recording)

    if len(files) > 0:
        continue_upload(files[0], folder_video_recording, folder_failed_video_recording)
    else:
        logger.info("upload_video: No existen videos para cargar en MS Stream")
        print("No existen videos para cargar en MS Stream")


def continue_upload(file_to_upload, folder_video_recording, folder_failed_video_recording):
    path_file_to_upload = folder_video_recording + file_to_upload

    record_data = RecordHistory.objects.filter(obsNameVideo=file_to_upload)

    centro = Centro.objects.all()
    canal_stream = centro[0].canalStream
    email_stream = centro[0].smtpUsuario
    password_stream = centro[0].smtpContrasena

    if record_data:
        save_video = record_data[0].saveVideo
        desc_video = record_data[0].observation

        if save_video == "Y":
            logger.info("upload_video: Video registrado para cargarse en MS Stream")
            print("Video registrado para cargarse en MS Stream")

            logger.info("----- upload_video: Nombre del archivo: " + file_to_upload + " -----")
            logger.info("----- upload_video: Ruta del archivo: " + path_file_to_upload + " -----")
            logger.info("----- upload_video: Nombre canal: " + canal_stream + " -----")
            logger.info("----- upload_video: Desc. video: " + desc_video + " -----")

            print("----- Nombre del archivo: " + file_to_upload + " -----")
            print("----- Ruta del archivo: " + path_file_to_upload + " -----")
            print("----- Nombre canal: " + canal_stream + " -----")
            print("----- Desc. video: " + desc_video + " -----")

            # record_update = RecordHistory.objects.get(id=id_video)
            record_data[0].statusUpload = "IN_PROCESS"
            record_data[0].save()
            url_upload = automatization_ms_stream.upload_record_video(
                path_file_to_upload, desc_video, canal_stream, email_stream, password_stream)

            if url_upload:
                logger.info("----- upload_video: Archivo cargado correctamente, actualizando BD -----")
                print("----- Archivo cargado correctamente, actualizando BD -----")
                print(url_upload)

                now = datetime.datetime.now()
                record_data[0].statusUpload = "FINISH"
                record_data[0].dateUpload = now.strftime("%Y-%m-%d %H:%M:%S")

                # se actualiza la BD
                # record_history_update_finish = RecordHistory(record_data[0])
                record_data[0].save()

                logger.info("----- upload_video: Moviendo video a la carpeta correspondiente -----")
                print("----- Moviendo video a la carpeta correspondiente -----")
                # se mueve el archivo a la carpeta correspondiente para ser eliminado
                os.replace(folder_video_recording + file_to_upload, folder_failed_video_recording + file_to_upload)

                # Envio de notificaciones
                send_mail.send_notification(desc_video, url_upload)
        else:
            logger.info("upload_video: Video se registro como no guardado, moviendo a la carpeta correspondiente")
            print("Video se registro como no guardado, moviendo a la carpeta correspondiente")
            os.replace(folder_video_recording + file_to_upload, folder_failed_video_recording + file_to_upload)
    else:
        logger.info("upload_video: No hay registro encontrados en BD para el video")
        print("No hay registro encontrados en BD para el video")


def ls(path):
    return [obj.name for obj in scandir(path) if obj.is_file()]


# la 1 era cada 5 segundos, despues se obtiene la diferencia entre los rangos de horarios
# Se debe preguntar el rango horario para la subida de archivos a MS
# rango_horario_data = views.get_rango_horario_data()
# print(rango_horario_data)
def start_ws():
    s.enter(5, 1, process_ws, (s,))
    s.run()
