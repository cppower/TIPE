'''
ouvrir fichier txt
pour chacune des parties
	jouer la partie
	mettre chaque position dans une bdd temp
	a la fin en fonction du gagnant actualiser les poids
	pour chaque position
		si elle n'est pas presente dans la bdd globale
			la mettre dans la bdd
		actualiser la moyenne

structure bdd global
pB:pN:dB:dN;valeur;nb.'''
import os
import numpy as np
from dames import testDFS
from tkinter import * 
count = 0
scoreFinal=""
winner=""
localBDD = [[],[]]
blancHaut = False
INFINI=10**10
	#Déplacements
cat1 =  [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45]
d1 = [-5,-4,5,6]
d2 =  [-6,-5,4,5]
class Plateau:
	def __init__(self,pB= 1<<50|1<<49|1<<48|1<<47|1<<46|1<<45|1<<44|1<<43|1<<42|1<<41|1<<40|1<<39|1<<38|1<<37|1<<36|1<<35|1<<34|1<<33|1<<32|1<<31,
	 pN=1<<20|1<<19|1<<18|1<<17|1<<16|1<<15|1<<14|1<<13|1<<12|1<<11|1<<10|1<<9|1<<8|1<<7|1<<6|1<<5|1<<4|1<<3|1<<2|1<<1, dB=0,dN=0):
		self.pionsBlancs=pB
		self.pionsNoirs=pN
		self.damesBlanches=dB
		self.damesNoires=dN
		
def joueHumain(origine, coup, arrivee, plateau, noir):
	dame = False
	if (not noir and (plateau.damesBlanches>>origine)%2==1) or (noir and (plateau.damesNoires>>origine)%2==1):
		dame = True
	if coup=="-":
		return modifieDamier(origine, coup, arrivee, plateau, noir, dame)
	else:
		if noir:
    		chemins = testDFS.DFS(origine,plateau.pionsBlancs|plateau.damesBlanches,plateau.pionsBlancs,plateau.pionsNoirs,plateau.damesBlanches,plateau.damesNoires, dame)
		else:
    		chemins = testDFS.DFS(origine,plateau.pionsNoirs|plateau.damesNoires,plateau.pionsBlancs,plateau.pionsNoirs,plateau.damesBlanches,plateau.damesNoires, dame)     
    	cheminsPossibles =  []
    	cheminRetenu =  []
    	maximum = 0
    	iMax = 0 
		for i in range(0,len(chemins)): 
            if chemins[i][1]==arrivee:
                cheminsPossibles.append([chemins[i][0], chemins[i][2], chemins[i][3]]) #Choix des chemins arrivant au bon endroi
        for i in range(0,len(cheminsPossibles)):
        	if cheminsPossibles[i][0]>maximum:
                maximum = cheminsPossibles[i][0]    					#puis choix des plus longs chemins
                iMax = i
    	cheminRetenu = [cheminsPossibles[iMax][1], cheminsPossibles[iMax][2]] #param1:  pions pris, param2 : dames prises   
		return modifieDamier(origine, "x", arrivee, plateau, noir, dame, cheminRetenu.copy())	

def modifieDamier(origine, coup, arrivee, plateau, noir, dame, chemin = None): #Function complete
	nPB=plateau.pionsBlancs
	nPN = plateau.pionsNoirs
	nDB = plateau.damesBlanches
	nDN = plateau.damesNoires
	if not dame:
		if noir:
			if arrivee not in  [46,47,48,49,50]: #promotion blanc
				nPN ^= (1<<origine)
				nPN ^= (1<<arrivee)
			else:
				nPN ^= (1<<origine)
				nDN ^= (1<<arrivee)		
		else:
			if arrivee not in [1,2,3,4,5]: #promotion noire
				nPB ^= (1<< origine)
				nPB ^= (1<<arrivee)
			else:
				nPB^= (1<<origine)
				nDB ^= (1<<arrivee)
	else:
		if noir:
			nDN ^= (1<<origine)
			nDN ^= (1<<arrivee)
		else:
			nDB ^= (1<<origine)
			nDB ^= (1<<arrivee)

	if coup == "x":
		for pion in chemin[0]: # Suppression des pions ennemis du plateau
			if noir:
				nPB ^= (1<<pion)
			else:
				nPN ^= (1<<pion)
		for dam in chemin[1]: #Suppression des dames ennemies du plateau
			if noir:
				nDB ^= (1<<dam)
			else:
				nDN ^= (1<<dam)


	npla =  Plateau(nPB,nPN,nDB, nDN)
	return npla
def increment(line, elements, delimiter=';'):
    if not elements:
        return
    chaine,couleur,valeur, inc = line.split(delimiter)
    inc = int(inc)
    if (chaine+";"+couleur) not in elements[0]:
        inc = inc
    else:
        a = elements[0].index((chaine+";"+couleur))
        newVal = elements[1][a]
        elements[0].remove((chaine+";"+couleur))
        del elements[1][a]
        valeur=float(valeur)
        valeur = (valeur*inc+newVal)/(inc+1)
        valeur = str(round(valeur,4))
        inc += 1

    new_line = '{chaine};{couleur};{valeur};{inc}\n'.format(chaine=chaine, couleur=couleur,valeur= valeur,inc=inc)

    return new_line
def updateGlobalBDD2():
    print("Mise à jour de la bdd2")
    with open('bdd2.txt', 'a+') as f:
        lines = []
        for i in range(len(localBDD[0])):
            lines.append(localBDD[0][i]+";"+str(round(localBDD[1][i],4))+"\n")
        f.writelines(lines)
def updateGlobalBDD():
    print("Mise à jour de la bdd")
    with open('bdd.txt', 'r+') as f:
        allLignes = [line.rstrip('\n') for line in f]
        lines = []
        for line in allLignes:
            new = increment(line, localBDD)
            lines.append(new)
        
        for i in range(len(localBDD[0])-1):
            lines.append(localBDD[0][i]+";"+str(round(localBDD[1][i],4))+';1\n')
        f.seek(0)
        f.truncate()
        f.writelines(lines) # écriture de l'ensemble des lignes
def updateLocalBDD(pionsBlancs, pionsNoirs, damesBlanches, damesNoires,coup,tour, nbTours,noir,winner):
	global count
	global localBDD
    if noir and winner=="N":
        signe=1
    elif not noir and winner=="B":
        signe=1
    else:
        signe = -1
    if winner=="D":
        signe=0
	#s=str(pionsBlancs)+":"+str(pionsNoirs)+":"+str(damesBlanches)+":"+str(damesNoires)+":"+str(coup)
    s=str(pionsBlancs)+":"+str(pionsNoirs)+":"+str(damesBlanches)+":"+str(damesNoires)
    if noir:
       s+=";1"
    else:
        s+=";-1"
    
	localBDD[0].append(s)
	localBDD[1].append((signe*tour/nbTours))
	count+=1

def occupee():
    return damesBlanches | damesNoires | pionsBlancs | pionsNoirs

def litFichier(i):
    global scoreFinal
    global winner,blancHaut
    os.chdir("/Users/Victor/Dames/parties_champions/")    
    mon_fichier = open("dames"+str(i)+".txt", "r")
    contenu = mon_fichier.read()
    s = ""
    i=0
    while contenu[i]!='\n':
        s+=contenu[i]
        i+=1
    i+=1
    t=""
    while contenu[i]!='\n':
        t+=contenu[i]
        i+=1
    i+=1
    while contenu[i]!='\n':
        scoreFinal+=contenu[i]
        i+=1
    scoreFinal = scoreFinal[0]+scoreFinal[2]
    if scoreFinal[0]=='1':
        if scoreFinal[1]=='2':
            winner="D"
        else:
            winner ="B"
    elif scoreFinal[1]=='1':
        winner="N"
    else:
        winner=""
    contenu = contenu[(i+1)::]
    nbTours = int(s)
    blancHaut = False
    if t=='1':
        blancHaut = True
    mon_fichier.close()
    contenu = contenu.replace('\n',' ')
    return preTraitement(contenu,nbTours,blancHaut)
def preTraitement(chaine,nbTours, blancHaut):
    chaineTmp = chaine
    for i in range(nbTours,0,-1):
        number = str(i)+". "
        chaineTmp = chaineTmp.replace(number,'')
    print(chaineTmp)
    return chaineTmp, nbTours, blancHaut   
def affichageGUI(pionsBlancs,pionsNoirs,damesBlanches, damesNoires):
    gui=[[0,50],[0,150],[0,250],[0,350],[0,450],[50,0],[50,100],[50,200],[50,300],[50,400],[100,50],[100,150],[100,250],[100,350],[100,450],
[150,0],[150,100],[150,200],[150,300],[150,400],[200,50],[200,150],[200,250],[200,350],[200,450],[250,0],[250,100],[250,200],[250,300],[250,400],
[300,50],[300,150],[300,250],[300,350],[300,450],[350,0],[350,100],[350,200],[350,300],[350,400],[400,50],[400,150],[400,250],[400,350],[400,450],
[450,0],[450,100],[450,200],[450,300],[450,400]]
    fenetre = Tk()
    label = Label(fenetre, text="DAMIER")
    label.pack()
    canvas = Canvas(fenetre, width=500, height=500)
    for i in range(0,10):
        for j in range(0,10):
            if (i%2==0 and j%2==1) or (i%2==1 and j%2==0):
                canvas.create_rectangle(i*50,j*50,i*50+50,j*50+50,fill='brown')
    
    if not blancHaut:          
        for i in range(1,51):
            canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,font=("Purisa", 12),text=str(i), fill='black')
            if (pionsNoirs>>i)%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='black')
                canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,font=("Purisa", 12),text=str(i), fill='white')

            elif (pionsBlancs>>i)%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='white')
            elif (damesNoires>>i)%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='black')
                canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,text='R', fill='white')
            elif (damesBlanches>>i)%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='white')
                canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,text='R', fill='black')
    else:
        for i in range(1,51):
            canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,font=("Purisa", 12),text=str(50-i+1), fill='black')
            if (pionsNoirs>>(50-i+1))%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='black')
                canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,font=("Purisa", 12),text=str((50-i+1)), fill='white')

            elif (pionsBlancs>>(50-i+1))%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='white')
            elif (damesNoires>>(50-i+1))%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='black')
                canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,text='R', fill='white')
            elif (damesBlanches>>(50-i+1))%2==1:
                canvas.create_oval(gui[i-1][1],gui[i-1][0],gui[i-1][1]+50,gui[i-1][0]+50,fill='white')
                canvas.create_text(gui[i-1][1]+25,gui[i-1][0]+25,text='R', fill='black')   
    canvas.pack()
    fenetre.mainloop()
def affichage(pionsBlancs, pionsNoirs, damesBlanches, damesNoires):
    a = int(pionsNoirs | damesNoires)
    b=  int(pionsBlancs|damesBlanches)      
    for i in range(1,50,5):
        if i%2==1:
            print(" ", end=' ')
        for k in range(0,5):
            print((b>>(i+k))%2-(a>>(i+k))%2, end='   ')
        print("")
    
  
#INITIALISATION
def main(i):
    global localBDD
    plateau = Plateau()
    noir = False
    pointeur = 0
    chaine, nbTours, blancHaut = litFichier(i)
    localBDD = [[],[]]
    
    #affichage(pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
    #FIN INITIALISATION
    
    for i in range (0,nbTours):
        nxtChar = 0
        while chaine[pointeur+nxtChar].isnumeric():
            nxtChar+=1
        a = int(chaine[pointeur:pointeur+nxtChar])-1
        c = chaine[pointeur+nxtChar]
        pointeur = pointeur+nxtChar+1
        nxtChar = 0
        while chaine[pointeur+nxtChar].isnumeric():
            nxtChar+=1
        b = int(chaine[pointeur:pointeur+nxtChar])-1
        pointeur = pointeur+nxtChar+1
        a+=1
        b+=1
        cJ = str(a)+str(c)+str(b)
        print(str(a)+c+str(b))
        dame = False
        coup=c
        pionsBlancs = plateau.pionsBlancs
        pionsNoirs = plateau.pionsNoirs
        damesBlanches = plateau.damesBlanches
        damesNoires = plateau.damesNoires
        updateLocalBDD(pionsBlancs,pionsNoirs, damesBlanches,damesNoires,cJ,i,nbTours,noir,winner)
        #FIN LECTURE
        plateau=joueHumain(a, c, b , plateau, noir)                
        noir = not noir
        #affichageGUI(pionsBlancs, pionsNoirs, damesBlanches,damesNoires)
    updateGlobalBDD()

#216,232
for iPartie in range(300,400):
    main(iPartie)

