
#from newsapi import NewsApiClient
import smtplib
#from selenium import webdriver
import schedule
import time

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






def Prep(source, querys, filters, locationlist, location, apiuser, recever):

    RedAlert = PrepModule(source,querys,filters, locationlist, location)

    if RedAlert.connectiontest() == False:
        print('No Connection to the internet')
    else:   
        asteroids = RedAlert.asteroid()
        volcanos = RedAlert.volcano()
        solar = RedAlert.Solar()
        weather = RedAlert.Weather()
        #covid = RedAlert.covid()
        outbreaks = RedAlert.outbreak()
        earthquake = RedAlert.earthquake()
        floods = RedAlert.floodwarnings()
        #news = RedAlert.newssearch()
        #resevoir = RedAlert.resevoir_levels()

        email_message = f''' 
{asteroids}
See https://cneos.jpl.nasa.gov/scout/#/ for more details.

{volcanos}

Solar Warnings:
{solar}

{weather}

{outbreaks}

See https://www.who.int/emergencies/disease-outbreak-news for more information
{earthquake}

{floods}
'''

        with smtplib.SMTP("smtp-relay.sendinblue.com", 587) as smtp_server:
                smtp_server.login("danielbenward@gmail.com", "xsmtpsib-8bcb8dec308c2d8d8748ecf8bfd18f61df452bc45c7b6be1ee8bf37dad93cd26-hQHNvbCVrGWZ2IaD")
                smtp_server.sendmail(str(apiuser), str(recever), email_message.encode('utf-8'))


Prep(source, querys, filters, locationlist, location, apiuser, recever)
#if __name__ == "__main__":
#
#    schedule.every().day.at('06:00').do(Prep(source, querys, filters, locationlist, location, apiuser, recever))

#    while True:

#        schedule.run_pending()
#        time.sleep(1)
        

