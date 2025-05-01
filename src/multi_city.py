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

# ==== First Travel ====
# === Departure input ===
departure_input =  driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[1]")
try:
    time.sleep(1)
    departure_input.send_keys(Keys.CONTROL, "a")
    time.sleep(1)
    departure_input.send_keys(Keys.BACKSPACE)
    time.sleep(1)
    departure_input =  driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[1]")
    departure_input.send_keys("São Paulo")
    time.sleep(1)
    origin = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
    origin.click()
except Exception as e:
    print("Error in departure field:", e)

# === Destination input ===
destination_input =  driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[2]")
try:
    destination_input.send_keys(Keys.CONTROL, "a")
    destination_input.send_keys(Keys.BACKSPACE)
    destination_input =  driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[2]")
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

# ==== Second Travel ====
# === Departure input ===
second_travel_departure_input = driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[3]")
try:
    time.sleep(1)
    second_travel_departure_input.send_keys(Keys.CONTROL, "a")
    time.sleep(1)
    second_travel_departure_input.send_keys(Keys.BACKSPACE)
    time.sleep(1)
    second_travel_departure_input = driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[3]")
    second_travel_departure_input.send_keys("Istanbul")
    time.sleep(1)
    origin = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
    origin.click()
except Exception as e:
    print("Erro")

# === Destination input ===
try:
    second_travel_departure_input = driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[4]")
    second_travel_departure_input.send_keys(Keys.CONTROL, "a")
    second_travel_departure_input.send_keys(Keys.BACKSPACE)
    second_travel_departure_input = driver.find_element(By.XPATH, "(//input[@class='hm__style_booker-input__7lsdw'])[4]")
    second_travel_departure_input.send_keys("Tunis")
    time.sleep(1)
    destiny = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
    destiny.click()
except Exception as e:
    print("Error in destination field:", e)

# === Destination date ===
try:
    date2 = driver.find_element(By.XPATH, "//abbr[@aria-label='May 30, 2025']/ancestor::button")
    date2.click()
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
    confirmation_button = driver.find_element(By.CLASS_NAME, 'hm__style_thy-button__ZfnOU.hm__MultiCityTab_searchButton___jq2U')
    confirmation_button.click()
    print("Confirmation done.")
except Exception as e:
    print("Error in confirming data:", e)

# ==== Getting flight data ====
# === JSON structure for saving ===
flight_data = {
    "first_flight": {
        "price": "",
        "departure_airport_info": {
            "airport": "",
            "flight_time": "",
            "company_and_flight_code": "",
        },
        "arrival_airport_info": {
            "airport": "",
            "arrival_time": "",
        }
    },
    "second_flight": {
        "price": "",
        "departure_airport_info": {
            "airport": "",
            "flight_time": "",
            "company_and_flight_code": "",
        },
        "arrival_airport_info": {
            "airport": "",
            "arrival_time": ""
        }
    },
}

# === Itinerary blocks ===
view_itinerary = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flightItem_recommendedOrder_0_0"]/div/div[1]/div/div/div/div[2]/div')))
time.sleep(1)
view_itinerary.click()

# === First Flight ===
# == Price ==
flight_data["first_flight"]["price"] = driver.find_element(By.CLASS_NAME, 'av__style_pricePart__lYxno').text
# == Departure Airport Info ==
flight_data["first_flight"]["departure_airport_info"]["airport"] = driver.find_element(By.XPATH, '(//*[@id="flightItem_recommendedOrder_0_0"]/div[2]/div/div[2]/div/div/div[3]/div[2])[1]').text
flight_data["first_flight"]["departure_airport_info"]["flight_time"] = driver.find_element(By.XPATH, '(//*[@id="flightItem_recommendedOrder_0_0"]/div[2]/div/div[2]/div/div/div[3]/div[1]/div/span[1])[1]').text
flight_data["first_flight"]["departure_airport_info"]["company_and_flight_code"] = driver.find_element(By.XPATH, '(//*[@id="flightItem_recommendedOrder_0_0"]/div[2]/div/div[2]/div/div/div[3]/div[4])[1]').text

# == Arrival Airport Info ==
flight_data["first_flight"]["arrival_airport_info"]["airport"] = driver.find_element(By.XPATH, '//*[@id="flightItem_recommendedOrder_0_0"]/div[2]/div/div[2]/div/div/div[3]/div[8]').text
flight_data["first_flight"]["arrival_airport_info"]["arrival_time"] = driver.find_element(By.XPATH, '//*[@id="flightItem_recommendedOrder_0_0"]/div[2]/div/div[2]/div/div/div[3]/div[7]/div/span[1]').text

# == Selecting Ticket ==
ticket_button = driver.find_element(By.CLASS_NAME, 'av__style_metro-radio__YF2_k')
ticket_button.click()
time.sleep(1)
try:
    ticket_confirmation_button = driver.find_element(By.CLASS_NAME, 'av__style_package-card-footer__pHrvc')
    ticket_confirmation_button.click()
    driver.execute_script("arguments[0].click();", ticket_confirmation_button)
except Exception as e:
    print(f"Erro ao clicar: {e}")
    buttons = driver.find_elements(By.XPATH, '//*[@id="RS"]/div[3]/button')
    print(f"Encontrados {len(buttons)} botões")

# === Second Flight ===
# == Itinerary blocks ==
view_itinerary = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='av__style_flight-detail___KZDm'])[2]")))
time.sleep(1)
view_itinerary.click()
time.sleep(1)

# == Price ==
flight_data["second_flight"]["price"] = driver.find_element(By.XPATH, "//span[@id='amount-of-price-currency']").text

# == Departure Airport Info ==
flight_data["second_flight"]["departure_airport_info"]["airport"] = driver.find_element(By.CLASS_NAME, 'av__style_name__IDpLN').text
flight_data["second_flight"]["departure_airport_info"]["flight_time"] = driver.find_element(By.CLASS_NAME, 'av__style_date__zutq0').text
flight_data["second_flight"]["departure_airport_info"]["company_and_flight_code"] = driver.find_element(By.CLASS_NAME, 'av__style_carrier__eYot3').text

# # == Arrival Airport Info ==
flight_data["second_flight"]["arrival_airport_info"]["airport"] = driver.find_element(By.XPATH, "(//div[@class='av__style_name__IDpLN'])[2]").text
flight_data["second_flight"]["arrival_airport_info"]["arrival_time"] = driver.find_element(By.XPATH, "(//span[@class='av__style_date__zutq0'])[2]").text

# time.sleep(6000)

json_result = json.dumps(flight_data, ensure_ascii=False, indent=2)
print(json_result)