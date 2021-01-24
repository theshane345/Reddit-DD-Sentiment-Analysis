import praw

reddit = praw.Reddit(client_id='lELNGnTUoXms4Q', client_secret='vjkYp6AJfkA4lHRaiA_S2KkTQl_ndQ', user_agent='DD Analysis')

subs = ['investing','stocks','wallstreetbets']
tick=input("Please enter ticker symbol (leave blank for all)")

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