import requests
import json
import pandas as pd
import time

# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
with open('../../Data/image/Microsoft/subKey', 'r') as myfile:
  subscription_key = myfile.read().replace('\n', '')
print(subscription_key)
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the "westus" region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"
headers = {'Ocp-Apim-Subscription-Key': subscription_key }
params  = {'visualFeatures': 'Categories,Description,Color'}
analyze_url = vision_base_url + "analyze"

df = pd.read_csv('../../Data/image/faceplusplus/DataDump.csv')
links = df.url
ids = df.id
captionList = []
for link in links:
	time.sleep(5)
	data    = {'url': link}
	print(link)
	response = requests.post(analyze_url, headers=headers, params=params, json=data)
	response.raise_for_status()
	# The 'analysis' object contains various fields that describe the image. The most
	# relevant caption for the image is obtained from the 'description' property.
	analysis = response.json()
	if len(analysis["description"]) != 0:
		image_caption = analysis["description"]
	else:
		image_caption = " "
	captionList.append(image_caption)
df["description"] = captionList
df.to_csv("../../Data/image/faceplusplus/DataDump.csv")
