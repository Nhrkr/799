from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time


api = PushshiftAPI()

df = pd.read_csv('pushShiftAPI-RoastMe_posts_0918.csv')

flag = True

posts = df["id"]
i=0
for post in posts:
    outDf = pd.DataFrame(columns=['post_id','id','comment','score'])
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
        outDf = outDf.append({'post_id': comment.link_id[3:], 'id': comment.id, 'comment': comment.body, 'score': comment.score}, ignore_index=True)
    if flag:
        outDf.to_csv("testTopComment.csv")
        flag = False
    else:
        outDf.to_csv('testTopComment.csv', mode='a', header=False)
    print(str(i)+ " " + post + " done")
    i=i+1
    
#df = pd.DataFrame(columns=['id','title','url','author','score', 'num_comments', 'comments_url'])
#for post in listOfPosts:
#    if post.num_comments >=10:
#        df = df.append({'id': post.id, 'title': post.title, 'url': post.url, 'author': post.author, 'score': post.score, 'num_comments': post.num_comments, 'comments_url': post.permalink}, ignore_index=True)

#df.to_csv("pushShiftAPI-RoastMe.csv")
