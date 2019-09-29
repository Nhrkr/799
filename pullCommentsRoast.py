from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time


api = PushshiftAPI()

df = pd.read_csv('pushShiftAPI-RoastMe.csv')

outDf = pd.DataFrame(columns=['post_id','id','parent_id','comment','score'])

posts = df["id"]
for post in posts:
    after_post = int(time.time())
    listOfPosts = []
    while(True):
        if len(listOfPosts) == 0:
            tempList = list(api.search_comments(subreddit='roastme', link_id = post, limit=500))
            listOfPosts.extend(tempList)
            after_post = listOfPosts[-1].created_utc
        else:
            tempList = list(api.search_comments(before = after_post, subreddit='roastme', link_id = post, limit=500))
            listOfPosts.extend(tempList)
            after_post = listOfPosts[-1].created_utc
        if len(tempList) < 500:
            break
    for comment in listOfPosts:
        outDf = outDf.append({'post_id': comment.link_id[3:], 'id': comment.id, 'parent_id': comment.parent_id[3:], 'comment': comment.body, 'score': comment.score}, ignore_index=True)
    outDf.to_csv("testComment.csv")
    print(post + " done")
    
#df = pd.DataFrame(columns=['id','title','url','author','score', 'num_comments', 'comments_url'])
#for post in listOfPosts:
#    if post.num_comments >=10:
#        df = df.append({'id': post.id, 'title': post.title, 'url': post.url, 'author': post.author, 'score': post.score, 'num_comments': post.num_comments, 'comments_url': post.permalink}, ignore_index=True)

#df.to_csv("pushShiftAPI-RoastMe.csv")
