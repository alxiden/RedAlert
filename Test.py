import json
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver

def Solar(self):
        self.browser.get("https://www.spaceweatherlive.com/en/solar-activity/solar-flares.html")
        solar = self.browser.find_element_by_xpath('//*[@id="ActiveWarnings"]')
        #print(solar)
        solar = solar.text
        XC = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[5]/div[1]/div/table/tbody/tr[3]/td[2]/span')
        Xclass = XC.text

        warning = f'{solar}, the chance of X Class solar storm {Xclass}'

        #print(Xclass, solar)
        #print(warning)
        return warning


def Solar2 ():
    res = requests.get(f'https://www.metoffice.gov.uk/weather/specialist-forecasts/space-weather')
    soup = BeautifulSoup(res.content, 'html.parser')
    text = str(soup.find(class_ = 'space-notifications section'))
    text = text.replace('''<div class="space-notifications section">
<h2>Space weather notifications</h2>
<p>''','')
    text = text.replace('''</p>''','')
    text = text.replace('''</div>''','')
    #posa = text.index('h2.Space weather notifications')
    print(text)

Solar2()