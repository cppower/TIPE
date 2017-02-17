from matplotlib.pyplot import *
import matplotlib.cm as cm

N = 100
x = np.linspace(-0.25,0.25,N)
y = np.linspace(-0.25,0.25,N)
X,Y = np.meshgrid(x,y)
Z=grad

ti = np.linspace(-0.25,0.25,100)
#z_interp = interpolate.interp2d(X,Y,Z, kind='linear')
XI,YI = np.meshgrid(ti,ti)
interpol = Rbf(X,Y,Z,epsilon=0.1)
ZI= interpol(XI,YI)
zi = z_interp(ti,ti)
pcolor(XI,YI,ZI,cmap=cm.jet)
colorbar()