
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_webdriver(chromedriver_path):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('headless')  

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def accept_cookies(driver):
    """Wait for and click the cookie acceptance button."""
    try:
        wait = WebDriverWait(driver, 10)
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "cookieAccpetBtn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", cookie_btn)
        cookie_btn.click()
    except Exception as e:
        print("Cookie acceptance button not found or not clickable:", e)
