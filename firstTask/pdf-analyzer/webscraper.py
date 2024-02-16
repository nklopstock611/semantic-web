import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

download_folder = "..."

chrome_options = Options()
prefs = {"download.default_directory": download_folder,
         "download.prompt_for_download": False,
         "safebrowsing.disable_download_protection": True,
         "download.directory_upgrade": True}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--safebrowsing-disable-download-protection")
chrome_options.add_argument("--disable-features=SafeBrowsing")

service = Service(executable_path='.../chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('http://localhost:8070')

# 1. Click en "TEI"
# Espera hasta que el enlace "TEI" esté presente
link = WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.LINK_TEXT, "TEI"))
)
link.click()

# 2. Seleccionar "processHeaderDocument" en el select
# Espera hasta que el elemento <select> esté presente
select_element = WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.ID, 'selectedService'))
)
select = Select(select_element)
select.select_by_value('processHeaderDocument')

# 3. Cargar un archivo PDF
# Espera hasta que el input esté presente
input_element = WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.ID, 'input'))
)
file_path = '...'
input_element.send_keys(file_path)

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

time.sleep(120)
driver.quit()
