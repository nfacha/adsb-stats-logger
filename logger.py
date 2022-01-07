import json
import logging
import os
import time
from datetime import datetime

import geopy.distance

DATA_PATH = '/run/dump1090-fa/'
STATION_LOCATION = (37.7, -25.5)
data = {}


def load_data():
    logging.info("Loading data file...")
    global data
    with open('./data.json', 'r') as f:
        data = json.load(f)


def save_data():
    logging.info("Saving data file...")
    global data
    print(data)
    with open('./data.json', 'w') as f:
        json.dump(data, f)


def init_data():
    logging.info("Creating new data file...")
    with open('./data.json', 'w') as f:
        json.dump({
            'times': {
                'start': None,
                'latest': None
            },
            'flights': [],
            'operators': [],
            'maxAltitude': {
                'altitude': 0,
                'latitude': 0,
                'longitude': 0,
                'flight': None,
                'seenAt': None
            },
            'maxGroundSpeed': {
                'groundSpeed': 0,
                'latitude': 0,
                'longitude': 0,
                'flight': None,
                'seenAt': None
            },
            'furthestFlight': {
                'distance': 0,
                'latitude': 0,
                'longitude': 0,
                'flight': None,
                'seenAt': None
            },
            'closestFlight': {
                'distance': 0,
                'latitude': 0,
                'longitude': 0,
                'flight': None,
                'seenAt': None
            },
            'maxSignal': {
                'signal': 0,
                'distance': 0,
                'latitude': 0,
                'longitude': 0,
                'flight': None,
                'seenAt': None
            },
            'minSignal': {
                'signal': 0,
                'distance': 0,
                'latitude': 0,
                'longitude': 0,
                'flight': None,
                'seenAt': None
            },
        }, f)


def parse_file():
    logging.info("Parsing aircraft json")
    hData = json.loads(open(DATA_PATH + '/aircraft.json', 'r').read())
    # hData = json.loads(open('./sample.json', 'r').read())
    data_time = datetime.fromtimestamp(hData['now'])
    data_time_parsed = data_time.strftime('%Y-%m-%d %H:%M:%S')

    # Updates data timeframes
    if data['times']['latest'] is None or data_time < datetime.strptime(data['times']['latest'], '%Y-%m-%d %H:%M:%S'):
        newer_file = data_time_parsed
        data['times']['latest'] = oldest_file

    if data['times']['start'] is None or data_time > datetime.strptime(data['times']['start'], '%Y-%m-%d %H:%M:%S'):
        oldest_file = data_time_parsed
        data['times']['start'] = newer_file
    for flight in hData['aircraft']:
        if 'flight' not in flight:
            logging.debug("Flight without flight number: " + str(flight['hex']))
            continue

        flight['flight'] = flight['flight'].rstrip()
        # Flights
        if not any(x['flight'] == flight['flight'] for x in data['flights']):
            logging.info("Found new flight: " + flight['flight'])
            data['flights'].append({
                'flight': flight['flight'],
                'firstSeen': data_time_parsed,
                'lastSeen': data_time_parsed,
            })
        else:
            logging.info("Found existing flight: " + flight['flight'])
            existing_flight = next(x for x in data['flights'] if x['flight'] == flight['flight'])
            existing_flight_index = find(data['flights'], 'flight', flight['flight'])
            data['flights'][existing_flight_index]['lastSeen'] = data_time_parsed

        # Operators
        operator = ''.join(i for i in flight['flight'] if not i.isdigit())
        if not any(x['operator'] == operator for x in data['operators']):
            logging.info("Found new operator: " + operator)
            data['operators'].append({
                'operator': operator,
                'firstSeen': data_time_parsed,
                'lastSeen': data_time_parsed,
            })
        else:
            logging.info("Found existing operator: " + operator)
            existing_operator = next(x for x in data['operators'] if x['operator'] == operator)
            existing_operator_index = find(data['operators'], 'operator', operator)
            data['operators'][existing_operator_index]['lastSeen'] = data_time_parsed

        # Max Altitude
        if 'alt_geom' in flight:
            altitude = flight['alt_geom']
            if altitude > data['maxAltitude']['altitude']:
                logging.info("Found new max altitude: " + str(altitude) + "ft by " + flight['flight'])
                data['maxAltitude']['altitude'] = altitude
                data['maxAltitude']['flight'] = flight['flight']
                data['maxAltitude']['seenAt'] = data_time_parsed
                if 'lat' in flight and 'lon' in flight:
                    data['maxAltitude']['latitude'] = flight['lat']
                    data['maxAltitude']['longitude'] = flight['lon']
                else:
                    data['maxAltitude']['latitude'] = None
                    data['maxAltitude']['longitude'] = None

        # Max Speed
        if 'gs' in flight:
            speed = flight['gs']
            if speed > data['maxGroundSpeed']['groundSpeed']:
                logging.info("Found new max ground speed: " + str(speed) + "kt by " + flight['flight'])
                data['maxGroundSpeed']['groundSpeed'] = speed
                data['maxGroundSpeed']['flight'] = flight['flight']
                data['maxGroundSpeed']['seenAt'] = data_time_parsed
                if 'lat' in flight and 'lon' in flight:
                    data['maxGroundSpeed']['latitude'] = flight['lat']
                    data['maxGroundSpeed']['longitude'] = flight['lon']
                else:
                    data['maxGroundSpeed']['latitude'] = None
                    data['maxGroundSpeed']['longitude'] = None

        # Station Distance
        if 'lat' in flight and 'lon' in flight:
            distance_to_station = geopy.distance.geodesic((flight['lat'], flight['lon']), STATION_LOCATION).nm
            if distance_to_station > data['furthestFlight']['distance']:
                logging.info("Found new furthest flight: " + str(distance_to_station) + "nm by " + flight['flight'])
                data['furthestFlight']['distance'] = distance_to_station
                data['furthestFlight']['flight'] = flight['flight']
                data['furthestFlight']['seenAt'] = data_time_parsed
                data['furthestFlight']['latitude'] = flight['lat']
                data['furthestFlight']['longitude'] = flight['lon']
            elif distance_to_station < data['closestFlight']['distance'] or data['closestFlight']['distance'] == 0:
                logging.info("Found new closest flight: " + str(distance_to_station) + "nm by " + flight['flight'])
                data['closestFlight']['distance'] = distance_to_station
                data['closestFlight']['flight'] = flight['flight']
                data['closestFlight']['seenAt'] = data_time_parsed
                data['closestFlight']['latitude'] = flight['lat']
                data['closestFlight']['longitude'] = flight['lon']

        # Signal
        if 'rssi' in flight:
            signal = flight['rssi']
            distance_to_station = geopy.distance.geodesic((flight['lat'], flight['lon']), STATION_LOCATION).nm
            if signal > data['maxSignal']['signal'] or data['maxSignal']['signal'] == 0:
                logging.info(
                    "Found new max signal: " + str(distance_to_station) + "nm by " + flight[
                        'flight'] + " with signal: " + str(
                        signal))
                data['maxSignal']['signal'] = signal
                data['maxSignal']['distance'] = distance_to_station
                data['maxSignal']['flight'] = flight['flight']
                data['maxSignal']['seenAt'] = data_time_parsed
                if 'lat' in flight and 'lon' in flight:
                    data['maxSignal']['latitude'] = flight['lat']
                    data['maxSignal']['longitude'] = flight['lon']
                else:
                    data['maxSignal']['latitude'] = None
                    data['maxSignal']['longitude'] = None
            elif signal < data['minSignal']['signal'] or data['minSignal']['signal'] == 0:
                logging.info(
                    "Found new min signal: " + str(distance_to_station) + "nm by " + flight[
                        'flight'] + " with signal: " + str(
                        signal))
                data['minSignal']['signal'] = signal
                data['minSignal']['distance'] = distance_to_station
                data['minSignal']['flight'] = flight['flight']
                data['minSignal']['seenAt'] = data_time_parsed
                if 'lat' in flight and 'lon' in flight:
                    data['minSignal']['latitude'] = flight['lat']
                    data['minSignal']['longitude'] = flight['lon']
                else:
                    data['minSignal']['latitude'] = None
                    data['minSignal']['longitude'] = None

    save_data()


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


#####
logging.basicConfig(level=logging.INFO)
logging.info("Initializing...")
if not os.path.exists('./data.json'):
    init_data()
load_data()
while True:
    parse_file()
    time.sleep(0.1)