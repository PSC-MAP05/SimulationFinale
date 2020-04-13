# Libraries Included:
# Numpy, Scipy, Scikit, Pandas
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.special import ndtr
class scenario:
    def __init__(self, n_utilisateurs, n_periodes, n_plat, matrice_notes, matrice_Rank):


        self.n_utilisateurs = n_utilisateurs


        self.n_periodes = n_periodes

        self.n_plat = n_plat

        # tab pour savoir si un tuilsaeur a achete ou non
        # tab qui donne les indices des utilisateurs qui peuvent encore acheter

        self.tab_consom_potentiel = [i for i in range(n_utilisateurs)]
        self.matrice_notes = matrice_notes
        self.matrice_Rank = matrice_Rank
   
    def tiragePoisson(self,periode):
      
      
        a = (-abs(periode-12)+ 12)*10
        b= 1

        pam_lambd = np.random.uniform(low=a , high=a + b)

        return pam_lambd





    # tab_s est composée d'une matrice pour chaque plat. Donc pour accéder à la matrice d'un plat on fera tab_s[plat][utilisateurs][prix]

    # tab_prix sera la matrice qui pour un plat donné donne le vecteur ligne des prix pour un jour donné. Par exemple [[1 3 4 5 6 7 9] [10 10 10 10 10 10]] veut dire que pour le plat 1, on a mis les prix 1 à 20H, 3 à 20H10, 4 à 20H20. et 10 pour le plat 2

    def generer(self,propension, prix):
        # cette fonction sert à générer la  de l'utilsateurs à partir de la propension a payer
        note = (propension - prix)  /propension * 5
        return note


    def argmaxCritere(self,propension, tab_prix, periode):
        argmax = -1
        maximu = -500
        for plat in range(len(tab_prix)):
            if (propension[plat] - tab_prix[plat])/tab_prix[plat] > maximu and (propension[plat] - tab_prix[plat])>0 :
                argmax = plat
                maximu = (propension[plat]-tab_prix[plat])/tab_prix[plat]

        return argmax




    def f(self,i, n):
        if i <= n / 3:
            return 0, 0, n/3
        elif i >= 2 * n / 3:
            return 2, 2*n/3,n
        else:
            return 1, n/3, 2*n/3
            """
        k = n/self.n_plat
        for i in range(0,n,int(n/self.n_plat)):
            return i*int(self.n_plat/n), i, i + int(n/self.n_plat) """
   

    def g(self,i, e_low, e_high,p):
        i = i-e_low
        e_high = e_high - e_low
        e_low = 0
        resultat = 0
        k = e_high / self.n_plat
        n = self.n_utilisateurs

        if  (int(i /(int(e_high / self.n_plat))) == p ):
            return 5
        else:
            return np.random.uniform(1,4)

        """
        if i <= e_high / 3:
            resultat = 0
        elif i >= 2 * e_high / 3:
            resultat =  2
        else:
            resultat = 1
        return resultat
"""
        """   if p ==1:
                    resultat+=1
                    resultat %= 3
                if p==2:
                    resultat +=2
                    resultat%=3
                    """
       
    def rankTorec(self, ranking):

        return (np.exp(-ranking))*5

    def findRank(self, plat, utilisateur):
        return self.matrice_Rank[utilisateur][plat]

    def z(self,classe, gout_plat, ranking_plat):


        return 0.05*(classe+1) *(gout_plat +1)*(self.rankTorec(ranking_plat)+1)

    """def remplir_prix(self,tab_prix,jr):
        for i in range(len(tab_prix[0])):
            tab_prix[0][i] =  (1+ jr)*0.01
            tab_prix[1][i] = 2
            if tab_prix[1][i]<=0:
                tab_prix[1][i] = 0.01
            tab_prix[2][i] = 1
        return tab_prix

    """
    def simuler(self, per,  liste_prix):
        tab_ventes = [0 for i in range(self.n_plat)]
        tab_lambda = 0


        n_util_restant = len(self.tab_consom_potentiel)
        tab_lambda = self.tiragePoisson(per)
        # np = lambda
        p = tab_lambda/ n_util_restant
        temp = []
        # pour chaque personne restante, tirer une loi de bernoulli et voir si elle consomme ou pas. Si c'est le cas, on l'enlève de la liste des consommateurs potentiels
        for indice in self.tab_consom_potentiel:
            if (np.random.rand() < p):
                temp.append(indice)
        self.tab_consom_potentiel = np.array(self.tab_consom_potentiel)
        self.tab_consom_potentiel = np.delete(self.tab_consom_potentiel, temp)
        # ici, on a la liste actualisée de tous les individus susceptibles de consommer
        tab_notes = []
        for i in temp:

            propension = [0 for i in range(self.n_plat)]
            # np.random.exponential(scale= parametre)
            # maintenant on peut découper notre population selon la classe sociale et le gout pour chaque produit. L'attributino se fait en fonction de l'indice de la personne
            classe, extremite_low, extremite_high = self.f(i, self.n_utilisateurs)
            liste_notes = [0 for i in range(self.n_plat)]

            for plat in range(self.n_plat):
               # gout_plat = self.g(i, extremite_low, extremite_high, plat)

               #trouver le ranking
                ranking = self.findRank(plat,i)

                gout_plat = self.matrice_notes[i][plat]
                liste_notes[plat] = gout_plat
                propension[plat] = np.random.exponential(scale=(self.z(classe, gout_plat + 0.5,ranking)))

            plat = self.argmaxCritere(propension, liste_prix, per)

            if plat>=0:
                tab_ventes[plat] += 1
                tab_notes.append([i, plat, liste_notes[plat]])

                # on a 2 possibilités: il achete le plat qui maximise un critère, ou bien il n'achète pas

        # plt.plot([i for i in range(n_periodes)], tab_ventes[1])
        # plt.show()
        # tab_plot.append(tab_ventes[2][4])


        return tab_ventes, tab_notes

    def vente_jour(self,tab_prix):




            tab_ventes = [[0 for j in range(self.n_periodes)] for i in range(self.n_plat)]
            tab_lambda = [0 for i in range(self.n_periodes)]
            tab_consom_potentiel = [i for i in range(self.n_utilisateurs)]

            for per in range(self.n_periodes):
                n_util_restant = len(tab_consom_potentiel)
                tab_lambda[per] = self.tiragePoisson(per)
                # np = lambda
                p = tab_lambda[per] / n_util_restant
                temp = []
                # pour chaque personne restante, tirer une loi de bernoulli et voir si elle consomme ou pas. Si c'est le cas, on l'enlève de la liste des consommateurs potentiels
                for indice in tab_consom_potentiel:
                    if (np.random.rand() < p):
                        temp.append(indice)
                tab_consom_potentiel = np.array(tab_consom_potentiel)
                tab_consom_potentiel = np.delete(tab_consom_potentiel, temp)
                # ici, on a la liste actualisée de tous les individus susceptibles de consommer
                for i in temp:

                    propension = [0 for i in range(self.n_plat)]
                    # np.random.exponential(scale= parametre)
                    # maintenant on peut découper notre population selon la classe sociale et le gout pour chaque produit. L'attributino se fait en fonction de l'indice de la personne
                    classe, extremite_low, extremite_high = self.f(i, self.n_utilisateurs)
                    gout_plat = g(i,extremite_low,extremite_high,p)
                    for p in range(self.n_plat):
                        #gout_plat = self.g(i, extremite_low, extremite_high, p)
                        gout_plat = self.matrice_notes[i][p]
                        propension[p] = np.random.exponential(scale=(self.z(classe, gout_plat+0.5)))
                    plat = self.argmaxCritere(propension, tab_prix, per)
                    tab_ventes[plat][per] += 1
                    tab_notes.append([i,gout_plat])
                    # on a 2 possibilités: il achete le plat qui maximise un critère, ou bien il n'achète pas

           # plt.plot([i for i in range(n_periodes)], tab_ventes[1])
            #plt.show()
            #tab_plot.append(tab_ventes[2][4])



            return tab_ventes, tab_notes


    """jr = 500
    tab_ventes_final,tab_prix_final = vente_mois(jr)
    per = 12
    tab_X = []
    for i in range(jr):


            tab_X.append([tab_prix_final[i][0][per],tab_prix_final[i][1][per],tab_prix_final[i][2][per]])
    tab_Y = []
    for i in range(jr):

            tab_Y.append((tab_ventes_final[i][0][per]))

    #transformer tab_prix

    data = np.column_stack((tab_X, tab_Y))
    print(tab_X)
    print(tab_Y)
    np.savetxt('data_X.dat', tab_X)
    np.savetxt('data_Y.dat', tab_Y)"""





