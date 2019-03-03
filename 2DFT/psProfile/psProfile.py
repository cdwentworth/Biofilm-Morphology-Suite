# -*- coding: utf-8 -*-
"""
Title: Power Spectrum Profile
File: 
Version: 3.1.2019.1
Author: C.D. Wentworth

Summary: This program calculates the profile of the power spectrum 
of the Fourier Transform of an image.

usage: python psProfile.py
Revisions: 
    3.1.2019.1: base
    
"""
import matplotlib.pylab as plt
import numpy as np
import scipy.fftpack as scfft
import skimage.io as skio

testImage = skio.imread('testBiofilmImage.tif')

# perform the Fourier Transform
fft1 = scfft.fft2(testImage)
fft2 = scfft.fftshift( fft1 )

# calculate the power spectrum
ps = np.abs(fft2)
ps = 20*np.log10(ps+0.1)
ps = ps.astype(int)
h,w = ps.shape

# make sure all power spectrum values greater than or equal to
# zero
for r in range(h):
    for c in range(w):
        if ps[r,c]<0:
            ps[r,c]=0
# calculate the profile for a given theta
theta = 80 # angle in degrees
theta = np.deg2rad(theta)
pl = []
rl = []
for sx in range(1,int(w/2)):
    sy = sx*np.tan(theta)
    px = int(sx + w/2)
    py = int(sy + h/2)
    r = np.sqrt(sx**2 + sy**2)
    if px < w and py < h:
        pl.append(ps[py,px])
        rl.append(r)

plt.figure(1)
plt.clf()
plt.imshow(ps)
plt.figure(2)
plt.clf()
plt.plot(rl,pl)
plt.savefig('testBiofilmImagePSProfile.png')
plt.show()

