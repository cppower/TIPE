#Réseau de neurones Input-> L1 -> L2 -> Output
#Algdorithme d'optimisation : BGFS


from matplotlib.pyplot import *
import numpy as np
from scipy import optimize
from scipy.interpolate import Rbf
from random import *
import os

from time import time
os.chdir("/Users/Victor/Dames")
eta=0.5
alpha=0
def transform(l):
    tmp = l
    pB,pN,dB, reste = tmp.split(":")
    dN, couleur, val, num = reste.split(";")
    return int(pB), int(pN), int(dB), int(dN), int(couleur),float(val)
def convertToArray():
    global X
    global Y
    count=0
    file = open('bdd.txt','r')
    lines = file.readlines()
    X=np.zeros((len(lines),2))
    Y =np.zeros(len(lines))
    print(len(lines))
    j=0
    for l in np.random.permutation(lines):
        pB, pN, dB,dN, couleur,val = transform(l)
        totalB=0
        totalN=0
        totalB2 = 0
        totalN2=0
                        
        for i in range(0, 51):
            if (pB>>i)%2==1:
                totalB+=1
            elif (pN>>i)%2==1:
                totalN+=1
            elif (dB>>i)%2==1:
                totalB2+=1
            elif (dN>>i)%2==1:
                totalN2+=1
        if couleur==1:
            X[j,0]=totalN-totalB
            X[j,1]=totalN2-totalB2
        else:
            X[j,0]=totalB-totalN
            X[j,1]=totalB2-totalN2
        '''
        for i in range(0,10): #lignes
            m=0
            for k in range(0,5):
                if couleur==1 and ( (pN>>(5*i+k))%2==1 or (dN>>(5*i+k))%2==1):
                    m+=1
                if  couleur==-1 and ((pB>>(5*(9-i)+k))  or (dB>>(5*(9-i)+k))%2==1):
                    m+=1
            if couleur==1:
                X[j,i]=m/(totalB+totalB2)
            else:
                X[j,i]=m/(totalN+totalN2)
        #print(couleur)
       # print(X[j])'''
        Y[count]=val
        count+=1
        j+=1
    return X,Y
def evalue(nn,pB,pN, dB,dN, col):
    x = np.zeros(2)
    if col==False:
        couleur=-1
    else:
        couleur=1
        
    NN = Neural_Network()
    totalB=0
    totalN=0
    totalB2 = 0
    totalN2=0
    for i in range(0, 51):
        if (pB>>i)%2==1:
            totalB+=1
        elif (pN>>i)%2==1:
            totalN+=1
        elif (dB>>i)%2==1:
            totalB2+=1
        elif (dN>>i)%2==1:
            totalN2+=1
    if  col:
        x[0]=totalN-totalB
        x[1]=totalN2-totalB2
    else:
        x[0]=totalB-totalN
        x[1]=totalB2-totalN2
    return nn.forward(x).squeeze()

#Exemples
X,Y = convertToArray()


class Neural_Network(object):
    def __init__(self):        
        self.inputLayerSize = 2
        self.outputLayerSize = 1
        #Poids Input->Output
        self.W1 = np.random.randn(self.inputLayerSize,self.outputLayerSize)

    def sigmoid(self, z):
        return z
    
    def sigmoidDerivative(self,z):
        return 1
        
    def forward(self, X):
        self.z2 = np.dot(X, self.W1)
        yHat = self.sigmoid(self.z2)
        return yHat
    
    def costFunction(self, X, y):
        self.yHat = self.forward(X)
        #Fonction de cout quadratique
        J = 0.5*((y-self.yHat)**2)
        return J
        
    def costFunctionPrime(self, X, y):
        self.yHat = self.forward(X)
        delta = (-(y-self.yHat)*self.sigmoidDerivative(self.z2))
        dJdW1 = np.dot(X.T,delta)  
        return dJdW1

class trainer(object):
    def __init__(self, N):
        self.N = N

    def train2(self, X,y):
        a = [i for i in range(0,100)]
        ord1 = []
        for L in range(0,100):
            tmpW1 =np.zeros((len(self.N.W1),len(self.N.W1[0])))
            moyenne=0
            for exemple in range(0,len(X)):
                self.X=X[exemple][np.newaxis]
                self.y=y[exemple]
                dJdW1=self.N.costFunctionPrime(self.X,np.array(self.y))
                dJdW1 = dJdW1.squeeze()
                for i in range(0,len(self.N.W1)):
                    tmpW1[i]+=dJdW1[i]*eta
                moyenne += self.N.costFunction(X[exemple],y[exemple])
            moyenne/=len(X)
            moyenne =moyenne.squeeze()
            ord1.append(moyenne)
            tmpW1.squeeze()
            for i in range(0,len(self.N.W1)):
                self.N.W1[i]-=tmpW1[i]/len(X)

        plot(a, ord1)
    def donneGradient(self,X,y):
            tmpW1 =np.zeros((len(self.N.W1),len(self.N.W1[0])))
            for exemple in range(0,len(X)):
                self.X=X[exemple][np.newaxis]
                self.y=y[exemple]
                dJdW1=self.N.costFunctionPrime(self.X,np.array(self.y))
                dJdW1 = dJdW1.squeeze()
                for i in range(0,len(self.N.W1)):
                    tmpW1[i]+=dJdW1[i]*eta
            return (math.sqrt((tmpW1[0]/len(X))**2+(tmpW1[1]/len(X))**2))
    def trainMiniBatch(self,X,y,iter):
        a = [i for i in range(0,iter)]
        ord1 = []
        ord2 = []
        per=0
        debut = time()
        archivesX=[]
        archivesY = []
        for L in range(0,iter):
            X = np.random.permutation(X)
            if L==int(iter/100*2):
                fin = time()
                diff=round((fin-debut)/2*100,1)
                print("Temps estimé à l'apprentissage : "+str(diff)+" s")
            if L>=iter/100*(per+10):
                per+=10
                print(str(per)+"%")
            lBatch = int(len(X)/20)
            moyenne=0
            prev=[0 for i in range(0,len(self.N.W1))]
            for iBatch in range(0,20):
                tmpW1 =np.zeros((len(self.N.W1),len(self.N.W1[0])))
                for j in range(lBatch*iBatch, lBatch*(iBatch+1)):
                    self.X=X[j][np.newaxis]
                    self.y=y[j]
                    dJdW1=self.N.costFunctionPrime(self.X,np.array(self.y))
                    dJdW1 = dJdW1.squeeze()
                    for i in range(0,len(self.N.W1)):
                        tmpW1[i]+=dJdW1[i]*eta
                    moyenne += self.N.costFunction(X[j],y[j])
                for i in range(0,len(self.N.W1)):
                    self.N.W1[i]-=tmpW1[i]/lBatch+prev[i]*alpha
                    prev[i]=tmpW1[i]/lBatch
                archivesX.append(self.N.W1[0][0])
                archivesY.append(self.N.W1[1][0])
            moyenne=self.N.W1[1]/self.N.W1[0]
            moyenne =moyenne.squeeze()
            ord1.append(moyenne)
        
        #plot(a,ord1)  
        plot(archivesX,archivesY)


grad = np.zeros((100,100))
for i in range(0,100):
    print(i)
    for j in range(0,100):            
            NN=Neural_Network(i/400*2-0.25,j/400*2-0.25)
            T = trainer(NN)
            grad[i,j]=T.donneGradient(X,Y)
            #print(grad[i,j])

'''
if __name__=='__main__':
    #Affichage des résultats

    NN = Neural_Network()
    T = trainer(NN)
    #T.train(X,Y)
    T.trainMiniBatch(X,Y,500)
    print(NN.W1)
    #T = trainer(NN)
    #T.train2(X,Y)
'''