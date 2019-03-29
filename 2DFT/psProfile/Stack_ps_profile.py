# -*- coding: utf-8 -*-
"""
Title: Stack Power Spectrum Profile 
Author: Sarah Vaughn
Version: 3.27.2019.2
Summary:
Code to calculate the profile of a stack of images at certain degree values. This code
will produce a .txt file that will contain a list of all of the values of Mu (the decay ratio)
and the values of the degree with the corrisponding image number.

History:
    3-26-2019.1: Base
    3-26-2019.2: added code to write data to a file using
                 numpy.savetxt
    3.27.2019.1: placed bounds on parameter search in Profile
    3.27.2019.2: put in a check that N0 is positive
    
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
    thetaInRad = np.deg2rad(theta)
    pl = []
    rl = []
    for sx in range(1,int(w/2)):
        sy = sx*np.tan(thetaInRad)
        px = int(sx + w/2)
        py = int(sy + h/2)
        r = np.sqrt(sx**2 + sy**2)
        if px < w and py < h:
            if (px >= 0) and (py >= 0):
                pl.append(ps[py,px])
                rl.append(r)    
    return rl,pl

def createAngles(thetaMax, numAngles):
    """
    This function calculates the angles for performing a power
    spectrum profile.  It returns a list of the angles.  The
    angles are in degrees.
    """
    dtheta = thetaMax/numAngles
    angle = thetaMax
    angleList = []
    while angle >= -thetaMax :
        angleList.append(angle)
        angle = angle - dtheta
    return angleList

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

def profileFit(r,Nmin,mu,N0):
    """
    This function calculates the power spectrum profile using
    a shifted exponential decay model.
    """
    f = N0*np.exp(-mu*r)+Nmin
    return f

def Profile(ps,thetaMax,numAngles):
    """
    Title: Profile
    Author: Sarah Vaughn
    Version: 3.27.2019.1
    Summary: This function takes a power spectrum and for a set
             of directions fits the power spectrum profile along
             the direction to a modified exponential function.
             It returns two lists, the angles and the best-fit
             decay rate.
    Returns: angleList: the list of angles in degrees
             muList: the list of best-fit decay rates
    History:
        3.26.2019.1: base
        3.27.2019.1: placed bounds on parameter search
	   3.27.2019.2: put in a check that N0 is positive
        

    """    
    # make sure all power spectrum values greater than or equal to
    # zero
    for r in range(h):
        for c in range(w):
            if ps[r,c]<0:
                ps[r,c]=0
    angleList = createAngles(thetaMax, numAngles)
    pFitList = []
    for theta in angleList:
        # create profile
        rl,pl = calcProfile(ps,theta)
        # fit profile
        N0 = np.amax(ps)
        if N0>0:
            Nmin = 70
            mu = 0.1
            p = Nmin,mu,N0
            boundsLower = (50,0,0.95*N0)
            boundsUpper = (200,np.inf,1.05*N0)
            try:
                popt,pcov = curve_fit(profileFit,rl,pl,p,
                                      bounds=(boundsLower,boundsUpper))
            except RuntimeError:
                popt = -1000 , -1000 , -1000
        else:
            popt = -1000 , -1000 , -1000
        pFitData = popt[0],popt[1], popt[2]
        pFitList.append(pFitData)

    NminList = []
    muList = []
    N0List = []
    for f in pFitList:
        NminList.append(f[0])
        muList.append(f[1])
        N0List.append(f[2])
    return angleList, NminList, muList, N0List
        
#main program
    
#read in the tiff stack
tiffStackFile = 'Processed_033018_W1FITC100-CAM_S15_T_0.5dyne_cm2.tif'
tiffStack = skio.imread(tiffStackFile)
tiffStackFilePieces = tiffStackFile.split('.')

#get the size of the stack
numImages,h,w = tiffStack.shape
psStack = np.zeros((numImages,h,w),dtype=np.int16)
thetaMax = 85
numAngles = 12
# construct the data array
numRows = numImages*(2*numAngles+1)
data = np.zeros((numRows,5),
                dtype=np.float64)
i = 0
while i < numImages:
    #image for whatever i is
    iImage = tiffStack[i,:,:]
    #find the power spectrum
    power_spectrum = PowerSpectrum(iImage)
    #psStack[i] = power_spectrum
    angleList, NminList, muList, N0List = Profile(power_spectrum,
                                                  thetaMax,numAngles)
    # add data to the data array
    numAnglesInList = len(angleList)
    imageSet = i*numAnglesInList
    for j in range(numAnglesInList):
        data[imageSet+j,0] = float(i)
        data[imageSet+j,1] = angleList[j]
        data[imageSet+j,2] = muList[j] 
        data[imageSet+j,3] = NminList[j]
        data[imageSet+j,4] = N0List[j]
    #update i for the loop
    i = i + 1
headerString1 = 'number_of_images= %5i number_of_angles= %5i \n' % (numImages,2*numAngles+1)
headerString2 = 'image       angle       mu          Nmin       N0'
headerString = headerString1 + headerString2
np.savetxt('Processed_033018_W1FITC100-CAM_S15_T_0.5dyne_cm2_profileData.txt',data,fmt='% 8.3e', delimiter='  ',
           header=headerString)
