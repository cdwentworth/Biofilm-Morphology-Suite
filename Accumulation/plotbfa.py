# Accumulation - PA01 System
#
import numpy as np
import matplotlib.pylab as plt

# Read in data
cols1 = np.loadtxt('bfa_0.20Dy.txt',skiprows=2)
timeData1 = cols1[:,0]
bfaData1 = cols1[:,1]

cols2 = np.loadtxt('bfa_0.50Dy.txt',skiprows=2)
timeData2 = cols2[:,0]
bfaData2 = cols2[:,1]

cols3 = np.loadtxt('bfa_1.0Dy.txt',skiprows=2)
timeData3 = cols3[:,0]
bfaData3 = cols3[:,1]

# Plot data

#plt.plot(timeData1,bfaData1,linestyle='-',marker='d', label=r'$0.20 \; Dyne/cm^2$',
#         markersize=8.0)
#plt.plot(timeData2,bfaData2,linestyle='-',marker='o', label=r'$0.50 \; Dyne/cm^2$',
#         markersize=8.0)     
#plt.plot(timeData3,bfaData3,linestyle='-',marker='^', label=r'$1.00 \; Dyne/cm^2$',
#         markersize=8.0)   
plt.semilogy(timeData1,bfaData1,linestyle='-',marker='d', label=r'$0.20 \; Dyne/cm^2$',
         markersize=8.0)
plt.semilogy(timeData2,bfaData2,linestyle='-',marker='o', label=r'$0.50 \; Dyne/cm^2$',
         markersize=8.0)     
plt.semilogy(timeData3,bfaData3,linestyle='-',marker='^', label=r'$1.00 \; Dyne/cm^2$',
         markersize=8.0)            
plt.xlim([0,1500])
#plt.ylim([0,1.5])
plt.xlabel(r'$t\;[min]$',fontsize=14)
plt.ylabel(r'$N \; [rel]$',fontsize=14)
#plt.title(r'$Roughness \; Coefficient\;-\;0.50\;dyne/cm^2$',fontsize=16)
plt.title(r'$Biofilm \; Accumulation$',fontsize=16)
plt.legend(loc=2)
plt.savefig('bfa.png',dpi=300)
plt.show()
