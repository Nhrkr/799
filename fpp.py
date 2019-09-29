import requests
import os
import csv
import json
import pandas as pd
import jsonToCsv
import time
import numpy as np
from modules import getTitles
from modules import getData

df = pd.read_csv('pushShiftAPI-RoastMe_posts_0918.csv')
print(len(df))
links = df.url
ids = df.id
title = df.title
author = df.author
score = df.score
num_comments = df.num_comments
comments_url = df.comments_url
count = 0
for link in links:
    newList = []
    if (link[-3:] in ["jpg", "JPG", "png", "PNG"] or link[-4:] in ["jpeg", "JPEG"]):
        print(count, link, ids[count])
        with open('/data/roastme/roastme/Data/image/faceplusplus/apiKey', 'r') as myfile:
            apiKey = myfile.read().replace('\n', '')
        with open('/data/roastme/roastme/Data/image/faceplusplus/apiSecret', 'r') as myfile:
            apiSecret = myfile.read().replace('\n', '')
        analyze_url = "https://api-us.faceplusplus.com/facepp/v3/detect"
        params     = {'api_key': apiKey, 'api_secret': apiSecret, 'image_url': link, 'return_attributes': 'gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,eyestatus,skinstatus'}
        postData = [ids[count], link, title[count], author[count], score[count], num_comments[count], comments_url[count]]
        if count == 0:
            titles, newList = getTitles(analyze_url, params, postData, newList, link)
        else:
            newList = getData(analyze_url, params, postData, count, newList, link) 
    count += 1
    if len(newList) > 0:
        df2 = pd.DataFrame(pd.DataFrame(np.array(newList),
    columns=titles))
    if count == 1:
        df2.to_csv("PushShift_FacePlusPlus-roast.csv", index=False)
    elif len(newList) > 0:
        df2.to_csv("PushShift_FacePlusPlus-roast.csv", mode='a', header=False, index=False)

