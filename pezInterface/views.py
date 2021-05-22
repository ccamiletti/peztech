import speech_recognition as sr
import datetime
import json
import os
import os.path
import time
import subprocess
import sys
import pytz
import logging

from gtts import gTTS
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from os import scandir
from pezAutomatization import automatization_ms_stream, send_mail, upload_video_ws
from pezInterface.forms import ModuleForm, JaulaForm
from pezInterface.models import Modulo, Jaula, Centro, CentroDestinatario, RecordHistory, JaulaView, JsonTransformer
from pezTech.settings import BASE_DIR
from subprocess import PIPE, CalledProcessError
from vosk import Model, KaldiRecognizer

# Get an instance of a logger
logger = logging.getLogger(__name__)

json_properties = BASE_DIR + "/static/properties.json"

palabra_iniciar = ["inicio", "inicia", "iniciar", "inicial", "iniciar sesión"]


def getJaula(jaulaNumero):
    data = []
    sw = 0
    modulos = Modulo.objects.all()
    for mod in modulos:
        jaulas = Jaula.objects.all().filter(modulo_id=mod.id)
        for jau in jaulas:
            if (str(jaulaNumero) == str(jau.jaulaNumero)):
                return jau


def readingJaulas():

    # Sample rate is how often values are recorded
    sample_rate = 48000
    # Chunk is like a buffer. It stores 2048 samples (bytes of data)
    # here.
    # it is advisable to use powers of 2 such as 1024 or 2048
    chunk_size = 2048
    # Initialize the recognizer
    #r = sr.Recognizer()
    # generate a list of all audio cards/microphones
    #mic_list = sr.Microphone.list_microphone_names()

    # the following loop aims to set the device ID of the mic that
    # we specifically want to use to avoid ambiguity.
    # for i, microphone_name in enumerate(mic_list):
    #    if microphone_name == mic_name:
    #        print("microphone_name => ", i)
    #        device_id = i

    device_id = 7
    text = ""
    # use the microphone as source for input. Here, we also specify
    # which device ID to specifically look for incase the microphone
    # is not working, an error will pop up saying "device_id undefined"
    with sr.Microphone(device_index=device_id, sample_rate=sample_rate, chunk_size=chunk_size) as source:
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        sr.Recognizer().adjust_for_ambient_noise(source)
        print("Say Something")
        # listens for the user's input
        audio = sr.Recognizer().listen(source)
        try:
            text = sr.Recognizer().recognize_sphinx(audio, language="es-ES")
            print("you said: " + text)

        # error occurs when google could not understand what was said

        except sr.Recognizer().UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.Recognizer().RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service {0}".format(e))

    return text


def getJaulaByVoice(request):
    sw = 0
    while sw == 0:
        try:
            jaulaNumero = readingJaulas()
            int(jaulaNumero)
            jaulaObj = getJaula(jaulaNumero)
            print("jaula object encontrada => ", jaulaObj)
            if jaulaObj is None:
                readAudio(
                    "jaula no encontrada, por favor repita numero de Jaula")
            else:
                print("jaula encontrada => ", jaulaObj)
                sw = 1
        except:
            print(
                "exception trying to get jaula wih text [NOT] => ", jaulaNumero)
            readAudio("jaula no encontrada, por favor repita numero de Jaula")

    return HttpResponse(json.dumps(jaulaNumero), content_type='application/json')


def bienvenida(request):
    readAudio('Bienvenido a peztech, por favor seleccione las jaulas')
    return HttpResponse(json.dumps("OK"), content_type='application/json')


def readAudio(texto):
    import os
    import mpyg321
    language = 'es'
    myobj = gTTS(text=texto, lang=language, slow=False)
    myobj.save("static/audios/welcome.mp3")
    os.system("mpg321 static/audios/welcome.mp3")
    response = {'modulo': 'example'}


def speech_to_text(palabras=[], *args):
    import os
    import pyaudio
    import json

    if not os.path.exists("model"):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    model = Model("model")
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    sw = 0
    word = "Palabra no encontrada"
    cont = 1
    while sw == 0:
        cont = cont + 1
        print(cont)
        data = stream.read(10000, exception_on_overflow=False)
        if len(data) == 0:
            print("breaking process")
            break
        if rec.AcceptWaveform(data):
            print("result ->" + json.loads(rec.Result())['text'])
            print("result json ->" + rec.Result())
            word = json.loads(rec.Result())['text']
        else:
            print("PartialResult ->" +
                  json.loads(rec.PartialResult())['partial'])
            print("PartialResult json ->" + rec.PartialResult())
            word = json.loads(rec.Result())['text']

        for init in palabras:
            if (word == init):
                sw = 1

    print("palabra aceptada")
    stream.stop_stream()
    # stream.close()
    p.terminate()

    return word


# Create your views here.
def index(request):
    # cierre_forzado_process(request)
    record = RecordHistory.objects.all().filter(statusRecord="IN_PROCESS")
    print("record => ")
    print(record)
    if record:
        record_in_process = "Y"
    else:
        record_in_process = "N"

    print("record_in_process => ")
    print(record_in_process)
    contexto = {'recordInProcess': record_in_process, 'record': record}
    return render(request, 'pezInterface/index.html', contexto)


def modulos_list(request):
    modulo = Modulo.objects.all()
    contexto = {'modulos': modulo}
    return render(request, 'pezInterface/modulos_list.html', contexto)


def modulo_view(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('pezInterface:modulos_listar')
    else:
        form = ModuleForm()

    return render(request, 'pezInterface/modulos_form.html', {'form': form})


def modulo_edit(request, id_modulo):
    modulo = Modulo.objects.get(id=id_modulo)
    if request.method == 'GET':
        form = ModuleForm(instance=modulo)
    else:
        form = ModuleForm(request.POST, instance=modulo)
        if form.is_valid():
            form.save()
        return redirect('pezInterface:modulos_listar')
    return render(request, 'pezInterface/modulos_form.html', {'form': form})


def modulo_delete(request, id_modulo):
    modulo = Modulo.objects.get(id=id_modulo)
    if request.method == 'POST':
        modulo.delete()
        return redirect('pezInterface:modulos_listar')
    return render(request, 'pezInterface/modulo_delete.html', {'modulo': modulo})


def jaulas_list(request, id_modulo):
    jaulas = Jaula.objects.all().filter(modulo_id=id_modulo)
    contexto = {'jaulas': jaulas, 'id_modulo': id_modulo}
    return render(request, 'pezInterface/jaulas_list.html', contexto)


def jaulas_list_ajax(request):
    data = []
    modulos = Modulo.objects.all()
    for mod in modulos:
        jaulas = Jaula.objects.all().filter(modulo_id=mod.id)
        for jau in jaulas:
            jaulaView = JaulaView(jau.id, jau.jaulaNumero,
                                  mod.moduloNumero, mod.id)
            data.append(jaulaView)

    s = json.dumps([p.__dict__ for p in list(data).__iter__()])
    return HttpResponse(s, content_type='application/json')


def jaula_view(request, id_modulo):
    if request.method == 'POST':
        form = JaulaForm(request.POST)
        if form.is_valid():
            form.instance.modulo_id = id_modulo
            form.save()
        return redirect('pezInterface:jaulas_listar', id_modulo)
    else:
        form = JaulaForm()

    return render(request, 'pezInterface/jaulas_form.html', {'form': form, 'id_modulo': id_modulo})


def jaula_delete(request, id_jaula):
    jaula = Jaula.objects.get(id=id_jaula)
    modulo_id = jaula.modulo.id
    if request.method == 'POST':
        jaula.delete()
        return redirect('pezInterface:jaulas_listar', modulo_id)
    return render(request, 'pezInterface/jaula_delete.html', {'jaula': jaula})


def centro_list(request):
    centro = Centro.objects.all()

    if centro:
        centro_id = centro[0].id
        emails = CentroDestinatario.objects.all().filter(centro_id=centro_id)
    else:
        emails = None

    contexto = {'centro': centro, 'emails': emails}
    return render(request, 'pezInterface/centro_list.html', contexto)


def centro_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        rango_horario_desde = request.POST['rangoHorarioDesde']
        rango_horario_hasta = request.POST['rangoHorarioHasta']
        dias_almacenamiento_stream = request.POST['diasAlmacenamientoStream']
        smtp_host = request.POST['smtpHost']
        smtp_usuario = request.POST['smtpUsuario']
        smtp_contrasena = request.POST['smtpContrasena']
        smtp_secure = request.POST['smtpSecure']
        smtp_puerto = request.POST['smtpPuerto']
        canal_stream = request.POST['canalStream']
        emails = request.POST.getlist('emails')

        centro1 = Centro(
            nombre=nombre,
            rangoHorarioDesde=rango_horario_desde,
            rangoHorarioHasta=rango_horario_hasta,
            diasAlmacenamientoStream=dias_almacenamiento_stream,
            canalStream=canal_stream,
            smtpHost=smtp_host,
            smtpUsuario=smtp_usuario,
            smtpContrasena=smtp_contrasena,
            smtpSecure=smtp_secure,
            smtpPuerto=smtp_puerto)
        centro1.save()

        for email in emails:
            email1 = CentroDestinatario(
                centro_id=centro1.id,
                email=email
            )
            email1.save()

        return redirect('pezInterface:centro_listar')

    return render(request, 'pezInterface/centro_form.html')


def centro_edit(request, id_centro):
    centro = Centro.objects.get(id=id_centro)
    destinatarios = CentroDestinatario.objects.all().filter(centro_id=id_centro)
    if request.method == 'GET':
        # form = ModuleForm(instance=centro)
        return render(request, 'pezInterface/centro_form.html', {'centro': centro, 'emails': destinatarios})
    else:
        id = request.POST['id']
        nombre = request.POST['nombre']
        rango_horario_desde = request.POST['rangoHorarioDesde']
        rango_horario_hasta = request.POST['rangoHorarioHasta']
        dias_almacenamiento_stream = request.POST['diasAlmacenamientoStream']
        canal_stream = request.POST['canalStream']
        smtp_host = request.POST['smtpHost']
        smtp_usuario = request.POST['smtpUsuario']
        smtp_contrasena = request.POST['smtpContrasena']
        smtp_secure = request.POST['smtpSecure']
        smtp_puerto = request.POST['smtpPuerto']
        emails = request.POST.getlist('emails')

        centro1 = Centro(
            id=id,
            nombre=nombre,
            rangoHorarioDesde=rango_horario_desde,
            rangoHorarioHasta=rango_horario_hasta,
            diasAlmacenamientoStream=dias_almacenamiento_stream,
            canalStream=canal_stream,
            smtpHost=smtp_host,
            smtpUsuario=smtp_usuario,
            smtpContrasena=smtp_contrasena,
            smtpSecure=smtp_secure,
            smtpPuerto=smtp_puerto)
        centro1.save()

        # se deben obtener los emails actuales en la BD, si ya no viene en el form se elimina

        for email in emails:
            validate_email = destinatarios.filter(email=email)

            if validate_email:
                logger.warning("Email ya existe en la BD")
                print("Email ya existe en la BD")
            else:
                email1 = CentroDestinatario(
                    centro_id=id,
                    email=email
                )
                email1.save()

        for dest in destinatarios:
            if dest.email in emails:
                logger.info("Si viene el email: " + dest.email)
                print("Si viene el email: " + dest.email)
            else:
                email_delete(dest.id)

    return redirect('pezInterface:centro_listar')


def email_delete(id_email):
    email = CentroDestinatario.objects.get(id=id_email)
    email.delete()


def record_view(request):
    datos = request.GET.get('data', None)
    datos_json = json.loads(datos)
    modulos = sorted(datos_json, key=lambda k: k['moduloId'], reverse=False)

    print("*************sasd**********")
    print(modulos)
    print("***************dasddsa********")
    record_description = ""
    sw = 0
    for mod in modulos:
        print(mod)
        if (sw == 0):
            record_description = "Modulo: " + str(mod['moduloNumero'])
            modaux = mod['moduloId']
            sw = 1

        if (modaux == mod['moduloId']):
            record_description += " (Jaula " + str(mod['numero_jaula']) + ")"
        else:
            record_description += ", Modulo: " + \
                str(mod['moduloNumero']) + " (Jaula " + \
                str(mod['numero_jaula']) + ")"
            modaux = mod['moduloId']

    print(record_description)

    """now = datetime.datetime.now()
    now_update = now + datetime.timedelta(seconds=10)  # se le agregan 10 seg. de delay para el comienzo de la grabación
    now_format = now_update.strftime("%Y-%m-%d %H:%M:%S")"""

    now_cl = datetime.datetime.now(pytz.timezone('America/Santiago'))
    now_cl_format = now_cl.strftime("%Y-%m-%d %H:%M:%S")

    record = RecordHistory(
        startTime=now_cl_format,
        observation=record_description,
        statusRecord="IN_PROCESS"
    )

    record.save()
    updateJson(now_cl_format, record_description)


def record_edit(request, now_format, save_video, file_name_video_recording_obs):
    record_id = request.GET.get('record_id', None)
    record = RecordHistory.objects.get(id=record_id)

    record1 = RecordHistory(
        id=record_id,
        startTime=record.startTime,
        endTime=now_format,
        observation=record.observation,
        saveVideo=save_video,
        statusRecord="FINISH",
        obsNameVideo=file_name_video_recording_obs
    )

    record1.save()


def iniciarSeleccion(request):
    print("starting !!!")
    modulo = Modulo.objects.all()
    contexto = {'modulos': modulo}
    word = speech_to_text(palabra_iniciar)
    print("proceo de voz terminado con palabra: " + word)

    return render(request, 'pezInterface/index_selection.html', contexto)


def iniciarSeleccion_old(request):
    modulo = Modulo.objects.all()
    contexto = {'modulos': modulo}
    return render(request, 'pezInterface/index_selection.html', contexto)


def iniciar(request):
    logger.info("----- Iniciando la grabacion -----")
    print("----- Iniciando la grabacion -----")

    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        obs_path = data_prop['obsPath']
        obs_file_name = data_prop['obsFileName']

    try:
        subprocess.Popen(obs_file_name, cwd=obs_path,
                         shell=True, stdout=PIPE, stderr=PIPE)
        logger.info("----- OBs iniciado -----")
        print("----- OBs iniciado -----")
        record_view(request)
    except CalledProcessError as e:
        if e.returncode == 127:
            sys.exit("program '%s' not found")
        elif e.returncode <= 125:
            sys.exit("'%s' failed, returned code %d" % e.returncode)
        else:
            sys.exit("'%s' likely crashed, shell returned code %d" %
                     e.returncode)
    except OSError as e:
        sys.exit("failed to run shell: '%s'" % (str(e)))

    response = {'result': "success"}
    print("what happen now ?")
    return HttpResponse(json.dumps(response), content_type='application/json')


def finalizar(request):
    logger.info("----- Finalizando la grabacion -----")
    print("----- Finalizando la grabacion -----")

    """now = datetime.datetime.now()
    now_update = now + datetime.timedelta(seconds=10)  # se le agregan 10 seg. de delay para el fin de la grabación
    now_format = now_update.strftime("%Y-%m-%d %H:%M:%S")"""

    now_cl = datetime.datetime.now(pytz.timezone('America/Santiago'))
    now_cl_format = now_cl.strftime("%Y-%m-%d %H:%M:%S")

    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        json_path = data_prop['jsonPath']

    logger.info("----- Actualizando Json - Fecha fin de grabacion " +
                str(now_cl_format) + " -----")
    print("----- Actualizando Json - Fecha fin de grabacion " +
          str(now_cl_format) + " -----")

    with open(json_path, 'r') as file:
        data = json.load(file)
        data['end_time'] = now_cl_format

    with open(json_path, 'w') as file:
        file.write(json.dumps(data))

    # buscar el nombre del archivo con el que quedo en OBS
    time.sleep(45)
    save_video = request.GET.get('save_video', None)
    moveVideoRecord(request, now_cl_format, save_video)

    response = {'result': 'success'}
    return HttpResponse(json.dumps(response), content_type='application/json')


def updateJson(now_format, record_description):
    logger.info("----- Actualizando Json - Fecha inicio de grabacion -----")
    print("----- Actualizando Json - Fecha inicio de grabacion -----")

    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        json_path = data_prop['jsonPath']

    logger.info("----- Grabacion inicia a las " + str(now_format) + " -----")
    print("----- Grabacion inicia a las " + str(now_format) + " -----")
    with open(json_path, 'r') as file:
        data = json.load(file)
        data['enabled_record'] = "True"
        data['start_time'] = now_format
        data['description_record'] = record_description

    with open(json_path, 'w') as file:
        file.write(json.dumps(data))
    print("So ?")


def moveVideoRecord(request, now_format, save_video):
    logger.info("----- Moviendo video -----")
    print("----- Moviendo video -----")

    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        folder_video_recording = data_prop['folderVideoRecording']
        folder_failed_video_recording = data_prop['folderFailedVideoRecording']
        folder_to_upload_video_recording = data_prop['folderToUploadVideoRecording']
        extension_video_recording = data_prop['extensionVideoRecording']
        so = data_prop['so']
        userSoPassword = data_prop['userSoPassword']

    files = ls(folder_video_recording)
    move_folder = ""
    file_name_video_recording_obs = ""

    for file in files:
        if extension_video_recording in file:
            file_name_video_recording_obs += file

            if save_video == "N":
                move_folder += folder_failed_video_recording
            else:
                move_folder += folder_to_upload_video_recording

    if not os.path.exists(move_folder):
        os.mkdir(move_folder)

    """if so == "Windows":
        os.replace(folder_video_recording + file_name_video_recording_obs, move_folder + file_name_video_recording_obs)
    else:
        sudo_password = 'qwe12qwe'
        # command = 'mv '+folder_video_recording + file_name_video_recording_obs+" "+move_folder + file_name_video_recording_obs
        command = "mv "+folder_video_recording + file_name_video_recording_obs+" "+move_folder
        command2 = "sudo killall obs"
        logger.info(command2)
        logger.info(command)
        # os.system('echo %s|sudo -S %s' % (sudo_password, command))
        os.popen("sudo -S %s" % command2, 'w').write(sudo_password)
        os.popen("sudo -S %s" % command, 'w').write(sudo_password)"""

    os.replace(folder_video_recording + file_name_video_recording_obs,
               move_folder + file_name_video_recording_obs)

    if so == "Linux":
        sudo_password = userSoPassword
        command = "sudo killall obs"
        logger.info(command)
        print(command)
        os.popen("sudo -S %s" % command, 'w').write(sudo_password)

    record_edit(request, now_format, save_video, file_name_video_recording_obs)


def testWS(self):
    logger.info("info AQUI ES TEST WS")
    print("info AQUI ES TEST WS")

    response = {'result': "success"}
    return HttpResponse(json.dumps(response), content_type='application/json')


def otros_list(request):
    return render(request, 'pezInterface/otros_list.html')


def cierre_confirmacion(request):
    return render(request, 'pezInterface/cierre_forzado.html')


def cierre_forzado_process(request):
    logger.info("----- Cierre forzado -----")
    print("----- Cierre forzado -----")

    # 1. Dejar en FINISH todas las grabaciones en proceso
    records = RecordHistory.objects.all().filter(statusRecord="IN_PROCESS")

    if records:
        logger.info("----- Actualizando grabaciones IN_PROCESS -----")
        print("----- Actualizando grabaciones IN_PROCESS -----")
        for record in records:
            record.statusRecord = "FINISH"
            record.save()

    # 2. Dejar el archivo obs.properties por default
    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        json_path = data_prop['jsonPath']
        folder_video_recording = data_prop['folderVideoRecording']
        folder_failed_video_recording = data_prop['folderFailedVideoRecording']
        extension_video_recording = data_prop['extensionVideoRecording']

    with open(json_path, 'r') as file:
        data = json.load(file)
        data['enabled_record'] = "False"
        data['start_time'] = ""
        data['description_record'] = ""
        data['end_time'] = ""
        data['save_record'] = "False"
        data['loop_seconds'] = 5000

    with open(json_path, 'w') as file:
        file.write(json.dumps(data))

    # 3. Mover todos los archivos de la carpeta obs/video a obs/video/pendingRemove
    files = ls(folder_video_recording)
    move_folder = folder_failed_video_recording

    for file in files:
        if extension_video_recording in file:
            os.replace(folder_video_recording + file, move_folder + file)

    # return render(request, 'pezInterface/index.html',)
    print("redirecting")
    return redirect('pezInterface:index')


def grabaciones_pendientes_list(request):

    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        folder_video_recording = data_prop['folderToUploadVideoRecording']

    files = ls(folder_video_recording)

    data_list = []
    for file in files:
        record_data = RecordHistory.objects.filter(obsNameVideo=file)
        if record_data:
            data_list.append(record_data[0])

    contexto = {'records': data_list}
    return render(request, 'pezInterface/grabaciones_pendientes_list.html', contexto)


def enviar_notificacion(request, id_record):
    centro = Centro.objects.all()
    record = RecordHistory.objects.get(id=id_record)
    contexto = {'centro': centro[0], 'record': record}
    return render(request, 'pezInterface/enviar_notificacion.html', contexto)


def proceso_carga_confirmacion(request, id_record):
    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        folder_video_recording = data_prop['folderToUploadVideoRecording']

    record = RecordHistory.objects.get(id=id_record)
    contexto = {'record': record,
                'folder_video_recording': folder_video_recording}
    return render(request, 'pezInterface/proceso_carga_confirmacion.html', contexto)


def enviar_email(request):
    datos = request.GET.get('data', None)
    datos_json = json.loads(datos)

    id_record = datos_json['id_record']
    url_video = datos_json['url_video']
    nombre_centro = datos_json['nombre_centro']
    observation = datos_json['observacion']
    desc_video = nombre_centro+", "+observation

    send_mail.send_notification(desc_video, url_video)

    record = RecordHistory.objects.get(id=id_record)
    record.statusUpload = "FINISH"
    record.save()

    response = {'result': "success"}
    return HttpResponse(json.dumps(response), content_type='application/json')


def cargar_video(request):
    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        folder_video_recording = data_prop['folderToUploadVideoRecording']
        folder_failed_video_recording = data_prop['folderFailedVideoRecording']

    datos_request = request.GET.get('data_request', None)
    datos_request_json = json.loads(datos_request)
    file_name = datos_request_json['file_name']

    upload_video_ws.continue_upload(
        file_name, folder_video_recording, folder_failed_video_recording)

    response = {'result': "success"}
    return HttpResponse(json.dumps(response), content_type='application/json')


def ls(path):
    return [obj.name for obj in scandir(path) if obj.is_file()]
