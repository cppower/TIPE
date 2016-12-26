import os
import copy     
import numpy as np
from dames import testDFS
from dames import reseauNeurones
from time import time
from random import *
from pprint import pprint 
from tkinter import * 
from dames import DFSV2

INFINI = 10**10
epsilon = 10**-5
log = []
borderMask =  [1,2,3,4,5,6,7,8,9,10]
cur_arbre = []
deltaP = [-5,-4,5,6]
pairs = [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45]
deltaI = [-6,-5,4,5]
fZone = [1,2,3,4,5,6,16,26,36,46,47,48,49,50,15,25,35,45]
borders = [[1,[0,1]],[2,[0,1]], [3,[0,1]],[4,[0,1]],[5,[0,1,3]],[6,[0,2]],[16,[0,2]],[26,[0,2]],[36,[0,2]],[46,[0,2,3]],[47,[2,3]],[48,[2,3]],[49,[2,3]],[50,[2,3]],
[15,[1,3]],[25,[1,3]],[35,[1,3]],[45,[1,3]]]
turn = 0
zobritz = [[0 for i in range(0,4)] for j in range(0,100)]
for i in range(0,100):
    for j in range(0,4):
        zobritz[i][j]=(int(random()*2**31))

hashmap = {}
history={}
blancHaut = False
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
def occupee(pionsBlancs,pionsNoirs,damesBlanches,damesNoires):
    return damesBlanches | damesNoires | pionsBlancs | pionsNoirs

def compute_zobrist(pionsBlancs,pionsNoirs,damesBlanches,damesNoires): #Fonction de hachage du damier  O(n)
    return int(str(pionsBlancs)+str(pionsNoirs)+str(damesBlanches)+str(damesNoires))
def evaluation_simple(pionsBlancs,pionsNoirs, damesBlanches,damesNoires, couleur):
    valBlanche=0
    valNoir = 0
    for i in range(1,51):
            if (pionsBlancs>>i)%2==1:
                valBlanche+=1
            elif (pionsNoirs>>i)%2==1:
                valNoir+=1
            elif (damesBlanches>>i)%2==1:
                valBlanche+=3
            elif (damesNoires>>i)%2==1:
                valNoir+=3

    if couleur:
        return (valNoir-valBlanche)
    else: 
        return (valBlanche-valNoir)

def minimaxAB(profondeur,nodeId, arbre,alpha,beta,color): #Effectue l'algo minimax + elagage AB  FONCTIONNE CORRECTEMENT
    global hashmap
    global valeurs
    global best_value,best_move
    if profondeur==5:
        return arbre[nodeId][8]*color
    val=-INFINI
    for fils in ids:
        if fils%10==profondeur+1 and arbre[fils][0]==nodeId:
            v = -minimaxAB(profondeur+1,fils,arbre,-beta,-alpha, -color)
            if v>val:
                val =v
            alpha = max(alpha, v)
            if alpha>=beta:
                break
    if profondeur==1:
        valeurs[nodeId]=val
    return val
def calculDamier(a, coup,b, noir, pionsBlancs, pionsNoirs, damesBlanches, damesNoires):
    dame = False
    p=0
    if (noir and (damesNoires>>a)%2==1) or  (not noir and (damesBlanches>>a)%2==1): #Vérifie si la case de départ est occupée par une dame
        #print("Dame")
        dame = True 

    #damier[x_dep][y_dep] = 0
    if coup=='-':
        if noir and not dame:
            if b in [47,48,49,50]:
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
            if not dame:
                if noir:
                    chemins = testDFS.DFS(a,pionsBlancs|damesBlanches,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
                else:
                    chemins = testDFS.DFS(a,pionsNoirs|damesNoires,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)     
                cheminsPossibles =  []
                cheminRetenu =  []
                print("--------")
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
                print(cheminRetenu)
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

            cheminsPossibles =  []
            cheminRetenu =  []
            for k in range(0,len(chemins)): 
                if chemins[k][1]==b:
                    cheminsPossibles.append([chemins[k][0], chemins[k][2], chemins[k][3]]) #Choix des chemins arrivant au bon endroit
            maximum = 0
            iMax = 0
            if cheminsPossibles==[]:
                print("Failed to find any legal path")
            else:#debug   
                for i in range(0,len(cheminsPossibles)):
                    if cheminsPossibles[i][0]>maximum:
                        maximum = cheminsPossibles[i][0]    #puis choix des plus longs chemins
                        iMax = i
                cheminRetenu = [cheminsPossibles[iMax][1], cheminsPossibles[iMax][2]] 
                p = len(cheminRetenu[0])+len(cheminRetenu[1])#param1:  pions pris, param2 : dames prises
                print(p)
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
    return (pionsBlancs, pionsNoirs, damesBlanches, damesNoires,p)
def verifieValidite(depart, arrivee, coup, noir,pionsBlancs, pionsNoirs, damesBlanches, damesNoires): #TO DO FIX VALIDATION CAPTURE
    if coup=='-':
        if (damesBlanches>>depart)%2==0 or (damesNoires>>depart)%2==0:  #pas un mouvement de dames
            if (occupee(pionsBlancs,pionsNoirs,damesBlanches,damesNoires)>>arrivee)%2==0:
                if depart not in borderMask: 
                    if (noir and ((depart in pairs and arrivee-depart in deltaP) or (depart not in pairs and arrivee-depart in deltaI ))) or (not noir and ((depart in pairs and arrivee-depart in deltaP) or (depart not in pairs and arrivee-depart in deltaI ))):
                        if (noir and arrivee-depart<0) or (not noir and arrivee-depart>0):
                            return False
                        if depart in fZone and ((depart in pairs and deltaP.index(arrivee-depart) in (borders[fZone.index(depart)][1])) or (depart not in pairs and deltaI.index((arrivee-depart)) in (borders[fZone.index(depart)][1]))):
                            return False
                        return True
            return False
        else:
            return False #A compléter
    elif coup=='x':
        if (noir and (damesNoires>>depart)%2==1) or  (not noir and (damesBlanches>>depart)%2==1): # Capture avec dame
            print("Capture avec dame") 
            if noir:
                chemins = testDFS.DFS(depart,pionsBlancs|damesBlanches,pionsBlancs,pionsNoirs,damesBlanches,damesNoires,True)
            else:
                chemins = testDFS.DFS(depart,pionsNoirs|damesNoires,pionsBlancs,pionsNoirs,damesBlanches,damesNoires,True)  
        else:    
            if noir:
                chemins = testDFS.DFS(depart,pionsBlancs|damesBlanches,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
            else:
                chemins = testDFS.DFS(depart,pionsNoirs|damesNoires,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)  
            cheminsPossibles =  []
            for i in range(0,len(chemins)): 
                if chemins[i][1]==arrivee:
                   cheminsPossibles.append([chemins[i][0], chemins[i][2], chemins[i][3]]) #Choix des chemins arrivant au bon endroit
            maximum = 0
            iMax = 0
            if cheminsPossibles==[]:
                return False  
            return True
        '''
        else: #déplacement simple d'une dame

        elif damier[depart[0]][depart[1]]==2*mod:
            if damier[arrivee[0]][arrivee[1]]==0:
                for i in range (0,4):
                    for l in range(1,10):
                        if DFS.dansDamier(depart[0]+l*delta[i][0],depart[1]+l*delta[i][1]):
                            if (damier[depart[0]+l*delta[i][0]][depart[1]+l*delta[i][1]]<0 and noir) or (damier[depart[0]+l*delta[i][0]][depart[1]+l*delta[i][1]]>0 and not noir):
                                break
                        if [arrivee[1]-depart[1],arrivee[0]-depart[0]]==[l*delta[i][0],l*delta[i][1]]:
                            return True
            return False
        return False
    elif coup=='x': #prise
        if (damesBlanches>>depart)%2==0 or (damesNoires>>depart)%2==0: #pas un mouvement de dames
            chemins = DFS. DFS_pion(depart[0],depart[1],noir,damier)
            for i in range(0,len(chemins)):
                if  

        elif damier[depart[0]][depart[1]]==2*mod:
            #print("rafle dame")
            chemins = DFS.plusLongCheminDames(damier, casesNoires,0,0, depart, arrivee, noir,False)
            #print("DFS over")
            #print(str(depart)+" "+str(arrivee)+" "+str(noir))
            if chemins !=[]:
                return True
            return False
        return False
    return False
    '''
def ajouteCoup(dep,arr,coup,noir, pionsBlancs,pionsNoirs, damesBlanches,damesNoires,network=None): #Ajoute un coup valide à l'arbre
    global cur_arbre
    (pionsBlancs, pionsNoirs, damesBlanches, damesNoires)= calculDamier(dep,coup,arr,noir,pionsBlancs, pionsNoirs, damesBlanches, damesNoires)[0:4]
    #evaly    = evaluation(pionsBlancs|damesBlanches,pionsNoirs|damesNoires,noir)
    #evaly = reseauNeurones.evalue(network,pionsBlancs, pionsNoirs, damesBlanches, damesNoires,noir)*2-1 #Normalement l'éval vient d'un réseau de neurones...
    evalB = evaluation_simple(pionsBlancs,pionsNoirs, damesBlanches, damesNoires,noir)
    cur_arbre.append((dep,coup,arr,pionsBlancs, pionsNoirs, damesBlanches, damesNoires,evalB))
    #print("Coup de "+str(dep)+","+str(coup)+" vers "+str(arr)+" ajouté")
    
def deplacePieceP(dep,noir,pionsBlancs, pionsNoirs, damesBlanches,damesNoires): #Vérification pour chaque case de départ pour chaque case d'arrivée s'il peut y avoir un déplacement
#Complexité à améliorer...
    global cur_arbre
    prise = False
    best = 0
    for i in range(1,51):
            if i!=dep:
                if verifieValidite(dep,i,'x',noir,pionsBlancs,pionsNoirs, damesBlanches, damesNoires):
                    prise=True
                    ajouteCoup(dep,i,'x',noir,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
    return prise
def deplacePieceN(dep,noir,pionsBlancs, pionsNoirs, damesBlanches,damesNoires): #Vérification pour chaque case de départ pour chaque case d'arrivée s'il peut y avoir un déplacement
#Complexité à améliorer...
    global cur_arbre
    for i in range(1,51):
            if dep!=i:
                if verifieValidite(dep,i,'-',noir, pionsBlancs, pionsNoirs, damesBlanches, damesNoires):
                    ajouteCoup(dep,i,'-',noir,pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
def creeArbre(noir,pionsBlancs,pionsNoirs,damesBlanches,damesNoires): #Effectue une exploration exhaustive de l'arbre des possibilités
	global cur_arbre
	global ids
	global profondeurs
	profondeurs = [0 for i in range(0,10)]
	arbre = {}
	arbre[0]=(-INFINI,INFINI,"",-INFINI, pionsBlancs, pionsNoirs, damesBlanches, damesNoires, -INFINI,noir)
    ids = [0]
    for profondeur in range(1,9):
        print("------profondeur--------- "+str(profondeur))
	    for id in ids:
	    	if id%10 == profondeur - 1 :
	    		#print("Id pere : "+str(id))
	    		(dep, coup, arr, curPB, curPN, curDB, curDN,eval,noir) = (arbre.get(id))[1:]
                if compute_zobrist(curPB, curPN, curDB, curDN) in history:
                    break
                history[compute_zobrist(curPB, curPN, curDB, curDN)]=eval
                cur_arbre= []
                saut = False
                for dep in range (1,51):
                    if (noir and ((curPN | curDN)>>dep)%2==1) or (not noir and ((curPB | curDB)>>dep)%2==1):
                        saut = saut | deplacePieceP(dep,noir,curPB, curPN, curDB, curDN)
                if not saut : 
                    for dep in range (1,51):
                        if (noir and ((curPN | curDN)>>dep)%2==1) or (not noir and ((curPB | curDB)>>dep)%2==1):
                            deplacePieceN(dep,noir,curPB, curPN, curDB, curDN)
	    		for elem in cur_arbre:
	    		    tmpId=randint(0,10**8) 
		    		while tmpId in ids :
		    			tmpId=randint(0,10**8)
                    newId=tmpId-(tmpId%10)+profondeur
		    		ids.append(newId)
		    		profondeurs[profondeur]+=1
		    		arbre[newId] = (id,)+elem+(noir,)
    
    	noir = not noir
    return arbre
# FONCTION PRINCIPALE 
def init():
    AINet = reseauNeurones.Neural_Network()
    T = reseauNeurones.trainer(AINet)
    X,Y = reseauNeurones.convertToArray()
    #T.trainMiniBatch(X,Y,2000)
    return AINet

def prochain_coup(arbre, best_move):
    fenetre = Tk()
    canvas = Canvas(fenetre, width=300, height=100)
    canvas.create_text(100,50, font=('Liberation Serif','20'),text=str(arbre[best_move][1])+arbre[best_move][2]+str(arbre[best_move][3]))
    canvas.pack()
    fenetre.mainloop()
#network = init()
pB= 1<<50|1<<49|1<<48|1<<47|1<<46|1<<45|1<<44|1<<43|1<<42|1<<41|1<<40|1<<39|1<<38|1<<37|1<<36|1<<35|1<<34|1<<33|1<<32|1<<31
pN= 1<<20|1<<19|1<<18|1<<17|1<<16|1<<15|1<<14|1<<13|1<<12|1<<11|1<<10|1<<9|1<<8|1<<7|1<<6|1<<5|1<<4|1<<3|1<<2|1<<1
dN = 0
dB = 0
n = False

while(True):
    valeurs = {}
    debut = time()
    arbre = creeArbre(False,pB, pN, dB, dN)
    inter = time()
    best_move=0
    best_value=-INFINI 
    tmp=0
    for i in range(1,profondeurs[1]+1):
        tmp = max(tmp, calculDamier(arbre[ids[i]][1],arbre[ids[i]][2],arbre[ids[i]][3],False,pB,pN, dB,dN)[4])
    if tmp==0: #Capture prioritaire
        print("Pas de prise")
        minimaxAB(0,0,arbre,-INFINI,INFINI,1)
        for (k,v) in valeurs.items():
            if v>=best_value:
                best_value=v
                best_move=k     
        print(best_value)
    else:
        nxtCoup = 0
        for i in range(1, profondeurs[1]+1):
            curA = arbre[ids[i]]
            if curA[2]=="x" and calculDamier(curA[1],curA[2],curA[3],False,pB,pN, dB,dN)[4]>best:
                best= calculDamier(curA[1],curA[2],curA[3],False,pB,pN, dB,dN)[4]
                nxtCoup = ids[i]
    fin=time()
    print(str(fin-debut)+" secondes")
    prochain_coup(arbre, best_move)
    log.append(str(arbre[best_move][1])+arbre[best_move][2]+str(arbre[best_move][3]))
    pB,pN,dB,dN,p=calculDamier(arbre[best_move][1],arbre[best_move][2],arbre[best_move][3],False, pB,pN, dB,dN)
    affichageGUI(pB,pN,dB,dN)
    #afficheListeCoups(arbre)
    a = int(input())
    c =input()
    b = int(input())
    print("L'adversaire joue : "+str(a)+c+str(b)) 
    pB,pN,dB,dN,p=calculDamier(a,c,b,True, pB,pN,dB,dN)
    affichageGUI(pB,pN,dB,dN)
    print(pB)