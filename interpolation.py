from matplotlib.pyplot import *
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

N = 51
x = np.linspace(-1,1,N)
y = np.linspace(-1,1,N)
X,Y = np.meshgrid(x,y)
Z=grad



#fig = figure()
#ax = axes(projection='3d')
#ax.plot_wireframe(X, Y, Z)
graphe = contourf(X,Y,Z,300,cmap=cm.spectral)
#plot(graphe)
#pcolor(X,Y,Z,cmap=cm.nipy_spectral_r)
title("Fonction dans le plan (W1,W2)")
colorbar()
