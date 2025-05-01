from utils.selenium_setup import selenium_setup
from utils.accept_cookies import accept_cookies
from utils.insert_passengers import insert_passengers
from utils.flight_location import fill_location
from selenium.webdriver.common.by import By
import time
import json

# ==== Opening Turkish Airlines site with selenium ====
driver = selenium_setup()
driver.maximize_window()
driver.get("https://www.turkishairlines.com/")

# ===== Accept cookies =====
accept_cookies(driver)

# ===== Selecting One-Way option =====
travel = driver.find_element(By.ID, 'round-trip')
travel.click()

# ==== Flight Location ====
# === Departure input ===
fill_location(driver, "fromPort", "São Paulo")
# === Arrival input ===
fill_location(driver, "toPort", "Kabul")

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

# ===== Passengers number =====
insert_passengers(driver, adults=1, children=1, infants=1)

# ==== Confirming data and searching flights ====
try: 
    confirmation_button = driver.find_element(By.CLASS_NAME, 'hm__RoundAndOneWayTab_buttonWrapper__v15PI')
    confirmation_button.click()
    print("Confirmation done.")
except Exception as e:
    print("Error in confirming data:", e)

print("\n[INFO] Waiting for page loading...")
time.sleep(10)

# ==== Getting flight data ====
view_itinerary = driver.find_element(By.CLASS_NAME, 'av__style_flight-detail-title___37OQ')
view_itinerary.click()

# === JSON structure for saving ===
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

# === Itinerary blocks ===
itinerary = driver.find_elements(By.CLASS_NAME, "av__style_details__6sbBo")
departure = itinerary[0]
arrival = itinerary[-1]

time.sleep(2)

# === Travel Price ===
flight_data["price"] = driver.find_element(By.CLASS_NAME, 'av__style_pricePart__lYxno').text

# === Departure Airport ===
flight_data["departure_airport_info"]["airport"] = departure.find_element(By.CLASS_NAME, "av__style_name__IDpLN").text
flight_data["departure_airport_info"]["time"] = departure.find_element(By.CLASS_NAME, "av__style_date__zutq0").text
flight_data["departure_airport_info"]["company"] = departure.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
flight_data["departure_airport_info"]["flight_code"] = departure.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text

# === Arrival Airport ===
flight_data["arrival_airport_info"]["airport"] = arrival.find_element(By.CLASS_NAME, "av__style_name__IDpLN").text
flight_data["arrival_airport_info"]["time"] = arrival.find_element(By.CLASS_NAME, "av__style_date__zutq0").text
flight_data["arrival_airport_info"]["company"] = arrival.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text
flight_data["arrival_airport_info"]["flight_code"] = arrival.find_element(By.CLASS_NAME, "av__style_carrier__eYot3").text

json_result = json.dumps(flight_data, ensure_ascii=False, indent=2)
print(json_result)