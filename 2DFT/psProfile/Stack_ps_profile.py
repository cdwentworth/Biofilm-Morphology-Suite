# -*- coding: utf-8 -*-
"""
Code to calculate the profile of a stack of images at certain degree values. This code
will produce a .txt file that will contain a list of all of the values of Mu (the decay ratio)
and the values of the degree with the corrisponding image number.

@author: Sarah
"""
import matplotlib.pylab as plt
import numpy as np
import scipy.fftpack as scfft
import skimage.io as skio
from scipy.optimize import curve_fit


def PowerSpectrum(inputImage):
    fft1 = scfft.fft2(inputImage)
    fft2 = scfft.fftshift( fft1 )
    ps = np.abs(fft2)
    ps = 50*np.log10(ps+0.1)
    ps = ps.astype(int)
    h,w = ps.shape
    for r in range(h):
        for c in range(w):
            if ps[r,c]<0:
                ps[r,c]=0
    return ps

def calcProfile(ps,theta):
    """
    This function calculates the experimental profile for a 
    given theta.
    """
    pl = []
    rl = []
    for sx in range(1,int(w/2)):
        sy = sx*np.tan(theta)
        px = int(sx + w/2)
        py = int(sy + h/2)
        r = np.sqrt(sx**2 + sy**2)
        if px < w and py < h:
            if (px >= 0) and (py >= 0):
                pl.append(ps[py,px])
                rl.append(r)    
    return rl,pl

def profileFit(r,Nmin,mu,N0):
    """
    This function calculates the power spectrum profile using
    a shifted exponential decay model.
    """
    f = N0*np.exp(-mu*r)+Nmin
    return f

def Profile(ps):
    # make sure all power spectrum values greater than or equal to
    # zero
    for r in range(h):
        for c in range(w):
            if ps[r,c]<0:
                ps[r,c]=0
                # define angles
    thetaMax = 85
    numAngles = 12
    dtheta = thetaMax/numAngles
    angle = thetaMax
    angleList = []
    angleListNeg = []
    while angle > 0. :
        angleRad = np.deg2rad(angle)
        angleList.append(angleRad)
        angleListNeg.append(-angleRad)
        angle = angle - dtheta
        angleList = angleListNeg + angleList   

    pFitList = []
    for theta in angleList:
    # create profile
        rl,pl = calcProfile(ps,theta)
    # fit profile
        N0 = np.amax(ps)
        Nmin = 70
        mu = 0.1
        p = Nmin,mu,N0
        popt,pcov = curve_fit(profileFit,rl,pl,p)
        pFitData = popt[0],popt[1]
        pFitList.append(pFitData)

    muList = []
    for f in pFitList:
        muList.append(f[1])
        
    return angleList, muList
        

#main
#read in the tiff stack
tiffStackFile = 'Processed_041118_W1FITC 100- CAM_S24_T_1.0 dyne_cm2.tif'
tiffStack = skio.imread(tiffStackFile)
tiffStackFilePieces = tiffStackFile.split('.')

#get the size of the stack
numImages,h,w = tiffStack.shape
psStack = np.zeros((numImages,h,w),dtype=np.int16)

i = 0
while i < numImages:
    #image for whatever i is
    iImage = tiffStack[i,:,:]
    #find the power spectrum
    power_spectrum = PowerSpectrum(iImage)
    #psStack[i] = power_spectrum
    psProfile = Profile(power_spectrum)
    file = open("TEST.txt","w")
    file.write(str(i))
    file.write(str(psProfile))
    #update i for the loop
    i = i + 1
file.close