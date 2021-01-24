import praw

reddit = praw.Reddit(client_id='lELNGnTUoXms4Q', client_secret='vjkYp6AJfkA4lHRaiA_S2KkTQl_ndQ', user_agent='DD Analysis')

subs = ['investing','stocks','wallstreetbets']

for sub in subs:
    getHot = reddit.subreddit(sub).new(limit=1000)
    lst = []
    for post in getHot:
        
        if 'DD' in post.title:
            lst.append(post.title)
        
    print(lst)