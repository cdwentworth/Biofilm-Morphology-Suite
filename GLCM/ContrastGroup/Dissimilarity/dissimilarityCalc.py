"""

Title: Dissimilarity Calculation
Author: A. Ewen
Version: 6-18-2020.1
Usage: python dissimilarityCalc.py
Summary:
History:
    6-22-2020.1: base
    
"""
import numpy as np
import matplotlib.pylab as plt
import skimage.io as skio
from skimage.feature import greycomatrix, greycoprops
from skimage import color

#Read in stack and middle image
im = skio.imread(r'../07-19-2019__w1FITC_1.5D_s1.tif')
midImage = im[144,:,:]

iGray = color.rgb2gray(midImage)
dList = []
for i in range(1,513):
    dList.append(i)
d = np.array(dList)

#Create GLCM and calculate feature
gx = greycomatrix(iGray, dList, [0], levels=256, symmetric=True, normed=True)
gy = greycomatrix(iGray, dList, [np.pi/2], levels=256, symmetric=True, normed=True)
cx = greycoprops(gx, 'dissimilarity')
cy = greycoprops(gy, 'dissimilarity')

fig = plt.figure()
plt.plot(d,cx, linestyle='',marker='o',label='0')
plt.plot(d,cy, linestyle='',marker='o', color='red',label='pi/2')
plt.xlabel('n size')
plt.ylabel('Dissimiarity')
plt.title('Dissimilarity for x and y directions')
plt.legend()
plt.savefig('dissimilarity_xy.png')
plt.show()