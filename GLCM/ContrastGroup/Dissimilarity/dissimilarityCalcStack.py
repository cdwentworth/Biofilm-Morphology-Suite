# -*- coding: utf-8 -*-
"""
Title: Dissimilarity Calculation for Stack
Author: A. Ewen
Version: 7.2.2020.1
Usage: python dissimilarityCalcStack.py
Summary:
History:
    7.2.2020.1: base
    
"""

import matplotlib.pylab as plt
import skimage.io as skio
import skimage.feature as skf
import sys
import numpy as np

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

# Main Program
   
# establish input data and output files
tiffStack = skio.imread(r'..\07-19-2019__w1FITC_1.5D_s1.tif')
tiffStackFilePieces = tiffStackFile.split('.')
outFileName = tiffStackFilePieces[0] + '.txt'
outFile = open(outFileName,'w')

numImages = tiffStack.shape[0]

# get first image
zeroImage = tiffStack[0,:,:]

timeMinutes = 0
d = np.linspace(1,500,100)

for i in range(5,50,5):
    iImage = tiffStack[i,:,:]
    adjImage = adjust(iImage,zeroImage)
    gx = skf.greycomatrix(adjImage, d, [0], 712, 
                        symmetric=True, normed=True)
    cx = skf.greycoprops(gx, 'dissimilarity')
    cx = np.ndarray.flatten(cx)
    cx = np.ndarray.tolist(cx)
    timeMinutes = timeMinutes + 30
    outFile.write('%8.2f\t' % timeMinutes)
    for n in cx:
        outFile.write('%8.3e\t' % n)
    outFile.write('\n')

outFile.close()
