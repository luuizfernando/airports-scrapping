from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def accept_cookies(driver, timeout=10, button_id="allowCookiesButton"):
    try:
        cookie_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, button_id))
        )
        cookie_btn.click()
        print("Cookies accepted.")
    except Exception as e:
        print("Cookies button not found or error:", e)