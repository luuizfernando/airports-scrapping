from selenium.webdriver.common.by import By
import time

def insert_passengers(driver, adults=1, children=1, infants=1):
    try:
        passengers = driver.find_element(By.ID, 'bookerFlightPaxpicker')
        passengers.click()
        time.sleep(0.5)

        for _ in range(adults):
            driver.find_element(By.ID, 'bookerFlightPaxPickerPlusAdult').click()
            time.sleep(0.5)
        
        for _ in range(children):
            driver.find_element(By.ID, 'bookerFlightPaxPickerPlusChild').click()
            time.sleep(0.5)
        
        for _ in range(infants):
            driver.find_element(By.ID, 'bookerFlightPaxPickerPlusInfant').click()
            time.sleep(0.5)

        print("Passengers added.")
    except Exception as e:
        print("Erro ao selecionar passageiros:", e)