import cv2
import sys
import math
import pandas as pd
import urllib.request

if len(sys.argv) == 1:
    print("provide arguments. 0 for Face++; 1 for Amazon")
    exit(1)
if sys.argv[1] == "1":
    df = pd.read_csv("../../Data/image/AWS/DataDump.csv")
    links = df.url
    ids = df.id
    left_coordinate = df["BoundingBox.Left"]
    top_coordinate = df["BoundingBox.Top"]
    width = df["BoundingBox.Width"]
    height = df["BoundingBox.Height"]
    for count in range(len(links)):
        url = links[count]
        curr_id = ids[count]
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'XynoBot')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, "../../Data/image/faceCrops/Amazon/" + curr_id + "." + url[-3:])
        print("image retrieved")
        image = cv2.imread("../../Data/image/faceCrops/Amazon/" + curr_id + "." + url[-3:])
        left = math.floor(left_coordinate[count] * image.shape[1]) - 10
        top = math.floor(top_coordinate[count] * image.shape[0]) - 10
        right = left + math.floor(width[count] * image.shape[1]) + 10
        bottom = top + math.floor(width[count] * image.shape[0]) + 10
        cropImage = image[top:bottom, left:right]
        cv2.imwrite("../../Data/image/faceCrops/Amazon/" + curr_id + "." + url[-3:], cropImage)

elif sys.argv[1] == "0":
    df = pd.read_csv("../../Data/image/faceplusplus/1kPostsDump.csv")
    links = df.url
    ids = df.id
    left = df["faceRectangle.left"]
    top = df["faceRectangle.top"]
    width = df["faceRectangle.width"]
    height = df["faceRectangle.height"]
    for count in range(len(links)):
        url = links[count]
        curr_id = ids[count]
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'XynoBot')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, "../../Data/image/faceCrops/Face++/" + curr_id + "." + url[-3:])
        print("image retrieved")
        image = cv2.imread("../../Data/image/faceCrops/Face++/" + curr_id + "." + url[-3:])
        cropImage = image[top[count]:(top[count] + height[count]), left[count]:(left[count] + width[count])]
        cv2.imwrite("../../Data/image/faceCrops/Face++/" + curr_id + "." + url[-3:], cropImage)

else:
    print("invaid arguments. 0 for Face++; 1 for Amazon")
    exit(1)
