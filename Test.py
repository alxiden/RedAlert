import json
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import smtplib

def volcano(self):
        res = requests.get('https://www.volcanodiscovery.com/erupting_volcanoes.html')
        soup = BeautifulSoup(res.content, 'html.parser')

        volcanosstaus = []
        volcanoraw = str(soup.find_all(class_ = 'red'))
        volcanolist = volcanoraw.split('</li>')
        for item in volcanolist:
            if 'unrest' in item:
                status = 'unrest'
            elif 'minor activity / eruption warning' in item:
                status = 'minor activity / eruption warning'
            elif 'erupting' in item:
                status = 'erupting'
            else:
                status = 'unknown'
            if '.html' not in item:
                pass
            else:
                x = item.index('.html')
                y = item.index('href="')
                name = item[y:x]
                name = name.replace('href="', '')
                x = item.index(')')
                y = item.index('(')
                vollocation = item[y:x]
                volcanostat = f'{name} in {vollocation}) is currently {status}' 
                for l in self.locationlist:
                    if volcanostat in volcanosstaus:
                        pass
                    elif l in vollocation:
                        volcanosstaus.append(volcanostat)
                    elif l not in vollocation:
                        pass
                    else:
                        volcanosstaus.append(f'{name} is Unknown')
        volcanolevel = len(volcanosstaus)
        vol = f'Volcano alert level scale of 1 to 20: {volcanolevel}'
        print(vol)
        return vol

volcano()

