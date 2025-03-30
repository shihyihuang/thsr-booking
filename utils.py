import json
from selenium.common.exceptions import NoSuchElementException

def load_account_settings(filepath='data/user_account.json'):
    """Load user info from user_account.json"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_user_input(stations):
    """Display station data and get user input for booking details."""
    print("以下為站名對應號碼, 請輸入號碼進行訂票:")
    for station in stations:
        print(f"{station['StationID']}: {station['StationName']['Zh_tw']}")
    print("")
    start_station_input = input("請輸入出發站名: ").strip()
    dest_station_input = input("請輸入目的站名: ").strip()
    outbound_date = input("輸入日期 (e.g. 2025/01/01): ").strip()
    outbound_time = input("輸入時間 (e.g. 07:00): ").strip()
    ticket_amount = input("輸入車票數量: ").strip()
    return start_station_input, dest_station_input, outbound_date, outbound_time, ticket_amount

def map_time_to_option(outbound_time):
    """
    Map an outbound_time string in HH:MM format to the option value.
    """
    mapping = {
        "00:00": "1201A", "00:30": "1230A",
        "05:00": "500A",  "05:30": "530A",
        "06:00": "600A",  "06:30": "630A",
        "07:00": "700A",  "07:30": "730A",
        "08:00": "800A",  "08:30": "830A",
        "09:00": "900A",  "09:30": "930A",
        "10:00": "1000A", "10:30": "1030A",
        "11:00": "1100A", "11:30": "1130A",
        "12:00": "1200N", "12:30": "1230P",
        "13:00": "100P",  "13:30": "130P",
        "14:00": "200P",  "14:30": "230P",
        "15:00": "300P",  "15:30": "330P",
        "16:00": "400P",  "16:30": "430P",
        "17:00": "500P",  "17:30": "530P",
        "18:00": "600P",  "18:30": "630P",
        "19:00": "700P",  "19:30": "730P",
        "20:00": "800P",  "20:30": "830P",
        "21:00": "900P",  "21:30": "930P",
        "22:00": "1000P", "22:30": "1030P",
        "23:00": "1100P", "23:30": "1130P"
    }
    return mapping.get(outbound_time, "")

def is_element_present(driver, by, value):
    """Return True if an element is present, False otherwise."""
    try:
        driver.find_element(by=by, value=value)
    except NoSuchElementException:
        return False
    return True