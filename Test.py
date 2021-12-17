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
        #print(soup)
        outbreaklist = str(soup.find_all(class_ = 'trimmed'))
        print(outbreaklist)
        #print(type(outbreaklist))
        outbreaklist = outbreaklist.split('<span class="trimmed">')
        #print(outbreaklist)
        for o in outbreaklist[0:4]:
            event = o.replace('\n', '')
            #print(f'{event} is made')
            if '</span>' in event:
                event = event.replace('''</span>''', '')
                event = event.replace(',','')
                #print(f'{event} was added')
                outbreaknews.append(event)
                #print(event)
            else:
                pass
        browser.close()


        print(outbreaknews)


outbreak(browser)