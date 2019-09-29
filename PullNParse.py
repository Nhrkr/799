import requests
import csv
import json

count = "100"

dataDump = open('../../Data/image/DataDump.csv', 'w')
csvwriter = csv.writer(dataDump)
csvwriter.writerow(['id', 'title', 'url', 'author', 'score', 'ups', 'downs', 'num_comments', 'comments_url'])
session = requests.session()
for turn in range(10):
    if turn == 0:
        r = session.get(url='https://reddit.com/r/roastme/top/.json?limit='+ count + '&t=all', headers = {'User-agent': 'XynoBot'})
    else:
        r = session.get(url='https://reddit.com/r/roastme/top/.json?limit='+ count + '&t=all&after=' + name, headers = {'User-agent': 'XynoBot'})
    with open('../../Data/image/metadata' + str(turn) + '.json', 'w') as outfile:
        json.dump(r.json(), outfile)
    for item in r.json()['data']['children']:
        print(item['data']['url'])
        itemID = item['data']['id']
        itemTitle = item['data']['title']
        itemComments = item['data']['permalink']
        itemLink = item['data']['url']
        itemScore = item['data']['score']
        itemAuthor = item['data']['author']
        itemUps = item['data']['ups']
        itemDowns = item['data']['downs']
        itemNumComments = item['data']['num_comments']
        name = item['data']['name']
        row = [itemID, itemTitle, itemLink, itemAuthor, itemScore, itemUps, itemDowns, itemNumComments, itemComments]
        csvwriter.writerow(row)
dataDump.close()

