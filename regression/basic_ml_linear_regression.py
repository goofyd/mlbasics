from sklearn import linear_model as lm
from sklearn.model_selection import train_test_split
from pandas.io.json import json_normalize
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


reg = lm.LinearRegression()
'''
reg.fit(feature,label)

print(reg.score([[93,5, 110]], [[19]]))

print(reg.predict([[115,4, 133]]))
'''



with open('datasets/cars.json') as file:
    data = json.load(file)
    json_normalize(data)

cars_data = pd.DataFrame.from_dict(data)
Y = cars_data['Miles_per_Gallon'].fillna(math.floor(cars_data['Miles_per_Gallon'].median()))

hp = cars_data['Horsepower'].fillna(math.floor(cars_data['Horsepower'].median()))


dummy_pd = cars_data

dummy_pd['Horsepower']=hp
dummy_pd['Miles_per_Gallon']=Y


X = dummy_pd[['Horsepower', 'Cylinders', 'Displacement', 'Acceleration', 'Weight_in_lbs']]
Y = dummy_pd['Miles_per_Gallon']


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
reg.fit(X_train, y_train)

print(reg.score(X_test, y_test))

print(reg.predict([[90, 4, 100, 8, 2000]]))

plt.scatter(dummy_pd['Weight_in_lbs'], Y)
plt.plot(dummy_pd['Weight_in_lbs'], reg.predict(X), color='blue')
plt.show()