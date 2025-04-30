from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests

# ===== Selenium Setup =====
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options = Options()
options.add_experimental_option('prefs', {
    'intl.accept_languages': 'en,en_US'
})

# Habilitando o Network do DevTools
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# Iniciando o driver
driver = webdriver.Chrome(options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
    """
})

driver.maximize_window()
driver.get("https://www.turkishairlines.com/")

# ===== Aceita cookies =====
try:
    cookie_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "allowCookiesButton"))
    )
    cookie_btn.click()
    print("Cookies aceitos com sucesso.")
except Exception as e:
    print("Botão de cookies não encontrado ou erro ao clicar:", e)

# ===== Interagindo com o formulário =====
travel = driver.find_element(By.ID, 'one-way')
travel.click()

# ===== Preenche origem =====
try:
    origin_input = driver.find_element(By.ID, 'fromPort')
    time.sleep(1)
    origin_input.send_keys(Keys.CONTROL, "a")
    time.sleep(1)
    origin_input.send_keys(Keys.BACKSPACE)
    time.sleep(1)
    origin_input = driver.find_element(By.ID, 'fromPort')
    origin_input.send_keys("São Paulo")
    time.sleep(1)
    origin = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
    origin.click()
except Exception as e:
    print("Erro ao preencher origem:", e)

# ===== Preenche destino =====
try:
    origin_input = driver.find_element(By.ID, 'toPort')
    origin_input.send_keys(Keys.CONTROL, "a")
    origin_input.send_keys(Keys.BACKSPACE)
    origin_input = driver.find_element(By.ID, 'toPort')
    origin_input.send_keys("Kabul")
    time.sleep(1)
    origin = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
    origin.click()
except Exception as e:
    print("Erro ao preencher destino:", e)

# ===== Preenche data =====
try:
    date = driver.find_element(By.XPATH, "//abbr[@aria-label='May 20, 2025']/ancestor::button")
    date.click()
    print("Data selecionada.")
except Exception as e:
    print("Erro ao selecionar data:", e)

# ===== Número de passageiros =====
try:
    passengers = driver.find_element(By.ID, 'bookerFlightPaxpicker')
    passengers.click()
    time.sleep(.5)
    # == Adults ==
    add_adult = driver.find_element(By.ID, 'bookerFlightPaxPickerPlusAdult')
    add_adult.click()
    time.sleep(.5)
    # == Child ==
    add_child = driver.find_element(By.ID, 'bookerFlightPaxPickerPlusChild')
    add_child.click()
    time.sleep(.5)
    # == Infant ==
    add_infant = driver.find_element(By.ID, 'bookerFlightPaxPickerPlusInfant')
    add_infant.click()
    time.sleep(.5)
    print("Passageiros inclusos")
except Exception as e:
    print("Erro ao selecionar passageiros:", e)

# === Confirmando os dados e procura os voos ===
try: 
    confirmation_button = driver.find_element(By.CLASS_NAME, 'hm__RoundAndOneWayTab_buttonWrapper__v15PI')
    confirmation_button.click()
    print("Confirmação efetuada")
except Exception as e:
    print("Erro ao confirmar dados:", e)

# === Percorrendo as opções de passagem ===
# == Ver itinerary details ==
time.sleep(30)
itinerary = driver.find_element(By.CLASS_NAME, 'av__style_flight-detail-title___37OQ')
itinerary.click()
try:
    div = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'av__style_segments__kK9ax'))
    )
except Exception as e:
    print("Erro ao achar o elemento:", e)
# Pega todos os elementos filhos dentro da div
children = div.find_elements(By.XPATH, './*')
dados = []
for child in children:
    tag_name = child.tag_name
    texto = child.text
    dados.append({
        "tag": tag_name,
        "texto": texto
    })

# Converte para JSON
json_resultado = json.dumps(dados, ensure_ascii=False, indent=2)
print(json_resultado)

# == Selecionar categoria econômica ==
economy_btn = driver.find_element(By.CLASS_NAME, 'av__style_metro-radio__YF2_k')
economy_btn.click()