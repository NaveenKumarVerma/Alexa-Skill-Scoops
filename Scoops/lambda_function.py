from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import time
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
ask = Ask(app, "/")
newsDictionary = {
        'success': True,
        'data': []
    }
news_string = ''
# @app.route('/')
# def homepage():
#     return "hi there, how ya doin?"

@app.route('/')
@ask.launch
def start_skill():
    welcome_message = 'Welcome to ShortBuzz .................'
    next_message = 'here are top News....................'

    return statement(welcome_message + next_message + speak_news() )

def get_new_data():
    global newsDictionary
    try:
        htmlBody = requests.get('https://www.inshorts.com/en/read/')
    except requests.exceptions.RequestException as e:
        newsDictionary['success'] = False
        newsDictionary['errorMessage'] = str(e.message)
        return newsDictionary

    soup = BeautifulSoup(htmlBody.text, 'lxml')
    newsCards = soup.find_all(class_='news-card')
    if not newsCards:
        newsDictionary['success'] = False
        newsDictionary['errorMessage'] = 'Invalid Category'
        return newsDictionary

    for card in newsCards:
        try:
            title = card.find(class_='news-card-title').find('a').text
        except AttributeError:
            title = None

        newsObject = {
            'title': title,
        }

        newsDictionary['data'].append(newsObject)

    return newsDictionary

def get_news_content():
    global newsDictionary
    global news_string
    if newsDictionary.get('success'):
        data = newsDictionary.get('data')
        count = 1
        for item in data:
            if count == 1:
                news_string +="1st ......"
            elif count == 2:
                news_string +="2nd ......"
            elif count == 3:
                news_string +="3rd ......"
            else:
                news_string +=str(count)+"th ......"
            news_string +=item.get('title')
            news_string += "\n"
            count +=1
    else:
        news_string = 'Sorry ......... i am facing some technical issue......... please try again after some time'

get_new_data()
get_news_content()
def speak_news():
    global news_string
    return news_string

if __name__ == '__main__':
    app.run(debug=True)

