# -*- coding: utf-8 -*-
"""
Title: Power Spectrum
File: 
Version: 12.4.2018.1
Author: C.D. Wentworth

Summary: This program calculates the Fourier transform of an image, 
shifts the fft so that the dc signal is in the center, calculates the
power spectrum of the fft, reduces the value range by taking the log10,
and finally creates an image of the power spectrum.

usage: python powerSpectrum.py
Revisions: 
    12.4.2018.1: base
    1.5.2019.1: set negative power spectrum values to zero
    
"""
import matplotlib.pylab as plt
import numpy as np
import scipy.fftpack as scfft
import skimage.io as skio

testImage = skio.imread('dCosine1.png')
fft1 = scfft.fft2(testImage)
fft2 = scfft.fftshift( fft1 )
ps = np.abs(fft2)
ps = 20*np.log10(ps+0.1)
ps = ps.astype(int)
h,w = ps.shape
for r in range(h):
    for c in range(w):
        if ps[r,c]<0:
            ps[r,c]=0
plt.figure(1)
plt.clf()
plt.imshow(testImage)
plt.figure(2)
plt.clf()
plt.imshow(ps)
plt.savefig('ps_dCosine1.png')
plt.show()
#skio.imshow(testImage)
#skio.imsave('powerSpectrum.png',np.log10(ps))
