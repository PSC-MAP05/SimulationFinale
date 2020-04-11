import regression
import scenario
import mdp

import math
import numpy as np
import modelfree

import matplotlib.pyplot as plt

n_periodes =10
n_clients = 10000
n_jours_training = 500
n_jours_simu = 10
n_plat = 1
liste_prix = []
stock_beg = 30
pmin= 1.
pmax = 10.
k = 5

epsilon = 0.2
liste_MDP = []

liste_prix_possible = [i for i in range(1,11)]
for i in range(n_plat):

    mdipi = modelfree.modelfree(n_periodes, stock_beg, pmin, pmax, k)
    liste_MDP.append(mdipi)
def remplir_indice(s,time):
    liste_indice = [0 for i in range(n_plat)]
    for i in range(n_plat):
        if(np.random.uniform(0,1) < epsilon):
            #Random action
            liste_indice[i] = np.random.choice([i for i in range(len(liste_MDP[0].liste_Prix))])
        else:
            vopt, maximum = liste_MDP[i].findArgmax([time,s[i]])
            liste_indice[i] = maximum
    return liste_indice

    #là le MDP est rempli avec toutes les valeurs disponibles

revenusfinaux = []

for i in range(n_jours_training):
    print("Jour ", i)
    revenu = 0
    liste_prix = [0 for i in range(n_plat)]
    state = [stock_beg for i in range(n_plat)]
    scen = scenario.scenario(n_clients, n_periodes, n_plat)
    for pe in range(n_periodes-1):
        liste_indice = remplir_indice(state,pe)
        liste_prix = [liste_MDP[i].liste_Prix[liste_indice[i]] for i in range(n_plat)]
        listeDemandes = scen.simuler(pe, liste_prix)
        for plat in range(n_plat):
            b = state[plat]

            state[plat] -= listeDemandes[plat]

            a = 0
            if state[plat] < 0:
                a = listeDemandes[plat]+state[plat]
            else:
                a = listeDemandes[plat]
            state[plat] = max(0, state[plat])
            liste_MDP[plat].updateQ([pe,b], liste_indice[plat],[pe+1,state[plat]])
            revenu+=(b-state[plat])*liste_prix[0]

    revenusfinaux.append(revenu)
for i in range(n_periodes):
    liste = []
    for j in range(stock_beg):
        vopt, max = liste_MDP[0].findArgmax([i,j])
        liste.append(liste_MDP[0].liste_Prix[max])
    print(liste)

print(liste_MDP[0].qvalues[6])
plt.plot([i for i in range(n_jours_training)],revenusfinaux)
plt.show()