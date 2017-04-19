#!/usr/bin/env python3
#quickWeather.py - by Mark Magree
#show radar with imposed forecast discussion
#Usage: QuickWeather.py [city state]
#if no command line arguments are given, QuickWeather will ask

import json, requests, os, sys
from PIL import Image, ImageDraw, ImageFont

fontSize = 16
height, width = 750, 1200


#TODO : ADD WARNINGS


#first take cli args, then ask for city/state if none
if len(sys.argv) > 2 and not \
        str(' '.join(sys.argv[-2:])).lower() in\
        ['new york','new hampshire','new mexico',\
        'north carolina','north dakota',\
        'south carolina','south dakota',\
        'west virginia','new jersey']:
    city = ' '.join(sys.argv[1:-1])
    state = sys.argv[-1]
elif len(sys.argv) > 2 and \
        str(' '.join(sys.argv[-2:])).lower() in\
        ['new york','new hampshire','new mexico',\
        'north carolina','north dakota',\
        'south carolina','south dakota',\
        'west virginia','new jersey']:
    city = ' '.join(sys.argv[1:-2])
    stateLong = ' '.join(sys.argv[-2:])
    with open('statelist.json') as json_data:
        d = json.load(json_data)
        state = d[stateLong.title()]
else:
    city = input('City: ')
    state = input('State: ')

#get personal Wunderground api key from home folder
keyFile = open(os.path.join(os.path.expanduser('~'), '.WundKey'))
key = keyFile.read().strip()
keyFile.close()

#get info and radar from wunderground
forecastUrl = 'http://api.wunderground.com/api/%s/forecast/q/%s/%s.json' % (key, state, city)
radarUrl = 'http://api.wunderground.com/api/%s/radar/q/%s/%s.png?width=%s&height=%s&newmaps=1' % (key, state, city, width, height)
resForecast = requests.get(forecastUrl)
resForecast.raise_for_status()
resRadar = requests.get(radarUrl)
resRadar.raise_for_status()

#save radar file
imgFile = open('RadarForecast.png', 'wb')
for chunk in resRadar.iter_content(100000):
    imgFile.write(chunk)
imgFile.close()

#convert and prepare JSON data
rawData = json.loads(resForecast.text)
try:
    data = rawData['forecast']['txt_forecast']['forecastday']
except KeyError:
    print("Location not found")
    sys.exit()

#prepare data for radar text
times = {'today':[],'tonight':[],'tomorrow':[],'tomNight':[]}
t = 0 #right now is 0
for d in times.values():
    d.append(data[t]['title'])
    for s in data[t]['fcttext'].split('. '):
        d.append(s)
    t += 1

#reopen radar image and prepare to add text
img = Image.open('RadarForecast.png').convert('RGBA')
draw = ImageDraw.Draw(img)
fontsFolder = os.path.join('/','usr','share','fonts','ttf')
droidFont = ImageFont.truetype(os.path.join(fontsFolder, 'DroidSans.ttf'), fontSize)

#add text to radar
def placeText(data):
    draw.text((x, y), data, fill='white', font=droidFont)
x,y = 30,10
for i in times['today']:
    placeText(i)
    y = y + fontSize + 10
x,y = 30, height - ((10 + fontSize) * len(times['tomorrow']))
for i in times['tonight']:
    placeText(i)
    y = y + fontSize + 10
x,y = width - 360,10
for i in times['tomorrow']:
    placeText(i)
    y = y + fontSize + 10
x,y = width - 360, height - ((10 + fontSize) * len(times['tomNight']))
for i in times['tomNight']:
    placeText(i)
    y = y + fontSize + 10


#save final image
del draw
os.remove('RadarForecast.png')
img.save('RadarForecastInfo.png')
img.show()
