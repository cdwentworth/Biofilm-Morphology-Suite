# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 16:17:58 2019

@author: Sarah
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
for c in range(0, w):
    v = maxI*np.sin(20*c)+np.sin(10*p)
    for r in range(0,h):
        newImage[r,c]=v
skio.imsave('Sine_Pattern.png',newImage)
