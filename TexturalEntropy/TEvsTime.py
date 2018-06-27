#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Textural Entropy
File: TE.py
Date: 4/14/2018 12:46
Author: C. Wentworth
"""

import matplotlib.pylab as plt
import skimage.io as skio
import skimage.feature as skf
from sklearn.metrics.cluster import entropy
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

TEarray = []
timeArray = []
timeMinutes = 0

for i in range(5,numImages,6):
    iImage = tiffStack[i,:,:]
    adjImage = adjust(iImage,zeroImage)
    glcm = skf.greycomatrix(adjImage, [1,2,3,4], [0,1.5708], 712, 
                        symmetric=True, normed=True)
    TE = entropy(glcm)
    TEarray.append(TE)
    timeArray.append(timeMinutes)
    timeMinutes = timeMinutes + 30
    outFile.write('%8.2f\t%8.4e\n' % (timeMinutes, TE))
    
outFile.close()
plt.plot(timeArray,TEarray,linestyle='',marker='o')
plt.savefig(graphFileName,dpi=300)
plt.show()
