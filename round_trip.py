from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

BROWSER = webdriver.Chrome()
BROWSER.maximize_window()        

BROWSER.get("https://www.turkishairlines.com/")
WebDriverWait(BROWSER, 10).until(
    EC.presence_of_element_located((By.ID, "fromPort"))
)