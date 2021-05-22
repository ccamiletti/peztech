import json
import time
import logging

from pezTech.settings import BASE_DIR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Get an instance of a logger
logger = logging.getLogger(__name__)


def upload_record_video(video_path, video_desc, canal_name, email_stream, password_stream):
    # paths y configuraciones
    logger.info("----- UPLOAD MS: Entrando en upload record video -----")
    logger.info("----- UPLOAD MS: Leyendo JSON de configuraciones -----")

    print("----- UPLOAD MS: Entrando en upload record video -----")
    print("----- UPLOAD MS: Leyendo JSON de configuraciones -----")

    json_properties = BASE_DIR + "/static/properties.json"
    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        url_upload = data_prop['urlToUploadRecordingStream']
        web_driver_name = data_prop['webDriverName']
        so = data_prop['so']
        modality_automatization_web = data_prop['modalityAutomatizationWeb']

    if so == "Linux":
        logger.info("----- UPLOAD MS: S.O. es Linux -----")
        print("----- UPLOAD MS: S.O. es Linux -----")
        web_driver_path = '/usr/lib/chromium-browser/chromedriver'
    else:
        web_driver_path = BASE_DIR + "/dchrome/"+web_driver_name

    logger.info("----- UPLOAD MS: web_driver_path: " + web_driver_path + " -----")
    print("----- UPLOAD MS: web_driver_path: " + web_driver_path + " -----")

    if modality_automatization_web == "web":
        logger.info("----- UPLOAD MS: Lanzando WebDriver modalidad WEB -----")
        print("----- UPLOAD MS: Lanzando WebDriver modalidad WEB -----")

        if so == "Linux":
            # https://ivanderevianko.com/2020/01/selenium-chromedriver-for-raspberrypi
            print("----- UPLOAD MS: S.O. es Linux -----")
            driver = webdriver.Chrome(executable_path=web_driver_path)
        else:
            print("----- UPLOAD MS: S.O. NO es Linux -----")
            driver = webdriver.Chrome(executable_path=r""+web_driver_path)
    else:
        logger.info("----- UPLOAD MS: Lanzando WebDriver modalidad 2do plano. -----")
        print("----- UPLOAD MS: Lanzando WebDriver modalidad 2do plano. -----")

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        if so == "Linux":
            # https://ivanderevianko.com/2020/01/selenium-chromedriver-for-raspberrypi
            print("----- UPLOAD MS: S.O. es Linux -----")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(web_driver_path, chrome_options=chrome_options)
        else:
            print("----- UPLOAD MS: S.O. NO es Linux -----")
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"" + web_driver_path)

    driver.get(url_upload)
    time.sleep(15)

    logger.info("----- UPLOAD MS: Realizando Login en MS Stream -----")
    logger.info("----- UPLOAD MS: Email: "+email_stream+" -----")

    print("----- UPLOAD MS: Realizando Login en MS Stream -----")
    print("----- UPLOAD MS: Email: "+email_stream+" -----")
    # 1. se ingresan los datos para iniciar sesion
    user_form = driver.find_element_by_id("i0116")
    user_form.send_keys(email_stream)
    user_form.send_keys(Keys.ENTER)
    time.sleep(10)

    password_form = driver.find_element_by_id("i0118")
    password_form.send_keys(password_stream)
    password_form.send_keys(Keys.ENTER)
    time.sleep(10)
    logger.info("----- UPLOAD MS: Sesion Iniciada -----")
    print("----- UPLOAD MS: Sesion Iniciada -----")

    # 1.1 click en boton para no mantener la sesion iniciada
    mantener_sesion = driver.find_element_by_id("idBtn_Back")
    mantener_sesion.send_keys(Keys.ENTER)
    time.sleep(30)

    logger.info("----- UPLOAD MS: Creando Evento MS Stream -----")
    print("----- UPLOAD MS: Creando Evento MS Stream -----")
    # 2. click en boton Crear
    navigation = driver.find_element_by_id("create-desktop-navigation")
    navigation.click()
    time.sleep(10)

    logger.info("----- UPLOAD MS: Cargando video desde los archivos locales -----")
    print("----- UPLOAD MS: Cargando video desde los archivos locales -----")
    # 3. click en Cargar Video
    cargar_video = driver.find_element_by_xpath("/html/body/div[1]/top-nav/topbar/div/div/div/div[1]/nav/ul/li[4]/div/ul/li[1]")
    cargar_video.click()
    time.sleep(15)

    # 4. examinar video
    elm = driver.find_element_by_xpath("//input[@type='file']")
    elm.send_keys(video_path)
    # examinar = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div[1]/div/div/upload-permissions/div/div/div/div/div/div[1]/button")
    time.sleep(30)

    logger.info("----- UPLOAD MS: Agregando Descripcion de video y permisos -----")
    print("----- UPLOAD MS: Agregando Descripcion de video y permisos -----")
    # 4.1 descripcion del video
    description = driver.find_element_by_name("uploaddescription")
    description.send_keys(video_desc)
    time.sleep(20)

    # 4.2 permisos
    perm = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/v-accordion/v-pane[2]")
    perm.click()
    time.sleep(15)

    # 4.3 destickear permisos para toda la empresa
    # perm_empresa = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/div/label/input")
    perm_empresa = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/div/label/span")
    perm_empresa.click()
    time.sleep(15)

    confirmar_dialog = driver.find_element_by_class_name("confirmation-dialog")
    find_button_confirmar = confirmar_dialog.find_elements_by_class_name("stream-btn")

    for option_button_confirmar in find_button_confirmar:
        if "Sí" in option_button_confirmar.text:
            logger.info("----- UPLOAD MS: Quitando el acceso a toda la empresa ---")
            print("----- UPLOAD MS: Quitando el acceso a toda la empresa ---")
            option_button_confirmar.click()

    time.sleep(25)
    
    dropdown = driver.find_element_by_name("dropdown")
    dropdown.click()

    logger.info("----- UPLOAD MS: Agregando canal de video -----")
    print("----- UPLOAD MS: Agregando canal de video -----")
    canal_option = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/video-permissions/div/div/principal-group-search/div/div[1]/drop-down/div/div/div[2]/div[2]")
    # hover = ActionChains(driver).move_to_element(canal_option)
    # hover.perform
    canal_option.click()
    time.sleep(20)

    # nombre_canal = driver.find_element_by_xpath("//*[
    # @id='principal-group-search-2af54823-bcde-d4b9-8e52-9f408abc2c33']")
    nombre_canal = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/video-permissions/div/div/principal-group-search/div/div[1]/form/div/input")
    nombre_canal.send_keys(canal_name)
    nombre_canal.send_keys(Keys.ENTER)
    time.sleep(20)

    # del div contenedor de la lista de canales, si listan todos los elementos div de este
    lista_canales = driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/video-permissions/div/div/principal-group-search/div/div[2]/div/div")
    count = 0
    for option in lista_canales:
        if count == 1:
            option.click()

        count += 1
        time.sleep(5)

    time.sleep(20)

    logger.info("----- UPLOAD MS: Publicando video -----")
    print("----- UPLOAD MS: Publicando video -----")
    # Progress bar status
    progress_status = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/div/div[1]/div[1]/div/span")
    progress_status_text = progress_status.text
    logger.info("----- UPLOAD MS: Progreso: "+progress_status_text+" -----")
    print("----- UPLOAD MS: Progreso: "+progress_status_text+" -----")

    print("----- Progreso: "+progress_status_text+" -----")

    logger.info("----- UPLOAD MS: Wait... -----")
    print("----- UPLOAD MS: Wait... -----")
    locator = (By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/div/div[1]/div[1]/div/span")
    WebDriverWait(driver, 300, 5).until(
        EC.text_to_be_present_in_element(locator, "El procesamiento se ha completado"))

    progress_status = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/div/div[1]/div[1]/div/span")
    progress_status_text = progress_status.text
    logger.info("----- UPLOAD MS: Progreso: " + progress_status_text + " -----")
    print("----- UPLOAD MS: Progreso: " + progress_status_text + " -----")

    time.sleep(10)

    # 5. Link para compartir
    logger.info("----- UPLOAD MS: Buscando Link del video -----")
    print("----- UPLOAD MS: Progreso: Buscando Link del video -----")

    compartir = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/div/button[1]")
    compartir.click()

    compartir_dialog = driver.find_element_by_class_name("video-share-embed-dialog")
    find_input = compartir_dialog.find_elements_by_tag_name("input")

    count_compartir = 0
    link_compartir = ""
    for option_input in find_input:
        if count_compartir == 2:
            link_compartir = option_input.get_attribute("value")

        count_compartir += 1
        time.sleep(8)

    time.sleep(10)
    # find_button_close_dialog = compartir_dialog.find_element_by_class_name("stream-btn")
    # find_button_close_dialog.click()
    find_div_footer_dialog = compartir_dialog.find_element_by_class_name("dialog-footer")
    find_button_close_dialog = find_div_footer_dialog.find_element_by_tag_name("button")
    find_button_close_dialog.click()

    logger.info("----- UPLOAD MS: Link del video: "+link_compartir)
    print("----- UPLOAD MS: Link del video: "+link_compartir)
    time.sleep(10)

    # 6. Publicar
    logger.info("----- UPLOAD MS: Publicando -----")
    print("----- UPLOAD MS: Publicando -----")

    publicar_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/section/div[1]/div/button[2]")
    publicar_button.click()
    time.sleep(10)

    logger.info("----- UPLOAD MS: Proceso Finalizado, Video cargado correctamente -----")
    print("----- UPLOAD MS: Proceso Finalizado, Video cargado correctamente -----")

    return link_compartir

# video_path = "D:/Videos/pendingUpload/2020-09-11 00-10-27.mp4"
# video_desc = "DESC. AUTOMATICA"
# canal_name = "Canal de Prueba"


# upload_record_video("D:/Videos/pendingUpload/2020-09-27 21-20-24.mp4", "DESC. AUTOMATICA", "Colaco4-Cermaq", "inbox@azurtech.cl", "Yod38776")
