# Coverage - PA01 System
#
import numpy as np
import matplotlib.pylab as plt

# Read in data
cols1 = np.loadtxt('bfc_0.20Dy.txt',skiprows=4)
timeData1 = cols1[:,0]
CData1 = cols1[:,1]

cols2 = np.loadtxt('bfc_0.50Dy.txt',skiprows=4)
timeData2 = cols2[:,0]
CData2 = cols2[:,1]

cols3 = np.loadtxt('bfc_1.0Dy.txt',skiprows=4)
timeData3 = cols3[:,0]
CData3 = cols3[:,1]

# Plot data

plt.plot(timeData1,CData1,linestyle='-',marker='d', label=r'$0.20 \; Dyne/cm^2$',
         markersize=8.0)
plt.plot(timeData2,CData2,linestyle='-',marker='o', label=r'$0.50 \; Dyne/cm^2$',
         markersize=8.0)     
plt.plot(timeData3,CData3,linestyle='-',marker='^', label=r'$1.00 \; Dyne/cm^2$',
         markersize=8.0)               
plt.xlim([0,1500])
plt.ylim([0,100])
plt.xlabel(r'$t\;[min]$',fontsize=14)
plt.ylabel(r'$C \; [\%]$',fontsize=14)
#plt.title(r'$Roughness \; Coefficient\;-\;0.50\;dyne/cm^2$',fontsize=16)
plt.title(r'$Biofilm \; Coverage$',fontsize=16)
plt.legend(loc=4)
plt.savefig('C.png',dpi=300)
plt.show()
