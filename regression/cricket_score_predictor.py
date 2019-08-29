import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as pt

dataset = pd.read_excel('datasets/cricket_scores.xlsx')

X = dataset[['Overs', 'Innings', 'Wickets', 'Score']]
Y = dataset['FinalScore']
reg = linear_model.LinearRegression()

#pt.plot(dataset['Overs'], Y)
#pt.show()

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
reg.fit(X,Y)

print(reg.score(X_test,y_test))

print(reg.predict([[47.1, 2, 6, 228]]))


