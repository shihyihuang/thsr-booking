import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils import map_time_to_option

def fill_first_page(driver, start_station_nameZh, dest_station_nameZh,
                    outbound_date, outbound_time, ticket_amount, captcha_input):
    """
    First step: Fill in the booking form with station names, date, time, ticket amount, and captcha.
    Change booking method to time and fill in the booking info then click the first SubmitButton.
    """
    wait = WebDriverWait(driver, 10)
    # 1. Choose booking method "時間"
    time_radio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-target='search-by-time']")))
    time_radio.click()
    
    # 2. Select outbound time from the dropdown
    time_select = Select(driver.find_element(By.CSS_SELECTOR, "select[name='toTimeTable']"))
    option_value = map_time_to_option(outbound_time)
    if option_value:
        time_select.select_by_value(option_value)
    else:
        print("No matching option for outbound_time:", outbound_time)
    
    # 3. Set start and destination stations
    start_station_select = Select(driver.find_element(By.NAME, "selectStartStation"))
    start_station_select.select_by_visible_text(start_station_nameZh)
    
    dest_station_select = Select(driver.find_element(By.NAME, "selectDestinationStation"))
    dest_station_select.select_by_visible_text(dest_station_nameZh)
    
    # 4. Fill in outbound date 
    date_input = driver.find_element(By.XPATH, "//input[contains(@class, 'uk-input') and @readonly]")
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
    date_input.clear()
    date_input.send_keys(outbound_date)
    
    # 5. Set ticket amount
    ticket_select = Select(driver.find_element(By.NAME, "ticketPanel:rows:0:ticketAmount"))
    ticket_select.select_by_visible_text(ticket_amount)
    
    # 6. Fill in captcha input
    captcha_field = driver.find_element(By.NAME, "homeCaptcha:securityCode")
    captcha_field.clear()
    captcha_field.send_keys(captcha_input)
    
    # 7. Click first SubmitButton
    driver.find_element(By.ID, "SubmitButton").click()

def select_first_train_and_submit(driver):
    """
    Second step: Wait for train options, select the first one, and click SubmitButton.
    """
    wait = WebDriverWait(driver, 10)
    train_options = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "input[name^='TrainQueryDataViewPanel:TrainGroup']")))
    if train_options:
        train_options[0].click()
    else:
        raise Exception("No train options found on second page.")
    
    driver.find_element(By.ID, "SubmitButton").click()

def fill_third_page_and_confirm(driver, id_number, phone, email):
    """
    Third step: Fill in ID, phone, email, select the membership checkbox, and click the final confirm button.
    """
    wait = WebDriverWait(driver, 10)
    id_field = wait.until(EC.presence_of_element_located((By.ID, "idNumber")))
    id_field.clear()
    id_field.send_keys(id_number)
    
    phone_field = driver.find_element(By.ID, "mobilePhone")
    phone_field.clear()
    phone_field.send_keys(phone)
    
    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys(email)
    
    membership_checkbox = driver.find_element(By.ID, "memberShipCheckBox")
    if not membership_checkbox.is_selected():
        membership_checkbox.click()
    
    # Fill ID
    try:
        ms_field = driver.find_element(By.ID, "msNumber")
        ms_field.clear()
        ms_field.send_keys(id_number)
    except Exception:
        pass
    
    driver.find_element(By.ID, "isSubmit").click()

def complete_booking(driver, pid, phone):
    """
    (OPT) display summary information and complete booking.
    """
    driver.find_element(By.ID, "idNumber").send_keys(pid)
    driver.find_element(By.ID, "mobilePhone").send_keys(phone)
    
    money = driver.find_element(By.ID, "TotalPrice").text
    start_time = driver.find_element(By.ID, "InfoDeparture0").text
    arrive_time = driver.find_element(By.ID, "InfoArrival0").text
    duration = driver.find_element(By.ID, "InfoEstimatedTime0").text
    info_date = driver.find_element(By.ID, "InfoDepartureDate0").text
    car_info = driver.find_element(By.ID, "InfoCode0").text
    
    print("\n訂票資訊:")
    print(f"出發時間: {start_time}")
    print(f"抵達時間: {arrive_time}")
    print(f"車次: {car_info}")
    print(f"行車時間: {duration}")
    print(f"日期: {info_date}")
    print("票價:", money)
    
    confirm = input("確認訂票? (y/n): ").strip().lower()
    if confirm == "y":
        driver.find_element(By.ID, "isSubmit").click()
        time.sleep(1)
        try:
            seat = driver.find_element(By.XPATH, '//div[@class="seat-label"]/span').text
            code = driver.find_element(By.XPATH, '//td[@class="td-data"]/p[@class="pnr-code"]/span').text
            status = driver.find_element(By.XPATH, '//td[@class="td-data"]/p[@class="payment-status"]').text
            driver.minimize_window()
            print("座位:", seat, "訂票碼:", code, "付款狀態:", status)
        except Exception as e:
            print("Failed to retrieve final booking details:", e)
    else:
        print("取消訂票")
