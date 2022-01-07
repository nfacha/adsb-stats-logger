import configparser
import json
import logging
import sentry_sdk

data = {}
config = configparser.ConfigParser()
config.read('config.ini')
USE_METRIC = True

def load_config():
    global config
    global USE_METRIC
    logging.basicConfig(level=logging.getLevelName(int(config['LOGGING']['LOG_LEVEL'])))
    logging.info("Logging level: " + config['LOGGING']['LOG_LEVEL'])
    USE_METRIC = config.getboolean('UNITS', 'USE_METRIC_SYSTEM')
    logging.info("Use metric system: " + str(USE_METRIC))
    if config['LOGGING']['SENTRY_DSN'] is not '':
        sentry_sdk.init(
            config['LOGGING']['SENTRY_DSN'],
            traces_sample_rate=1.0,
            environment=config['LOGGING']['SENTRY_ENVIRONMENT']
        )
def load_data():
    global data
    with open('./data.json', 'r') as f:
        data = json.load(f)

load_config()
load_data()
print("--- Metrics ---")
print("Data range: "+data['times']['start'] + " - " + data['times']['latest'])
print("Unique Flights: "+str(len(data['flights'])))
print("Unique Operators: "+str(len(data['operators'])))
if USE_METRIC:
    print("Max Altitude: Flight " + data['maxAltitude']['flight'] + " " + str(data['maxAltitude']['altitude'] / 3281) + " km at " + data['maxAltitude']['seenAt'])
    print("Max Speed: Flight " + data['maxGroundSpeed']['flight'] + " " + str(data['maxGroundSpeed']['groundSpeed'] * 1.852) + " kmh at " + data['maxGroundSpeed']['seenAt'])
    print("Max Station Distance: Flight " + data['furthestFlight']['flight'] + " " + str(data['furthestFlight']['distance'] * 1.852) + " km at " + data['furthestFlight']['seenAt'])
    print("Min Station Distance: Flight " + data['closestFlight']['flight'] + " " + str(data['closestFlight']['distance'] * 1.852) + " km at " + data['closestFlight']['seenAt'])
else:
    print("Max Altitude: Flight " + data['maxAltitude']['flight'] + " " + str(data['maxAltitude']['altitude']) + " ft at " + data['maxAltitude']['seenAt'])
    print("Max Speed: Flight " + data['maxGroundSpeed']['flight'] + " " + str(data['maxGroundSpeed']['groundSpeed']) + " kn at " + data['maxGroundSpeed']['seenAt'])
    print("Max Station Distance: Flight " + data['furthestFlight']['flight'] + " " + str(data['furthestFlight']['distance']) + " nm at " + data['furthestFlight']['seenAt'])
    print("Min Station Distance: Flight " + data['closestFlight']['flight'] + " " + str(data['closestFlight']['distance']) + " nm at " + data['closestFlight']['seenAt'])

print("Max Signal: Flight "+data['maxSignal']['flight']+" "+str(data['maxSignal']['signal'])+" db at "+data['maxSignal']['seenAt'])
print("Min Signal: Flight "+data['minSignal']['flight']+" "+str(data['minSignal']['signal'])+" db at "+data['minSignal']['seenAt'])
print('--- Unique Flights Seen ---')
for flight in data['flights']:
    print(flight['flight'] + " last seen on "+flight['lastSeen'])
print('--- Unique Operators Seen ---')
for operator in data['operators']:
    print(operator['operator'] + " last seen on "+operator['lastSeen'])