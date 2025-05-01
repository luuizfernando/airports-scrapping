from utils.selenium_setup import selenium_setup
from utils.accept_cookies import accept_cookies
from utils.insert_passengers import insert_passengers
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import requests

# ==== Opening Turkish Airlines site with selenium ====
driver = selenium_setup()
driver.maximize_window()
driver.get("https://www.turkishairlines.com/")

# ===== Accept cookies =====
accept_cookies(driver)

# ===== Selecting One-Way option =====
travel = driver.find_element(By.ID, 'one-way')
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
try:
    date = driver.find_element(By.XPATH, "//abbr[@aria-label='May 20, 2025']/ancestor::button")
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

# ===== Catching Payload Request ====
print("\n[INFO] Waiting for page loading and requests...")
time.sleep(10)

# ==== Getting the network logs ====
logs = driver.get_log("performance")
target_url = "https://www.turkishairlines.com/api/v1/availability/cheapest-prices"

payload_capture = None

for entry in logs:
    try:
        log = json.loads(entry["message"])["message"]
        if "Network.requestWillBeSent" in log["method"]:
            request = log["params"]["request"]
            if request["url"] == target_url and request["method"] == "POST":
                print("\n[INFO] POST request to Pricing API found!")
                print(f"URL: {request['url']}")
                
                # === Obtendo o payload ===
                if "postData" in request:
                    payload = request["postData"]
                    print("Payload found:")
                    print(payload)
                    
                    # === Saving the payload to a file ===
                    with open('payload_preco.json', 'w', encoding='utf-8') as f:
                        f.write(payload)
                        print("\n[INFO] Payload saved in payload_preco.json'")
                    
                    # === Trying to convert to JSON ===
                    try:
                        payload_json = json.loads(payload)
                        print("Payload converted to JSON:")
                        print(json.dumps(payload_json, indent=2))
                        payload_capturado = payload_json
                        break
                    except json.JSONDecodeError as e:
                        print(f"Error converting payload to JSON: {e}")
                else:
                    print("\n[WARNING] No payload found in request")
    except Exception as e:
        continue

if payload_capturado is None:
    print("\n[ERROR] Unable to capture request payload")
    driver.quit()
    exit(1)

# ==== Transfer Selenium cookies to requests ====
session = requests.Session()
selenium_cookies = driver.get_cookies()
for cookie in selenium_cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# ===== Making the API request ====
print("\n[INFO] Making a request to the API...")

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'content-type': 'application/json',
    'origin': 'https://www.turkishairlines.com',
    'priority': 'u=1, i',
    'referer': 'https://www.turkishairlines.com/en-int/flights/booking/availability-international?cId=fa2f34a3-d89c-4c0d-9dd3-3b6cffae464a',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-bfp': 'f2a9ad902b644642d4182d28db84dbcf',
    'x-clientid': 'dd031584-8e72-439e-bb3e-ccbe9cfa0374',
    'x-conversationid': 'fa2f34a3-d89c-4c0d-9dd3-3b6cffae464a',
    'x-country': 'int',
    'x-requestid': '2725c1e9-f87e-4130-ac56-47b13377f39e',
}

# ==== Setting up the session with retry ====
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
                    data = json.loads(response.content.decode("utf-8"))
                except Exception as e:
                    print("[ERROR] Failed to decode JSON:", e)
                    print("Trying to unzip with gzip...")

                    import gzip
                    from io import BytesIO
                    try:
                        decompressed = gzip.GzipFile(fileobj=BytesIO(response.content)).read()
                        data = json.loads(decompressed.decode("utf-8"))
                    except Exception as gz_e:
                        print("[ERROR] Also failed to decompress with gzip:", gz_e)
                        print("\nRaw answer:")
                        print(response.content[:500])
                        driver.quit()
                        exit(1)
            else:
                print("[ERROR] Response is not JSON.")
                print(response.text[:500])
                driver.quit()
                exit(1)
        except Exception as e:
            print(f"[ERROR] Unexpected failure while processing response: {e}")
            driver.quit()
            exit(1)

        print("\n[INFO] API Response:")
        print(json.dumps(data, indent=2)[:1000])
        
        # === Processing the price data ===
        if 'data' in data and 'dailyPriceList' in data['data']:
            print("\n[INFO] Lista de preços diários:")
            for price in data['data']['dailyPriceList']:
                date = price.get('date', 'N/A')
                price_data = price.get('price')
                if price_data:
                    currency = price_data.get('currencySign', '')
                    amount = price_data.get('amount', 0)
                    print(f"Data: {date}, Price: {currency}{amount:.2f}")
                else:
                    print(f"Data: {date}, Price: Indisponível")
        else:
            print("\n[WARNING] Daily Price data not found in response")
    else:
        print(f"[ERRO] Status code {response.status_code}")
        print(response.text)
except requests.exceptions.RequestException as e:
    print(f"[ERROR] Request failed: {e}")
    driver.quit()
    exit(1)

# ==== Getting flight data ====
view_itinerary = driver.find_element(By.CLASS_NAME, 'av__style_flight-detail-title___37OQ')
view_itinerary.click()

# === JSON structure for saving ===
flight_data = {
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

# Bloco de ida e volta
departure = itinerary[0]
arrival = itinerary[-1]

time.sleep(2)

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