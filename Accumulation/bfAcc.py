#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Biofilm Accumulation
File: bfAcc.py
Version: 6-26-2018.1
Author: C. Wentworth
Revisions:
    6-3-2018.1
    6-26-2018.1: added thresholding 

"""

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio
import skimage.filters as skf

def adjust(inputImage,imageZero):
#    import numpy as np
    h,w = np.shape(inputImage)
    adjustedImage = np.zeros((h,w),dtype=np.uint16)
    for i in range(0,h):
        for j in range(0,w):
            iI=inputImage[i,j]
            iZ=imageZero[i,j]
            if (iI>iZ):
                a = iI - iZ
            else:
                a = 0
            adjustedImage[i,j] = a
    return adjustedImage

# open output file
outFile = open('bfa_1.0Dy.txt','w')

tiffStack = skio.imread('041118_W1FITC 100- CAM_S24_1D_T.tif')
numImages = tiffStack.shape[0]

# get first image
zeroImage = tiffStack[0,:,:]

# calculate threshold value
adjImage = adjust(tiffStack[23,:,:],zeroImage)
thresh = skf.threshold_triangle(adjImage)

intensityArray = []
timeArray = []
timeMinutes = 0

for i in range(5,numImages,6):
    iImage = tiffStack[i,:,:]
    adjImage = adjust(iImage,zeroImage)
    binaryImage = adjImage > thresh
    intensityTotal = np.sum(adjImage[binaryImage])

    intensityArray.append(intensityTotal)
    timeArray.append(timeMinutes)
    timeMinutes = timeMinutes + 30
    outFile.write('%8.2f\t%8.4e\n' % (timeMinutes, intensityTotal))
    
outFile.close()
plt.plot(timeArray,intensityArray,linestyle='',marker='o')
plt.xlabel('t [min]')
plt.ylabel('N [rel]')
plt.savefig('033018_W1FITC 100- CAM_S4_bfa_1.0D_T.png')
plt.show()
