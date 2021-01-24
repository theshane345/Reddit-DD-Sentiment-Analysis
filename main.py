import praw

reddit = praw.Reddit(client_id='lELNGnTUoXms4Q', client_secret='vjkYp6AJfkA4lHRaiA_S2KkTQl_ndQ', user_agent='DD Analysis')

subs = ['investing','stocks','wallstreetbets']
tick=input("Please enter ticker symbol (leave blank for all)")

for sub in subs:
    getHot = reddit.subreddit(sub).new(limit=None)
    lst = []
    for post in getHot:

        if 'dd' in post.title.lower() and tick in post.title.lower() and 'reddit' not in post.title.lower()  and '?' not in post.title.lower() :
            text = post.selftext
            length = round((len(text)/40000)*100)
            line = post.title + ' -' + str(length) + '%'
            lst.append(line)
            
        
    print(*lst, sep="\n")