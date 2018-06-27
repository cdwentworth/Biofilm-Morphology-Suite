#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Roughness Coefficient
File: roughnessCoef.py
Version: 4-14-2018.1
Author: C. Wentworth

This script creates a plot of the biofilm roughness coefficient as a funciton of time  
measured from a stack of microscope images using the FITC fluorescence channel.  
It assumes that the intensity of the GFP fluorescence at a pixel is proportional 
to the thickness of the film at the location. It uses the image intensity at a 
pixel from the first image in the stack for thresholding.  This procedure will give
the roughness associated with the living cells, not the entire biofilm.

"""

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio
import sys

def adjust(inputImage,imageZero):
    import numpy as np
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
AveRCarray = []
timeArray = []
timeMinutes = 0

for i in range(5,numImages,6):
    iImage = tiffStack[i,:,:]
    adjImage = adjust(iImage,zeroImage)
    flatImage = adjImage.flatten()
    thickAvg = float(np.mean(flatImage))
    N = len(flatImage)
    Ra = 0 
    for t in flatImage:
        tf = float(t)
        a = np.abs(tf-thickAvg)/thickAvg
        Ra = Ra + a
    RC = Ra/N
    AveRCarray.append(RC)
    timeArray.append(timeMinutes)
    timeMinutes = timeMinutes + 30
    outFile.write('%8.2f\t%8.4e\n' % (timeMinutes, RC))
    
outFile.close()
plt.plot(timeArray,AveRCarray,linestyle='',marker='o')
plt.savefig(graphFileName,dpi=300)
plt.show()
