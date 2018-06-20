# Figure 1
# Roughness - PA01 System
#
import numpy as np
import matplotlib.pylab as plt

# Read in data
cols1 = np.loadtxt('TE_0.20Dy.txt',skiprows=2)
timeData1 = cols1[:,0]
TEData1 = cols1[:,1]

cols2 = np.loadtxt('TE_0.50Dy.txt',skiprows=2)
timeData2 = cols2[:,0]
TEData2 = cols2[:,1]

cols3 = np.loadtxt('TE_1.00Dy.txt',skiprows=2)
timeData3 = cols3[:,0]
TEData3 = cols3[:,1]

# Plot data

plt.plot(timeData1,TEData1,linestyle='-',marker='d', label=r'$0.20 \; Dyne/cm^2$',
         markersize=8.0)
plt.plot(timeData2,TEData2,linestyle='-',marker='o', label=r'$0.50 \; Dyne/cm^2$',
         markersize=8.0) 
plt.plot(timeData3,TEData3,linestyle='-',marker='^', label=r'$1.00 \; Dyne/cm^2$',
         markersize=8.0)            
plt.xlim([0,1500])
plt.ylim([0,1.5])
plt.xlabel(r'$t\;[m]$',fontsize=14)
plt.ylabel(r'$TE$',fontsize=14)
#plt.title(r'$Roughness \; Coefficient\;-\;0.50\;dyne/cm^2$',fontsize=16)
plt.title(r'$Textural \; Entropy$',fontsize=16)
plt.legend(loc=2)
plt.savefig('TE.png',dpi=300)
plt.show()
