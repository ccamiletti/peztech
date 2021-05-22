import json
import time
import datetime
import pytz

from pezTech.settings import BASE_DIR
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def delete_video_ms_stream(dias_tope_almacenamiento_ms, email_ms, password_ms):
    # paths y configuraciones
    print("----- Entrando en delete video ms stream -----")
    print("----- delete_video_ms_stream: Leyendo JSON de configuraciones -----")

    json_properties = BASE_DIR + "/static/properties.json"
    with open(json_properties, 'r') as file:
        data_prop = json.load(file)
        url_upload = data_prop['urlToUploadRecordingStream']
        web_driver_name = data_prop['webDriverName']
        so = data_prop['so']
        modality_automatization_web = data_prop['modalityAutomatizationWeb']

    if so == "Linux":
        print("----- S.O. es Linux -----")
        web_driver_path = '/usr/lib/chromium-browser/chromedriver'
    else:
        web_driver_path = BASE_DIR + "/dchrome/"+web_driver_name

    print("----- web_driver_path: " + web_driver_path + " -----")

    if modality_automatization_web == "web":
        print("----- Lanzando WebDriver modalidad WEB -----")

        if so == "Linux":
            print("----- S.O. es Linux -----")
            driver = webdriver.Chrome(executable_path=web_driver_path)
        else:
            print("----- S.O. NO es Linux -----")
            driver = webdriver.Chrome(executable_path=r""+web_driver_path)
    else:
        print("----- Lanzando WebDriver modalidad 2do plano. -----")

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        if so == "Linux":
            print("----- S.O. es Linux -----")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(web_driver_path, chrome_options=chrome_options)
        else:
            print("----- S.O. NO es Linux -----")
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"" + web_driver_path)

    driver.get(url_upload)
    time.sleep(10)

    print("----- Realizando Login en MS Stream -----")
    # 1. se ingresan los datos para iniciar sesion
    user_form = driver.find_element_by_id("i0116")
    user_form.send_keys(email_ms)
    user_form.send_keys(Keys.ENTER)
    time.sleep(10)

    password_form = driver.find_element_by_id("i0118")
    password_form.send_keys(password_ms)
    password_form.send_keys(Keys.ENTER)
    time.sleep(10)
    print("----- Sesion Iniciada -----")

    # 1.1 click en boton para no mantener la sesion iniciada
    mantener_sesion = driver.find_element_by_id("idBtn_Back")
    mantener_sesion.send_keys(Keys.ENTER)
    time.sleep(10)

    print("----- Entrando en mi contenido MS Stream -----")
    # 2. click en boton "Mi contenido"
    navigation = driver.find_element_by_id("topbar-mycontent-navigation-button-desktop")
    navigation.click()
    time.sleep(10)

    print("----- Listando videos -----")
    # 3. click en Videos
    videos = driver.find_element_by_xpath("/html/body/div[1]/top-nav/topbar/div/div/div/div[1]/nav/ul/li[3]/div/ul/li[1]/a")
    videos.click()
    time.sleep(10)

    # 4. listado de videos
    lista_videos = driver.find_elements_by_class_name("list-item")
    count = 1

    now_cl = datetime.datetime.now(pytz.timezone('America/Santiago'))
    now_cl_format = now_cl.strftime('%Y-%m-%d %H:%M:%S')
    now_date = datetime.datetime.strptime(now_cl_format, '%Y-%m-%d %H:%M:%S')
    print("----- Fecha actual: " + str(now_date) + " -----")

    for option in lista_videos:
        video_tittle = option.find_element_by_class_name("video-title").text
        print("----- Nombre del video: " + video_tittle + " -----")

        video_date = option.find_element_by_class_name("uploaded-date-column").text
        video_date_format = datetime.datetime.strptime(video_date, '%d-%m-%Y')
        print("----- Fecha del video: " + str(video_date_format) + "-----")

        days_diff = (now_date - video_date_format).days
        print("----- Dias de diferencia: " + str(days_diff) + " -----")

        if days_diff >= dias_tope_almacenamiento_ms:
            print("----- Video pasado, se debe borrar -----")
            # clickeando = option.find_element_by_xpath("/html/body/div[1]/div/div[2]/studio-page/div/section/div/div/studio-video-results/video-results/div[2]/items-list/div/div[1]/div["+str(count)+"]/item/item/video-item/div/list-row/ng-transclude/list-cell[5]/div/div/ng-transclude/div/flex-drawer/div/div/span[1]/button")
            option_button_path = "/html/body/div[1]/div/div[2]/studio-page/div/section/div/div/studio-video-results/video-results/div[2]/items-list/div/div[1]/div[" + str(
                count) + "]/item/item/video-item/div/list-row/ng-transclude/list-cell[5]/div/div/ng-transclude/div/flex-drawer/div/div/span[1]/button"
            # print(option_button_path)

            option_button = option.find_element_by_xpath(option_button_path)
            # print("Clickeando")
            driver.execute_script("arguments[0].click();", option_button)
            time.sleep(10)

            delete_button_path = "/html/body/div[1]/div/div[2]/studio-page/div/section/div/div/studio-video-results/video-results/div[2]/items-list/div/div[1]/div[" + str(
                count) + "]/item/item/video-item/div/list-row/ng-transclude/list-cell[5]/div/div/ng-transclude/div/flex-drawer/div/div/ul/li[3]/button"
            delete_button = option.find_element_by_xpath(delete_button_path)
            driver.execute_script("arguments[0].click();", delete_button)
            time.sleep(10)

            # delete_button.send_keys(Keys.ENTER)
            dialog = driver.find_element_by_class_name("confirmation-dialog")
            find_button = dialog.find_elements_by_class_name("stream-btn")

            for option_button in find_button:
                if "Eliminar" in option_button.text:
                    print("----- Eliminando Video... ---")
                    option_button.click()

            time.sleep(10)

            # print("Desclickeando")
            # driver.execute_script("arguments[0].click();", option_button)
        else:
            print("----- No es necesario borrar el video -----")

        time.sleep(10)
        count += 1

    print("----- Proceso Finalizado -----")
    return "success"

# delete_video_ms_stream(1, "inbox@azurtech.cl", "Yod38776")
