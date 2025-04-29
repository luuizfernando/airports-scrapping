from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

BROWSER = webdriver.Chrome()
BROWSER.maximize_window()

def collect_round_trip_data(departure, destination, departure_date, return_date):
    try:
        BROWSER.get('https://www.turkishairlines.com/')
        WebDriverWait(BROWSER, 10).until(
            EC.presence_of_element_located((By.ID, "fromPort"))
        )

    except Exception as e:
        print(f"Erro durante a execução: {e}")
        return None

    finally:
         BROWSER.quit()

def main():
    print("== Coletor de Voos Turkish Airlines ==")


if __name__ == "__main__":
    main()
