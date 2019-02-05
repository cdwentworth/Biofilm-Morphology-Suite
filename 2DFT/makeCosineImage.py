#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Make Test Image
File: makeCosineImage.py
Version: 1-5-2019.1
Author: C.D. Wentworth

Summary: This program will construct a 16 bit grayscale image with a 
cosine variation of intensity.  The wavelength and direction of the variation
is given by the values of kx and ky, the x and y components of the wave
number.  In Fourier analysis kx and ky would be called frequencies.

usage: python makeCosineImage.py
Revisions: 
    1-5-2019.1: base version

definitions:
    
h = image height in pixels
w = image width in pixels    
kx = x component of wave number (Fourier frequency)
ky = y component of wave number (Fourier frequency)

"""

import matplotlib.pylab as plt
import numpy as np
import skimage.io as skio

# main
h = 800
w = 800
maxI = 65535
newImage = np.zeros((h,w),dtype='uint16')
kx = 1.
ky = 0.
for x in range(0,w):
    for y in range(0,h):
        v = maxI*(np.cos(kx*x+ky*y)+1)/2
        newImage[y,x]=int(v)
skio.imsave('hCosine2.png',newImage)
    
