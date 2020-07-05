import csv
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split




dataset = pd.read_csv('production.csv')
dataset1=pd.read_csv('regressiondb.csv')
dataset2=pd.read_csv('cropph.csv')



cropdict = {'Bajra' :1 ,'Banana':2,'Barley':3,'Bean':4,'Black pepper':5,'Blackgram':6,'Bottle Gourd':7,'Brinjal':8,'Cabbage':9,'Cardamom':10,'Carrot':11,'Castor seed':12,'Cauliflower':13,'Chillies':14,'Colocosia':15,'Coriander':16,'Cotton':17,'Cowpea':18,'Drum Stick':19,'Garlic':20,'Ginger':21,'Gram':22,'Grapes':23,'Groundnut':24,'Guar seed':25,'Horse-gram':26,'Jowar':27,'Jute':27,'Khesari':28,'Lady Finger':29,'Lentil':30,'Linseed':31,'Maize':32,'Mesta':33,'Moong(Green Gram)':34,'Moth':35,'Onion':36,'Orange':37,'Papaya':38,'Peas & beans (Pulses)':39,'Pineapple':40,'Potato':41,'Raddish':42,'Ragi':43,'Rice':44,'Safflower':45,'Sannhamp':46,'Sesamum':47,'Soyabean':48,'Sugarcane':49,'Sunflower':50,'Sweet potato':51,'Tapioca':52,'Tomato':53,'Turmeric':54,'Urad':55,'Varagu':56,'Wheat':57}


dataset1['Cropconversion'] = dataset1['Cropconversion'].map(cropdict)
a=dataset1.Cropconversion



'''print("------------------------------------------------------------------")
print(dataset1.head())
print(dataset1.shape)
print(dataset1.index)
print(list(dataset1.columns))

print("-------------------------------------------------------------------")
print(dataset.head())
print(dataset.shape)
print(dataset.index)
print(list(dataset.columns))

lm1 = smf.ols(formula='Production ~ Rainfall+Temperature+Ph', data=dataset1).fit()
print(lm1.params)'''


#linear_reression
X1 = dataset[['Rainfall', 'Temperature', 'Ph']]
Y1 = dataset.Production
# Split data
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, Y1, random_state=1)
# Instantiate model
lm_2 = LinearRegression()
# Fit Model
lm_2.fit(X1_train, y1_train)
# Predict
y1_pred = lm_2.predict(X1_test)
# RMSE
rmse = np.sqrt(metrics.mean_squared_error(y1_test, y1_pred))
print('Root Mean Square error is: ',rmse)

linear_model_1 = smf.ols(formula='Production ~ Rainfall+Temperature+Ph', data=dataset).fit()
print(linear_model_1.params)

sns.pairplot(dataset, x_vars=['Rainfall','Temperature','Ph'], y_vars='Production', height=7, aspect=0.7,kind='reg')
plt.show()