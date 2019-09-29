import requests
import os
import csv
import json
import pandas as pd
import jsonToCsv
import time
import numpy as np

def getTitles(analyze_url, params, postData, newList, link):
    try:
        response = requests.post(analyze_url, params = params)
        response.raise_for_status()
        analysis = response.json()
        titles = ["id", "url", "title", "author", "score", "num_comments", "comments_url"]
        jsonToCsv.getTitles(titles, analysis["faces"][0]["attributes"], "")
        jsonToCsv.getTitles(titles, analysis["faces"][0]["face_rectangle"], "faceRectangle")
        row = postData
        if analysis["faces"]:
            jsonToCsv.flatten(row, analysis["faces"][0]["attributes"])
            jsonToCsv.flatten(row, analysis["faces"][0]["face_rectangle"])
            newList.append(row)
            print("wrote", postData[0], postData[1])
        return titles, newList
    except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("retrying for " + link)
                titles, newList = getTitles(analyze_url, params, postData, newList, link)
                return titles, newList
            else:
                print(e)

def getData(analyze_url, params, postData, count, newList, link):
    try:
        response = requests.post(analyze_url, params = params)
        response.raise_for_status()
        analysis = response.json()
        with open('Data/image/'+postData[0]+'.json', 'w') as outfile:
            json.dump(analysis, outfile)
        row = postData
        if analysis["faces"]:
            jsonToCsv.flatten(row, analysis["faces"][0]["attributes"])
            jsonToCsv.flatten(row, analysis["faces"][0]["face_rectangle"])
            newList.append(row)
            print("wrote", postData[0], postData[1])
        else:
            print("not written", postData[0], postData[1])
    except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("retrying for " + link)
                newList = getData(analyze_url, params, postData, count, newList,link)
            else:
                print(e)
    return newList
