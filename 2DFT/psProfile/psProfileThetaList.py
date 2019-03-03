# -*- coding: utf-8 -*-
"""
Title: Power Spectrum Profile
File: 
Version: 3.3.2019.1
Author: C.D. Wentworth

Summary: This program calculates the profile of the power spectrum 
of the Fourier Transform of an image. It fits the power spectrum to
a shifted exponential decay model and creates a list of the decay
rate as a function of angle measured from the x-axis.

usage: python psProfile.py
Revisions: 
    3.1.2019.1: base
    3.3.2019.1: added a check that r, ps profile distance to
                origin, was not too large
    
"""
import matplotlib.pylab as plt
import numpy as np
import scipy.fftpack as scfft
import skimage.io as skio
from scipy.optimize import curve_fit

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

def profileFit(r,Nmin,mu):
    """
    This function calculates the power spectrum profile using
    a shifted exponential decay model.

    """
    f = N0*np.exp(-mu*r)+Nmin
    return f

#--Main Program
testImage = skio.imread('testBiofilmImage.tif')

# perform the Fourier Transform
fft1 = scfft.fft2(testImage)
fft2 = scfft.fftshift( fft1 )

# calculate the power spectrum
ps = np.abs(fft2)
ps = 20*np.log10(ps)
ps = ps.astype(int)
h,w = ps.shape

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
    p = Nmin,mu
    popt,pcov = curve_fit(profileFit,rl,pl,p)
    pFitData = popt[0],popt[1]
    pFitList.append(pFitData)

muList = []
for f in pFitList:
    muList.append(f[1])
angleList = np.rad2deg(angleList)
plt.plot(angleList,muList,linestyle='',marker='^',
         markersize=8)
plt.xlim([-90,90])
plt.ylim([0,0.75])
plt.xlabel(r'$\theta \ [deg]$',fontsize=14)
plt.ylabel(r'$\mu$',fontsize=14)
plt.savefig('psFit.png')
