from random import *
from time import time
from dames import testDFS
NB_PARAMS = 1
TAILLE_CHROMO = 4
TAILLE_TOTALE = NB_PARAMS*TAILLE_CHROMO
POPULATION = 100
MUTATION = 0.005
CROSSOVER = 0
NB_GENERATIONS = 1
resultats = [0 for i in range(0,POPULATION)]

class Plateau:
	def __init__(self,pB= 1<<50|1<<49|1<<48|1<<47|1<<46|1<<45|1<<44|1<<43|1<<42|1<<41|1<<40|1<<39|1<<38|1<<37|1<<36|1<<35|1<<34|1<<33|1<<32|1<<31,
	 pN=1<<20|1<<19|1<<18|1<<17|1<<16|1<<15|1<<14|1<<13|1<<12|1<<11|1<<10|1<<9|1<<8|1<<7|1<<6|1<<5|1<<4|1<<3|1<<2|1<<1, dB=0,dN=0):
		self.pionsBlancs=pB
		self.pionsNoirs=pN
		self.damesBlanches=dB
		self.damesNoires=dN

INFINI=10**10
	#Déplacements
cat1 =  [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45]
d1 = [-5,-4,5,6]
d2 =  [-6,-5,4,5]
#Gestion des bords

fZone = [1     ,2    , 3   ,4    ,5  ,46  ,  47  ,48    ,49   ,50   ,6   ,16    ,26   ,36    ,15    ,25  ,35  ,45]
vMove = [[5,6],[5,6],[5,6],[5,6],[5],[-5],[-5,-6],[-5,-6],[-5,-6],[-5,-6],[-5,5],[-5,5],[-5,5],[-5,5],[-5,5],[-5,5],[-5,5],[-5,5]]
arbre = []
#© Victor Amblard
history={}

def minimaxAB(profondeur,nodeId, arbre,alpha,beta,color,noir): #Effectue l'algo minimax + elagage AB  FONCTIONNE CORRECTEMENT
    global hashmap
    global valeurs
    global best_value,best_move
	if profondeur==4 and not noir:
		return arbre[nodeId][7][1]*color
	if profondeur==4 and noir:
		return arbre[nodeId][7][0]*color
    val=-INFINI
    for fils in ids:
        if fils%10==profondeur+1 and arbre[fils][0]==nodeId:
            v = -minimaxAB(profondeur+1,fils,arbre,-beta,-alpha, -color,noir)
            if v>val:
                val =v
            alpha = max(alpha, v)
            if alpha>=beta:
				break
    if profondeur==1:
        valeurs[nodeId]=val
    return val
def compute_zobrist(plateau): #Fonction de hachage du damier  O(n)
    return int(str(plateau.pionsBlancs)+str(plateau.pionsNoirs)+str(plateau.damesBlanches)+str(plateau.damesNoires))
def evalue(plateau, noir,b): #Function complete
	pB = plateau.pionsBlancs
	pN = plateau.pionsNoirs
	dB = plateau.damesBlanches
	dN = plateau.damesNoires
	totalB=0
	totalN=0
	totalB2 = 0
	totalN2=0
	for i in range(0, 51):
		if (pB>>i)%2==1:
			totalB+=1
			totalB2+=1
		elif (pN>>i)%2==1:
			totalN+=1
			totalN2+=1
		elif (dB>>i)%2==1:
			totalB+=b
			totalB2+=methode
		elif (dN>>i)%2==1:
			totalN+=b
			totalN2+=methode

	if noir:
		return (totalN-totalB, totalN2-totalB2)
	return (totalB-totalN,totalB2-totalN2)

def explore(plateau,noir,b): #Function complete
	CAPTURE=False
	for i in range(1,51):
		if (noir and ((plateau.pionsNoirs|plateau.damesNoires)>>i)%2==1) or (not noir and ((plateau.pionsBlancs|plateau.damesBlanches)>>i)%2==1):
			CAPTURE = CAPTURE | prisesPossibles(i,plateau,noir,b)

	if not CAPTURE:
		for i in range(0,51):
			if (noir and ((plateau.pionsNoirs|plateau.damesNoires)>>i)%2==1) or (not noir and ((plateau.pionsBlancs|plateau.damesBlanches)>>i)%2==1):
				deplacementsPossibles(i,plateau, noir,b)

def prisesPossibles(origine, plateau, noir,b):
		#Recherche de prise
	global arbre
	global priority
	dame = False
	if (not noir and (plateau.damesBlanches>>origine)%2==1) or (noir and (plateau.damesNoires>>origine)%2==1):
		dame = True
	if noir:
    	chemins = testDFS.DFS(origine,plateau.pionsBlancs|plateau.damesBlanches,plateau.pionsBlancs,plateau.pionsNoirs,plateau.damesBlanches,plateau.damesNoires,dame)
	else:
    	chemins = testDFS.DFS(origine,plateau.pionsNoirs|plateau.damesNoires,plateau.pionsBlancs,plateau.pionsNoirs,plateau.damesBlanches,plateau.damesNoires,dame)     
	if chemins != []:
    	cheminRetenu =  []
    	maximum = 0
    	iMax = 0 
        for i in range(0,len(chemins)):
        	if chemins[i][0]>maximum:
                maximum = chemins[i][0]    
                arrivee = chemins[i][1]					#puis choix des plus longs chemins
                iMax = i
    	cheminRetenu = [chemins[iMax][2], chemins[iMax][3]]
    	#print(chemins)
    	#print(cheminRetenu) #param1:  pions pris, param2 : dames prises   
		priority = maximum
		nPlateau = modifieDamier(origine, "x", arrivee, plateau, noir, dame, cheminRetenu.copy())	
		arbre.append((origine, "x", arrivee, nPlateau, noir, priority, evalue(nPlateau,noir,b)))
		return True
	return False
def deplacementsPossibles(origine, plateau, noir,b): #Function complete
		global arbre
		pB = plateau.pionsBlancs
		pN = plateau.pionsNoirs
		dB = plateau.damesBlanches
		dN = plateau.damesNoires
		dame = False
		if (not noir and (dB>>origine)%2==1) or (noir and (dN>>origine)%2==1):
			dame = True
		if not dame:
			if origine in cat1:
				for deplacement in d1:
					arrivee = origine+deplacement
					if ((origine not in fZone) or (origine in fZone and deplacement in vMove[fZone.index(origine)])) and arrivee>=0 and arrivee<=50:
						if ((pB|pN|dB|dN)>>arrivee)%2==0:
							if (noir and arrivee-origine>0) or (not noir and arrivee-origine<0):
								nplat = modifieDamier(origine, "-",arrivee, plateau, noir,False)
								arbre.append((origine, "-",arrivee, nplat,noir, 0, evalue(nplat, noir,b)))
			else:
				for deplacement in d2:
					arrivee=origine+deplacement
					if ((origine not in fZone) or (origine in fZone and deplacement in vMove[fZone.index(origine)])) and arrivee>=0 and arrivee<=50:
						if ((pB|pN|dB|dN)>>arrivee)%2==0:
							if (noir and arrivee-origine>0) or (not noir and arrivee-origine<0):
								nplat = modifieDamier(origine, "-",arrivee, plateau, noir,False)
								arbre.append((origine, "-", arrivee, nplat, noir, 0, evalue(nplat, noir,b)))

		else:
			for i in range(0,4):
				cur = origine
				if cur in cat1:
					deplacement = d1[i]
				else:
					deplacement = d2[i]
				while (cur not in fZone) or (cur in fZone and deplacement in vMove[fZone.index(cur)]) and cur+deplacement>=0 and cur+deplacement<=50:
					if ((pB|pN|dB|dN)>>(cur+deplacement))%2!=0:
						break
					#print(str(cur+deplacement)+" "+str(i))
					nplat = modifieDamier (origine,  "-",cur+deplacement,plateau, noir, True)
					arbre.append((origine, "-", cur+deplacement, nplat, noir, 0, evalue(nplat, noir,b)))
					if cur in cat1:
						deplacement = d2[i]
						cur += d1[i]
					else:
						deplacement = d1[i]
						cur+=d2[i]

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

def highestPriority(plateau,noir):
	global arbreTotal
	iMax = 0
	maxi = -INFINI
	for i in range(0,profondeurs[1]):
		element = arbreTotal[ids[i+1]]
		if element[2]=='x':
			if element[-2]>maxi:
				iMaxi=ids[i+1]
				maxi=element[-2]
	if maxi != -INFINI:
		return iMaxi
	else:
		a= minimaxAB(0,0,arbreTotal,-INFINI,INFINI,1,noir)
		maxi =-INFINI
		iMax = 0
		for (key,val) in valeurs.items():
			if val>maxi:
				maxi=val
				iMax=key
		return iMax
				
def creeArbre(noir, plateau):
	global arbre
	global ids
	global arbreTotal
	global profondeurs
	global history
	profondeurs = [0 for i in range(0,10)]
	arbreTotal = {}
	arbreTotal[0]=(-INFINI,INFINI,"",-INFINI,plateau, not noir, -INFINI,-INFINI)

	ids = [0]
	deb = time()
	for profondeur in range(1,7):
	    #print("------profondeur--------- "+str(profondeur))
	    for id in ids:
	    	if id%10 == profondeur - 1 :
	    		(dep, coup, arr,plateau, noir,evalu,priority) = (arbreTotal.get(id))[1:]
	    		noir = not noir
	            if compute_zobrist(plateau) in history:
					break
	            arbre= []
				explore(plateau, noir)
	    		for elem in arbre:
	    		    tmpId=randint(0,10**8) 
		    		while tmpId in ids :
		    			tmpId=randint(0,10**8)
	                newId=tmpId-(tmpId%10)+profondeur
		    		ids.append(newId)
		    		profondeurs[profondeur]+=1
		    		arbreTotal[newId] = (id,)+elem
	en=time()
	delta=en-deb
	print(delta)
	#print(len(arbreTotal))
	return arbre
def play(a,b):
    pass
def find(a):
    pass    
def initialise():
    popu = []
    for i in range(0,POPULATION):
        popu.append(randint(0,2**TAILLE_TOTALE))
    return popu

def fitness(i, chaine):
    curParams = [0 for i in range(0,NB_PARAMS)]
    curPl = Plateau()
    total=0
    print(chaine)
    for i in range(0, NB_PARAMS):
        curParams[i]= (chaine>>TAILLE_CHROMO)<<TAILLE_CHROMO
        chaine=chaine>>TAILLE_CHROMO
    curParams.reverse()
    print(curParams)
    for i in range(0, 10):
		arbreTotal =  {}
		priority = 0
		valeurs  = {}
		history={}
		priority = 0
		creeArbre(True, curPl)
		bestMove = highestPriority(nPlateau,True)
        nPlateau = arbreTotal[bestMove][4]
        tPlateau = find(curPl)
        total+=(nPlateau==tPlateau)
    resultats[i]=total
def selectionRoulette(curPop):
    nPop = []
    somme = sum(resultats)
    for i in range(0,int((1-CROSSOVER)*POPULATION)):
        r = random() * somme
        s = somme
        c = False
        for i in range(0, POPULATION):
            s-=resultats[i]
            if s<=0:
                nPop.append(curPop[i])
                c=True
        if not c:
            nPop.append(curPop[-1])
    return nPop    
    
def mutation():
    for i in range(0,POPULATION):
        for j in range(0,TAILLE_TOTALE):
            if random() > MUTATION:
                popu[i]^= (1<<j)

    return popu

popu = initialise()
for i in range(0,NB_GENERATIONS):
    print("Generation "+str(i))
    for j in range(0, POPULATION):
        fitness(j, popu[j])
    popu = selectionRoulette(popu)
    popu = mutation()
    #popu = crossover()
    

            
    