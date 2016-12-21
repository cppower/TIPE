fichier = "citystate.in"
FichierI = open(fichier, "r")
fichierSortie = 'citystate.out'
FichierO = open(fichierSortie, "a+")
lines = FichierI.readlines()
FichierI.close()
n,= map(int,lines[0].split())
villes = []
etats = {}
for line in lines[1:]:
    ville,etat = map(str, line.split())
    villes.append(ville)
    nxt = ville[0:2]+etat
    if nxt not in etats:
        etats[nxt] = 0
total = 0
for key, value in etats.items():
    if (key[2:]+key[0:2]) in etats:
        total+=1

FichierO.write(str(int(total/2)))
FichierO.close()
    