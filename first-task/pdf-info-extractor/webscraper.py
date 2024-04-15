# ====================================== #
# WE DO NOT USE THIS FILE! IT WAS PART OF
# THE STARTING TEST-PHASE OF THE PROJECT.
# WE LEFT IT HERE TO SHOW OUR PROCESS.
# ====================================== #

import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

download_folder = "C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/downloads/"

chrome_options = Options()
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--safebrowsing-disable-download-protection")
chrome_options.add_argument("--disable-features=SafeBrowsing")

service = Service(executable_path='C:/Users/nklop/Driver/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

def find_tei():
    # 1. Click en "TEI"
    # Espera hasta que el enlace "TEI" esté presente
    link = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.LINK_TEXT, "TEI"))
    )
    link.click()

def select_service(service_name: str):
    # 2. Seleccionar "processHeaderDocument" en el select
    # Espera hasta que el elemento <select> esté presente
    select_element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'selectedService'))
    )
    select = Select(select_element)
    select.select_by_value(service_name) # 'processHeaderDocument' o 'processReferences'

def download_xml(file_path: str):
    # 3. Cargar un archivo PDF
    # Espera hasta que el input esté presente
    input_element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'input'))
    )
    input_element.send_keys(file_path)
    # 'C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/pdfs/SSDBM09_PTS.pdf'

    # 4. Click en "Submit"
    # Espera hasta que el botón "Submit" esté presente
    submit_button = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'submitRequest'))
    )
    submit_button.click()

    # 5. Descargar el archivo XML
    # Esperar a que el botón "Download" esté presente
    btn_download = WebDriverWait(driver, 200).until(
        EC.visibility_of_element_located((By.ID, 'btn_download'))
    )    
    btn_download.click()
    time.sleep(1)
    pyautogui.press('enter') # Presionar la tecla "Enter" para descargar el archivo en Descargas

if __name__ == "__main__":
    driver.get('http://localhost:8070')
    find_tei()
    select_service('processHeaderDocument')
    # toca iterar por cada archivo
    # tener un diccionario o alguna estructura que contenga el nombre del archivo y se pone en el parámetro
    download_xml('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/pdfs/SSDBM09_PTS.pdf')
    
    select_service('processReferences')
    # toca iterar por cada archivo
    # tener un diccionario o alguna estructura que contenga el nombre del archivo y se pone en el parámetro
    download_xml('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/pdfs/SSDBM09_PTS.pdf')

    time.sleep(120)
    driver.quit()
