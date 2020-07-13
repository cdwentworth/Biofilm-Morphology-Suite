#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Biofilm Accumulation
File: bfAcc.py
Version: 6-26-2018.2
Author: C. Wentworth
Revisions:
    6-3-2018.1: base code
    6-26-2018.1: added thresholding 
    6-26-2018.2: added command line argument processing
Summary: This program will read a stack of tif images obtained from 
         the BioFlux microscope station, perform some thresholding,
         and then measure the relative biofilm accumulation as a 
         function of time.
Usage: python bfAcc.py stackFileName.tif  
  
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
plt.savefig(graphFileName,dpi=300)
plt.show()
