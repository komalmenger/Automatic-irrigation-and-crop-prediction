#importing the required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import urllib.request
import json
import time

READ_API_KEY='3G9GGW09Q5U4V7IK'
CHANNEL_ID= '998487'

#Reading the csv file
data=pd.read_csv('cpdata.csv')
#print(data.head(1))

#Creating dummy variable for target i.e label
label= pd.get_dummies(data.label).iloc[: , 1:]
data= pd.concat([data,label],axis=1)
data.drop('label', axis=1,inplace=True)
#print('The data present in one row of the dataset is')
#print(data.head(1))
train=data.iloc[:, 0:3].values
test=data.iloc[: ,4:].values

#Dividing the data into training and test set
X_train,X_test,y_train,y_test=train_test_split(train,test,test_size=0.3)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Importing Decision Tree classifier
from sklearn.tree import DecisionTreeRegressor
clf=DecisionTreeRegressor()

#Fitting the classifier into training set
clf.fit(X_train,y_train)
pred=clf.predict(X_test)

from sklearn.metrics import accuracy_score
# Finding the accuracy of the model
a=accuracy_score(y_test,pred)
print("The accuracy of this model is: ", a*100)


for i in range (1,11):
    TS = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                       % (CHANNEL_ID,READ_API_KEY))

    response = TS.read()
    data = json.loads(response)

    a = data['created_at']
    b = data['field1']
    c = data['field2']
    d = data['field3']
    e = data['field4']

    l=[]
    l.append(b)
    l.append(c)
    l.append(d)
print(l)
print("pH of the soil is: ",d)

predictcrop=[l]
if (d<str(5.5)):
    print("The soil is deficient of nutrients but has minerals")
elif (str(5.5)<d<str(8)):
    print("The soil has enough nutrients")
else:
    print("The soil is deficient of nutrients and minerals")


# Putting the names of crop in a single list
crops=['wheat','mungbean','Tea','millet','maize','lentil','jute','cofee','cotton','ground nut','peas','rubber','sugarcane','tobacco','kidney beans','moth beans','coconut','blackgram','adzuki beans','pigeon peas','chick peas','banana','grapes','apple','mango','muskmelon','orange','papaya','watermelon','pomegranate']
cr='rice'

#Predicting the crop
predictions = clf.predict(predictcrop)
count=0
for i in range(0,30):
    if(predictions[0][i]==1):
        c=crops[i]
        count=count+1
        break;
    i=i+1
if(count==0):
    print('The predicted crop is %s'%cr)
else:
    print('The predicted crop is %s'%c)

'''#Sending the predicted crop to database
cp=firebase.put('/croppredicted','crop',c)'''
