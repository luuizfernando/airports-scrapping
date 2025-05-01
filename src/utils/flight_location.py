from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def fill_location(driver, field_id, city_name):
    try:
        location_input = driver.find_element(By.ID, field_id)
        time.sleep(0.5)
        location_input.send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        location_input.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        location_input = driver.find_element(By.ID, field_id)
        location_input.send_keys(city_name)
        time.sleep(1)
        suggestion = driver.find_element(By.CLASS_NAME, 'hm__style_booker-input-list-item-text__ajPdH')
        suggestion.click()
        print(f"{field_id} preenchido com: {city_name}")
    except Exception as e:
        print(f"Erro ao preencher {field_id} ({city_name}):", e)