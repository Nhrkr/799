import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import collections

face = pd.read_csv('../../Data/image/faceplusplus/DataDump.csv')
aws = pd.read_csv('../../Data/image/AWS/DataDump.csv')
for i in range(len(aws['.Emotions'])):
    emotion_data = json.loads(aws['.Emotions'][i].replace("'",'"'))
    Newdict = {}
    for j in emotion_data:
        Newdict[j['Type']] = j['Confidence']
    dfdict = collections.OrderedDict(sorted(Newdict.items()))
    if i == 0:
        emotion = pd.DataFrame(dfdict, index=[0])
    else:
        df = (pd.DataFrame(dfdict, index=[i]))
        emotion = emotion.append(df)

np.random.seed(19680801)
colors = np.random.rand(emotion.shape[0])

dfhappy = emotion[['HAPPY']].join(face[['emotion.happiness']])
corr = dfhappy.corr()
print(corr)
dfhappy.plot.scatter(y='HAPPY', x='emotion.happiness')
plt.show()


dfanger = emotion[['ANGRY']].join(face[['emotion.anger']])
corr = dfanger.corr()
print(corr)
dfanger.plot.scatter(y='ANGRY', x='emotion.anger')
plt.show()

dfsurprise = emotion[['SURPRISED']].join(face[['emotion.surprise']])
corr = dfsurprise.corr()
print(corr)
dfsurprise.plot.scatter(y='SURPRISED', x='emotion.surprise')
plt.show()

dfsad = emotion[['SAD']].join(face[['emotion.sadness']])
corr = dfsad.corr()
print(corr)
dfsad.plot.scatter(y='SAD', x='emotion.sadness')
plt.show()

dfdisgust = emotion[['DISGUSTED']].join(face[['emotion.disgust']])
corr = dfdisgust.corr()
print(corr)
dfdisgust.plot.scatter(y='DISGUSTED', x='emotion.disgust')
plt.show()

dfcalm = emotion[['CALM']].join(face[['emotion.neutral']])
corr = dfcalm.corr()
print(corr)
dfcalm.plot.scatter(y='CALM', x='emotion.neutral')
plt.show()

dfAge = aws[['AgeRange.Low']].join(aws[['AgeRange.High']]).join(face[['age.value']])
dfAge.plot(y=['AgeRange.Low', 'AgeRange.High', 'age.value'])
dfAge['match'] = np.where(aws['AgeRange.Low'] <= face['age.value'], True, False)
print("percentage match of Age : \n", dfAge['match'].value_counts(normalize=True) * 100)
plt.show()

dfhappy['match'] = np.where(aws['Gender.Value'] == face['gender.value'], True, False)
print("percentage match of gender : \n", dfhappy['match'].value_counts(normalize=True) * 100)
