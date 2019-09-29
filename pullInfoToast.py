from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time


api = PushshiftAPI()
start_epoch = int(time.time())

listOfPosts = []
df = pd.read_csv('pushShiftAPI-RoastMe_posts_0918.csv')
ids = df['id']
titles = df['title']
authors = df['author']
scores = df['score']
urls = df['url']
num_commentss = df['num_comments']
comment_urls = df['comments_url']
data = pd.DataFrame(columns=['author', 'Rid', 'Rtitle', 'Rurl', 'Rscore', 'Rnum_comments', 'Rcomments_url', 'Tid', 'Ttitle', 'Turl', 'Tscore', 'Tnum_comments', 'Tcomments_url'])
for i in range(len(ids)):
    newList = (list(api.search_submissions(author=authors[i],
                            subreddit='toastme',
                            filter=['id', 'permalink', 'url','author', 'title', 'subreddit', 'score','num_comments'])))
    if(len(newList) > 0):
        print(authors[i])
        post = newList[-1]
        data = data.append({'author': post.author, 'Rid': ids[i], 'Rtitle': titles[i], 'Rurl': urls[i], 'Rscore': scores[i], 'Rnum_comments': num_commentss[i], 'Rcomments_url': comment_urls[i], 'Tid': post.id, 'Ttitle': post.title, 'Turl': post.url, 'Tscore': post.score, 'Tnum_comments': post.num_comments, 'Tcomments_url': post.permalink}, ignore_index=True)

data.to_csv("pushShiftAPI-ToastMe_posts_0918.csv")
