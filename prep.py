import json
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import urllib.request

class PrepModule:

    def __init__(
        self,source, querys, filters, browser, locationlist, location
    ):
        #self.api = api
        self.source = source
        self.querys = querys
        self.filters = filters
        self.browser = browser
        self.locationlist = locationlist
        self.location = location

    def connectiontest(self):
        try:
            urllib.request.urlopen('https://twitter.com/', timeout=8)
            return True
        except:
            return False

    #print news sources availible
    def sources(self):
        news_sources = self.api.get_sources()
        for source in news_sources['sources']:
            print(source['name'])

    #gets local earthquake events
    def earthquake(self):

        res = requests.get("https://www.volcanodiscovery.com/earthquakes/today.html")
        soup = BeautifulSoup(res.content, 'html.parser')
        text = str(soup.select('div.textbox')[0].text)
        x = text.index('...')
        earthq = text[:x]
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
        solarlist = self.browser.find_elements_by_xpath('//*[@class="alertbalk waarschuwing"]')
        if solarlist == []:
            warning =self.browser.find_element_by_xpath('//*[@class="alertbalk waarschuwing2"]')
        else:
            warning = self.browser.find_element_by_xpath('//*[@class="alertbalk waarschuwing"]')
        solar = warning.text

        XC = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[5]/div[1]/div/table/tbody/tr[3]/td[2]/span')
        Xclass = XC.text

        warning = f'{solar}, the chance of X Class solar storm {Xclass}'

        #print(Xclass, solar)
        return warning

    #Gets volcano status for iceland
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
                    #status = (article['title'])
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
        return covidcases

    #WHO watchlist and outbreaks
    def outbreak(self):
        outbreaknews = ''
        today = date.today()
        d1 = today.strftime('''%Y''')
        d2 = today.strftime('''%B''')
        res = requests.get('https://www.who.int/emergencies/disease-outbreak-news')
        soup = BeautifulSoup(res.content, 'html.parser')
        #print(soup)
        outbreaklist = str(soup.find_all(class_ = 'sf-list-vertical__title'))
        outbreaklist = outbreaklist.replace('</h4>, <h4 class="sf-list-vertical__title">', "")
        outbreaklist = outbreaklist.replace('<span>', '')
        outbreaklist = outbreaklist.replace('<span aria-hidden="true" class="full-title" style="display: none">', '')
        outbreaklist = outbreaklist.replace('<span class="trimmed">',"")
        outbreaklist = outbreaklist.replace('</span>', "")
        outbreaklist = outbreaklist.replace('</h4>]', '')
        outbreaklist = outbreaklist.replace('[<h4 class="sf-list-vertical__title">', '')

        outbreaklist = outbreaklist.split('|')
        #print(outbreaklist)
        for o in outbreaklist:
            o = o.replace('\n', '')
            #print(o)
            event = o
            if str(d1) not in event:
                break 
            event = event.replace('Disease Outbreak News', ' ')
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
            asteroids.append(f'{name} has a TS of {ts} (1-10)')   

        res = requests.get('https://ssd-api.jpl.nasa.gov/scout.api')
        data = res.json()
        for item in data['data']:
            if item['rating'] == '0' or item['rating'] == None:
                pass
            else:
                o = item['objectName']
                s = item['rating']
                asteroids.append(f'Object {o} has a impact score {s} (0-4)')
        return asteroids

    def floodwarnings(self):
        res = requests.get(f'https://check-for-flooding.service.gov.uk/location?q={self.location}#outlook')
        soup = BeautifulSoup(res.content, 'html.parser')
        #print(soup)
        data = str(soup.find_all(class_ = "govuk-body"))
        #print(data)
        x = data.index('The flood risk for')
        y = data.rindex('</p>')
        data = data[x:y]
        data = data.replace('<p>', '')
        data = data.replace('</p>', '')
        data = data.replace('<span>', '')
        data = data.replace('</span>', '')
        return data
