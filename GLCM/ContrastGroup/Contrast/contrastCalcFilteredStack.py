# -*- coding: utf-8 -*-
"""
Title: Contrast Calculation for Filtered Stack
Author: A. Ewen
Version: 7.13.2020.1
Usage: python contrastCalcFilteredStack.py
Summary:
History:
    7.13.2020.1: base
    
"""

import matplotlib.pylab as plt
import skimage.io as skio
import skimage.feature as skf
import sys
import numpy as np

# Main Program
   
# establish input data and output files
tiffStackFile = 'subStack.tif'
tiffStack = skio.imread(r'..\subStack.tif')
tiffStackFilePieces = tiffStackFile.split('.')
outFileXName = tiffStackFilePieces[0] + 'cx' + '.txt'
outFileYName = tiffStackFilePieces[0] + 'cy' + '.txt'
outFileX = open(outFileXName,'w')
outFileY = open(outFileYName,'w')

# Write header to x data file
xHeader = ['    D%d' % (i+1) for i in range(102)]
xHeader.insert(0,'Time')
xHeader = "\t".join(xHeader) + '\n'
outFileX.write(xHeader)

# Write header to y data file
yHeader = ['    D%d' % (i+1) for i in range(102)]
yHeader.insert(0,'Time')
yHeader = "\t".join(yHeader) + '\n'
outFileY.write(yHeader)

numImages = tiffStack.shape[0]

timeMinutes = 0
d = np.arange(1,100,2)
de= np.arange(101,512,8)
d = np.concatenate((d,de))

for i in range(5,numImages,6):
    iImage = tiffStack[i,:,:]
    gx = skf.greycomatrix(iImage, d, [0], 712, 
                        symmetric=True, normed=True)
    cx = skf.greycoprops(gx, 'contrast')
    cx = np.ndarray.flatten(cx)
    cx = np.ndarray.tolist(cx)
    gy = skf.greycomatrix(iImage, d, [1.5708], 712, 
                        symmetric=True, normed=True)
    cy = skf.greycoprops(gy, 'contrast')
    cy = np.ndarray.flatten(cy)
    cy = np.ndarray.tolist(cy)    
    timeMinutes = timeMinutes + 30
    outFileX.write('%8.2f\t' % timeMinutes)
    for n in cx:
        outFileX.write('%8.3f\t' % n)
    outFileX.write('\n')
    outFileY.write('%8.2f\t' % timeMinutes)
    for n in cy:
        outFileY.write('%8.3f\t' % n)
    outFileY.write('\n')

outFileX.close()
outFileY.close()
