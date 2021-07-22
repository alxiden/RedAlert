
from newsapi import NewsApiClient
import smtplib
from selenium import webdriver

from prep import PrepModule


browser = webdriver.Firefox()
api= NewsApiClient(api_key = '267427d315da494f9dd6b8c907f394cf')
source = ['BBC-News', 'Independent']
querys =['War','Earthquake', 'EMP', 'Storm', 'virus', 'Nuclear', 'Climate', 'asteroid', 'comet', 'meteors', 'riot', 'volcano', 'inflation']
filters = [
    'war','EMP','EMPs', 'nuclear', 'climate change', 'storm', 'virus outbreak', 'variant',  'asteroid', 'comet', 'meteors', 'riot', 'volcano', 'inflation', 'UK', 'economy',
    'supercell', 'Biosecurity', 'riots', 'dead', 'protesters'
    ]
locationlist =['Italy', 'Iceland', 'Germany', 'France ', 'Northern Atlantic Ocean', 'Spain', 'Spanien', 'Czechia']

#location used for flood warnings
location = 'bs348xt'

#Email stuff
apiuser = 'sender'
userpass = 'password'
recever = ''

if __name__ == "__main__":

    RedAlert = PrepModule(api,source,querys,filters,browser, locationlist, location)

    if RedAlert.connectiontest() == False:
        print('No Connection to the internet')
    else:   
        asteroids = RedAlert.asteroid()
        volcanos = RedAlert.volcano()
        solar = RedAlert.Solar()
        weather = RedAlert.Weather()
        news = RedAlert.newssearch()
        covid = RedAlert.covid()
        outbreaks = RedAlert.outbreak()
        earthquake = RedAlert.earthquake()
        floods = RedAlert.floodwarnings()

        email_message = f''' 
{asteroids}

{volcanos}

{solar}

{weather}

{news}

{covid}

{outbreaks}

{earthquake}

{floods}
'''

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login(apiuser, userpass)
                smtp_server.sendmail(str(apiuser), str(recever), email_message.encode('utf-8'))

