import praw
import chromedriver_binary
import string
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import math
import matplotlib.pyplot as plt
import datetime as dt
from datetime import date
import pandas as pd
import numpy as np
import csv


#nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')

#praw
reddit = praw.Reddit(client_id='lELNGnTUoXms4Q', client_secret='vjkYp6AJfkA4lHRaiA_S2KkTQl_ndQ', user_agent='DD Analysis')

#reddit scraping data
subs = ['investing','stocks','wallstreetbets','stockmarket','options','securityanalysis','eupersonalfinance','cryptocurrency']
keyword=['dd', 'analysis']
excluded=['reddit', 'ladder','add', 'added' ]

#Yahoo finance
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
pd.options.display.float_format = '{:.0f}'.format

DRIVER_PATH = "C:\\Users\\Shane\\proj\\chromedriver"
BASE_URL = 'https://finance.yahoo.com/quote/'

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


#start of program
financials=input("Would you like to check financials? (y/n)")
tick=input("Please enter ticker symbol (leave blank for all)")




def getYahooFinancePrice():
    driver.get(BASE_URL+tick.upper())
    html = driver.execute_script('return document.body.innerHTML;')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    price = [entry.text for entry in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
    print(price)


def searchAllTickers():
    list1 =[]
    with open('Ticker/amex.csv','rt')as f:
        for row in f:
            list1.append(row.split(',')[0])
    res = list1[1:]  

    list2 =[]
    with open('Ticker/nyse.csv','rt')as f:
        for row in f:
            list2.append(row.split(',')[0])
    res2 = list2[1:]  

    list3 =[]
    with open('Ticker/nasdaq.csv','rt')as f:
        for row in f:
            list3.append(row.split(',')[0])
    res3 = list3[1:] 

    suprList=str(res)+str(res2)+str(res3)
    #print(suprList)

    submission_statistics = []
    d = {}
    for sub in subs:
        getNew = reddit.subreddit(sub).new(limit=None)
        lst = []
        test = ''
        for post in getNew:
                if 'dd' in post.title.lower() and 'add' not in post.title.lower()and 'added' not in post.title.lower()and 'ladder' not in post.title.lower() and 'reddit' not in post.title.lower()  and '?' not in post.title.lower() and any(tic in post.title for tic in suprList):
                    print (post.title)
                    text = post.selftext
                    length = round((len(text)/40000)*100)
                    line = post.title + ' -' + str(length) + '%'
                    lst.append(line)
                    d = {}
                    d['sub'] = sub
                    d['num_comments'] = post.num_comments
                    d['comment_sentiment_average'] = commentSentiment(sub, post.url)
                    d['name'] = post.title
                    if d['comment_sentiment_average'] == 0.000000:
                        continue
                    d['latest_comment_date'] = latestComment(sub, post.url)
                    d['score'] = post.score
                    d['upvote_ratio'] = post.upvote_ratio
                    d['date'] = post.created_utc
                    d['domain'] = post.domain
                    d['num_crossposts'] = post.num_crossposts
                    d['author'] = post.author
                    d['length'] = str(length)+'%'
                    d['link'] = post.url
                    
                    submission_statistics.append(d)
        print(*lst, sep="\n")
        if lst != []:
            dfSentimentStocks = pd.DataFrame(submission_statistics)

            _timestampcreated = dfSentimentStocks["date"].apply(get_date)
            dfSentimentStocks = dfSentimentStocks.assign(timestamp = _timestampcreated)

            _timestampcomment = dfSentimentStocks["latest_comment_date"].apply(get_date)
            dfSentimentStocks = dfSentimentStocks.assign(commentdate = _timestampcomment)

            dfSentimentStocks.sort_values("latest_comment_date", axis = 0, ascending = True,inplace = True, na_position ='last') 

            dfSentimentStocks


            dfSentimentStocks.author.value_counts()

            today = date.today()
            d1 = today.strftime("%d_%m_%Y")

            dfSentimentStocks.to_csv(f'All_Tickers\ALL_Reddit_Sentiment_Equity_{d1}.csv', index=False)
        else:
            print('no post found in r/' + sub)
            


def searchSpecificTick():
    submission_statistics = []
    d = {}
    for sub in subs:
        getNew = reddit.subreddit(sub).new(limit=None)
        lst = []
        test = ''
        for post in getNew:
            for key in keyword:

                if key in post.title.lower() and tick in post.title.lower() and 'add' not in post.title.lower()and 'added' not in post.title.lower()and 'ladder' not in post.title.lower()and 'reddit' not in post.title.lower() and '?' not in post.title.lower():
                    
                    words = post.title.lower().split()
                    if 'dd' in words[1:]:
                        test = words[words.index('dd')-1]
                    text = post.selftext
                    length = round((len(text)/40000)*100)
                    line = post.title + ' -' + str(length) + '%'
                    lst.append(line)
                    d = {}
                    d['ticker'] = tick
                    d['num_comments'] = post.num_comments
                    d['comment_sentiment_average'] = commentSentiment(sub, post.url)
                    if d['comment_sentiment_average'] == 0.000000:
                        continue
                    d['latest_comment_date'] = latestComment(sub, post.url)
                    d['score'] = post.score
                    d['upvote_ratio'] = post.upvote_ratio
                    d['date'] = post.created_utc
                    d['domain'] = post.domain
                    d['num_crossposts'] = post.num_crossposts
                    d['author'] = post.author
                    d['length'] = str(length)+'%'
                    d['link'] = post.url
                    
                    submission_statistics.append(d)
        print(*lst, sep="\n")

        if lst != []:
         
            dfSentimentStocks = pd.DataFrame(submission_statistics)

            _timestampcreated = dfSentimentStocks["date"].apply(get_date)
            dfSentimentStocks = dfSentimentStocks.assign(timestamp = _timestampcreated)

            _timestampcomment = dfSentimentStocks["latest_comment_date"].apply(get_date)
            dfSentimentStocks = dfSentimentStocks.assign(commentdate = _timestampcomment)

            dfSentimentStocks.sort_values("latest_comment_date", axis = 0, ascending = True,inplace = True, na_position ='last') 

            dfSentimentStocks

            dfSentimentStocks.author.value_counts()

            today = date.today()

            d1 = today.strftime("%d_%m_%Y")

            sym = tick.upper()

            dfSentimentStocks.to_csv(F'Specific_Tickers\{sym}_Reddit_Sentiment_Equity_{d1}.csv', index=False)
        else:
            print('no post found in r/' + sub)
            

def commentSentiment(ticker, urlT):
    subComments = []
    bodyComment = []
    try:
        check = reddit.submission(url=urlT)
        subComments = check.comments
    except:
        return 0
    
    for comment in subComments:
        try: 
            bodyComment.append(comment.body)
        except:
            return 0
    
    sia = SIA()
    results = []
    for line in bodyComment:
        scores = sia.polarity_scores(line)
        scores['headline'] = line

        results.append(scores)
    
    df =pd.DataFrame.from_records(results)
    df.head()
    df['label'] = 0
    
    try:
        df.loc[df['compound'] > 0.1, 'label'] = 1
        df.loc[df['compound'] < -0.1, 'label'] = -1
    except:
        return 0
    
    averageScore = 0
    position = 0
    while position < len(df.label)-1:
        averageScore = averageScore + df.label[position]
        position += 1
    averageScore = averageScore/len(df.label) 
    print (averageScore)
    
    return(averageScore)

def latestComment(ticker, urlT):
    subComments = []
    updateDates = []
    try:
        check = reddit.submission(url=urlT)
        subComments = check.comments
    except:
        return 0
    
    for comment in subComments:
        try: 
            updateDates.append(comment.created_utc)
        except:
            return 0
    
    updateDates.sort()
    return(updateDates[-1])

def get_date(date):
    return dt.datetime.fromtimestamp(date)
if financials.lower() == 'y':
    getYahooFinancePrice()



# if tick == '':
#     searchAllTickers()
# else:
#     searchSpecificTick()