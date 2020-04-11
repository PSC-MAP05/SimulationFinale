# produit Client supposé défini
# Segementation supposée effectuée
import numpy as np
import scipy.stats as stats
import math
import regression
import scipy.special as special


class mdp():
#PROBLEME DE LA VALEUR PAR DEFAUT
    def __init__(self, nb_states, stock_beg, fonction, pmin, pmax,k):
        self.Nb_States = nb_states
        self.Stock_beg = stock_beg

        self.tab_V = np.random.rand(self.Nb_States, self.Stock_beg+1)*0.10
        self.liste_Prix = np.array([])
        self.dic_prob = {}
        self.dic_rew = {}
        self.pmin = pmin
        self.pmax = pmax
        self.k = k
        self.coef1 = 0
        self.coef2 = 0
        self.coef3 = 0
        self.intercept = 0
        self.tabPrix = np.random.rand(self.Nb_States, self.Stock_beg+1)*0.10
        self.var_demande = 1
        pas = (self.pmax - self.pmin) / (self.k - 1)
        for i in range(self.k):
            self.liste_Prix = np.append(self.liste_Prix, (self.pmin + i * pas))
        for i in range(self.Nb_States - 1):
            for j in range(self.Stock_beg+1):
                for price in self.liste_Prix:
                    self.dic_rew[(i, j, price, i + 1)] = np.array([self.reward(i, j, price, i+1, z) for z in range(self.Stock_beg+1)])
        self.qvalues = [[0 for i in range(self.Nb_States)] for j in range(self.Stock_beg)]
        self.sigma = 0.2
        self.gamma = 0.2
        self.ranking = 0
    def Demand(self, time, price):

        return (regression.fonctionInversedeRegression(self.intercept + self.coef1*abs(time-12) + self.coef2*price + self.coef3*self.ranking))

    # alet Demand centrée en demand plus haut

    def Prob(self,i,j, prix, k,l):

        if (k != i + 1 or j< l):
            return 0
        if j == 0:
            return 0
        demande = self.Demand(i, prix)
        proba = special.ndtr(((j-l)+1-demande)/ self.var_demande) - special.ndtr((j-l-demande)/ self.var_demande)
        return proba
        # coder une densité ayant son maximum en Demand
        # retourner la probabilité


    def reward(self,i,j,prix,m,l):
        return prix*(j-l)


    def Esp(self,i,j, prix):

        P = self.dic_prob[(i,j,prix,i+1)]
        V_r = self.tab_V[i + 1] + self.dic_rew[(i,j, prix, i+1)]
        return np.dot(P, V_r)


    def ChooseAction(self,i,j):
        maximum = -np.inf
        argmax = 0
        for price in self.liste_Prix:
            esp = self.Esp(i,j,price)
            if esp>maximum:
                maximum = esp
                argmax = price
        return maximum,argmax

    def update_MDP(self):

        tab_int = np.zeros((self.Nb_States, self.Stock_beg+1))
        tab_prix = np.zeros((self.Nb_States, self.Stock_beg+1))

        for i in range(1, self.Stock_beg+1):
            tab_int[self.Nb_States - 1][i] = -5000
        tab_int[self.Nb_States - 1][0] = 0

        for i in range(self.Nb_States - 2, -1, -1):
            for j in range(self.Stock_beg+1):
                Vmax, prix = self.ChooseAction(i, j)
                tab_int[i][j] = Vmax
                tab_prix[i][j] = prix

        return tab_int, tab_prix

#permet d'initialiser le MDP avc les bons tableaux et d'update les valeurs  de V
    def remplir_MDP(self):



        # Creation action par pas de k


        # creation etats de 20h à 23h50 par pas de 10


        print("remplissange de la liste des prix : fini")


        print("remplissage des rewards fini")
        self.dic_prob = {}
        for i in range(self.Nb_States-1):
            for j in range(self.Stock_beg+1):
                for price in self.liste_Prix:

                    self.dic_prob[(i,j,price,i+1)] = np.array([self.Prob(i, j, price, i + 1, m) for m in range(self.Stock_beg+1)])
        print("remplissage des prob fini")

        self.tab_V, self.tabPrix = self.update_MDP()
        print("value iteration fini")

#attention au format de ce truc
    def findPrice(self,state):
        i = state[0]
        j = state[1]
        return self.tabPrix[i][j]

    def printMDPprice(self):
        for i in range(self.Nb_States):
            liste = []
            for j in range(self.Stock_beg):
                liste.append(self.findPrice([i,j]))
            print(liste)
    def printMDPdemande(self):
        print(self.liste_Prix)
        for i in range(self.Nb_States):
            liste = []
            for j in range(len(self.liste_Prix)):

                liste.append(self.Demand(i,self.liste_Prix[j]))

            print(liste)



