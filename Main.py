
#from newsapi import NewsApiClient
import smtplib
from selenium import webdriver

from prep import PrepModule

config = open('RedAlert\config.txt')
config = config.readlines()

apikey =config[1].replace('\n', '')

#api= NewsApiClient(api_key = apikey)
source = config[4].split()
#News key words to search by
querys = config[7].split()
#News Filters to filter out unrelated articles
filters = config[10].split()

#Volcano area filter
locationlist =config[13].split()

#location used for flood warnings
location = config[16]

#Email Credentials
apiuser = config[19]
userpass = config[22]
recever = config[25]

browser = webdriver.Firefox()

if __name__ == "__main__":

    RedAlert = PrepModule(source,querys,filters,browser, locationlist, location)

    if RedAlert.connectiontest() == False:
        print('No Connection to the internet')
    else:   
        asteroids = RedAlert.asteroid()
        volcanos = RedAlert.volcano()
        solar = RedAlert.Solar()
        weather = RedAlert.Weather()
        covid = RedAlert.covid()
        outbreaks = RedAlert.outbreak()
        earthquake = RedAlert.earthquake()
        floods = RedAlert.floodwarnings()
        #news = RedAlert.newssearch()

        email_message = f''' 
{asteroids}
See https://cneos.jpl.nasa.gov/scout/#/ for more details

{volcanos}

{solar}

{weather}

{covid}

{outbreaks}

{earthquake}

{floods}
'''

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login(apiuser, userpass)
                smtp_server.sendmail(str(apiuser), str(recever), email_message.encode('utf-8'))
