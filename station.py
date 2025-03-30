import json

def load_station_data():
    """Load station data from station.json"""
    with open('data/station.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def find_station(id, data):
    """
    Search for a station by its id and return: id, Mandarin name, and English name.
    """
    for station in data:
        if station['StationID'].strip() == id.strip():
            return station['StationID'], station['StationName']['Zh_tw'], station['StationName']['En']
    return None, None, None
