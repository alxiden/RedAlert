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
        posa = text.index('Latest quake:')
        posb = text.index('Strongest quake today:')
        posc = text.index(' Past 7 days:')
        latest = text[posa:posb]
        strongest = text[posb:posc]
        earthq = (latest + strongest)
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
        solar = self.browser.find_element_by_xpath('//*[@id="ActiveWarnings"]')
        #print(solar)
        solar = solar.text
        XC = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[5]/div[1]/div/table/tbody/tr[3]/td[2]/span')
        Xclass = XC.text

        warning = f'{solar}, the chance of X Class solar storm {Xclass}'

        #print(Xclass, solar)
        #print(warning)
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
        volcanolevel = len(volcanosstaus)
        vol = f'Volcano alert level scale of 1 to 20: {volcanolevel}'
        return vol

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
        self.browser.close()
        return outbreaknews

    #nasa scout and sentery to monitor near earth objects
    def asteroid(self):
        chance = 1
        asteroids =''
        res = requests.get('https://ssd-api.jpl.nasa.gov/sentry.api?all=1&days=7')
        data  = res.json()
        for item in data['data']:
            if item['ts'] == '0' or item['ts'] == None:
                pass
            else:
                name = item['fullname']
                ts = item['ts'] 
                tsi = int(ts)  
                if tsi in range(0,5):
                    chance = chance + tsi
                elif tsi in range(5,8):
                    chance = chance + (tsi * 5)
                elif tsi in range(8,11):
                    chance = chance + (tsi * 10)
                

        res = requests.get('https://ssd-api.jpl.nasa.gov/scout.api')
        data = res.json()
        for item in data['data']:
            if item['rating'] == '0' or item['rating'] == None:
                pass
            else:
                ir = item['rating']
                if ir == '1' or ir == '2':
                    chance = chance + 1
                elif ir == '3' or ir == '4':
                    chance = chance + (ir * 5)

        asteroids = f'Chance of an asteroid strike in the near future {chance}%'
        return asteroids

    #local flood warnings by postcode
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

    #south west resovoir levels used to monitor possible water shortages
    def resevoir_levels(self):
        res = requests.get('https://www.southwestwater.co.uk/environment/a-precious-resource/current-reservoir-storages/')
        soup = BeautifulSoup(res.content, 'html.parser')
        #code = open("test.txt","w+")
        #code.write(str(soup))
        data = str(soup)
        x1 = data.index('Total reservoir storage for the week')
        y1 = data.index('</tbody>')
        data = data[x1:y1]
        data = data.replace('</td>', '')
        data = data.replace('<td style="width: 27.78%; height: 18px; background-color: #eaeaea;">', '')
        data = data.replace('</tr>', '')
        return data
        #print(data)
        
