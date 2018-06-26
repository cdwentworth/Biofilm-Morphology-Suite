#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Biofilm Coverage
File: bfCoverage.py
Date: 6/1/2018 12:46
Author: C. Wentworth

This script produces a plot of biofilm surface coverage percent as a
function of time using a stack of BioFlux images.

"""

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio
import skimage.filters as skf
from skimage import img_as_uint


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
outFile = open('bfc_1.0Dy.txt','w')

tiffStack = skio.imread('041118_W1FITC 100- CAM_S24_1D_T.tif')
numImages = tiffStack.shape[0]

# get first image
zeroImage = tiffStack[0,:,:]

# calculate threshold value
adjImage = adjust(tiffStack[23,:,:],zeroImage)
thresh = skf.threshold_triangle(adjImage)

# size of image    
h,w = np.shape(zeroImage)
size = h*w
size = float(size)
coverageArray = []
timeArray = []
timeMinutes = 0

for i in range(5,numImages,6):
    iImage = tiffStack[i,:,:]
    adjImage = adjust(iImage,zeroImage)
    binaryImage = adjImage > thresh
    numberOfTrues = np.count_nonzero(binaryImage)
    percentCoverage = numberOfTrues*100/size
    coverageArray.append(percentCoverage)
    timeArray.append(timeMinutes)
    timeMinutes = timeMinutes + 30
    outFile.write('%8.2f\t%8.4e\n' % (timeMinutes, percentCoverage))
    
outFile.close()
plt.plot(timeArray,coverageArray,linestyle='',marker='o')
plt.xlabel('t [min]')
plt.ylabel('c [%]')
plt.savefig('041118_W1FITC 100- CAM_S24_1D_bfc_T.png')
plt.show()
