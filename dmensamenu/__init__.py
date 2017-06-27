import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from subprocess import Popen, PIPE

def getmeals(day):
    meals = []
    page = requests.get('http://stw.uni-heidelberg.de/de/speiseplan').text
    html = BeautifulSoup(page, 'html.parser')
    h2 = html.body.find('h2', text='Mensa Im Neuenheimer Feld 304')
    for h4 in h2.find_next_sibling('div').find_all('h4'):
        if datetime.strptime(h4.text.split(' ')[1], '%d.%m.%Y').date() == day:
            for tr in h4.next_sibling.find_all('tr'):
                tds = tr.find_all('td')
                if tds:
                    meal = ' '.join(tds[0].text.split()) # replace any whitespaces by a single ' '
                    output = tds[1].text
                    price = tds[2].text
                    text = output
                    text += ' ' * (5 - len(text))
                    text += price
                    text += ' ' * (12 - len(text))
                    text += meal
                    meals.append(text)
    return meals

def showmeals(meals):
    p = Popen(['dmenu', '-l', str(len(meals))], stdin=PIPE)
    p.communicate(input=str.encode('\n'.join(meals)))

def main():
    daytoshow = date.today()
    if (datetime.now().hour >= 14): # canteen closes at 14:00, show tomorrow's menu instead
        daytoshow += timedelta(days=1)

    meals = getmeals(daytoshow)
    showmeals(meals)
