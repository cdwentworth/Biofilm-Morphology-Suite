# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 13:04:13 2019

@author: Sarah
code to take each of the images from the tiff stack and perform a fourier transform
of all of the images and print them out.

"""
import matplotlib.pylab as plt
import numpy as np
import scipy.fftpack as scfft
import skimage.io as skio

#function to perform the Fourier Transform and find the Power Spectrum
def PowerSpectrum(inputImage):
#    fft1 = scfft.fft2(tiffStack)
    fft1 = scfft.fft2(inputImage)
    fft2 = scfft.fftshift( fft1 )
    ps = np.abs(fft2)
#    ps = 20*np.log10(ps+0.1)
    ps = 50*np.log10(ps)
    ps = ps.astype(int)
    h,w = ps.shape
    for r in range(h):
        for c in range(w):
            if ps[r,c]<0:
                ps[r,c]=0
    return ps

#read in the tiff stack
tiffStackFile = 'biofilmSubStack.tif'
tiffStack = skio.imread(tiffStackFile)
tiffStackFilePieces = tiffStackFile.split('.')

#get the size of the stack
#numImages = tiffStack.shape[0]
numImages,h,w = tiffStack.shape
psStack = np.zeros((numImages,h,w),dtype=np.int16)

i = 0
while i < numImages:
    #image for whatever i is
    iImage = tiffStack[i,:,:]
    #find the power spectrum
    power_spectrum = PowerSpectrum(iImage)
    psStack[i]=power_spectrum
    #show the image and the power spectrum
#    plt.imshow(iImage)
#    plt.imshow(power_spectrum)
    #update i for the loop
    i = i + 1
skio.imsave('psStack.tif',psStack)
    
    
    