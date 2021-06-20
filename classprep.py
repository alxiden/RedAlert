
import json
import time
from datetime import date
import requests
from bs4 import BeautifulSoup

import requests
from selenium import webdriver

class PrepModule:

    def __init__(
        self,api,volcanosa,volcanosb,volcanosc,source, querys, filters, browser
    ):
        self.api = api
        self.volcanosa = volcanosa
        self.volcanosb = volcanosb
        self.volcanosc = volcanosc
        self.source = source
        self.querys = querys
        self.filters = filters
        self.browser = browser


    #print news sources availible
    def sources(self):
        news_sources = self.api.get_sources()
        for source in news_sources['sources']:
            print(source['name'])

    #gets local earthquake events
    def earthquake(self):

        res = requests.get("https://www.volcanodiscovery.com/earthquakes/today.html")
        soup = BeautifulSoup(res.content, 'html.parser')
        text = soup.select('div.textbox')[0].text
        earthq = text
        return earthq
    
    #gets local weather events
    def Weather(self):
        today = date.today()
        today = today.day
        #print(today)
        res = requests.get(f'https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-warnings#?date={today}')
        soup = BeautifulSoup(res.content, 'html.parser')
        weather = soup.select('div.tab-warning')[0].text
        return weather

    #Checks the sun for solar activity
    def Solar(self):
        self.browser.get("https://www.spaceweatherlive.com/en/solar-activity/solar-flares.html")

        warning = self.browser.find_element_by_xpath('//*[@class="alertbalk waarschuwing"]')
        solar = warning.text

        XC = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[5]/div[1]/div/table/tbody/tr[3]/td[2]/span')
        Xclass = XC.text

        warning = solar + Xclass

        #print(Xclass, solar)
        self.browser.close()
        return warning

    #Gets volcano status for iceland
    def volcano(self):
        volcanosstaus = []
        res = requests.get('https://www.volcanodiscovery.com/volcanoes/indonesia/sumatra/toba/')
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.select('b')[6].text
        if title == 'normal or dormant':
            pass
        else:
            volcanosstaus.append(f'toba is currently {title}')

        for v in self.volcanosa:
            a = 6
            if v == 'Bardarbunga' or v == 'etna':
                a = 7
            elif v == 'campocalatrava':
                a = 4
            res = requests.get(f'https://www.volcanodiscovery.com/{v.lower()}.html')
            soup = BeautifulSoup(res.content, 'html.parser')
            title = soup.select('b')[a].text
            if title == 'normal or dormant':
                pass
            else:
                volcanosstaus.append(f'{v} is currently {title}')
        for v in self.volcanosb:
            if v == 'Snaefellsjokull':
                res = requests.get('https://www.volcanodiscovery.com/iceland/snaefellsjoekull/')
                soup = BeautifulSoup(res.content, 'html.parser')
                title = soup.select('b')[5].text
            else:
                res = requests.get(f'https://www.volcanodiscovery.com/iceland/{v.lower()}.html')
                soup = BeautifulSoup(res.content, 'html.parser')
                title = soup.select('b')[5].text
            if title == 'normal or dormant':
                pass
            else:
                volcanosstaus.append(f'{v} is currently {title}')
        for v in self.volcanosc:
            res = requests.get(f'https://www.volcanodiscovery.com/volcanoes/europe/iceland/{v.lower()}/')
            soup = BeautifulSoup(res.content, 'html.parser')
            title = soup.select('b')[5].text
            if title == 'normal or dormant':
                pass
            else:
                volcanosstaus.append(f'{v} is currently {title}')
        return volcanosstaus

    #Searches news outlets
    def newssearch(self):
        news = []
        with open ('newsstorage.txt', 'r') as f:
            newsStorage = json.load(f)
        #print(newsStorage)
        for sou in self.source:
            #print(sou)
            for que in self.querys:
                #print(que)
                all_articles = self.api.get_everything(
                    q= str(que),
                    sources = str(sou),
                    language= 'en',
                )

                for article in all_articles['articles']:
                    #title = (article['title'])
                        if article['title'] in newsStorage:
                            #print(f'{title} is in storage')
                            pass
                        else:
                            for gfil in self.filters:
                                if gfil.lower() not in article['title'].lower():
                                    #print(f'{title} did not contain {gfil} ')
                                    pass
                                else:
                                #print(f'added {title}')
                                    news.append(article['title'])
                                    newsStorage.append(article['title'])
        with open ('newsstorage.txt', 'w') as f:
            json.dump(newsStorage, f, indent= 2)
        return news

    #local covid cases
    def covid(self):
        self.browser.get("https://www.covidlive.co.uk/")
        time.sleep(4)
        self.browser.find_element_by_xpath('//*[@id="South-Gloucestershire"]').click()
        time.sleep(1)
        covidcases = self.browser.find_element_by_xpath('/html/body/div/div[1]/div[3]/div/div/p[1]').text
        self.browser.close()
        return covidcases

    #WHO watchlist and outbreaks
    def outbreak(self):
        outbreaknews = ''
        today = date.today()
        d1 = today.strftime('''%Y''')
        d2 = today.strftime('''%B''')
        self.browser.get("https://www.who.int/emergencies/disease-outbreak-news")
        outbreaklist = self.browser.find_elements_by_class_name('sf-list-vertical__item')
        for o in outbreaklist:
            event = o.text
            if str(d1) not in event:
                break 
            event = event.replace('Disease Outbreak News', '')
            if str(d1) not in event:
                pass
            elif event == '':
                pass
            elif str(d2) in event:
                outbreaklist.append(event)
                #print(event)
            else:
                pass
        if outbreaknews == '':
            outbreaknews = ['No new outbreaks!']

        self.browser.close()

        return outbreaknews

    def asteroid(self):
        asteroids =[]
        res = requests.get('https://ssd-api.jpl.nasa.gov/sentry.api?all=1&days=7')
        data  = res.json()
        for item in data['data']:
            if item['ts'] == '0':
                pass
        else:
            name = item['fullname']
            ts = item['ts']
            asteroids.append(f'{name} has a TS of {ts}')   

        res = requests.get('https://ssd-api.jpl.nasa.gov/scout.api')
        data = res.json()
        for item in data['data']:
            if item['rating'] == '0' or item['rating'] == None:
                pass
            else:
                o = item['objectName']
                s = item['rating']
                asteroids.append(f'Object {o} has a impact score {s}')
        return asteroids
