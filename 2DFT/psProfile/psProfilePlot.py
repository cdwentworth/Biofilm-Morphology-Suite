# -*- coding: utf-8 -*-
"""
Title: Power Spectrum Profile Fits
File: 
Version: 3.8.2019.1
Author: C.D. Wentworth

Summary: This program reads in data for the power
spectrum decay rate as function of angle for different 
images and creates a single graph.

usage: python psFitCombined.py
Revisions:
"""
import matplotlib.pylab as plt
import numpy as np

#--Main Program

cols = np.loadtxt('Processed_033018_W1FITC_100-CAM_S14_T_0.5_dyne_cm2_profileData.txt',skiprows=2)
numAngles = 25

# process image 1
imageSet = 100
initialRow = imageSet*numAngles
finalRow = initialRow + numAngles
angles = cols[initialRow:finalRow,1]
mu = cols[initialRow:finalRow,2]
plt.plot(angles,mu,linestyle='',marker='^',markersize=5,label='100')

# process image 2
imageSet = 150
initialRow = imageSet*numAngles
finalRow = initialRow + numAngles
angles = cols[initialRow:finalRow,1]
mu = cols[initialRow:finalRow,2]
plt.plot(angles,mu,linestyle='',marker='^',markersize=5,label='150')

# process image 3
imageSet = 200
initialRow = imageSet*numAngles
finalRow = initialRow + numAngles
angles = cols[initialRow:finalRow,1]
mu = cols[initialRow:finalRow,2]
plt.plot(angles,mu,linestyle='',marker='^',markersize=5,label='200')

# process image 4
imageSet = 250
initialRow = imageSet*numAngles
finalRow = initialRow + numAngles
angles = cols[initialRow:finalRow,1]
mu = cols[initialRow:finalRow,2]
plt.plot(angles,mu,linestyle='',marker='^',markersize=5,label='250')

plt.xlabel(r'$\theta$',fontsize=14)
plt.ylabel(r'$\mu$',fontsize=14)
plt.title(r'$PS \ Profile - 0.5 \ dyne/cm^2 \ Ch \ 14$',fontsize=16)
plt.xlim([-90,90])
plt.ylim([0,1])
plt.legend()
plt.savefig('Processed_033018_W1FITC_100-CAM_S14_T_0.5_dyne_cm2_profileData.png')
plt.show()