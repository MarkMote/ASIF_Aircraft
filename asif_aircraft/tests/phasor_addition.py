# Imports 
from time import time
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import os, sys, inspect

# Relative Imports 
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))) # add parent directory to path  
from simulation import *

# sys.exit()

# Set Params 
v = 100; 
omg = 0.2; 
x1 = [ 500, 1000, .4]
x2 = [-5500, -300, np.pi/4]
Ds = 0 
Nsteps = 1000
T = 90
timevec = np.linspace(0,T,Nsteps)

# Derived Params 
Rmin = v/omg; 
theta1 = x1[2]
theta2 = x2[2]
b01 = x1[0]-Rmin*np.sin(x1[2])
c01 = x1[1]+Rmin*np.cos(x1[2])
b02 = x2[0]-Rmin*np.sin(x2[2])
c02 = x2[1]+Rmin*np.cos(x2[2])
delta_b = b01-b02
delta_c = c01-c02 
A1 = delta_b**2 + delta_c**2 + (2*Rmin**2)*(1-np.cos(theta1-theta2))

alpha1 = 2*delta_b*Rmin 
alpha2 = 2*delta_c*Rmin 
gamma = 2*np.sin(0.5*(theta1-theta2))
A2 = gamma*np.sqrt(alpha1**2+alpha2**2)

beta1 = 0.5*(theta1+theta2)
beta2 = beta1-np.pi/2
Phi = np.arctan( (alpha1*np.sin(beta1) + alpha2*np.sin(beta2))/(alpha1*np.cos(beta1) + alpha2*np.cos(beta2)))
print("Phi = ", Phi)
Phi = np.arctan( (alpha1*np.sin(beta1) - alpha2*np.cos(beta1))/(alpha1*np.cos(beta1) + alpha2*np.sin(beta1)) )
print("Phi = ", Phi)


rho = np.zeros(timevec.__len__())
rho =  [ (A1+ A2*np.cos(omg*timevec[i]+Phi) +  Ds**2 ) for i in range(Nsteps) ] #  [ (A1 + A2*np.cos(omg*timevec[i]+Phi) - Ds**2 ) for i in range(Nsteps) ]

print("A1 = ", A1)


## Simulation 
aircraft_1 = Simulation(timevec, x1)
aircraft_2 = Simulation(timevec, x2)

for i in range(Nsteps-1):
    u = [v, omg]
    aircraft_1.step(u)
    aircraft_2.step(u)

# exit() 
# print(aircraft_1.dt)

dx2 = (aircraft_1.get_xpos()-aircraft_2.get_xpos())**2
dy2 = (aircraft_1.get_ypos()-aircraft_2.get_ypos())**2
rho2 = dx2+dy2-Ds**2

fig = plt.figure()
ax = plt.axes()
plt.plot( timevec, rho,  'r.') # from equation 
plt.plot( timevec, rho2, 'b') # simulated 
plt.grid(linewidth=0.25)

fig = plt.figure(2)
ax = plt.axes()
plt.plot(aircraft_1.get_xpos(), aircraft_1.get_ypos(),'b')
plt.plot(aircraft_2.get_xpos(), aircraft_2.get_ypos(),'r')
plt.show()

