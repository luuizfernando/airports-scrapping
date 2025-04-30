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

payload_capturado = None

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
                        payload_capturado = payload_json
                        break  # Sai do loop após capturar o payload
                    except json.JSONDecodeError as e:
                        print(f"Erro ao converter payload para JSON: {e}")
                else:
                    print("\n[AVISO] Não foi encontrado payload na requisição")
    except Exception as e:
        continue

if payload_capturado is None:
    print("\n[ERRO] Não foi possível capturar o payload da requisição")
    driver.quit()
    exit(1)

# ===== Fazendo a requisição à API ====
print("\n[INFO] Fazendo requisição à API...")

headers = {
    "Content-Type": "application/json",
    "Origin": "https://www.turkishairlines.com",
    "Referer": "https://www.turkishairlines.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

# Configurando a sessão com retry
session = requests.Session()
retry = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('https://', retry)

try:
    response = session.post(
        target_url,
        json=payload_capturado,
        headers=headers,
        timeout=30
    )

    if response.status_code == 200:
        try:
            content_type = response.headers.get("Content-Type", "")
            print(f"\n[DEBUG] Content-Type: {content_type}")
            
            if "application/json" in content_type:
                try:
                    # Tenta carregar diretamente como JSON
                    data = json.loads(response.content.decode("utf-8"))
                except Exception as e:
                    print("[ERRO] Falha ao decodificar JSON:", e)
                    print("Tentando descompactar com gzip...")

                    import gzip
                    from io import BytesIO
                    try:
                        decompressed = gzip.GzipFile(fileobj=BytesIO(response.content)).read()
                        data = json.loads(decompressed.decode("utf-8"))
                    except Exception as gz_e:
                        print("[ERRO] Também falhou ao descompactar com gzip:", gz_e)
                        print("\nResposta bruta:")
                        print(response.content[:500])
                        driver.quit()
                        exit(1)
            else:
                print("[ERRO] A resposta não é JSON.")
                print(response.text[:500])
                driver.quit()
                exit(1)
        except Exception as e:
            print(f"[ERRO] Falha inesperada ao processar resposta: {e}")
            driver.quit()
            exit(1)

        print("\n[INFO] Resposta da API:")
        print(json.dumps(data, indent=2)[:1000])
        
        # Processando os dados de preços
        if 'data' in data and 'dailyPriceList' in data['data']:
            print("\n[INFO] Lista de preços diários:")
            for price in data['data']['dailyPriceList']:
                date = price.get('date', 'N/A')
                currency = price.get('price', {}).get('currencySign', '')
                amount = price.get('price', {}).get('amount', 0)
                print(f"Data: {date}, Preço: {currency}{amount:.2f}")
        else:
            print("\n[AVISO] Dados de preços diários não encontrados na resposta")
    else:
        print(f"[ERRO] Status code {response.status_code}")
        print(response.text)
except requests.exceptions.RequestException as e:
    print(f"[ERRO] Falha na requisição: {e}")
    driver.quit()
    exit(1)

time.sleep(6000)