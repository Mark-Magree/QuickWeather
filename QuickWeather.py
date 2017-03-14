#!/usr/bin/env python3
#quickWeather.py - print weather for location
import json, requests, os

#get personal Wunderground api key
keyFile = open(os.path.join(os.path.expanduser('~'), '.WundKey'))
key = keyFile.read().strip()
keyFile.close()

#location settings
state = 'OH'
city = 'Cleveland'

#get json from wunderground
url = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (key, state, city)
response = requests.get(url)
response.raise_for_status()
weatherData = json.loads(response.text)

#all the good stuff is in current_observation
w = weatherData['current_observation']

#output 
print("Current weather conditions for %s" % (w['display_location']['full']))
print(w['observation_time'])
print('Temperature: ' + str(w['temp_f']))
print('Wind: ' + w['wind_string'])

