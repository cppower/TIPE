#Fonctions principales de es
import copy

def dansDamier(x,y):
    if x>=0 and y>=0 and x<10 and y<10:
        return True
    return False

def DFS_pion(x,y,noir,damier): #Retourne un tableau de l'ensemble des chemins possibles pour un pion effectuant une prise
    dejaVu = [[False for i in range(0,10)] for j in range(0,10)]
    pile = [[x,y]]
    dejaVu[x][y]=True
    
    deltaX = [-1,1,1,-1]
    deltaY= [-1,1,-1,1]
    chemins = []
    curChemin = []
    feuille=False
    while len(pile)!=0:
        x = pile[-1][0]
        y = pile[-1][1]
        if feuille:
            while len(curChemin)>0 and curChemin[-1]!=[x,y]:
                curChemin.pop()
        curChemin.append([x,y])
        #print(str(x)+" "+str(y))
        pile.pop()
        feuille=True
        for j in range(0,4):
            if dansDamier(x+2*deltaX[j], y+2*deltaY[j]):
                if ((noir and damier[x+deltaX[j]][y+deltaY[j]]<0) or (not noir and damier[x+deltaX[j]][y+deltaY[j]]>0)) and not (dejaVu[x+2*deltaX[j]][y+2*deltaY[j]]) and damier[x+2*deltaX[j]][y+2*deltaY[j]]==0:
                    pile.append([x+2*deltaX[j], y+2*deltaY[j]])
                    dejaVu[x+2*deltaX[j]][y+2*deltaY[j]]=True
                    feuille=False
        if (feuille):
            chemins.append(curChemin.copy())
    return chemins

def dameDFS(damier, casesNoires,a,b,a_tab,b_tab,noir,notation=True):
    dejaVu = [[False for i in range(0,10)] for j in range(0,10)]
    if notation:
        depart = [casesNoires[a][0],casesNoires[a][1]]
        arrivee = [casesNoires[b][0],casesNoires[b][1]]
    else:
        depart=a_tab
        arrivee=b_tab
    pile = [[depart[0],depart[1],0,0,0,0]]
    dejaVu[depart[0]][depart[1]]=True
    deltaX = [-1,1,1,-1]
    deltaY= [-1,1,-1,1]
    chemins = [[[]]]
    curChemin = []
    feuille=False
    tmpDamier = copy.deepcopy(damier)
    debut = True
    while len(pile)!=0:
        x = pile[-1][0]
        y = pile[-1][1]
        prev_x=pile[-1][2]
        prev_y=pile[-1][3]
        pion_x=pile[-1][4]
        pion_y=pile[-1][5]
        #print("alive"+str(prev_x)+" "+str(prev_y))
        if not debut:
            tmpDamier[x][y]=tmpDamier[pile[-1][2]][pile[-1][3]]
            tmpDamier[prev_x][prev_y]=0
            tmpDamier[pion_x][pion_y]=0
        debut = False
    
        if feuille:
            while len(curChemin)>0:
                tmpDamier[curChemin[-1][0]][curChemin[-1][1]]=0
                curChemin.pop()
        curChemin.append([x,y])
        pile.pop()
        feuille=True
        for j in range(0,4):
            pieceAdverse = 0
            change = False
            for l in range(1,10):
                if dansDamier(x+l*deltaX[j], y+l*deltaY[j]):
                    if ((noir and tmpDamier[x+l*deltaX[j]][y+l*deltaY[j]]>0) or (not noir and tmpDamier[x+l*deltaX[j]][y+l*deltaY[j]]<0)):
                        break #S'assure qu'il n'y a pas de piece de la meme équipe sur la trajectoire de la rafle
                    if ((noir and tmpDamier[x+l*deltaX[j]][y+l*deltaY[j]]<0) or (not noir and tmpDamier[x+l*deltaX[j]][y+l*deltaY[j]]>0)):
                        pieceAdverse+=1
                        change = True #S'assure qu'il y a une unique piece adverse sur la trajectoire
                        (x_prise, y_prise)=(x+l*deltaX[j], y+l*deltaY[j])
                    if  not (dejaVu[x+l*deltaX[j]][y+l*deltaY[j]]) and tmpDamier[x+l*deltaX[j]][y+l*deltaY[j]]==0 and pieceAdverse==1 and not change:
                        pile.append([x+l*deltaX[j], y+l*deltaY[j],x,y,x_prise,y_prise])
                        dejaVu[x+l*deltaX[j]][y+l*deltaY[j]]=True
                        feuille=False
                    change = False
                else:
                    break
        #tmp[prev_x][prev_x]=tmp[x][sy]
        #tmp[pion_x][pion_y]=(1 and not noir) or (0 and noir)
        if (feuille):
            chemins.append(curChemin.copy())
    #print(chemins)
    return chemins
def plusLongCheminDames(damier,casesNoires,a,b,a_tab,b_tab,noir, notation=True):
    cheminsPossibles = [[]]
    chemins = dameDFS(damier, casesNoires,a,b,a_tab,b_tab,noir,notation)
    if notation:
        depart = [casesNoires[a][0],casesNoires[a][1]]
        arrivee = [casesNoires[b][0],casesNoires[b][1]]
    else:
        depart=a_tab
        arrivee=b_tab
    for i in range(0,len(chemins)):
        if  (chemins[i][-1]==[arrivee[0],arrivee[1]]):
            cheminsPossibles.append(chemins[i].copy())
    cheminRetenu = max(cheminsPossibles)
    return cheminRetenu