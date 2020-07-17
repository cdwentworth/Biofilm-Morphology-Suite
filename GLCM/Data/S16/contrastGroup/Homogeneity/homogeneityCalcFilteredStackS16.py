"""
Title: Homogeneity Calculation for Filtered Stack
Author: A. Ewen and C.D. Wentworth
Version: 7.14.2020.1
Usage: python contrastCalcFilteredStack.py
Summary: This program reads in a tiff stack of microscope images and then
         calculates the GLCM homogeneity for 100 reference-point 
         distances for both the x and y directions. It is assumed that
         the microscope images have been filtered by subtracting out the
         intensity of the first image. The measurements are written to text 
         files, one for the x measurements and one for the y measurements.
History:
    7.14.2020.1: base
    7.15.2020.1: modified for measurements of S16 stack
    
"""

import matplotlib.pylab as plt
import skimage.io as skio
import skimage.feature as skf
import sys
import numpy as np

# Main Program

# User specified data
tiffStackFile = 'Processed_033018_W1FITC 100- CAM_S16_T_0.5 dyne_cm2.tif'  # This file should be in the same folder as prrogram
numSkippedFrames = 8
   
# establish input data and output files
tiffStack = skio.imread(tiffStackFile)
tiffStackFilePieces = tiffStackFile.split('.')
outFileXName = tiffStackFilePieces[0] + 'cx' + '.txt'
outFileYName = tiffStackFilePieces[0] + 'cy' + '.txt'
outFileX = open(outFileXName,'w')
outFileY = open(outFileYName,'w')

# Write header to x data file
xHeader1 = 'GLCM Homogeneity S16 x\n'
xHeader2 = ['    D%d' % (i+1) for i in range(102)]
xHeader2.insert(0,'Time')
xHeader = xHeader1 + "\t".join(xHeader2) + '\n'
outFileX.write(xHeader)

# Write header to y data file
yHeader1 = 'GLCM Homogeneity S16 y\n'
yHeader2 = ['    D%d' % (i+1) for i in range(102)]
yHeader2.insert(0,'Time')
yHeader = yHeader1 + "\t".join(yHeader2) + '\n'
outFileY.write(yHeader)

numImages = tiffStack.shape[0]

timeMinutes = 0
d = np.arange(1,100,2)
de= np.arange(101,512,8)
d = np.concatenate((d,de))

for i in range(5,numImages,numSkippedFrames):
    iImage = tiffStack[i,:,:]
    gx = skf.greycomatrix(iImage, d, [0], 1024, 
                        symmetric=True, normed=True)
    cx = skf.greycoprops(gx, 'homogeneity')
    cx = np.ndarray.flatten(cx)
    cx = np.ndarray.tolist(cx)
    gy = skf.greycomatrix(iImage, d, [1.5708], 1024, 
                        symmetric=True, normed=True)
    cy = skf.greycoprops(gy, 'homogeneity')
    cy = np.ndarray.flatten(cy)
    cy = np.ndarray.tolist(cy)    
    timeMinutes = timeMinutes + 5*numSkippedFrames
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
