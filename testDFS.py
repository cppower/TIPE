pairs = [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45]
maskPrise =  [1,2,3,4,5,6,7,8,9,10]
deltaP= [-5,-4,5,6]
deltaI = [-6,-5,4,5]
lSide = [6,16,26,36,46]
rSide = [5,15,25,35,45]
uSide = [1,2,3,4,5]
fZone = [1,2,3,4,5,6,16,26,36,46,47,48,49,50,15,25,35,45]
borders = [[1,[0,1]],[2,[0,1]], [3,[0,1]],[4,[0,1]],[5,[0,1,3]],[6,[0,2]],[16,[0,2]],[26,[0,2]],[36,[0,2]],[46,[0,2,3]],[47,[2,3]],[48,[2,3]],[49,[2,3]],[50,[2,3]],
[15,[1,3]],[25,[1,3]],[35,[1,3]],[45,[1,3]]]
tmp=0
tab = ""
chemins = []
pionsPris = []
damesPrises=[]
prev= -1

vus = [False for i in range(0,51)]
'''
  1  2  3  4  5
6  7  8  9  10 
 11  12  13  14 15
16  17  18  19 20 
 21  22  23  24 25
26  27 28  29 30 
  31  32  33 34 35

etc 
'''
def occupee(a,b,c,d):
    return  a| b | c | d |tmp

def affichage(pionsBlancs,pionsNoirs,damesBlanches,damesNoires):
    a = int(pionsNoirs | damesNoires)
    b=  int(pionsBlancs|damesBlanches)
    for i in range(1,50,5):
        if i%2==1:
            print(" ", end=' ')
        for k in range(0,5):
            print((b>>(i+k))%2-(a>>(i+k))%2, end='   ')
        print("")
def DFSrec(noeud,piecesAdv,pionsBlancs, pionsNoirs, damesBlanches,damesNoires, dame=False): #Prise d'un pion todo : s'assurer que le premier déplacement est dans le sens de la marche
    global tmp   
    global pionsPris
    global targets
    global damesPrises
    global tab  
    global prev
    global chemins
    if not vus[noeud]:
        vus[noeud]=True
        #print(tab+str(noeud)) #debug
        if noeud in maskPrise:
            tab = tab[0:len(tab)-2]
        #print(chemins)
        if dame:
            for iDir in range(0,4):
                if iDir==prev:
                    iDir+=1
                if iDir==4:
                    break
                target = -1 #      CORRIGER LES DEPASSEMENTS SUR LES BORDS !
                dest=noeud
                first = True
                last=False
                while first or (not last and dest<=50 and dest>=1 and dest not in lSide and dest not in rSide):
                    #print(dest)
                    if dest in fZone and iDir in borders[fZone.index(dest)][1]:
                        last=True
                    if   (piecesAdv>>dest)%2==1:#piece ennemie localise
                        target = dest
                        break
                    else:
                        if dest in pairs:
                            d1 = deltaP[iDir]
                        else:
                            d1 = deltaI[iDir]
                    dest+=d1
                    first=False
                #if target==-1:
                    #print("No target found according to dir "+str(iDir))
                if target!=-1 and target not in targets:
                    #print("Target locked : "+str(target)+"( dir : "+str(iDir)+" )")
                    targets.append(target)
                    dest=target
                    while dest not in lSide and dest not in rSide:
                        if dest in pairs:
                            d2 = deltaP[iDir]
                        else:
                            d2 = deltaI[iDir]               
                        dest = dest+d2
                        ennPion=False
                        ennDame=False
                        if dest>=1 and dest<=50 and (occupee(pionsBlancs, pionsNoirs, damesBlanches, damesNoires)>>dest)%2==0:
                            #print("Current destination : "+str(dest))
                            tab+=" "
                            tmp ^= 2**(dest)
                            if ((pionsBlancs|pionsNoirs)>>(target))%2==1:
                                ennPion=True
                                pionsPris.append(target)
                            elif ((damesBlanches|damesNoires)>>(target))%2==1:
                                ennDame=True
                                damesPrises.append(target)
                            chemins.append([len(pionsPris)+len(damesPrises),dest,pionsPris.copy(),damesPrises.copy()]) #a remplacer le [] par damesPrises
                            prev=iDir
                            DFSrec(dest, piecesAdv, pionsBlancs, pionsNoirs, damesBlanches, damesNoires, True)
                            tmp ^= 2**(dest)
                            if ennPion:
                                pionsPris.pop()
                            elif ennDame:
                                damesPrises.pop()
                        else:
                            break
                tab = tab[0:len(tab)-2]
            #print(pionsPris)
            return chemins          
        else:
            for i in range(0,4):
                if noeud in pairs: #Traite le cas rangées paires/impaires
                    d2 = deltaP[i]
                    d1 = deltaI[i]
                else:
                    d1 = deltaP[i]
                    d2 = deltaI[i]
                #print("D1/D2"+str(d1)+" "+str(d2))
                ennPion=False
                ennDame=False
                if noeud+d1+d2<=50 and noeud+d1+d2>=1 and noeud+d2 not in lSide and noeud+d2 not in rSide and (piecesAdv | 2**(noeud+d2) == piecesAdv):
                    if noeud in borders and i  in borders[fZone.index(noeud)][1]:
                        break
                    #print(str(noeud+d1+d2))
                    #affichage(pionsBlancs,pionsNoirs,damesBlanches,damesNoires)
                    if ((occupee(pionsBlancs,pionsNoirs,damesBlanches,damesNoires) >>(noeud+d1+d2))%2== 0):
                        tab+=" "
                        tmp ^= 2**(noeud+d1+d2)
                        if ((pionsBlancs|pionsNoirs)>>(noeud+d2))%2==1:
                            ennPion=True
                            pionsPris.append(noeud+d2)
                        elif ((damesBlanches|damesNoires)>>(noeud+d2))%2==1:
                            ennDame=True
                            damesPrises.append(noeud+d2)
                        chemins.append([len(pionsPris)+len(damesPrises),noeud+d1+d2,pionsPris.copy(),damesPrises.copy()]) #a remplacer le [] par damesPrises
                        DFSrec(noeud+d1+d2, piecesAdv,pionsBlancs, pionsNoirs, damesBlanches,damesNoires)
                        tmp^= 2**(noeud+d1+d2)
                        if ennPion:
                            pionsPris.pop()
                        elif ennDame:
                            damesPrises.pop()
            tab = tab[0:len(tab)-2]
        #print(pionsPris)

        return chemins
def DFS(noeud,piecesAdv,pionsBlancs, pionsNoirs, damesBlanches,damesNoires, dam=False):
    global chemins
    global vus   
    global pionsPris
    global damesPrises
    global tab  
    global chemins
    global tmp
    global prev
    global targets
    tmp=0
    tab = ""
    prev=-1
    chemins = []
    pionsPris = []
    damesPrises = []
    targets = []
    vus = [False for i in range(0,51)]
    return DFSrec(noeud,piecesAdv,pionsBlancs, pionsNoirs, damesBlanches,damesNoires, dam)
