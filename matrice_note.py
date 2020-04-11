import numpy as np

def genererMatrice(n_user,n_plat):
    m=np.array([[0 for k in range(n_plat)] for j in range(n_user)])
    for user in range(n_user):
        for plat in range(n_plat):
            m[user][plat]=(np.random.randint(1,plat+3))
    return m


def list_to_rank(list,taille_ranking):
    #on prend juste en compte la note ici, on pourrait faire plus compliqué
    #part=np.argpartition(list,-taille_ranking)[-taille_ranking:]     #temps linéaire

    aux=[(list[i],i) for i in range(len(list))]

    aux.sort()
    aux.reverse()
    sortie=[x[1] for x in aux]
    sortie=sortie[:taille_ranking]
   # O(nlog(n)) mais uniquement sur taille_ranking elements et pas sur tous les items !
   # sortie=[aux[taille_ranking-i-1][1] for i in range(taille_ranking)]    #trier dans le bon ordre
    return sortie


def mat_to_rank2(matrice_note,taille_ranking,n_plat):

    n_user, n_item = matrice_note.shape
    rang=[]
    for user in range(n_user):
        #print(matrice_note[user])

        ranking=list_to_rank(matrice_note[user],min(n_plat,taille_ranking))
        #print(ranking)
        rang.append(ranking)

    return np.array(rang)


def rang_moyen(ranking,n_plat):
    n=len(ranking) #nb d'utilisateurs
    plat=[0 for k in range(n_plat)]
    for classement in range(len(ranking[0])):
        for user in range(n):
            num_plat=ranking[user][classement]
            plat[num_plat]+=(classement+1)/n

    return np.array(plat)

