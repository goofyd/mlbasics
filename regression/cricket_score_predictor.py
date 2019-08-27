import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as pt

dataset = pd.read_excel('datasets/last_5_overs_cricket_scores.xlsx')

X = dataset[['Overs', 'Innings', 'Wickets', 'Score']]
Y = dataset['FinalScore']
reg = linear_model.LinearRegression()

#pt.plot(dataset['Overs'], Y)
#pt.show()

reg.fit(X,Y)

print(reg.score([[46, 2, 6, 190], [42, 2, 3, 170]], [204, 220]))

print(reg.predict([[40, 2, 9, 121]]))


