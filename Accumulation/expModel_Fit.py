'''
File: expModel_Fit.py
Version: 5-18-2018.1
Author: C.D. Wentworth

This script shows an example of how to fit data, contained in a text file, to the  
exponential model function using a least-squares algorithm from the library function
scipy.optimize.curve_fit.  It also plots the best-fit solution and the data.
'''
import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit

def N(t,N0,r):
    import numpy as np
    N = N0*np.exp(r*t)
    return N

# Read in data
cols = np.loadtxt('bfa_0.20Dy_sub.txt',
                  skiprows=4)
td = cols[:,0]
OD = cols[:,1]

# Define initial guess for model parameters
N0 = 0.036
r = 0.002
p = N0,r

popt,pcov = curve_fit(N,td,OD,p)

# Calculate uncertainty in the parameters
se = np.sqrt(np.diag(pcov))
ser = se[1]
# Calculate theoretical values
# Define the time grid
t = np.linspace(0,1100,200)
N0,r = popt
Na =[]
for tt in t:
    Ntemp = N(tt,N0,r)
    Na.append(Ntemp)
    
# Plot the solution
plt.plot(td,OD,linestyle='',marker='o',markersize=10.0,
         label='Data')
plt.plot(t,Na,color='g',label='exp model')
plt.legend()
plt.xlabel('t [m]')
plt.ylabel('N [OD]')
plt.savefig('bfa_0.20Dy_sub.png')
plt.show()
# print out the growth rate
print('growth rate = %10.3e +- %10.1e' % (r,ser))
