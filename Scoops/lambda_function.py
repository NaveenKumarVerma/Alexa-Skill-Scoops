# from flask import Flask
# from flask_ask import Ask, statement, question, session
# import json
# import time
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)
# ask = Ask(app, "/")
# newsDictionary = {
#         'success': True,
#         'data': []
#     }
# news_string = ''
# @app.route('/')
# def homepage():
#     return "hi there, how ya doin?"

# @ask.launch
# def start_skill():
#     welcome_message = 'Welcome to ShortBuzz .................'
#     next_message = 'here are top News....................'

#     return statement(welcome_message + next_message + speak_news() )

# def get_new_data():
#     global newsDictionary
#     try:
#         htmlBody = requests.get('https://www.inshorts.com/en/read/')
#     except requests.exceptions.RequestException as e:
#         newsDictionary['success'] = False
#         newsDictionary['errorMessage'] = str(e.message)
#         return newsDictionary

#     soup = BeautifulSoup(htmlBody.text, 'lxml')
#     newsCards = soup.find_all(class_='news-card')
#     if not newsCards:
#         newsDictionary['success'] = False
#         newsDictionary['errorMessage'] = 'Invalid Category'
#         return newsDictionary

#     for card in newsCards:
#         try:
#             title = card.find(class_='news-card-title').find('a').text
#         except AttributeError:
#             title = None

#         newsObject = {
#             'title': title,
#         }

#         newsDictionary['data'].append(newsObject)

#     return newsDictionary

# def get_news_content():
#     global newsDictionary
#     global news_string
#     if newsDictionary.get('success'):
#         data = newsDictionary.get('data')
#         count = 1
#         for item in data:
#             if count == 1:
#                 news_string +="1st ......"
#             elif count == 2:
#                 news_string +="2nd ......"
#             elif count == 3:
#                 news_string +="3rd ......"
#             else:
#                 news_string +=str(count)+"th ......"
#             news_string +=item.get('title')
#             news_string += "\n"
#             count +=1
#     else:
#         news_string = 'Sorry ......... i am facing some technical issue......... please try again after some time'

# get_new_data()
# get_news_content()
# def speak_news():
#     global news_string
#     return news_string

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
# import unidecode
# import pygame
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
ask = Ask(app, "/")
category = ['national', 'business', 'sports', 'world', 'politics', 'technology', 'startup', 'entertainment', 'miscellaneous', 'science']
selected_category = ''
newsDictionary = {
        'success': True,
        'data': []
    }
news_string = ''
@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    # welcome_message = 'Welcome to this amazing skill, Would you like to hear Rick And Morty Quotes??'
    hi = 'Hey do you want to hear news'
    return question(hi)

def get_new_data():
    global newsDictionary
    try:
        if selected_category:
            htmlBody = requests.get('https://www.inshorts.com/en/read/'+selected_category)
            print 'https://www.inshorts.com/en/read/'+selected_category
        else:
            htmlBody = requests.get('https://www.inshorts.com/en/read')
            print 'https://www.inshorts.com/en/read'
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

        # try:
        #     content = card.find(class_='news-card-content').find('div').text
        # except AttributeError:
        #     content = None

        # try:
        #     date = card.find(clas='date').text
        # except AttributeError:
        #     date = None

        # try:
        #     time = card.find(class_='time').text
        # except AttributeError:
        #     time = None

        newsObject = {
            'title': title,
            # 'content': content,
            # 'date': date,
            # 'time': time,
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
        news_string = 'Sorry Due to some error I am unable to fetch news'

@ask.intent("YesIntent")
def share_headlines():
    category_str = ''
    
    # quote_msg = 'Listen, Jerry, I don\'t want to overstep my bounds or anything.It\'s your house. It\'s your world. You\'re a real Julius Caesar, but I\'ll tell\
    #              you some, tell you how-how I feel about school, Jerry. It\'s a waste of time, a bunch of people running around, bumping into each other. \
    #              G-guy up front says, two plus two. The people in the back say, four.Then the bell rings, and they give you a carton of milk and a piece of\
    #              paper that says you can take a dump or something.\
    #              I mean, it\'s it\'s not a place for smart people, Jerry, and I know that\'s not a popular opinion,\
    #              but it\'s my two cents on the issue. '

    # pygame.mixer.init()
    # pygame.mixer.music.load("love.mp3")
    # pygame.mixer.music.play()

    # # time.sleep(20)
    # pygame.mixer.init()
    # pygame.mixer.music.load("last_song.mp3")
    # pygame.mixer.music.play()
    # return statement(news_string)
    ques_start_str = "which category news do you want to here from the follwoing category\n\n\n\n"
    for item in category:
        category_str += item+'\n\n\n'
    return question(ques_start_str + category_str)


def speak_news():
    global news_string
    get_new_data()
    get_news_content()
    return news_string

@ask.intent("NationalCategoryIntent")
def national_category_intent():
    global selected_category
    selected_category = 'national'
    return statement(speak_news())

@ask.intent("BusinessCategoryIntent")
def business_category_intent():
    global selected_category
    selected_category = 'business'
    return statement(speak_news())

@ask.intent("SportsCategoryIntent")
def sports_category_intent():
    global selected_category
    selected_category = 'sports'
    return statement(speak_news())

@ask.intent("WorldCategoryIntent")
def world_category_intent():
    global selected_category
    selected_category = 'world'
    return statement(speak_news())

@ask.intent("PoliticsCategoryIntent")
def politics_category_intent():
    global selected_category
    selected_category = 'politics'
    return statement(speak_news())

@ask.intent("TechnologyCategoryIntent")
def technology_category_intent():
    global selected_category
    selected_category = 'technology'
    return statement(speak_news())

@ask.intent("StartupCategoryIntent")
def startup_category_intent():
    global selected_category
    selected_category = 'startup'
    return statement(speak_news())

@ask.intent("EntertainmentCategoryIntent")
def entertainment_category_intent():
    global selected_category
    selected_category = 'entertainment'
    return statement(speak_news())

@ask.intent("MiscellaneousCategoryIntent")
def miscellaneous_category_intent():
    global selected_category
    selected_category = 'miscellaneous'
    return statement(speak_news())

@ask.intent("ScienceCategoryIntent")
def science_category_intent():
    global selected_category
    selected_category = 'science'
    return statement(speak_news())


@ask.intent("NoIntent")
def no_intent():
    # bye_text = 'I am not sure what you disliked about me... well it was nice meeting you bye'
    # return statement(bye_text)
    # pygame.mixer.init()
    # pygame.mixer.music.load("oh_man.wav")
    # pygame.mixer.music.play()
    return statement("bye")
if __name__ == '__main__':
    app.run(debug=True)
