import numpy as np
from sklearn.linear_model import LinearRegression
import math
import matplotlib.pyplot as plt
"""
tab_X = np.loadtxt('data_X.dat')
tab_Y = np.loadtxt('data_Y.dat')
print(tab_Y)
for i in range(len(tab_Y)):
    #tab_Y[i] = math.sqrt(-2*math.log(tab_Y[i]/300))
    tab_Y[i] = tab_Y[i]
    #tab_Y[i] = np.log(tab_Y[i]+0.01)
model = LinearRegression().fit(tab_X,tab_Y)
print(model.score(tab_X, tab_Y))
tab_XX = tab_X[:,0]
plt.plot(tab_XX, tab_Y)
plt.show()
"""

#idée étant donnée des données d'entrainement et de sortie, renvoyer la fonction de régression
def fonctiondeRegression(tab_Y):
    tab = []
    for i in range(len(tab_Y)):
        tab.append(np.log(tab_Y[i]+1))
    return tab
def fonctionInversedeRegression(x):
    return np.exp(x)

def regresser(tab_X, tab_Y):
    tab_temp = [[abs(tab_X[i][0]-12),tab_X[i][1], tab_X[i][2]] for i in range(len(tab_X))]

    model = LinearRegression().fit(tab_temp,tab_Y)

    return np.append(np.array([model.intercept_]),model.coef_)