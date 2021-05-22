import json
import os

from os import scandir
from pezTech.settings import BASE_DIR

json_properties = BASE_DIR + "/static/properties.json"


def process_delete_local_videos():
    print("En delete_local_videos: process_delete_local_videos...")

    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        folder_failed_video_recording = data_prop['folderFailedVideoRecording']
        extension_video_recording = data_prop['extensionVideoRecording']

    files = ls(folder_failed_video_recording)
    print("Cantidad de archivos para eliminar: "+str(len(files)))

    for file in files:
        if extension_video_recording in file:
            print("Eliminando archivo: "+file)
            os.remove(folder_failed_video_recording+file)
            print("Archivo eliminado!")


def ls(path):
    return [obj.name for obj in scandir(path) if obj.is_file()]