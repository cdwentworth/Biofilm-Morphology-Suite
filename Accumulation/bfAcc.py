#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Biofilm Accumulation
File: bfAcc.py
Version: 6-1-2018.1
Author: C. Wentworth

This script creates a plot of the biofilm accumulation as a funciton of time  
measured from a stack of microscope images using the FITC fluorescence channel.  
It assumes that the intensity of the GFP fluorescence at a pixel is proportional 
to the number of living cells at that location. It uses the image intensity at a 
pixel from the first image in the stack for thresholding.
  
"""

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio

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
outFile = open('bfAccData.txt','w')

testStack = skio.imread('testData.tif')
numImages = testStack.shape[0]

# get first image
zeroImage = testStack[0,:,:]

intensityArray = []
timeArray = []
timeMinutes = 0

for i in range(5,numImages,6):
    iImage = testStack[i,:,:]
    adjImage = adjust(iImage,zeroImage)
    flatImage = adjImage.flatten()
    intensityTotal = flatImage.sum()

    intensityArray.append(intensityTotal)
    timeArray.append(timeMinutes)
    timeMinutes = timeMinutes + 30
    outFile.write('%8.2f\t%8.4e\n' % (timeMinutes, intensityTotal))
    
outFile.close()
plt.plot(timeArray,intensityArray,linestyle='',marker='o')
plt.xlabel('t [min]')
plt.ylabel('N [rel]')
plt.savefig('testData.png')
plt.show()
