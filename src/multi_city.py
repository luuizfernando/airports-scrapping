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

# ===== Selecting Multi-city option =====
travel = driver.find_element(By.ID, 'multi-city')
travel.click()

# Textos para preencher nos 2 primeiros trechos
destinations = ["Istanbul", "Tunis"]

# Captura todos os campos de origem e destino pela ordem de aparição
from_inputs = driver.find_elements(By.ID, "fromPort")
to_inputs = driver.find_elements(By.ID, "toPort")

for i in range(2):  # ajusta se tiver mais trechos
    try:
        # Preencher origem
        departure_input = driver.find_elements(By.ID, 'fromPort')
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

        # === Destination input ===
        try:
            destination_input = driver.find_element(By.ID, 'toPort')
            destination_input.send_keys(Keys.CONTROL, "a")
            destination_input.send_keys(Keys.BACKSPACE)
            destination_input = driver.find_element(By.ID, 'toPort')
            destination_input.send_keys("Istanbul")
            time.sleep(1)
            destiny = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
            destiny.click()
        except Exception as e:
            print("Error in destination field:", e)

        # === Departure date ===
        try:
            date = driver.find_element(By.XPATH, "//abbr[@aria-label='May 20, 2025']/ancestor::button")
            date.click()
            print("Date selected.")
        except Exception as e:
            print("Error in select date:", e)

        to_inputs[i].click()
        to_inputs[i].send_keys(Keys.CONTROL, 'a')
        to_inputs[i].send_keys(Keys.BACKSPACE)
        to_inputs[i].send_keys(destinations[i])
        time.sleep(1)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH'))
        ).click()

        time.sleep(1)

    except Exception as e:
        print(f"[ERRO] Erro no trecho {i+1}: {e}")

# # ==== First Travel ====
# # === Departure input ===
# departure_input = driver.find_elements(By.ID, 'fromPort')
# try:
#     departure_input = driver.find_element(By.ID, 'fromPort')
#     time.sleep(1)
#     departure_input.send_keys(Keys.CONTROL, "a")
#     time.sleep(1)
#     departure_input.send_keys(Keys.BACKSPACE)
#     time.sleep(1)
#     departure_input = driver.find_element(By.ID, 'fromPort')
#     departure_input.send_keys("São Paulo")
#     time.sleep(1)
#     origin = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
#     origin.click()
# except Exception as e:
#     print("Error in departure field:", e)

# # === Destination input ===
# try:
#     destination_input = driver.find_element(By.ID, 'toPort')
#     destination_input.send_keys(Keys.CONTROL, "a")
#     destination_input.send_keys(Keys.BACKSPACE)
#     destination_input = driver.find_element(By.ID, 'toPort')
#     destination_input.send_keys("Istanbul")
#     time.sleep(1)
#     destiny = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
#     destiny.click()
# except Exception as e:
#     print("Error in destination field:", e)

# # === Departure date ===
# try:
#     date = driver.find_element(By.XPATH, "//abbr[@aria-label='May 20, 2025']/ancestor::button")
#     date.click()
#     print("Date selected.")
# except Exception as e:
#     print("Error in select date:", e)

# # ==== Second Travel ====
# # === Departure input ===
# try:
#     second_travel_departure_input = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input__7lsdw]')
#     time.sleep(1)
#     second_travel_departure_input.send_keys(Keys.CONTROL, "a")
#     time.sleep(1)
#     second_travel_departure_input.send_keys(Keys.BACKSPACE)
#     time.sleep(1)
#     second_travel_departure_input = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input__7lsdw')
#     second_travel_departure_input.send_keys("Istanbul")
#     time.sleep(1)
#     origin = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
#     origin.click()
# except Exception as e:
#     print("Erro")

# # === Destination input ===
# try:
#     second_travel_departure_input = driver.find_element(By.ID, 'toPort')
#     second_travel_departure_input.send_keys(Keys.CONTROL, "a")
#     second_travel_departure_input.send_keys(Keys.BACKSPACE)
#     second_travel_departure_input = driver.find_element(By.ID, 'toPort')
#     second_travel_departure_input.send_keys("Tunis")
#     time.sleep(1)
#     destiny = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
#     destiny.click()
# except Exception as e:
#     print("Error in destination field:", e)

# === Departure date ===
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
view_itinerary = driver.find_element(By.CLASS_NAME, 'av__style_flight-detail-title___37OQ')
view_itinerary.click()

# === JSON structure for saving ===
flight_data = {
    "first_flight": {
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
    },
    "second_flight": {
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
    },
}

# === Itinerary blocks ===
itinerary = driver.find_elements(By.CLASS_NAME, "av__style_details__6sbBo")

# Verifica se há ao menos dois voos (ida e volta)
if len(itinerary) >= 2:
    first = itinerary[0]
    second = itinerary[1]

    time.sleep(2)

# === Travel Price ===
flight_data["price"] = driver.find_element(By.CLASS_NAME, 'av__style_pricePart__lYxno').text

# === First Flight ===
flight_data["first_flight"]["departure_airport_info"]["airport"] = first.find_element(By.CLASS_NAME, "av__style_name__IDpLN").text
flight_data["first_flight"]["departure_airport_info"]["time"] = first.find_element(By.CLASS_NAME, "av__style_date__zutq0").text
flight_data["first_flight"]["departure_airport_info"]["company"] = first.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
flight_data["first_flight"]["departure_airport_info"]["flight_code"] = first.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text

flight_data["first_flight"]["arrival_airport_info"]["airport"] = first.find_elements(By.CLASS_NAME, "av__style_name__IDpLN")[-1].text
flight_data["first_flight"]["arrival_airport_info"]["time"] = first.find_elements(By.CLASS_NAME, "av__style_date__zutq0")[-1].text
flight_data["first_flight"]["arrival_airport_info"]["company"] = first.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
flight_data["first_flight"]["arrival_airport_info"]["flight_code"] = first.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text

# === Second Flight ===
flight_data["second_flight"]["departure_airport_info"]["airport"] = second.find_element(By.CLASS_NAME, "av__style_name__IDpLN").text
flight_data["second_flight"]["departure_airport_info"]["time"] = second.find_element(By.CLASS_NAME, "av__style_date__zutq0").text
flight_data["second_flight"]["departure_airport_info"]["company"] = second.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
flight_data["second_flight"]["departure_airport_info"]["flight_code"] = second.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text

flight_data["second_flight"]["arrival_airport_info"]["airport"] = second.find_elements(By.CLASS_NAME, "av__style_name__IDpLN")[-1].text
flight_data["second_flight"]["arrival_airport_info"]["time"] = second.find_elements(By.CLASS_NAME, "av__style_date__zutq0")[-1].text
flight_data["second_flight"]["arrival_airport_info"]["company"] = second.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
flight_data["second_flight"]["arrival_airport_info"]["flight_code"] = second.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text

json_result = json.dumps(flight_data, ensure_ascii=False, indent=2)
print(json_result)