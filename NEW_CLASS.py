import numpy as np
import pandas as pd
from surprise import Reader, Dataset
from surprise import SVD
import surprise



class dataset :

    def __init__(self,data,nom,jour):

        self.nom=nom
        self.jour=jour
        #data est un pd.dataframe avec 3 colonnes, user, item, rating
        self.data = data
        self.dic = {}
    def new_note(self,user,item,note):
        ajout=[user,item,note]
        if (user,item) in self.dic.keys():
            self.data.loc[self.dic[(user,item)]] = [user,item,note]
        else:
            self.data.loc[len(self.data)] = ajout
            self.dic[(user,item)]= len(self.data)

    def factorisation(self,n_user,n_item):
        #retourne la matrice note complète avec n_user et n_item
        reader = Reader()
        data = Dataset.load_from_df(self.data, reader)
        SVD = surprise.SVD(n_factors=4, n_epochs=10, lr_all=.01, reg_all=.05)
        results = surprise.model_selection.validation.cross_validate(SVD, data, measures=['MSE'], cv=3, verbose=True)
        #maintenant on rempli la matrice
        print("temps d'attente estimé : ", round(n_user * n_item / 105000), "secondes.")
        M = []
        for u in range(n_user):
            M.append([SVD.predict(u, i).est for i in range(n_item)])
        return np.array(M)

    def get(self,matrice_note,user,item):
        return matrice_note[user][item]


#df= pd.read_csv('C:\POLYTECHNIQUE\PSC\DATASET\dataset_movie_100k.csv')
#movie=dataset(df,"movie",1)
#matrice_note=movie.factorisation(600,9000)

