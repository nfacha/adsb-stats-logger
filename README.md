[![wakatime](https://wakatime.com/badge/user/65ddcee5-893d-45e3-989c-4d52691b9072/project/68abfa67-8b61-46d6-b31d-de28ef515ccb.svg)](https://wakatime.com/badge/user/65ddcee5-893d-45e3-989c-4d52691b9072/project/68abfa67-8b61-46d6-b31d-de28ef515ccb)

![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/nfacha/adsb-stats-logger?label=Latest%20version)
![GitHub Release Date](https://img.shields.io/github/release-date/nfacha/adsb-stats-logger)
![GitHub last commit](https://img.shields.io/github/last-commit/nfacha/adsb-stats-logger)

![GitHub Repo stars](https://img.shields.io/github/stars/nfacha/adsb-stats-logger?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/nfacha/adsb-stats-logger?style=social)

[![Discord](https://img.shields.io/discord/933444164379619348)](https://discord.gg/ecyK3y4zTW)
# ADS-B Stats Logger
## Like this project? Don't forget to STAR it and follow it for future releases :)

## Features

- Log all unique flights seen by the ADS-B receiver
- Log all unique operators seen by the ADS-B receiver
- Log the flight with the highest altitude seen by the ADS-B receiver
- Log the flight with the highest speed seen by the ADS-B receiver
- Log the flight the furthest away from the ADS-B receiver
- Log the flight closest from the ADS-B receiver
- Log the flight with the best signal strength seen by the ADS-B receiver
- Log the flight with the worst signal strength seen by the ADS-B receiver
- All data is available in Metric Units (by default) or Imperial Units

## Python Compatibility
This has been tested and confirmed to work on Python 3.10, but should work fine in Python.

## Usage
1. Clone the git repo on your ADS-B server and enter its directory:
```bash
git clone https://github.com/nfacha/adsb-stats-logger.git
cd adsb-stats-logger
```
2. Copy the config file sample:
```bash
cp config.ini.sample config.ini
```
3. Edit the config to your liking, one easy way would be using nano
```bash
nano config.ini
```
4. Edit the config to your liking, one easy way would be using nano
```ini
[PATHS]
DATA_PATH = /run/dump1090-fa/ #The path to your dump1090 logs folder
[LOCATION]
STATION_LAT = 37.7 #Your base station latitude, used for distance calculations
STATION_LNG = 37.7 #Your base station longitude, used for distance calculations
[LOGGING]
SENTRY_DSN =#Sentry DSN for error logging, leave empry to disable
SENTRY_ENVIRONMENT=#Sentry environment, leave empry to disable
LOG_LEVEL = 20 #Log level, see https://docs.python.org/3/library/logging.html#logging-levels
[UNITS]
USE_METRIC_SYSTEM = true #Use metric system for distance calculations, else use caveman units (a.k.a. imperial)
```
5. Leave the script running in the background, one easy way would be to use screen
```bash
screen -S logger -dm python3 logger.py
```
6. By now the script should be running, wait a bit for data to gather and as soon as you have at least one plane in your range it shoudl start to gather data, to see this data use
```bash
python3 show.py
```
You will get an output similar to this:

```
INFO:root:Logging level: 20
INFO:root:Use metric system: True
--- Metrics ---
Data range: 2022-01-07 16:33:15 - 2022-01-07 13:26:54
Unique Flights: 5
Unique Operators: 3
Max Altitude: Flight IBE6317 11.879000304785126 km at 2022-01-07 13:39:43
Max Speed: Flight IBE6501 851.3644 kmh at 2022-01-07 13:36:00
Max Station Distance: Flight RYR28FF 5449.571199579309 km at 2022-01-07 15:34:44
Min Station Distance: Flight SAT571 12.83198307011012 km at 2022-01-07 16:33:14
Max Signal: Flight IBE6317 -16.3 db at 2022-01-07 13:39:43
Min Signal: Flight IBE6501 -24.0 db at 2022-01-07 13:39:43
--- Unique Flights Seen ---
SAT2500 last seen on 2022-01-07 13:26:54
IBE6317 last seen on 2022-01-07 13:39:48
IBE6501 last seen on 2022-01-07 13:39:48
RYR28FF last seen on 2022-01-07 15:40:59
SAT571 last seen on 2022-01-07 16:33:15
--- Unique Operators Seen ---
SAT last seen on 2022-01-07 16:33:15
IBE last seen on 2022-01-07 13:39:48
RYRFF last seen on 2022-01-07 15:40:59

Process finished with exit code 0

```

If you want to see the runtime logs, or to be able to Ctrl-C you can enter the screen with:
```bash
screen -x logger
```

### Inspiration
This was inspired by wesmorgan1's Reddit post: https://www.reddit.com/r/ADSB/comments/rutot0/python3_script_to_profile_dump1090_output_and/