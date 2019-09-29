import urllib.request
import boto3
from botocore.exceptions import ClientError
import os
import csv
import json
import pandas as pd
import jsonToCsv

def check(s3, bucket, key):
    #try:
    #    s3.Object(bucket, key).load()
    #except ClientError as e:
    #    return int(e.response['Error']['Code']) != 404
    return False

df = pd.read_csv('../../Data/image/faceplusplus/DataDump.csv')
links = df.url
ids = df.id
count = 0
bucket = "ub-roastme"
os.makedirs("../../Data/image/AWS", exist_ok=True)
dataDump = open('../../Data/image/AWS/DataDump.csv', 'w')
csvwriter = csv.writer(dataDump)
for link in links:
    if link[-3:] in ["jpg", "JPG", "png", "PNG"]:
        imageFile=ids[count]+link[-3:]
        print(link)
        s3 = boto3.resource(service_name = 's3')
        if not check(s3, bucket, ids[count]+link[-3:]):
            s3client = boto3.client('s3')
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'XynoBot')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(link, "roast.jpg")
            s3client.upload_file("roast.jpg", bucket, imageFile)
        
        client=boto3.client('rekognition')
        response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':imageFile}}, Attributes = ["ALL"])
        with open('../../Data/image/AWS/'+ids[count]+'.json', 'w') as outfile:
            json.dump(response, outfile)
        row = [ids[count], link]
        if count == 0:
            titles = ["id", "url"]
            jsonToCsv.getTitles(titles, response["FaceDetails"][0], "")
            csvwriter.writerow(titles)
        count += 1
        if response["FaceDetails"]:
            jsonToCsv.flatten(row, response["FaceDetails"][0])
            csvwriter.writerow(row)
print('Done...')
