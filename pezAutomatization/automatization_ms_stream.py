import json
import time
import logging

from selenium.webdriver.common.action_chains import ActionChains
from pezTech.settings import BASE_DIR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

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

    driver = get_driver_config(so, web_driver_name, modality_automatization_web)
    driver.get(url_upload)
    time.sleep(15)

    logger.info("----- UPLOAD MS: Realizando Login en MS Stream -----")
    logger.info("----- UPLOAD MS: Email: " + email_stream + " -----")

    print("----- UPLOAD MS: Realizando Login en MS Stream -----")
    print("----- UPLOAD MS: Email: " + email_stream + " -----")
    # 1. se ingresan los datos para iniciar sesion
    delay = 600  # seconds

    while True:
        try:
            # WebDriverWait(driver, delay).until(EC.presence_of_element_located(driver.find_element_by_id("i0118")))
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'i0116')))
            logger.info("----- UPLOAD MS: usuario is ready! -----")
            print("----- UPLOAD MS: usuario is ready! -----")

            time.sleep(3)
            user_form = driver.find_element_by_id("i0116")
            user_form.send_keys(email_stream)
            user_form.send_keys(Keys.ENTER)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: usuario too much time!-Try again -----")
            print("----- UPLOAD MS: usuario too much time!-Try again -----")

    time.sleep(3)

    while True:
        try:
            # WebDriverWait(driver, delay).until(EC.presence_of_element_located(driver.find_element_by_id("i0118")))
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'i0118')))
            logger.info("----- UPLOAD MS: password is ready! -----")
            print("----- UPLOAD MS: password is ready! -----")

            time.sleep(3)
            password_form = driver.find_element_by_id("i0118")
            password_form.send_keys(password_stream)
            password_form.send_keys(Keys.ENTER)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: password too much time!-Try again -----")
            print("----- UPLOAD MS: password too much time!-Try again -----")

    time.sleep(3)
    # time.sleep(10)

    logger.info("----- UPLOAD MS: Sesion Iniciada -----")
    print("----- UPLOAD MS: Sesion Iniciada -----")

    # 1.1 click en boton para no mantener la sesion iniciada
    while True:
        try:
            WebDriverWait(driver, delay).until(
                # EC.presence_of_element_located(driver.find_element_by_id("idBtn_Back")))
                EC.presence_of_element_located((By.ID, 'idBtn_Back')))
            logger.info("----- UPLOAD MS: mantener sesion is ready! -----")
            print("----- UPLOAD MS: mantener sesion is ready! -----")

            time.sleep(3)
            mantener_sesion = driver.find_element_by_id("idBtn_Back")
            mantener_sesion.send_keys(Keys.ENTER)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: mantener sesion much time!-Try again -----")
            print("----- UPLOAD MS: mantener sesion much time!-Try again -----")

    # time.sleep(30)
    """logger.info("----- UPLOAD MS: Creando Evento MS Stream -----")
    print("----- UPLOAD MS: Creando Evento MS Stream -----")
    # 2. click en boton Crear
    navigation = driver.find_element_by_id("create-desktop-navigation")
    navigation.click()
    time.sleep(10)

    logger.info("----- UPLOAD MS: Cargando video desde los archivos locales -----")
    print("----- UPLOAD MS: Cargando video desde los archivos locales -----")
    # 3. click en Cargar Video
    cargar_video = driver.find_element_by_xpath("/html/body/div[1]/top-nav/topbar/div/div/div/div[1]/nav/ul/li[4]/
    div/ul/li[1]")
    cargar_video.click()
    time.sleep(15)"""

    time.sleep(3)

    # 4. examinar video
    while True:
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'c-hyperlink')))
            logger.info("----- UPLOAD MS: cargar archivo is ready! -----")
            print("----- UPLOAD MS: cargar archivo is ready! -----")

            time.sleep(3)
            elm = driver.find_element_by_xpath("//input[@type='file']")
            elm.send_keys(video_path)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: cargar archivo much time!-Try again -----")
            print("----- UPLOAD MS: cargar archivo much time!-Try again -----")

    time.sleep(3)
    # time.sleep(30)

    logger.info("----- UPLOAD MS: Agregando Descripcion de video y permisos -----")
    print("----- UPLOAD MS: Agregando Descripcion de video y permisos -----")
    # 4.1 descripcion del video

    while True:
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.NAME, "uploaddescription")))
            logger.info("----- UPLOAD MS: description is ready! -----")
            print("----- UPLOAD MS: description is ready! -----")

            time.sleep(3)
            description = driver.find_element_by_name("uploaddescription")
            description.send_keys(video_desc)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: description much time!-Try again -----")
            print("----- UPLOAD MS: description much time!-Try again -----")

    # time.sleep(20)
    time.sleep(3)

    logger.info("----- UPLOAD MS: Quitando permisos para toda la empresa -----")
    print("----- UPLOAD MS: Quitando permisos para toda la empresa -----")

    # 4.2 permisos
    while True:
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((
                    By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/"
                              "video-edit/section/div[1]/v-accordion/v-pane[2]")))
            logger.info("----- UPLOAD MS: sub menu permisos is ready! -----")
            print("----- UPLOAD MS: sub menu permisos is ready! -----")

            time.sleep(3)
            perm = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/"
                "section/div[1]/v-accordion/v-pane[2]")
            perm.click()

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: sub menu permisos much time!-Try again -----")
            print("----- UPLOAD MS: sub menu permisos much time!-Try again -----")

    # time.sleep(15)
    time.sleep(3)

    # 4.3 destickear permisos para toda la empresa
    while True:
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((
                    By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/"
                              "video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/"
                              "video-edit-permissions-pane/div/div/label/span")))
            logger.info("----- UPLOAD MS: permisos empresa is ready! -----")
            print("----- UPLOAD MS: permisos empresa is ready! -----")

            time.sleep(3)
            perm_empresa = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/"
                "section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/div/"
                "label/span")
            perm_empresa.click()

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: permisos empresa much time!-Try again -----")
            print("----- permisos empresa much time!-Try again -----")

    # time.sleep(15)
    time.sleep(3)

    # Confirmar la eliminacion de permisos
    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "confirmation-dialog")))
            logger.info("----- UPLOAD MS: confirmar eliminacion de permisos para empresa is ready! -----")
            print("----- UPLOAD MS: confirmar eliminacion de permisos para empresa is ready!  -----")

            time.sleep(3)
            confirmar_dialog = driver.find_element_by_class_name("confirmation-dialog")
            find_button_confirmar = confirmar_dialog.find_elements_by_class_name("stream-btn")

            for option_button_confirmar in find_button_confirmar:
                if "Sí" in option_button_confirmar.text:
                    logger.info("----- UPLOAD MS: Quitando el acceso a toda la empresa ---")
                    print("----- UPLOAD MS: Quitando el acceso a toda la empresa ---")
                    option_button_confirmar.click()

            break
        except TimeoutException:
            logger.info("----- UPLOAD MS: permisos empresa much time!-Try again -----")
            print("----- UPLOAD MS: permisos empresa much time!-Try again -----")

    # time.sleep(25)
    time.sleep(3)

    logger.info("----- UPLOAD MS: Agregando canal de video -----")
    print("----- UPLOAD MS: Agregando canal de video -----")

    # Agregando canal
    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, "dropdown")))
            logger.info("----- UPLOAD MS: seleccionando compartir con canales is ready! -----")
            print("----- UPLOAD MS: seleccionando compartir con canales is ready! -----")

            time.sleep(3)
            dropdown = driver.find_element_by_name("dropdown")
            # driver.execute_script("arguments[0].click();", dropdown)
            # dropdown.click()
            ActionChains(driver).move_to_element(dropdown).click(dropdown).perform()

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: seleccionando compartir con canales much time!-Try again -----")
            print("----- UPLOAD MS: seleccionando compartir con canales much time!-Try again -----")

    time.sleep(3)

    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.CLASS_NAME, "drop-down-list-container")))
            logger.info("----- UPLOAD MS: seleccionando opcion canales is ready! -----")
            print("----- UPLOAD MS: seleccionando opcion canales is ready! -----")

            time.sleep(3)
            listado_opciones = dropdown.find_element_by_class_name("drop-down-list-container")
            find_opcion_compartir_con = listado_opciones.find_elements_by_tag_name("div")

            for compartir_con in find_opcion_compartir_con:
                find_text_opcion_compartir_con = compartir_con.find_element_by_tag_name("span").text
                if "Canales" in find_text_opcion_compartir_con:
                    compartir_con.click()

                time.sleep(3)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: seleccionando compartir con canales much time!-Try again -----")
            print("----- UPLOAD MS: seleccionando compartir con canales much time!-Try again -----")

    time.sleep(3)

    """while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/"
                          "video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/"
                          "video-edit-permissions-pane/div/video-permissions/div/div/principal-group-search/div/div[1]/"
                          "drop-down/div/div/div[2]/div[2]")))
            logger.info("----- UPLOAD MS: seleccionando compartir con canales is ready! -----")
            print("----- UPLOAD MS: seleccionando compartir con canales is ready! -----")

            canal_option = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/"
                "section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/"
                "video-permissions/div/div/principal-group-search/div/div[1]/drop-down/div/div/div[2]/div[2]")
            # ActionChains(driver).move_to_element(canal_option).perform()
            canal_option.click()

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: seleccionando compartir con canales much time!-Try again -----")
            print("----- UPLOAD MS: seleccionando compartir con canales much time!-Try again -----")

    # time.sleep(20)
    time.sleep(3)"""

    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/"
                          "video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/"
                          "video-edit-permissions-pane/div/video-permissions/div/div/principal-group-search/div/"
                          "div[1]/form/div/input")))
            logger.info("----- UPLOAD MS: buscando canal is ready! -----")
            print("----- UPLOAD MS: buscando canal is ready! -----")

            time.sleep(3)
            nombre_canal = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/"
                "section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/"
                "video-permissions/div/div/principal-group-search/div/div[1]/form/div/input")
            nombre_canal.send_keys(canal_name)
            nombre_canal.send_keys(Keys.ENTER)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: buscando canal much time!-Try again -----")
            print("----- UPLOAD MS: buscando canal much time!-Try again -----")

    # time.sleep(20)
    time.sleep(3)

    # del div contenedor de la lista de canales, si listan todos los elementos div de este
    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/"
                          "video-edit/section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/"
                          "video-edit-permissions-pane/div/video-permissions/div/div/principal-group-search/div/"
                          "div[2]/div/div")))
            logger.info("----- UPLOAD MS: listado de canales is ready! -----")
            print("----- UPLOAD MS: listado de canales is ready! -----")

            time.sleep(3)
            lista_canales = driver.find_elements_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/"
                "section/div[1]/v-accordion/v-pane[2]/v-pane-content/div/video-edit-permissions-pane/div/"
                "video-permissions/div/div/principal-group-search/div/div[2]/div/div")

            count = 0
            for option in lista_canales:
                if count == 1:
                    option.click()

                count += 1
                time.sleep(5)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: listado de canales much time! -Try again -----")
            print("----- UPLOAD MS: listado de canales much time! -Try again -----")

    # time.sleep(20)
    time.sleep(3)

    logger.info("----- UPLOAD MS: Publicando video -----")
    print("----- UPLOAD MS: Publicando video -----")
    # Progress bar status
    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/div/"
                          "div[1]/div[1]/div/span")))
            logger.info("----- UPLOAD MS: progress bar is ready! -----")
            print("----- UPLOAD MS: progress bar is ready! -----")

            time.sleep(3)
            progress_status = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/div/div[1]/"
                "div[1]/div/span")
            progress_status_text = progress_status.text

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: progress bar much time! -Try again -----")
            print("----- UPLOAD MS: progress bar much time! -Try again -----")

    time.sleep(3)

    logger.info("----- UPLOAD MS: Progreso: " + progress_status_text + " -----")
    print("----- UPLOAD MS: Progreso: " + progress_status_text + " -----")

    logger.info("----- UPLOAD MS: Wait, esperando que termine de cargar el video... -----")
    print("----- UPLOAD MS: Wait, esperando que termine de cargar el video... -----")

    locator = (By.XPATH,
               "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/div/div[1]/"
               "div[1]/div/span")

    while True:
        try:
            """WebDriverWait(driver, 300, 5).until(
                EC.text_to_be_present_in_element(locator, "El procesamiento se ha completado"))"""

            WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element(
                locator, "El procesamiento se ha completado"))

            logger.info("----- UPLOAD MS:El procesamiento se ha completado is ready! -----")
            print("----- UPLOAD MS: El procesamiento se ha completado is ready! -----")

            break
        except TimeoutException:
            logger.info("----- UPLOAD MS: El procesamiento se ha completado much time! -Try again -----")
            print("----- UPLOAD MS: El procesamiento se ha completado much time! -Try again  -----")

    time.sleep(3)

    # progreso actualizado
    progress_status = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/div/div[1]/div[1]/"
        "div/span")
    progress_status_text = progress_status.text

    logger.info("----- UPLOAD MS: Progreso: " + progress_status_text + " -----")
    print("----- UPLOAD MS: Progreso: " + progress_status_text + " -----")

    time.sleep(3)

    # 5. Link para compartir
    logger.info("----- UPLOAD MS: Compartir: Buscando Link del video -----")
    print("----- UPLOAD MS: Compartir: Buscando Link del video -----")

    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/"
                          "video-edit/section/div[1]/div/button[1]")))
            logger.info("----- UPLOAD MS: compartir dialog is ready! -----")
            print("----- UPLOAD MS: compartir dialog is ready! -----")

            time.sleep(3)
            compartir = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/"
                "section/div[1]/div/button[1]")
            compartir.click()

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: compartir dialog much time! -Try again -----")
            print("----- UPLOAD MS: compartir dialog much time! -Try again  -----")

    time.sleep(3)

    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.CLASS_NAME, "video-share-embed-dialog")))
            logger.info("----- UPLOAD MS: compartir dialog form is ready! -----")
            print("----- UPLOAD MS: compartir dialog form is ready! -----")

            time.sleep(3)
            compartir_dialog = driver.find_element_by_class_name("video-share-embed-dialog")
            find_input = compartir_dialog.find_elements_by_tag_name("input")

            count_compartir = 0
            link_compartir = ""
            for option_input in find_input:
                if count_compartir == 2:
                    link_compartir = option_input.get_attribute("value")

                count_compartir += 1
                time.sleep(8)

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: compartir dialog form much time! -Try again -----")
            print("----- UPLOAD MS: compartir dialog form much time! -Try again -----")

    # time.sleep(10)
    time.sleep(3)

    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.CLASS_NAME, "dialog-footer")))
            logger.info("----- UPLOAD MS: dialog-footer is ready! -----")
            print("----- UPLOAD MS: dialog-footer is ready! -----")

            time.sleep(3)
            find_div_footer_dialog = compartir_dialog.find_element_by_class_name("dialog-footer")

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: dialog-footer much time! -Try again -----")
            print("----- UPLOAD MS: dialog-footer much time! -Try again -----")

    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.TAG_NAME, "button")))
            logger.info("----- UPLOAD MS: dialog-footer tag is ready! -----")
            print("----- UPLOAD MS: dialog-footer tag is ready! -----")

            time.sleep(3)
            find_button_close_dialog = find_div_footer_dialog.find_element_by_tag_name("button")
            find_button_close_dialog.click()

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: dialog-footer tag  much time! -Try again -----")
            print("----- UPLOAD MS: dialog-footer tag  much time! -Try again -----")

    time.sleep(3)

    logger.info("----- UPLOAD MS: Link del video: " + link_compartir)
    print("----- UPLOAD MS: Link del video: " + link_compartir)
    # time.sleep(10)
    time.sleep(3)

    # 6. Publicar
    logger.info("----- UPLOAD MS: Publicando -----")
    print("----- UPLOAD MS: Publicando -----")

    while True:
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/"
                          "video-edit/section/div[1]/div/button[2]")))
            logger.info("----- UPLOAD MS: boton publicar is ready!  -----")
            print("----- UPLOAD MS: boton publicar is ready! -----")

            time.sleep(3)
            publicar_button = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/upload-video/div/div/div[2]/div/upload-detail/section/div/video-edit/"
                "section/div[1]/div/button[2]")
            publicar_button.click()

            break  # se romperá del bucle una vez que el elemento específico esté presente.
        except TimeoutException:
            logger.info("----- UPLOAD MS: boton publicar much time! -Try again -----")
            print("----- UPLOAD MS: boton publicar much time! -Try again -----")

    # time.sleep(10)
    time.sleep(3)

    logger.info("----- UPLOAD MS: Proceso Finalizado, Video cargado correctamente -----")
    print("----- UPLOAD MS: Proceso Finalizado, Video cargado correctamente -----")

    return link_compartir


def get_driver_config(so, web_driver_name, modality_automatization_web):

    if so == "Linux":
        logger.info("----- UPLOAD MS: S.O. es Linux -----")
        print("----- UPLOAD MS: S.O. es Linux -----")
        web_driver_path = '/usr/lib/chromium-browser/chromedriver'
    else:
        web_driver_path = BASE_DIR + "/dchrome/" + web_driver_name

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
            driver = webdriver.Chrome(executable_path=r"" + web_driver_path)
    else:
        logger.info("----- UPLOAD MS: Lanzando WebDriver modalidad 2do plano. -----")
        print("----- UPLOAD MS: Lanzando WebDriver modalidad 2do plano. -----")

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        if so == "Linux":
            # https://ivanderevianko.com/2020/01/selenium-chromedriver-for-raspberrypi
            print("----- UPLOAD MS: S.O. es Linux -----")
            # chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(web_driver_path, chrome_options=chrome_options)
        else:
            print("----- UPLOAD MS: S.O. NO es Linux -----")
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"" + web_driver_path)

    return driver


# video_path = "D:/Videos/pendingUpload/2020-09-11 00-10-27.mp4"
# video_desc = "DESC. AUTOMATICA"
# canal_name = "Canal de Prueba"


"""upload_record_video(
    "D:/Videos/pendingUpload/2020-09-27 21-20-24.mp4",
    "DESC. AUTOMATICA",
    "Colaco4-Cermaq",
    "peztech@azurtech.cl",
    "Yod38776")"""