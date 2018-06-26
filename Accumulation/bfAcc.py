#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Biofilm Accumulation
File: bfAcc.py
Version: 6-26-2018.2
Author: C. Wentworth
Revisions:
    6-3-2018.1
    6-26-2018.1: added thresholding
    6-26-2018.2: added command line argument processing

"""

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio
import skimage.filters as skf
import sys
import getopt as go

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

def getArguments():
   inputfile = ''
   outputfile = ''
   argList = sys.argv[1:]
   try:
      opts, args = go.getopt(argList,"hi:o:",["ifile=","ofile="])
   except go.GetoptError:
      print ('bfAcc.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('bfAcc.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   return inputfile, outputfile

# main

# get command line arguments
tiffStackFile, bfaDataFile = getArguments()
   
# establish input data and output file
outFile = open(bfaDataFile ,'w')

tiffStack = skio.imread(tiffStackFile)
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
plt.savefig('033018_W1FITC 100- CAM_S4_bfa_1.0D_T.png')
plt.show()
