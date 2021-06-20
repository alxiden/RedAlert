
from newsapi import NewsApiClient
from classprep import PrepModule
import smtplib
from selenium import webdriver

browser = webdriver.Firefox()
api= NewsApiClient(api_key = '267427d315da494f9dd6b8c907f394cf')
source = ['BBC-News', 'Independent']
querys =['War','Earthquake', 'EMP', 'Storm', 'virus', 'Nuclear', 'Climate', 'asteroid', 'comet', 'meteors', 'riot', 'volcano', 'inflation']
filters = [
    'war','EMP','EMPs', 'nuclear', 'climate change', 'storm', 'virus outbreak', 'variant',  'asteroid', 'comet', 'meteors', 'riot', 'volcano', 'inflation', 'UK', 'economy',
    'supercell', 'Biosecurity', 'riots', 'dead', 'protesters'
    ]

#volcanos
volcanosa = [
    'Askja', 'Bardarbunga','brennisteinsfjoell', 'Eldey','grimsnes', 'grimsvoetn', 'heidarspordar', 'Hekla', 'Helgrindur', 'Hengill', 'Herdubreid','hromundartindur',
    'Hveravellir', 'Katla', 'Kolbeinsey-Ridge','kverkfjoell', 'Prestahnukur', 'Reykjanes', 'Thordarhyrna','tindfjallajoekull', 'tjoernes-fracture-zone','tungnafellsjoekull',
    'Vatnafjoell', 'taupo','etna','chainedespuys', 'olot_field','laacher_see', 'cheb', 'monte-albano-volcano', 'vesuvius', 'campi-flegrei', 'ischia-volcano',
    'yellowstone']
volcanosb = [  'eyjafjallajoekull', 'Fremrinamur','Krafla','krisuvik', 'oeraefajoekull','Snaefellsjokull','Theistareykjarbunga', 'torfajoekull',]
volcanosc = ['esjufjoell','Hofsjoekull','Kerlingarfjoell', 'langjoekull', 'ljosufjoell', 'loki-foegrufjoell','Lysuholl',]

#Email stuff
apiuser = 'email'
userpass = 'password'
recever = 'reciving email'

if __name__ == "__main__":

    RedAlert = PrepModule(api,volcanosa,volcanosb,volcanosc,source,querys,filters,browser)

    asteroids = RedAlert.asteroid
    volcanos = RedAlert.volcano()
    solar = RedAlert.Solar
    weather = RedAlert.Weather
    news = RedAlert.newssearch()
    covid = RedAlert.covid()
    outbreaks = RedAlert.outbreak

    email_message = f''' 
{asteroids}
{volcanos}
{solar}
{weather}
{news}
{covid}
{outbreaks}
'''

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(apiuser, userpass)
            smtp_server.sendmail(str(apiuser), str(recever), email_message.encode('utf-8'))
