from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# ===== Selenium Setup =====
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

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
    origin_input.send_keys("Istanbul")
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

# ===== Capturando o Payload da Requisição ====
print("\n[INFO] Aguardando carregamento da página e requisições...")
time.sleep(10)

# Obtendo os logs de rede
logs = driver.get_log("performance")
target_url = "https://www.turkishairlines.com/api/v1/availability/cheapest-prices"

for entry in logs:
    try:
        log = json.loads(entry["message"])["message"]
        if "Network.requestWillBeSent" in log["method"]:
            request = log["params"]["request"]
            if request["url"] == target_url and request["method"] == "POST":
                print("\n[INFO] Requisição POST para API de preços encontrada!")
                print(f"URL: {request['url']}")
                
                # Obtendo o payload
                if "postData" in request:
                    payload = request["postData"]
                    print("Payload encontrado:")
                    print(payload)
                    
                    # Salvando o payload em um arquivo
                    with open('payload_preco.json', 'w', encoding='utf-8') as f:
                        f.write(payload)
                        print("\n[INFO] Payload salvo em 'payload_preco.json'")
                    
                    # Tentando converter para JSON
                    try:
                        payload_json = json.loads(payload)
                        print("Payload convertido em JSON:")
                        print(json.dumps(payload_json, indent=2))
                    except json.JSONDecodeError as e:
                        print(f"Erro ao converter payload para JSON: {e}")
                else:
                    print("\n[AVISO] Não foi encontrado payload na requisição")
    except Exception as e:
        continue

time.sleep(6000)