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
options = Options()
options.add_experimental_option('prefs', {
    'intl.accept_languages': 'en,en_US'
})

options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# ==== Driver initializer ====
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

# ===== Accept cookies =====
try:
    cookie_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "allowCookiesButton"))
    )
    cookie_btn.click()
    print("Cookies accepted.")
except Exception as e:
    print("Cookies button not found or error:", e)

# ===== Selecting One-Way option =====
travel = driver.find_element(By.ID, 'round-trip')
travel.click()

# ===== Departure input =====
try:
    departure_input = driver.find_element(By.ID, 'fromPort')
    time.sleep(1)
    departure_input.send_keys(Keys.CONTROL, "a")
    time.sleep(1)
    departure_input.send_keys(Keys.BACKSPACE)
    time.sleep(1)
    departure_input = driver.find_element(By.ID, 'fromPort')
    departure_input.send_keys("São Paulo")
    time.sleep(1)
    origin = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
    origin.click()
except Exception as e:
    print("Error in departure field:", e)

# ===== Destination input =====
try:
    destination_input = driver.find_element(By.ID, 'toPort')
    destination_input.send_keys(Keys.CONTROL, "a")
    destination_input.send_keys(Keys.BACKSPACE)
    destination_input = driver.find_element(By.ID, 'toPort')
    destination_input.send_keys("Kabul")
    time.sleep(1)
    destiny = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
    destiny.click()
except Exception as e:
    print("Error in destination field:", e)

# ===== Travel date =====
# === Departure date ===
try:
    date = driver.find_element(By.XPATH, "//abbr[@aria-label='May 20, 2025']/ancestor::button")
    date.click()
    print("Date selected.")
except Exception as e:
    print("Error in select date:", e)
# === Return date ===
try:
    date = driver.find_element(By.XPATH, "//abbr[@aria-label='May 30, 2025']/ancestor::button")
    date.click()
    print("Date selected.")
except Exception as e:
    print("Error in select date:", e)

# ===== Passangers number =====
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
    print("Passangers added.")
except Exception as e:
    print("Erro ao selecionar passageiros:", e)

# ==== Confirming data and searching flights ====
try: 
    confirmation_button = driver.find_element(By.CLASS_NAME, 'hm__RoundAndOneWayTab_buttonWrapper__v15PI')
    confirmation_button.click()
    print("Confirmation done.")
except Exception as e:
    print("Error in confirming data:", e)

# ===== Catching Payload Request ====
print("\n[INFO] Waiting for page loading and requests...")
time.sleep(10)

# ==== Getting flight data ====
# Encontra todos os blocos de itinerário
itinerary_blocks = driver.find_elements(By.CLASS_NAME, "av__style_details__6sbBo")

# Lista para armazenar todos os dados dos voos
all_flights_data = []

# Percorre cada bloco de itinerário
for block in itinerary_blocks:
    try:
        # Estrutura para armazenar os dados do voo atual
        flight_data = {
            "price": "",
            "departure_airport_info": {
                "airport": "",
                "time": "",
                "company": "",
                "flight_code": "",
            },
            "arrival_airport_info": {
                "airport": "",
                "time": "",
                "company": "",
                "flight_code": "",
            }
        }

        # Encontra os elementos dentro do bloco atual
        try:
            # Preço do voo
            price_element = block.find_element(By.CLASS_NAME, 'av__style_pricePart__lYxno')
            flight_data["price"] = price_element.text if price_element else "Preço não disponível"
        except Exception as e:
            print(f"Erro ao obter preço: {e}")

        # Informações de partida
        try:
            departure_info = block.find_element(By.CLASS_NAME, "av__style_departure__1XqQZ")
            flight_data["departure_airport_info"]["airport"] = departure_info.find_element(By.CLASS_NAME, "av__style_name__IDpLN").text
            flight_data["departure_airport_info"]["time"] = departure_info.find_element(By.CLASS_NAME, "av__style_date__zutq0").text
            flight_data["departure_airport_info"]["company"] = departure_info.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
            flight_data["departure_airport_info"]["flight_code"] = departure_info.find_element(By.CLASS_NAME, "av__style_flightNumber__1XqQZ").text
        except Exception as e:
            print(f"Erro ao obter informações de partida: {e}")

        # Informações de chegada
        try:
            arrival_info = block.find_element(By.CLASS_NAME, "av__style_arrival__1XqQZ")
            flight_data["arrival_airport_info"]["airport"] = arrival_info.find_element(By.CLASS_NAME, "av__style_name__IDpLN").text
            flight_data["arrival_airport_info"]["time"] = arrival_info.find_element(By.CLASS_NAME, "av__style_date__zutq0").text
            flight_data["arrival_airport_info"]["company"] = arrival_info.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
            flight_data["arrival_airport_info"]["flight_code"] = arrival_info.find_element(By.CLASS_NAME, "av__style_flightNumber__1XqQZ").text
        except Exception as e:
            print(f"Erro ao obter informações de chegada: {e}")

        # Adiciona os dados do voo atual à lista
        all_flights_data.append(flight_data)

    except Exception as e:
        print(f"Erro ao processar bloco de itinerário: {e}")
        continue

# Converte todos os dados para JSON e salva em arquivo
try:
    json_result = json.dumps(all_flights_data, ensure_ascii=False, indent=2)
    with open('flight_data.json', 'w', encoding='utf-8') as f:
        f.write(json_result)
    print("\n[INFO] Dados dos voos salvos em 'flight_data.json'")
except Exception as e:
    print(f"Erro ao salvar dados em JSON: {e}")

# Imprime os dados no console
print("\n[INFO] Dados dos voos encontrados:")
print(json.dumps(all_flights_data, ensure_ascii=False, indent=2))

time.sleep(6000)