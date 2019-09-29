from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time


api = PushshiftAPI()
start_epoch = int(time.time())

listOfPosts = []

while(len(listOfPosts) < 100000):
    listOfPosts.extend(list(api.search_submissions(before=start_epoch,
                            subreddit='toastme',
                            filter=['id', 'permalink', 'url','author', 'title', 'subreddit', 'score','num_comments'],
                            limit=500)))
    start_epoch = listOfPosts[-1].created_utc
    print(listOfPosts[-1])
    
df = pd.DataFrame(columns=['id','title','url','author','score', 'num_comments', 'comments_url'])
for post in listOfPosts:
    if post.num_comments >=10:
        df = df.append({'id': post.id, 'title': post.title, 'url': post.url, 'author': post.author, 'score': post.score, 'num_comments': post.num_comments, 'comments_url': post.permalink}, ignore_index=True)

df.to_csv("pushShiftAPI-ToastMe_posts_all_0918.csv")
