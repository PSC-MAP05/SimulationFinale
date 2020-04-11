import scenario

scen = scenario.scenario(10000,24,3)
somme1 = 0
somme2 = 0
somme3= 0
for i in range(10000):
    tab = scen.simuler(12,[10,10,10])
    somme1+=tab[0]
    somme2+=tab[1]
    somme3+=tab[2]
print(somme1/10000)
print(somme2/10000)
print(somme3/10000)