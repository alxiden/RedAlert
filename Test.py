import json
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver

browser = webdriver.Firefox()

def outbreak(browser):
        outbreaknews = []
        res = requests.get('https://www.who.int/emergencies/disease-outbreak-news')
        soup = BeautifulSoup(res.content, 'html.parser')
        outbreaklist = str(soup.find_all(class_ = 'trimmed'))
        outbreaklist = outbreaklist.split('<span class="trimmed">')
        for o in outbreaklist[0:4]:
            event = o.replace('\n', '')
            if '</span>' in event:
                event = event.replace('''</span>''', '')
                event = event.replace(',','')
                outbreaknews.append(event)
            else:
                pass
        browser.close()
        return outbreaknews


outbreak(browser)