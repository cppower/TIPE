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

def updateGlobalBDD():
    print("Mise à jour de la bdd")
    with open('bdd.txt', 'r+') as f:
        allLignes = [line.rstrip('\n') for line in f]
        lines = []
        for line in allLignes:
            new = increment(line, localBDD)
            lines.append(new)
        
        for i in range(len(localBDD[0])):
            lines.append(localBDD[0][i]+";"+str(round(localBDD[1][i],4))+';1\n')
        f.seek(0)
        f.truncate()
        f.writelines(lines) # écriture de l'ensemble des lignes
def updateLocalBDD(pionsBlancs, pionsNoirs, damesBlanches, damesNoires,tour, nbTours,noir,winner):
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
    os.chdir("/Users/Victor/Dames/")    
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
    pionsBlancs= 2**50+2**49+2**48+2**47+2**46+2**45+2**44+2**43+2**42+2**41+2**40+2**39+2**38+2**37+2**36+2**35+2**34+2**33+2**32+2**31
    pionsNoirs= 2**20+2**19+2**18+2**17+2**16+2**15+2**14+2**13+2**12+2**11+2**10+2**9+2**8+2**7+2**6+2**5+2**4+2**3+2**2+2**1
    damesNoires = 0
    damesBlanches = 0
    noir = False
    pointeur = 0
    chaine, nbTours, blancHaut = litFichier(i)
    localBDD = [[],[]]
    
    affichage(pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
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
        print(str(a)+c+str(b))
        dame = False
        coup=c
        updateLocalBDD(pionsBlancs,pionsNoirs, damesBlanches,damesNoires,i,nbTours,noir,winner)
        if (noir and (damesNoires>>a)%2==1) or  (not noir and (damesBlanches>>a)%2==1): #Vérifie si la case de départ est occupée par une dame
            print("Dame")
            dame = True 
        if coup=='-':
            if noir and not dame:
                if b in [46,47,48,49,50]:
                    damesNoires ^= 2**b #promotion noire
                    pionsNoirs ^= 2**a
                else:
                    pionsNoirs ^=2**a
                    pionsNoirs ^=2**b
            elif not noir and not dame:
                if b in [1,2,3,4,5]: #promotion blanche
                    damesBlanches ^= 2**b
                    pionsBlancs ^= 2**a
                else:
                    pionsBlancs ^=2**a
                    pionsBlancs ^=2**b
            elif noir and dame:
                damesNoires ^= 2**a
                damesNoires ^= 2**b
            elif not noir and dame:
                damesBlanches ^= 2**a
                damesBlanches ^=2**b            
        else:
            if not dame:
                if noir:
                    chemins = testDFS.DFS(a,pionsBlancs|damesBlanches,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
                else:
                    chemins = testDFS.DFS(a,pionsNoirs|damesNoires,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)     
                cheminsPossibles =  []
                cheminRetenu =  []
                print(chemins)
                for i in range(0,len(chemins)): 
                    if chemins[i][1]==b:
                        cheminsPossibles.append([chemins[i][0], chemins[i][2], chemins[i][3]]) #Choix des chemins arrivant au bon endroit
                maximum = 0
                iMax = 0
                if cheminsPossibles==[]:
                    print("Failed to find any legal path") #debug   
                for i in range(0,len(cheminsPossibles)):
                    if cheminsPossibles[i][0]>maximum:
                        maximum = cheminsPossibles[i][0]    #puis choix des plus longs chemins
                        iMax = i
                cheminRetenu = [cheminsPossibles[iMax][1], cheminsPossibles[iMax][2]] #param1:  pions pris, param2 : dames prises
                for pion in range(0,len(cheminRetenu[0])): #Cas des pions
                    if noir:
                        #print("pion :")
                        print(cheminRetenu[0][pion])
                        pionsBlancs ^= 2**cheminRetenu[0][pion]
                    else:
                        #print("pion : ")
                        print(cheminRetenu[0][pion])
                        pionsNoirs ^= 2**cheminRetenu[0][pion]
                if noir:
                    pionsNoirs ^= 2**a
                    if b in [47,48,49,50]:
                        damesNoires ^= 2**b
                    else:
                        pionsNoirs ^= 2**b
                else:
                    pionsBlancs ^= 2**a
                    if b  in [1,2,3,4,5]:
                        damesBlanches ^= 2**b
                    else:
                        pionsBlancs ^= 2**b
                for dame in range(0,len(cheminRetenu[1])):
                    if noir:
                        damesBlanches ^= 2**cheminRetenu[1][dame]
                    else:
                        damesNoires ^= 2**cheminRetenu[1][dame] 
            else:
                #Cas d'une rafle avec dame
                if noir:
                    chemins = testDFS.DFS(a,pionsBlancs|damesBlanches,pionsBlancs,pionsNoirs,damesBlanches,damesNoires,True)
                else:
                    chemins = testDFS.DFS(a,pionsNoirs|damesNoires,pionsBlancs,pionsNoirs,damesBlanches,damesNoires,True)
    
                print(chemins)
                cheminsPossibles =  []
                cheminRetenu =  []
                for k in range(0,len(chemins)): 
                    if chemins[k][1]==b:
                        cheminsPossibles.append([chemins[k][0], chemins[k][2], chemins[k][3]]) #Choix des chemins arrivant au bon endroit
                maximum = 0
                iMax = 0
                if cheminsPossibles==[]:
                    print("Failed to find any legal path") #debug   
                for i in range(0,len(cheminsPossibles)):
                    if cheminsPossibles[i][0]>maximum:
                        maximum = cheminsPossibles[i][0]    #puis choix des plus longs chemins
                        iMax = i
                cheminRetenu = [cheminsPossibles[iMax][1], cheminsPossibles[iMax][2]] #param1:  pions pris, param2 : dames prises
                for pion in range(0,len(cheminRetenu[0])): #Cas des pions
                    if noir:
                        print(cheminRetenu[0][pion])
                        pionsBlancs ^= 2**cheminRetenu[0][pion]
                    else:
                        print(cheminRetenu[0][pion])
                        pionsNoirs ^= 2**cheminRetenu[0][pion]
                if noir:
                    damesNoires ^= 2**a
                    damesNoires ^= 2**b
                else:
                    damesBlanches ^= 2**a
                    damesBlanches ^= 2**b
                for dam in range(0,len(cheminRetenu[1])):
                    if noir:
                        damesBlanches ^= 2**cheminRetenu[1][dam]
                    else:
                        damesNoires ^= 2**cheminRetenu[1][dam] 
                
        noir = not noir
    #⌂affichageGUI(pionsBlancs, pionsNoirs, damesBlanches,damesNoires)
    updateGlobalBDD()

#216,232
for i in range(423,500):
    if i!=535 and i!=580:
        main(i)