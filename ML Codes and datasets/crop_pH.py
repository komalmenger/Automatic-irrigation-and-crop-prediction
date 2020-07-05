# -*- coding: utf-8 -*-

import csv
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import urllib.request
import json
import time

READ_API_KEY='3G9GGW09Q5U4V7IK'
CHANNEL_ID= '998487'

dataset=pd.read_csv('production.csv')
dataset1=pd.read_csv('regressiondb.csv')


dataa=pd.read_csv('cropph.csv')

X = dataset.iloc[:, :-1].values
Y = dataset.iloc[:, 3].values

A = dataa.iloc[:10, 0].values
B = dataa.iloc[:10, 1].values

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state = 0)
#P_train, P_test, Q_train, Q_test = train_test_split(P, Q, test_size = 0.1, random_state = 0)

regressor = LinearRegression()

regressor.fit(X_train, Y_train)
#regressor.fit(P_train, Q_train)
#predecting test set results

Y_pred = regressor.predict(X_test)
#P_Pred = regressor.predict(P_test)
print('Coefficients: \n', regressor.coef_)
print('Variance score: %.5f' % regressor.score(X_test, Y_test))
print("Mean squared error: %.5f" % np.mean((regressor.predict(X_test) - Y_test) ** 2))



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

if (d<str(5.5)):
    print("The soil is deficient of nutrients but has minerals")
elif (str(5.5)<d<str(8)):
    print("The soil has enough nutrients")
else:
    print("The soil is deficient of nutrients and minerals")




'''style.use('ggplot')
plt.plot(X_test,Y_test)
style.use('ggplot')
plt.title('TESTING DATA')
plt.ylabel('Production')
plt.xlabel('Rainfall, Temperature and PH Value')
#plt.plot(Y_train)'''


'''plt.plot(X_train,Y_train)
style.use('ggplot')
plt.title('TRAINING DATA')
plt.ylabel('Production')
plt.xlabel('Rainfall, Temperature and PH Value')'''
print(Y_train)
print(X_train)

print(Y_pred)


style.use('ggplot')
plt.scatter(A,B)

plt.title('Crop And their PH Values')
plt.ylabel('PH Value')
plt.xlabel('Crops')

plt.show()



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

if (d<5.5):
    print("The soil is deficient of nutrients but has minerals")
elif ((5.5)<d<(8)):
    print("The soil has enough nutrients")
else:
    print("The soil is deficient of nutrients and minerals")