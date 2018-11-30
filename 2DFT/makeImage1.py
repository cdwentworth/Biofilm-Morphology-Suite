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

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio

# main
h = 800
w = 800
maxI = 65535
newImage = np.zeros((h,w),dtype='uint16')
p = w/10
for c in range(0,w):
    v = maxI*(np.cos(2*np.pi*c/p)+1)/2
    for r in range(0,h):
        newImage[r,c]=v
skio.imsave('horizontalCosine.png',newImage)
    


#skio.imsave(outFileName,newTiffStack)    
#outFile.close()
#c = np.linspace(0,w,800)
#f = (np.cos(2*np.pi*c/p)+1)/2
#plt.plot(c,f)
#plt.savefig('cosine.png')
#plt.show()
