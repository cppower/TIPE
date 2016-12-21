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
    X=np.zeros((len(lines),52))
    Y =np.zeros(len(lines))
    print(len(lines))
    i=0
    for l in lines:
        pB, pN, dB,dN, couleur,val = transform(l)
        for i in range(1,51):
            if (pB>>i)%2==1:
                X[count,i-1]=1
            elif (pN>>i)%2==1:
                X[count,i-1]=-1
            elif (dB>>i)%2==1:
                X[count,i-1]=2
            elif (dN>>i)%2==1:
                X[count,i-1]=-2
            else:
                X[count,i-1]=0
        X[count, 51]=couleur
        Y[count]=(val+1)/2
        count+=1
        i+=1
    return X,Y
def evalue(nn,pB,pN, dB,dN, col):
    x = np.zeros(52)
    if col==False:
        couleur=-1
    else:
        couleur=1
    NN = Neural_Network()
    for i in range(1,51):
        if (pB>>i)%2==1:
            x[i-1]=1
        elif (pN>>i)%2==1:
            x[i-1]=-1
        elif (dB>>i)%2==1:
            x[i-1]=2
        elif (dN>>i)%2==1:
            x[i-1]=-2
        else:
            x[i-1]=0
    x[ 51]=couleur
    return nn.forward(x).squeeze()

#Exemples
X,Y = convertToArray()

'''
x= np.array(([[  0.,   0,   0.,  0.,   0.,   -1.,   0.,   -1.,   0.,   -1.,   -1.,
          0.,   0.,   0.,   0.,   0.,   0.,   0.,   -1.,   0.,   0.,  0.,
          0.,  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,  0.,
          0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
          0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
          0.,   0.,   0.,   0.,   0.,   0.,  1.,   0.,  -1.,   0.,  -1.,
          0.,  -1.,   0.,  -1.,  -1.,   0.,  1.,   0.,  -1.,   0.,  -1.,
          0.,  -1.,   0.,   0.,  1.,   0.,  1.,   0.,  -1.,   0.,  -1.,
          0.,  -1.,  -1.,   0.,  1.,   0.,  1.,   0.,  -1.,   0.,  -1.,
          0.,  1.]]))
#y = np.array(([0.5]), dtype=float)

#Normalisation
#X = X/np.amax(X, axis=0)
'''
#y = (Y+abs(np.amin(Y,axis=0)))/(np.amax(Y, axis=0)+abs(np.amin(Y,axis=0)))

class Neural_Network(object):
    def __init__(self):        
        self.inputLayerSize = 52
        self.outputLayerSize = 1
        self.hiddenLayers = [2,2,2]
        #Poids Input->L1->L2->Output
        self.W1 = np.random.randn(self.inputLayerSize,self.hiddenLayers[0])
        self.W2 = np.random.randn(self.hiddenLayers[0],self.hiddenLayers[1])
        self.W3 = np.random.randn(self.hiddenLayers[1],self.hiddenLayers[2])
        self.W4 = np.random.randn(self.hiddenLayers[2], self.outputLayerSize)
    def sigmoid(self, z):
        return 1/(1+np.exp(-z))
    
    def sigmoidDerivative(self,z):
        return np.exp(-z)/((1+np.exp(-z))**2)
        
    def forward(self, X):
        self.z2 = np.dot(X, self.W1)
        self.activation2 = self.sigmoid(self.z2) [np.newaxis]
        self.z3 = np.dot(self.activation2, self.W2)
        self.activation3 = self.sigmoid(self.z3)[np.newaxis]
        self.z4 = np.dot(self.activation3, self.W3)
        self.activation4 = self.sigmoid(self.z4)[np.newaxis]
        self.z5 = np.dot(self.activation4, self.W4)
        yHat = self.sigmoid(self.z5)
        return yHat
    
    def costFunction(self, X, y):
        self.yHat = self.forward(X)
        #Fonction de cout quadratique
        J = 0.5*((y-self.yHat)**2)
        return J
        
    def costFunctionPrime(self, X, y):
        self.yHat = self.forward(X)
        delta5 = (-(y-self.yHat)*self.sigmoidDerivative(self.z5))
        dJdW4 = np.dot(self.activation4.transpose(),delta5)
        
        delta4 = np.dot(delta5,self.W4.T)*self.sigmoidDerivative(self.z4)
        dJdW3 = np.dot(self.activation3.T, delta4)
        
        delta3 = np.dot(delta4,self.W3.T)*self.sigmoidDerivative(self.z3)
        dJdW2 = np.dot(self.activation2.T, delta3)
        
        delta2 = np.dot(delta3, self.W2.T)*self.sigmoidDerivative(self.z2)
        dJdW1 = np.dot(X.T, delta2)  
        
        return dJdW1, dJdW2, dJdW3,dJdW4
    
    def getParams(self):
        params = np.concatenate((self.W1.ravel(), self.W2.ravel(), self.W3.ravel(),self.W4.ravel()))
        return params
    
    def setParams(self, params):
        W1_start = 0
        W1_end = self.hiddenLayers[0] * self.inputLayerSize
        self.W1 = np.reshape(params[W1_start:W1_end], (self.inputLayerSize , self.hiddenLayers[0]))
        
        W2_end = W1_end + self.hiddenLayers[0]*self.hiddenLayers[1]
        self.W2 = np.reshape(params[W1_end:W2_end], (self.hiddenLayers[0], self.hiddenLayers[1]))
        
        W3_end = W2_end+self.hiddenLayers[1]*self.outputLayerSize
        self.W3 = np.reshape(params[W2_end:W3_end], (self.hiddenLayers[1], self.outputLayerSize))
        
    def computeGradients(self, X, y):
        dJdW1, dJdW2,dJdW3,dJdW4 = self.costFunctionPrime(X, y)
        return np.concatenate((dJdW1.ravel(), dJdW2.ravel(), dJdW3.ravel(),dJdW4.ravel()))


class trainer(object):
    def __init__(self, N):
        self.N = N
        
    def callbackF(self, params):
        self.N.setParams(params)
        self.J.append(self.N.costFunction(self.X, self.y))   
        
    def costFunctionWrapper(self, params, X, y):
        self.N.setParams(params)
        cost = self.N.costFunction(X, y)
        grad = self.N.computeGradients(X,y)
        return cost, grad
        
    def train(self, X, y):
        self.X = X
        self.y = y
        self.J = []
        
        params0 = self.N.getParams()
        print(params0)
        options = {'maxiter': 200, 'disp' : True}
        _res = optimize.minimize(self.costFunctionWrapper, params0, jac=True, method='BFGS', \
                                 args=(X, y), options=options, callback=self.callbackF)
        self.N.setParams(_res.x)
        self.optimizationResults = _res
    def train2(self, X,y):
        a = [i for i in range(0,100)]
        ord1 = []
        ord2 = []
        ord3 = []
        for L in range(0,100):
            tmpW1 =np.zeros((len(self.N.W1),len(self.N.W1[0])))
            tmpW2 = np.zeros((len(self.N.W2),len(self.N.W2[0])))
            tmpW3 = np.zeros((len(self.N.W3),len(self.N.W3[0])))
            tmpW4 = np.zeros((len(self.N.W4),len(self.N.W4[0])))
            moyenne=0
            for exemple in range(0,len(X)):
                self.X=X[exemple][np.newaxis]
                self.y=y[exemple]
                (dJdW1, dJdW2, dJdW3,dJdW4)=self.N.costFunctionPrime(self.X,np.array(self.y))
                dJdW1 = dJdW1.squeeze()
                dJdW2 = dJdW2.squeeze()
                dJdW3 = dJdW3.squeeze()
                dJdW4 = dJdW4.squeeze()
                for i in range(0,len(self.N.W1)):
                    tmpW1[i]+=dJdW1[i]*eta
                for i in range(0,len(self.N.W2)):
                    tmpW2[i]+=dJdW2[i]*eta
                for i in range(0,len(self.N.W3)):
                    tmpW3[i]+=dJdW3[i]*eta
                for i in range(0,len(self.N.W4)):
                    tmpW4[i]+=dJdW4[i]*eta
                moyenne += self.N.costFunction(X[exemple],y[exemple])
            moyenne/=len(X)
            moyenne =moyenne.squeeze()
            ord1.append(moyenne)
            tmpW1.squeeze()
            #ord2.append(self.N.costFunction(X[1],y[1]))
            #ord3.append(self.N.costFunction(X[1],y[1]))
            for i in range(0,len(self.N.W1)):
                self.N.W1[i]-=tmpW1[i]/len(X)
            for i in range(0,len(self.N.W2)):
                self.N.W2[i]-=tmpW2[i]/len(X)
            for i in range(0,len(self.N.W3)):
                self.N.W3[i]-=tmpW3[i]/len(X)  
            for i in range(0,len(self.N.W4)):
                self.N.W4[i]-=tmpW3[i]/len(X)
        plot(a, ord1)
    def trainMiniBatch(self,X,y,iter):
        a = [i for i in range(0,iter)]
        ord1 = []
        ord2 = []
        ord3 = []
        per=0
        debut = time()
        for L in range(0,iter):
            if L==int(iter/100*2):
                fin = time()
                diff=round((fin-debut)/2*100,1)
                print("Temps estimé à l'apprentissage : "+str(diff)+" s")
            if L>=iter/100*(per+10):
                per+=10
                print(str(per)+"%")
            lBatch = int(len(X)/10)
            moyenne=0
            for iBatch in range(0,  10):
                tmpW1 =np.zeros((len(self.N.W1),len(self.N.W1[0])))
                tmpW2 = np.zeros((len(self.N.W2),len(self.N.W2[0])))
                tmpW3 = np.zeros((len(self.N.W3),len(self.N.W3[0])))
                tmpW4 = np.zeros((len(self.N.W4),len(self.N.W4[0])))
                for j in range(lBatch*iBatch, lBatch*(iBatch+1)):
                    self.X=X[j][np.newaxis]
                    self.y=y[j]
                    (dJdW1, dJdW2, dJdW3,dJdW4)=self.N.costFunctionPrime(self.X,np.array(self.y))
                    dJdW1 = dJdW1.squeeze()
                    dJdW2 = dJdW2.squeeze()
                    dJdW3 = dJdW3.squeeze()
                    dJdW4 = dJdW4.squeeze()
                    for i in range(0,len(self.N.W1)):
                        tmpW1[i]+=dJdW1[i]*eta
                    for i in range(0,len(self.N.W2)):
                        tmpW2[i]+=dJdW2[i]*eta
                    for i in range(0,len(self.N.W3)):
                        tmpW3[i]+=dJdW3[i]*eta
                    for i in range(0,len(self.N.W4)):
                        tmpW4[i]+=dJdW4[i]*eta
                    moyenne += self.N.costFunction(X[j],y[j])
                for i in range(0,len(self.N.W1)):
                    self.N.W1[i]-=tmpW1[i]/lBatch
                for i in range(0,len(self.N.W2)):
                    self.N.W2[i]-=tmpW2[i]/lBatch
                for i in range(0,len(self.N.W3)):
                    self.N.W3[i]-=tmpW3[i]/lBatch  
                for i in range(0,len(self.N.W4)):
                    self.N.W4[i]-=tmpW4[i]/lBatch   
            moyenne/=len(X)
            moyenne =moyenne.squeeze()
            ord1.append(moyenne)
        plot(a, ord1)        

if __name__=='__main__':
    #Affichage des résultats
    NN = Neural_Network()
    T = trainer(NN)
    #T.train(X[0],Y[0])
    T.trainMiniBatch(X,Y,100)
    NN = Neural_Network()
    #T = trainer(NN)
    #T.train2(X,Y)

'''
result =[]
xa = [randint(-1,1) for i in range (0,100)]
ya = [sum(xa)]
for i in range (0,150
0):
        result.append(NN.forward(np.array([xa[i],ya[i]]))[0])
xi, yi = np.linspace(0,10**10, 150), np.linspace(0,10**10, 150)
xi, yi = np.meshgrid(xi, yi)
rbf = Rbf(xa, ya, result, function='linear')
zi = rbf(xi, yi)

imshow(zi, vmin=np.array(result).min(), vmax=np.array(result).max(), origin='lower',
           extent=[np.array(xa).min(), np.array(xa).max(), np.array(ya).min(), np.array(ya).max()])
colorbar()
show()'''

