#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Threshold Algorithm Test
File: thresholdTest.py
Version: 11-1-2018.1
Author: C. Wentworth

usage: python thresholdTest stack.tif
Revisions:

    
"""


import numpy as np
import skimage as sk
import skimage.io as skio
import skimage.filters as skf
import sys

def adjust(inputImage,imageZero):
#    import numpy as np
    h,w = np.shape(inputImage)
    adjustedImage = np.zeros((h,w),dtype=np.int)
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
outFileName = tiffStackFilePieces[0] + '_threshold.tif'
#outFile = open(outFileName,'w')

numImages , imageWidth , imageHeight = tiffStack.shape
newTiffStack = np.zeros(tiffStack.shape,dtype='uint16')


# get first image
zeroImage = tiffStack[0,:,:]

# calculate threshold value
adjImage = adjust(tiffStack[23,:,:],zeroImage)
thresh = skf.threshold_triangle(adjImage)

for i in range(0,numImages):
    iImage = tiffStack[i,:,:]
    adjImage = adjust(iImage,zeroImage)
    newTiffStack[i]=adjImage


skio.imsave(outFileName,newTiffStack)    
#outFile.close()

