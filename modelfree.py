import numpy as np
class modelfree:

    def __init__(self, nb_states, stock_beg, pmin, pmax,k):
        self.Nb_States = nb_states
        self.Stock_beg = stock_beg


        self.liste_Prix = np.array([])

        self.pmin = pmin
        self.pmax = pmax
        self.k = k

        pas = (self.pmax - self.pmin) / (self.k - 1)
        for i in range(self.k):
            self.liste_Prix = np.append(self.liste_Prix, (self.pmin + i * pas))

        self.qvalues = [[[1 for k in range(len(self.liste_Prix))] for i in range(self.Stock_beg+1)] for j in range(self.Nb_States)]
        self.sigma = 0.1
        self.gamma = 0.5

    def updateQ(self,s,a, s_p):
        time_beg = s[0]
        stock_beg = s[1]
        time_end = s_p[0]
        stock_end = s_p[1]

        reward = (stock_beg-stock_end)*self.liste_Prix[a]


        Vopt,argmax  = self.findArgmax(s_p)
        self.qvalues[time_beg][stock_beg][a] = (1-self.sigma)*self.qvalues[time_beg][stock_beg][a] + self.sigma*(reward+self.gamma*Vopt)

    def findArgmax(self,s):
        maximum = -np.inf
        argmax = -1
        for i in range(len(self.liste_Prix)):
            if self.qvalues[s[0]][s[1]][i] >= maximum:
                maximum = self.qvalues[s[0]][s[1]][i]
                argmax = i
        return maximum, argmax