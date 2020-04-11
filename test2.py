import regression
import scenario
import mdp
import math
import numpy as np

n_periodes =24
n_clients = 1000
n_jours_training = 100
n_jours_simu = 4
n_plat = 4



liste_prix = []
stock_beg = [10,30,50,70]
def fonctionDemandeInitiale(time,price):

    return "blabla"

liste_MDP = []
pmin = 1
pmax = 10
k = 10
for i in range(n_plat):

    mdipi = mdp.mdp(n_periodes, stock_beg[i], fonctionDemandeInitiale, pmin, pmax, k)
    mdipi.remplir_MDP()
    liste_MDP.append(mdipi)

    state = 0
    print("HOP UN DE FAIT")
    #là le MDP est rempli avec toutes les valeurs disponibles


listeDemandesFinal = []  #va nous permettre de faire les régressions etc.
listePrixFinal = []
print("MDP INITIALISES!!")

def z():
    return


def updateNoteMatrix():
    return 0

def normal_positive(taille_echantillon,moyenne,var):
    ecartType=var**(1/2)
    l=ecartType*np.random.randn(taille_echantillon)+moyenne
    x=[np.round(a,1) for a in l]
    for i in range(taille_echantillon):
        if x[i]<=.5:
            x[i]=10*np.random.random()
    return x

"""def remplirListePrix(pe):
    return [1 for k in range(n_plat)]"""



def remplirListePrix(pe):
    liste = [0 for i in range(n_plat)]
    for i in range(n_plat):
        liste[i] = np.random.randint(1,11,1)[0]
    return liste

def remplirListePrix2(pe,m):
    liste = [0 for i in range(n_plat)]
    for i in range(n_plat):
        nb=abs(m+6*np.random.random()-1)
        liste[i] = nb
    return liste
#PARTIE SIMULATION DES PREMIERES PERIODES AVEC PRIX AU HASARD
#définir listePRIX
liste_tab_Y = [[] for i in range(n_plat)]
liste_tab_X = [[] for i in range(n_plat)]
listeRevenus1 = [[] for i in range(n_plat)]
listeRevenus2 = [[] for i in range(n_plat)]
listeRevenus3 = [[] for i in range(n_plat)]

"""matriceOriginelle = matricefacto."""
for i in range(n_jours_training):
    print("Jour ", i)
    state = [x for x in stock_beg]
    scen = scenario.scenario(n_clients, n_periodes, n_plat)
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

        # rajouter la partie NOTES....
        listePrixFinal.append([pe]+liste_prix)

        # revoir cette ligne
        listeDemandesFinal.append(listeDemandes)
        liste_prix = remplirListePrix(pe)
        # problème, PRENDRE EN COMPTE LE TEMPS
        """for element in tab_notes:
            matrice.add(elmement)"""


for i in range(len(listePrixFinal)):

    for plat in range(n_plat):
        liste_tab_X[plat].append([listePrixFinal[i][0],listePrixFinal[i][plat+1]])

for i in range(len(listeDemandesFinal)):
    for plat in range(n_plat):
        liste_tab_Y[plat].append(listeDemandesFinal[i][plat])
"""for user in range(n_clients):
    for plat in range(n_plat):
        note = matrice.get(user, plat)
        if note>=3:
            compteur += 1
compteur = compteur/(n_clients*n_plat)"""
for i in range(n_jours_simu):
    print("Jour ", i)
    state = [x for x in stock_beg]
    scen = scenario.scenario(n_clients, n_periodes,n_plat)
    for plat in range(n_plat):

        coeff = regression.regresser(liste_tab_X[plat], regression.fonctiondeRegression(liste_tab_Y[plat]))
        liste_MDP[plat].intercept =  coeff[0]
        liste_MDP[plat].coef1 = coeff[1]
        liste_MDP[plat].coef2 = coeff[2]

        liste_MDP[plat].remplir_MDP()
#le -1 est là car on ne regarde pas ce qu'il se pass eà la fin de la journée!!
    liste_MDP[0].printMDPdemande()
    liste_MDP[0].printMDPprice()


    for pe in range(n_periodes-1):



        listeDemandes,tab_notes = scen.simuler(pe, liste_prix)

        for plat in range(n_plat):
            state[plat] -= listeDemandes[plat]
            a = 0
            if state[plat] < 0:
                a = listeDemandes[plat] + state[plat]
            else:
                a = listeDemandes[plat]
            state[plat] = max(0,state[plat])
            listeRevenus2[plat].append(a*liste_prix[plat])

            liste_tab_X[plat].append([pe,liste_prix[plat]])
            liste_tab_Y[plat].append(listeDemandes[plat])

            liste_prix[plat] = liste_MDP[plat].findPrice([pe, state[plat]])
        #rajouter la partie NOTES....
        listePrixFinal.append(liste_prix)

        #revoir cette ligne
        listeDemandesFinal.append(listeDemandes)

        #problème, PRENDRE EN COMPTE LE TEMPS
print(liste_tab_X)
print(liste_tab_Y)


n_jours_validations = 50
listeRevenusFinal = [[[] for i in range(n_plat)] for k in range(10)]
for k in range(1,11):
    for i in range(n_jours_validations):
        print("Jour ", i)
        state = [x for x in stock_beg]
        scen = scenario.scenario(n_clients, n_periodes, n_plat)
        for pe in range(n_periodes-1):
            liste_prix = remplirListePrix2(pe,k)
            print(liste_prix)
            listeDemandes, tab_notes = scen.simuler(pe, liste_prix)
            for plat in range(n_plat):
                state[plat] -= listeDemandes[plat]
                a = 0
                if state[plat] < 0:
                    a = listeDemandes[plat]+state[plat]
                else:
                    a = listeDemandes[plat]
                state[plat] = max(0, state[plat])
                listeRevenusFinal[k-1][plat].append(a*liste_prix[plat])

        # rajouter la partie NOTES....


        # revoir cette ligne

        # problème, PRENDRE EN COMPTE LE TEMPS

print("revenus phase training")
for i in range(len(listeRevenus1)):
    print(sum(listeRevenus1[i])/n_jours_training)
print("revenus phase test plat1")

jour=[[] for i in range(n_jours_simu)]
for i in range(n_jours_simu):
    print("revenus jours ", i)
    for plat in range(n_plat):
        jour[i].append(sum(listeRevenus2[plat][i*(n_periodes-1):(i+1)*(n_periodes-1)]))
        print(sum(listeRevenus2[plat][i*(n_periodes-1):(i+1)*(n_periodes-1)]))
print("revenus phase validation")

prix=[[] for k in range(len(listeRevenusFinal))]
for k in range(len(listeRevenusFinal)):
    print("Prix", k + 1)
    for plat in range(n_plat):
        prix[k].append(sum(listeRevenusFinal[k][plat]) / n_jours_validations)
        print(sum(listeRevenusFinal[k][plat]) / n_jours_validations)
print("FINI")

somme=[]
for k in range(len(jour)):
    j=np.array(jour[k])
    somme.append(j.sum())

moyenne_jour=np.array(somme).mean()

somme_prix=[]
for k in range(len(prix)):
    j=np.array(prix[k])
    somme_prix.append(j.sum())

print("benef par jour :", somme)
print("benef moyen :", moyenne_jour)

print("benef par jour avec prix constant : ", somme_prix)