import json

data = {}
def load_data():
    global data
    with open('./data.json', 'r') as f:
        data = json.load(f)

load_data()
print("--- Metrics ---")
print("Data range: "+data['times']['start'] + " - " + data['times']['latest'])
print("Unique Flights: "+str(len(data['flights'])))
print("Unique Operators: "+str(len(data['operators'])))
print("Max Altitude: Flight "+data['maxAltitude']['flight']+" "+str(data['maxAltitude']['altitude'])+" ft at "+data['maxAltitude']['seenAt'])
print("Max Speed: Flight "+data['maxGroundSpeed']['flight']+" "+str(data['maxGroundSpeed']['groundSpeed'])+" kn at "+data['maxGroundSpeed']['seenAt'])
print("Max Station Distance: Flight "+data['furthestFlight']['flight']+" "+str(data['furthestFlight']['distance'])+" nm at "+data['furthestFlight']['seenAt'])
print("Min Station Distance: Flight "+data['closestFlight']['flight']+" "+str(data['closestFlight']['distance'])+" nm at "+data['closestFlight']['seenAt'])
print("Max Signal: Flight "+data['maxSignal']['flight']+" "+str(data['maxSignal']['signal'])+" db at "+data['maxSignal']['seenAt'])
print("Min Signal: Flight "+data['minSignal']['flight']+" "+str(data['minSignal']['signal'])+" db at "+data['minSignal']['seenAt'])
print('--- Unique Flights Seen ---')
for flight in data['flights']:
    print(flight['flight'] + " last seen on "+flight['lastSeen'])
print('--- Unique Operators Seen ---')
for operator in data['operators']:
    print(operator['operator'] + " last seen on "+operator['lastSeen'])