import regression
import scenario
import mdp
import math
import numpy as np
import pandas as pd
import NEW_CLASS
import matrice_note
n_periodes =24
n_clients = 1000
n_jours_training = 100
n_jours_simu = 15
n_plat = 5



liste_prix = []
stock_beg = 100


def fonctionDemandeInitiale(time,price):

    return 0

liste_MDP = []
pmin = 1
pmax = 10
k = 10

for i in range(n_plat):

    mdipi = mdp.mdp(n_periodes, stock_beg, fonctionDemandeInitiale, pmin, pmax, k)
    mdipi.remplir_MDP()
    liste_MDP.append(mdipi)

    state = 0
    print("HOP UN DE FAIT")
   


listeDemandesFinal = []  #va nous permettre de faire les régressions etc.
listePrixFinal = []




#vraie_matrice_note = ....


print("MDP INITIALISES!!")

def z():
    return


def updateNoteMatrix():
    return 0

def remplirListePrix(pe):
    liste = [0 for i in range(n_plat)]
    for i in range(n_plat):
        liste[i] = np.random.randint(1,10,1)[0]
    return liste
def remplirListePrix2(pe,m):
    liste = [0 for i in range(n_plat)]
    for i in range(n_plat):
        liste[i] =m
    return liste



liste_tab_Y = []
liste_tab_X = []
listeRevenus1 = [[] for i in range(n_plat)]
listeRevenus2 = [[] for i in range(n_plat)]
listeRevenus3 = [[] for i in range(n_plat)]

vraie_matrice_note = matrice_note.genererMatrice(n_clients, n_plat)

"""matriceOriginelle = matricefacto."""


columns = ["user", "item", "rating"]
ds = pd.DataFrame([], columns= columns)
data = NEW_CLASS.dataset(ds,"ta", 12)

for i in range(n_clients):
    for j in range(n_plat):
        data.new_note(i,j,np.random.randint(1,7))




M = data.factorisation(n_clients, n_plat)
moyenne_rang=matrice_note.rang_moyen(matrice_note.mat_to_rank2(M,n_plat,n_plat),n_plat)
matrice_Rank = matrice_note.mat_to_rank2(M,n_plat,n_plat)


for i in range(n_jours_training):
    print("Jour ", i)
    state = [stock_beg for i in range(n_plat)]
    scen = scenario.scenario(n_clients, n_periodes, n_plat, vraie_matrice_note, matrice_Rank)

    tab_ranking = []
    for pe in range(n_periodes-1):
        liste_prix = remplirListePrix(pe)

        listeDemandes, tab_notes = scen.simuler(pe, liste_prix)
        for plat in range(n_plat):
            state[plat] -= listeDemandes[plat]
            a = 0
            if state[plat] < 0:
                a = listeDemandes[plat]+state[plat]
            else:
                a = listeDemandes[plat]
            state[plat] = max(0, state[plat])
            listeRevenus1[plat].append(a*liste_prix[plat])
            liste_tab_X.append([pe, liste_prix[plat], moyenne_rang[plat]])
            liste_tab_Y.append(listeDemandes[plat])

        for triplet in tab_notes:
            user = triplet[0]
            item = triplet[1]
            note = triplet[2]
            data.new_note(user,item,note)



     


        listePrixFinal.append([pe]+liste_prix)

       
        listeDemandesFinal.append(listeDemandes)
        liste_prix = remplirListePrix(pe)
        
        """for element in tab_notes:
            matrice.add(elmement)"""
    M = data.factorisation(n_clients, n_plat)
    moyenne_rang=matrice_note.rang_moyen(matrice_note.mat_to_rank2(M,n_plat,n_plat),n_plat)
    matrice_Rank = matrice_note.mat_to_rank2(M,n_plat,n_plat)
#for i in range(len(listePrixFinal)):

 #   for plat in range(n_plat):
  #      liste_tab_X[plat].append([listePrixFinal[i][0],listePrixFinal[i][plat+1], tab_ranking[plat]])

#for i in range(len(listeDemandesFinal)):
 #   for plat in range(n_plat):
  #      liste_tab_Y[plat].append(listeDemandesFinal[i][plat])
"""for user in range(n_clients):
    for plat in range(n_plat):
        note = matrice.get(user, plat)
        if note>=3:
            compteur += 1
compteur = compteur/(n_clients*n_plat)"""
for i in range(n_jours_simu):
    print("Jour ", i)
    state = [stock_beg for i in range(n_plat)]
    scen = scenario.scenario(n_clients, n_periodes,n_plat, vraie_matrice_note, matrice_Rank)

    coeff = regression.regresser(liste_tab_X, regression.fonctiondeRegression(liste_tab_Y))
    print(coeff)






    for plat in range(n_plat):
        liste_MDP[plat].ranking = moyenne_rang[plat]

        liste_MDP[plat].intercept = coeff[0]
        liste_MDP[plat].coef1 = coeff[1]
        liste_MDP[plat].coef2 = coeff[2]
        liste_MDP[plat].coef3 = coeff[3]
        liste_MDP[plat].remplir_MDP()

#le -1 est là car on ne regarde pas ce qu'il se pass eà la fin de la journée!!
    liste_MDP[0].printMDPdemande()
    liste_MDP[0].printMDPprice()
    M = data.factorisation(n_clients, n_plat)
    moyenne_rang = matrice_note.rang_moyen(matrice_note.mat_to_rank2(M, n_plat, n_plat), n_plat)
    matrice_Rank = matrice_note.mat_to_rank2(M, n_plat, n_plat)
    for pe in range(n_periodes-1):



        listeDemandes, tab_notes = scen.simuler(pe, liste_prix)
        for triplet in tab_notes:
            user = triplet[0]
            item = triplet[1]
            note = triplet[2]
            data.new_note(user,item,note)


        for plat in range(n_plat):
            state[plat] -= listeDemandes[plat]
            a = 0
            if state[plat] < 0:
                a = listeDemandes[plat] + state[plat]
            else:
                a = listeDemandes[plat]
            state[plat] = max(0,state[plat])
            listeRevenus2[plat].append(a*liste_prix[plat])

            liste_tab_X.append([pe,liste_prix[plat], moyenne_rang[plat]])
            liste_tab_Y.append(listeDemandes[plat])

            liste_prix[plat] = liste_MDP[plat].findPrice([pe, state[plat]])
        print("stock: ", state[0], " prix: ", liste_prix[0])
        print(state)
        #rajouter la partie NOTES....
        listePrixFinal.append(liste_prix)

        listeDemandesFinal.append(listeDemandes)

print(liste_tab_X)
print(liste_tab_Y)


n_jours_validations = 50
listeRevenusFinal = [[[] for i in range(n_plat)] for k in range(10)]
for k in range(1,11):
    for i in range(n_jours_validations):
        print("Jour ", i)
        state = [stock_beg for i in range(n_plat)]
        scen = scenario.scenario(n_clients, n_periodes, n_plat, vraie_matrice_note, matrice_Rank)
        for pe in range(n_periodes-1):
            liste_prix = remplirListePrix2(pe,k)

            listeDemandes , tab_notes = scen.simuler(pe, liste_prix)
            for plat in range(n_plat):
                state[plat] -= listeDemandes[plat]
                a = 0
                if state[plat] < 0:
                    a = listeDemandes[plat]+state[plat]
                else:
                    a = listeDemandes[plat]
                state[plat] = max(0, state[plat])
                listeRevenusFinal[k-1][plat].append(a*liste_prix[plat])


     

print("revenus phase training")
for i in range(len(listeRevenus1)):
    print(sum(listeRevenus1[i])/n_jours_training)
print("revenus phase test plat1")
for i in range(n_jours_simu):
    print("revenus jours ", i)
    for plat in range(n_plat):
        print(sum(listeRevenus2[plat][i*(n_periodes-1):(i+1)*(n_periodes-1)]))
print("revenus phase validation")
for k in range(len(listeRevenusFinal)):
    print("Prix", k + 1)
    for plat in range(n_plat):

        print(sum(listeRevenusFinal[k][plat]) / n_jours_validations)
print("FINI")

