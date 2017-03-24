#!/usr/bin/env python3
#quickWeather.py - print weather for location
import json, requests, os, sys
from PIL import Image, ImageDraw, ImageFont

fontSize = 16
height, width = 750, 1200

#get list of states from file
#dict from file to save script space

'''
with open('statelist.json') as json_data:
    d = json.load(json_data)
    state = stateFull
    print(d[state.title()])
'''

#first take cli args, then ask for city/state if none
if len(sys.argv) > 2 and not sys.argv[-2].lower() == 'new':
    city = ' '.join(sys.argv[1:-1])
    state = sys.argv[-1]
elif len(sys.argv) > 2 and sys.argv[-2].lower() == 'new':
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
radarUrl = 'http://api.wunderground.com/api/%s/radar/q/%s/%s.gif?width=%s&height=%s&newmaps=1' % (key, state, city, width, height)
resForecast = requests.get(forecastUrl)
resForecast.raise_for_status()
resRadar = requests.get(radarUrl)
resRadar.raise_for_status()

#save radar file
imgFile = open('RadarForecast.gif', 'wb')
for chunk in resRadar.iter_content(100000):
    imgFile.write(chunk)
imgFile.close()

#convert and prepare JSON data
rawData = json.loads(resForecast.text)
data = rawData['forecast']['txt_forecast']['forecastday']

#prepare data for radar text
times = {'today':[],'tonight':[],'tomorrow':[],'tomNight':[]}
t = 0 #right now is 0
for d in times.values():
    d.append(data[t]['title'])
    for s in data[t]['fcttext'].split('. '):
        d.append(s)
    t += 1

#reopen radar image and prepare to add text
img = Image.open('RadarForecast.gif').convert('RGBA')
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
os.remove('RadarForecast.gif')
img.save('RadarForecastInfo.gif')
img.show()
