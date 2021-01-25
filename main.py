import praw
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import math
import datetime as dt
import pandas as pd
import numpy as np

nltk.download('vader_lexicon')
nltk.download('stopwords')

reddit = praw.Reddit(client_id='lELNGnTUoXms4Q', client_secret='vjkYp6AJfkA4lHRaiA_S2KkTQl_ndQ', user_agent='DD Analysis')

subs = ['investing','stocks','wallstreetbets']
tick=input("Please enter ticker symbol (leave blank for all)")


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


for sub in subs:
    getNew = reddit.subreddit(sub).new(limit=None)
    lst = []
    for post in getNew:

        if 'dd' in post.title.lower() and tick in post.title.lower() and 'reddit' not in post.title.lower()  and '?' not in post.title.lower() :
            text = post.selftext
            length = round((len(text)/40000)*100)
            line = post.title + ' -' + str(length) + '%'
            lst.append(line)



        #TODO Get link to the post with the highest %
        #start sentiment analysis w sentiment.vader
        #TODO read documentation related to sentiment analysis and then learn more about how to code graphs in python
            
        
    print(*lst, sep="\n")