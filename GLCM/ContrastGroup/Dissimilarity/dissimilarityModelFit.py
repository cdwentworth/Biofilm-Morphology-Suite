"""

Title: Dissimilarity Model Fit
Author: A. Ewen and C.D. Wentworth
Version: 6.30.2020.1
Usage: python dissimilarityModelFit.py
Summary:
History:
    6.22.2020.1: base
    6.30.2020.1: adjusted the range of distances used
    
"""
import numpy as np
import matplotlib.pylab as plt
import skimage.io as skio
from skimage.feature import greycomatrix, greycoprops
from skimage import color
import scipy.optimize as so

def DM(n,a,b):
    dataline = (a*n)/(b+n)
    return dataline

#Read in stack and middle image
im = skio.imread(r'../07-19-2019__w1FITC_1.5D_s1.tif')
midImage = im[144,:,:]

iGray = color.rgb2gray(midImage)
dList = []
for i in range(1,512,5):
    dList.append(i)
d = np.array(dList)

#Create GLCM and calculate feature
gx = greycomatrix(iGray, dList, [0], levels=256, symmetric=True, normed=True)
gy = greycomatrix(iGray, dList, [np.pi/2], levels=256, symmetric=True, normed=True)
cx = greycoprops(gx, 'dissimilarity')
cy = greycoprops(gy, 'dissimilarity')
cx = np.ndarray.flatten(cx)
cy = np.ndarray.flatten(cy)

# Fit the dissimilarity data to the model
# Model Parameter guess
a = 1.01
b = 0.2
p = a,b,
popt,pcov = so.curve_fit(DM,dList,cx,p)
ax,bx = popt
popt,pcov = so.curve_fit(DM,dList,cy,p)
ay,by = popt

da = np.linspace(2,400,100)
cxModel = DM(da,ax,bx)
cyModel = DM(da,ay,by)

fig = plt.figure()
# Plot data
plt.plot(d,cx, linestyle='',marker='o', color='blue',label='0')
plt.plot(d,cy, linestyle='',marker='o', color='red',label='pi/2')

# Plot model
plt.plot(da,cxModel, linestyle='-',color='blue')
plt.plot(da,cyModel, linestyle='-',color='red')
plt.xlabel('n size')
plt.ylabel('Dissimiarity')
plt.title('Dissimilarity for x and y directions')
plt.legend()
plt.savefig('dissimilarity_xy.png')
plt.show()