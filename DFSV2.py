pairs = [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45]
dirP= [-5,-4,5,6]
dirI = [-6,-5,4,5]
chemins = []
cheminTMP = []
def occupee(pB,pN,dB,dN, cas):
	return ((pB|dB|pN|dN)>>cas)%2==1

def deplacementValide(pB,pN,dB,dN, curPos, dir1,dir2,i,col):
	borders=  [1,2,3,4,5,15,25,35,45,50,49,48,47,46,36,26,16,6]
	autorisesPions = 	 [[5,6],[5,6],[5,6],[5,6],[5],[-5,5],[-5,5],[-5,5],[-5,5],[-6,-5],[-6,-5],[-6,-5],[-6,-5],[-5],[-5,5],[-5,5],[-5,5],[-5,5]]
	if (curPos not in borders) or (curPos in borders and dir1[i] in autorisesPions[borders.index(curPos)]):
		if (curPos+dir1[i] not in borders ) or (curPos+dir1[i] in borders and dir2[i] in autorisesPions[borders.index(curPos+dir1[i])]):
			#print("Vérification du déplacement : "+str(curPos+dir1[i])+"/"+str(curPos+dir1[i]+dir2[i]))
			if not occupee(pB,pN,dB,dN,curPos+dir1[i]+dir2[i]):
				if (col=="N" and ((pB|dB)>>(curPos+dir1[i]))%2==1) or ((col=="B") and ((pN|dN)>>(curPos+dir1[i]))%2==1):
					return True
	return False

def modifieDamier(pB, pN, dB,dN, curPos, dir1,dir2,i,col):
	if col=="N":
		if (pB>>curPos+dir1[i])%2==0:
			dB^=2**(curPos+dir1[i])
		else:
			pB^=2**(curPos+dir1[i])
		pN^=2**(curPos+dir1[i]+dir2[i])
	else:
		if (pN>>curPos+dir1[i])%2==0:
			dN^= 2**(curPos+dir1[i])
		else:
			pN^=2**(curPos+dir1[i]+dir2[i])
		pB^= 2**(curPos+dir1[i]+dir2[i])
	return (pB, pN, dB, dN)

def DFS (curPos, pB, pN, dB, dN, coul):
	global chemins
	global cheminTMP
	if curPos in pairs:
		direction1 = dirP
		direction2=  dirI
	else:
		direction1 = dirI 
		direction2 = dirP

	for i in range(0,len(direction1)) :
		if deplacementValide(pB,pN, dB, dN, curPos, direction1,direction2,i,coul):
			cheminTMP.append((curPos+direction1[i],curPos+direction1[i]+direction2[i]))
			(pB, pN, dB, dN) = modifieDamier(pB,pN, dB, dN,curPos,direction1, direction2,i,coul)
			DFS(curPos+direction1[i]+direction2[i], pB, pN, dB, dN,coul)
	if cheminTMP != []:
		chemins.append(cheminTMP.copy())
		del cheminTMP[-1]
	return chemins