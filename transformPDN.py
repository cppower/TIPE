def ecris(score, tours, game,i):
    if i<10:
        fichier2 = open("dames50"+str(i)+".txt","w")
    else:
        fichier2 = open("dames5"+str(i)+".txt", "w")
        fichier2.write(str(playCount)+"\n")
    fichier2.write("1\n")
    fichier2.write(str(resultat)+"\n")
    fichier2.write(game)
cursor=0
mon_fichier = open("all5.txt", "r")
contenu = mon_fichier.read()
for i in range(0,100):
    resultatI = contenu.index("[Result ")
    resultat =  contenu[resultatI+9:resultatI+16]
    if not resultat[4].isnumeric():
        resultat = resultat[0:3]
    playCountI = contenu.index("[PlyCount ")
    playCount = contenu[playCountI+11:playCountI+14]
    if not playCount.isnumeric():
        playCount=playCount[0:2]
        cursor=playCountI+17
    else:
        cursor = playCountI+18
        
    debut = contenu[cursor:].index("[Event")
    print(contenu[cursor])
    game = contenu[cursor:cursor+debut-2]
    cursor=debut
    print("Score : "+resultat+", total : "+playCount+", partie \n"+game)
    contenu = contenu[cursor:]
    ecris(resultat, playCount,game,i)

