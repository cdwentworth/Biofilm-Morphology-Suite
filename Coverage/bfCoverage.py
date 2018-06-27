#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Biofilm Coverage
File: bfCoverage.py
Version: 6-26-2018.1
Author: C. Wentworth

This script produces a plot of biofilm surface coverage percent as a
function of time using a stack of BioFlux images.

Revisions:
    6-1-2018.1: initial commit
    6-26-2018.1: added command line argument processing

"""

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio
import skimage.filters as skf
import sys


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

# main

# get command line arguments
tiffStackFile = str(sys.argv[1])
   
# establish input data and output files
tiffStack = skio.imread(tiffStackFile)
tiffStackFilePieces = tiffStackFile.split('.')
outFileName = tiffStackFilePieces[0] + '.txt'
outFile = open(outFileName,'w')
graphFileName = tiffStackFilePieces[0] + '.png'

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
plt.savefig(graphFileName,dpi=300)
plt.show()
