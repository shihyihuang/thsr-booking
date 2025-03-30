import time
from station import load_station_data, find_station
from utils import get_user_input, load_account_settings, is_element_present
from web_driver import init_webdriver, accept_cookies
from captcha_solver import solve_and_fill_captcha
from booking import (fill_first_page, select_first_train_and_submit,
                          fill_third_page_and_confirm, complete_booking)
from selenium.webdriver.common.by import By

THSR_BOOKING_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"

def main():
    # Load station and account data
    stations = load_station_data()
    account = load_account_settings("data/user_account.json")
    
    # Get user input
    (start_station_input, dest_station_input, outbound_date,
     outbound_time, ticket_amount) = get_user_input(stations)
    
    start_station_id, start_station_nameZh, start_station_nameEn = find_station(start_station_input, stations)
    dest_station_id, dest_station_nameZh, dest_station_nameEn = find_station(dest_station_input, stations)
    
    print("出發站:", start_station_nameZh, "(EN:", start_station_nameEn, ")")
    print("目的站:", dest_station_nameZh, "(EN:", dest_station_nameEn, ")")
    
    # Initialize WebDriver
    chromedriver_path = "/usr/local/bin/chromedriver"
    driver = init_webdriver(chromedriver_path)
    driver.get(THSR_BOOKING_URL)
    
    # Accept cookies
    accept_cookies(driver)
    
    # --- FIRST PAGE ---
    max_attempts = 20
    attempts = 0
    success = False

    # Retry captcha until the second page appears (train option element exists)
    while attempts < max_attempts and not success:
        print(f"Captcha attempt {attempts+1}")
        # Solve and fill in the captcha
        solve_and_fill_captcha(driver)
        time.sleep(20)
        # Fill in the first page form (stations, date, time, ticket amount)
        fill_first_page(driver, start_station_nameZh, dest_station_nameZh,
                        outbound_date, outbound_time, ticket_amount, "")
        time.sleep(2)
        
        # check for the presence of an element that indicates the second page has loaded.
        if is_element_present(driver, By.CSS_SELECTOR, "input[name^='TrainQueryDataViewPanel:TrainGroup']"):
            success = True
            print("Captcha solved and first page submission successful.")
        else:
            print("Captcha attempt failed; retrying...")
            attempts += 1

    if not success:
        print("Maximum captcha attempts reached; aborting.")
        driver.quit()
        return
    
    # --- SECOND PAGE ---
    select_first_train_and_submit(driver)
    
    # --- THIRD PAGE ---
    fill_third_page_and_confirm(driver, account['pid'], account['phone'].strip(), account['email'].strip())
    
    # (OPT) complete booking by showing summary and confirming
    complete_booking(driver, account['pid'], account['phone'].strip())
    
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
