#!/usr/bin/env python3
#quickWeather.py - print weather for location
import json, requests, os, sys
from PIL import Image, ImageDraw, ImageFont

height, width = 550, 800

#first take cli args, then ask for city/state if none
if len(sys.argv) > 2:
    city = ' '.join(sys.argv[1:-1])
    state = sys.argv[-1]
else:
    city = input('City: ')
    state = input('State: ')

#get personal Wunderground api key from home folder
keyFile = open(os.path.join(os.path.expanduser('~'), '.WundKey'))
key = keyFile.read().strip()
keyFile.close()

#get info and radar from wunderground
#forecastUrl = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (key, state, city)
radarUrl = 'http://api.wunderground.com/api/%s/radar/q/%s/%s.gif?width=%s&height=%s&newmaps=1' % (key, state, city, width, height)
#resForecast = requests.get(forecastUrl)
#resForecast.raise_for_status()
resRadar = requests.get(radarUrl)
resRadar.raise_for_status()

#save radar file
imgFile = open('RadarForecast.gif', 'wb')
for chunk in resRadar.iter_content(100000):
    imgFile.write(chunk)
imgFile.close()

#prepare data for radar text

#reopen radar and prepare to add text
img = Image.open('RadarForecast.gif')
draw = ImageDraw.Draw(img)
fontsFolder = os.path.join('/','usr','share','fonts','ttf')
droidFont = ImageFont.truetype(os.path.join(fontsFolder, 'DroidSans.ttf'), 32)

#add text to radar
draw.text((40, 50), 'TEMpeRaTure Is fun egrees', fill='purple', font=droidFont)


#save final image
img.show()
#img.save('RadarForecast.gif')
