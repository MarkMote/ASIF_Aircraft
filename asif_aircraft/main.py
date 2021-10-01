"""
Main Script for running the simulation 
"""

# Imports 
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib import animation 
from simulation import *
import math 
# from visualization.animations import * 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Import the Desired Controller from the "controllers" directory 
from controllers.template import Controller 
# Import Active Set Invariance Filter (ASIF) (aka RTA mechanism)
from asif.cbf import ASIF 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Parameters 
T  = 60*1 # total simulation time [s]
Nsteps = math.ceil(5*T) # number steps in simulation time horizon
x0 = [-2000,0, 0.01] # initial state 


# Initialize Aircraft Simulation, Controller, and ASIF
timevec = np.linspace(0, T, Nsteps)
aircraft = Simulation(timevec, x0)
asif = ASIF()
controller = Controller() 

for i in range(Nsteps-1):

    x = aircraft.get_cstate()
    udes = controller.main(x)
    u = asif.main(x, udes)

    aircraft.step(u, udes)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#############################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


fig = plt.figure()
ax = plt.axes()
plt.plot(aircraft.get_xpos(), aircraft.get_theta())
# plt.show()

from visualization.animations import *
animate_aircraft(aircraft, 20)

exit()


def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = np.linspace(-1500, -100, 50)
y = np.linspace(-2, 2, 50)
Z1 = np.zeros([len(x),len(y)])
Z2 = np.zeros([len(x),len(y)])
X, Y = np.meshgrid(x, y)
for i in range(len(x)): 
    for j in range(len(y)): 
        asif.main([X[i,j], 0, Y[i,j]], [0])
        Z1[i,j] = asif.OMGmin[-1]
        Z2[i,j] = asif.OMGmax[-1]

        # print(asif.OMGmin[-1])

fig = plt.figure()

# ax=plt.axes()
# ax.contour(X,Y,Z)
# plt.show()
# exit() 

ax = plt.axes(projection='3d')
surf = ax.plot_surface(X, Y, Z1)
ax.plot_surface(X, Y, Z2)
ax.set_zlim([-.19,.19])
# ax.contour3D(X, Y, Z, 50)
ax.set_xlabel('x')
ax.set_ylabel('theta')
ax.set_zlabel('omgmin')
plt.show()


# plt.plot(aircraft.timevec, aircraft.get_xpos())
# plt.show()
exit()

# plt.plot(aircraft.timevec[:-1], asif.OMGmin,
#  aircraft.timevec[:-1], asif.OMG,
#  aircraft.timevec[:-1], asif.OMGmax)

# exit()
from visualization.animations import *
animate_aircraft(aircraft, 20)

print("mission success! \n")
