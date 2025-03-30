
import ddddocr
from selenium.webdriver.common.by import By

def solve_and_fill_captcha(driver):
    """
    Capture the captcha image, decode it using ddddocr, and fill in the captcha input.
    """
    captcha_element = driver.find_element(By.ID, "BookingS1Form_homeCaptcha_passCode")
    captcha_element.screenshot("captcha.png")
    
    ocr = ddddocr.DdddOcr(beta=True)
    with open("captcha.png", "rb") as f:
        img_bytes = f.read()
    captcha_text = ocr.classification(img_bytes)
    captcha_text = captcha_text.upper()
    captcha_text = captcha_text.strip()
    captcha_input = driver.find_element(By.NAME, "homeCaptcha:securityCode")
    captcha_input.clear()
    captcha_input.send_keys(captcha_text)
