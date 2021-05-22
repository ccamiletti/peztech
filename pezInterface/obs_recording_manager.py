#
# Project	OBS Recording Manager
# Version	1.0
# @author	JCARDENAS (cardenasvar@gmail.com)

import obspython as obs
import time
import json
import pytz

from datetime import datetime
from datetime import timedelta

Debug_Mode = True
start_time_record = ""
end_time_record = ""
loop_seconds = 30000

# ------------------------------------------------------------
# OBS Script Functions
# ------------------------------------------------------------


def script_load(settings):
	global Debug_Mode
	if Debug_Mode: print("Entrando en script_load")

	# obs.obs_data_set_bool(settings, "enabled_record", True)
	# script_update(settings)


def script_unload():
	global Debug_Mode
	if Debug_Mode: print("Entrando en script_unload")

	obs.timer_remove(timer_check)
	obs.timer_remove(timer_start_recording)


def script_save(settings):
	global Debug_Mode
	if Debug_Mode: print("Entrando en script_save")

	script_update(settings)


def script_defaults(settings):
	global Debug_Mode
	if Debug_Mode: print("Entrando en script_defaults")


def script_update(settings):
	global Debug_Mode
	global loop_seconds

	if Debug_Mode: print("Entrando en script_update")
	if Debug_Mode: print("Configurando timer")
	# obs.timer_add(timer_check, 5000)  # 5000

	print("Leyendo JSON")
	json_path = "/peztech/static/obs.json"
	# json_path = "D:/Documentos/PythonProjects/pezTech/static/obs.json"

	print("LOOP 1: "+str(loop_seconds))

	with open(json_path, 'r') as file:
		data = json.load(file)
		loop_seconds = int(data['loop_seconds'])
		print("LOOP 2: " + str(loop_seconds))
		obs.timer_add(timer_check, loop_seconds)  # 5 segundos


def script_description():
	global Debug_Mode
	if Debug_Mode: print("Entrando en script_description")

	return "<b>OBS Grabación automatizada</b>" + \
		"<hr>" + \
		"Grabación automatizada desde aplicación PezTech ©." + \
		"<br/>" + \
		"Se establece hora de inicio y fin para grabación desde la aplicación PezTech ©." + \
		"<br/>" + \
		"Modo de depuración simple para revisar funcionamiento de scripts en OBS." + \
		"<br/><br/>" + \
		"Realizado por JCARDENAS, © 2020" + \
		"<hr>"


def script_properties():
	global Debug_Mode
	if Debug_Mode: print("Entrando en script_properties")

	# now = datetime(2020,1,1,0,0)
	"""now = datetime.today()

	props = obs.obs_properties_create()
	obs.obs_properties_add_bool(props, "enabled_record", "Enabled")
	# obs.obs_properties_add_int(props, "duration", "Recording Duration (Minutes)", 1, 120, 1)
	st = obs.obs_properties_add_list(
		props, "start_time", "Record Start Time", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
	# este es el texto para el record start time
	obs.obs_property_list_add_string(st, "None", "None")
	et = obs.obs_properties_add_list(
		props, "end_time", "Record End Time", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)

	for x in range(96):
		obs.obs_property_list_add_string(st, str(datetime.time(now).strftime("%I:%M %p")), str(datetime.time(now)))
		obs.obs_property_list_add_string(et, str(datetime.time(now).strftime("%I:%M %p")), str(datetime.time(now)))
		now += timedelta(minutes=1)

	obs.obs_properties_add_bool(props, "enabled_stream", "Include Streaming")
	obs.obs_properties_add_bool(props, "debug_mode", "Debug Mode")
	return props"""

# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------


def timer_check():
	global Debug_Mode
	if Debug_Mode: print("Entrando en timer_check")

	global start_time_record
	global end_time_record
	global loop_seconds

	print("LOOP 3: "+str(loop_seconds))

	# in_process_record = False
	updated_json = False

	# leer archivo con configuraciones
	print("Leyendo JSON")
	json_path = "/peztech/static/obs.json"
	# json_path = "D:/Documentos/PythonProjects/pezTech/static/obs.json"
	with open(json_path, 'r') as file:
		data = json.load(file)

		enabled_record = bool(data['enabled_record'])
		start_time_record = data['start_time']
		end_time_record = data['end_time']

		if start_time_record:
			start_time_record = datetime.strptime(start_time_record, "%Y-%m-%d %H:%M:%S")
		else:
			enabled_record = False

		if end_time_record:
			end_time_record = datetime.strptime(end_time_record, "%Y-%m-%d %H:%M:%S")

		if enabled_record is True:
			print("Grabacion habilitada, procesando...")
			print("Hora de comienzo grabacion: "+str(start_time_record))
			print("Hora de fin grabacion: "+str(end_time_record))

			actual_time = datetime.now(pytz.timezone('America/Santiago'))
			actual_time = actual_time.strftime("%H:%M:%S")
			print("actualTime: " + str(actual_time))

			in_process_record = verify_in_process_record(actual_time, start_time_record, end_time_record)

			if in_process_record:
				print("La grabacion esta en proceso")

				# obs_frontend_recording_active: TRUE si la grabación está activa, False en caso contrario.
				if obs.obs_frontend_recording_active():
					print("En proceso de grabado...")
					# si la hora actual es mayor a la hora de fin de la grabacion, se finaliza
					if end_time_record:
						if Debug_Mode: print("Dejando de grabar ahora")
						#
						obs.obs_frontend_recording_stop()  # detiene la grabacion
						data['enabled_record'] = "False"
						data['start_time'] = ""
						data['end_time'] = ""
						data['description_record'] = ""
						data['loop_seconds'] = 5000
						updated_json = True
				else:
					print("Iniciando la grabacion...")
					data['loop_seconds'] = 45000
					loop_seconds = 45000
					# si la grabacion no esta activa, se inicia
					obs.obs_frontend_recording_start()  # Inicia la grabación.
					updated_json = True
			else:
				print("La grabacion aun no esta en el tiempo de comienzo o no esta activa")
				# obs_frontend_recording_active: TRUE si la grabación está activa, False en caso contrario.
				if obs.obs_frontend_recording_active():
					print("in_process_record FALSE, FINALIZANDO LA GRABACION")
					obs.obs_frontend_recording_stop()  # Detiene la grabación.
					data['enabled_record'] = "False"
					data['start_time'] = ""
					data['end_time'] = ""
					data['description_record'] = ""
					data['loop_seconds'] = 5000
					updated_json = True
		else:
			print("No existe grabacion habilitada")

	if updated_json is True:
		print("Actualizando JSON")
		with open(json_path, 'w') as file:
			file.write(json.dumps(data))
			obs.timer_remove(timer_check)


def timer_start_recording():
	global Debug_Mode
	if Debug_Mode: print("Entrando en timer_start_recording")

	# obs_frontend_recording_active: TRUE si la grabación está activa, False en caso contrario.
	if obs.obs_frontend_recording_active() is False:
		obs.obs_frontend_recording_start()  # Inicia la grabación.
		obs.timer_remove(timer_start_recording)


def verify_in_process_record(actual_time, start_time_record, end_time_record):
	start_time_record_format = start_time_record.strftime("%H:%M:%S")
	actual_time_format = time.strftime(actual_time)

	if start_time_record and str(end_time_record) == "":
		in_process_record = actual_time_format >= start_time_record_format
	elif start_time_record and end_time_record:
		end_time_record_format = end_time_record.strftime("%H:%M:%S")
		in_process_record = start_time_record_format <= actual_time_format <= end_time_record_format
	else:
		end_time_record_format = end_time_record.strftime("%H:%M:%S")
		in_process_record = not (actual_time_format > end_time_record_format)

	return in_process_record
