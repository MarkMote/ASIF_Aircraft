# Imports 
from time import time
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import os, sys, inspect

from numpy.core.function_base import linspace

# Relative Imports 
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))) # add parent directory to path  
from simulation import *

# Set Params 
v = 100; 
omg = 0.2; 
global Rmin, Ds 
Rmin = v/omg 
x1 = np.array([ 500, 1000, .4])
x2 = np.array([-5500, -300, np.pi/4])
# global Ds 
Ds = 0 
Nsteps = 1000
T = 90
timevec = np.linspace(0,T,Nsteps)

def h(x1,x2):
    global Rmin, Ds 
    theta1 = x1[2]
    theta2 = x2[2]
    db = x1[0]-Rmin*np.sin(x1[2]) - (x2[0]-Rmin*np.sin(x2[2]))
    dc = x1[1]+Rmin*np.cos(x1[2]) - (x2[1]+Rmin*np.cos(x2[2]))
    
    A1 = db**2 + dc**2 + (2*Rmin**2)*(1-np.cos(theta1-theta2))
    A2 = 4*Rmin*np.sin(0.5*(theta1-theta2))*np.sqrt(db**2+dc**2)

    return A1-A2-Ds**2

h(x1,x2)

def grad_h(x1,x2):
    global Rmin, Ds 
    db = x1[0]-Rmin*np.sin(x1[2]) - (x2[0]-Rmin*np.sin(x2[2]))
    dc = x1[1]+Rmin*np.cos(x1[2]) - (x2[1]+Rmin*np.cos(x2[2]))
    gamma = 4*Rmin*np.sin(0.5*(x1[2]-x2[2]))
    gh = np.array([0,0,0,0,0,0])
    gh[0] = 2*db - gamma*db/np.sqrt(db**2+dc**2)

    return gh 

def grad_h_approx(x1,x2):
    gh = np.array([0,0,0,0,0,0])
    delta = 10e-8
    d1 = np.array([delta, 0, 0]) #TODO: more efficient method 
    d2 = np.array([0, delta, 0]) 
    d3 = np.array([0, 0, delta]) 
    gh[0] = (h(x1+d1,x2)-h(x1-d1,x2))/(2*delta)# (h(x1+d1,x2)-h(x1-d1,x2))/(2*delta)
    return gh 

gh = grad_h(x1,x2)[0]
gha = grad_h_approx(x1,x2)[0]
print("grad_h = ", gh)
print("grad_h_approx = ", gha)
print("percent error = ", 100*np.abs(gh-gha)/gh)

sys.exit() 
# rho = np.zeros(timevec.__len__())
# rho =  [ (A1+ A2*np.cos(omg*timevec[i]+Phi) +  Ds**2 ) for i in range(Nsteps) ] #  [ (A1 + A2*np.cos(omg*timevec[i]+Phi) - Ds**2 ) for i in range(Nsteps) ]

# print("A1 = ", A1)
# print("A2 = ", A2)


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

