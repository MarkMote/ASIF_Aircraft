"""
INCOMPLETE
"""

# Imports 
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib import animation 
import math 
import sys, os, inspect
import os

# Relative Imports 
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))) # add parent directory to path  
from simulation import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Import the Desired Controller from the "controllers" directory 
from controllers.template import Controller 
# Import Active Set Invariance Filter (ASIF) (aka RTA mechanism)
from asif.geofence import ASIF 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Parameters 
T  = 60*1 # total simulation time [s]
Nsteps = math.ceil(5*T) # number steps in simulation time horizon
x01 = np.array([-2000,0, 0.01]) # initial state 
x02 = np.array([ 2000, 0, -np.pi])


# Initialize Aircraft Simulation, Controller, and ASIF
timevec = np.linspace(0, T, Nsteps)
aircraft_1 = Simulation(timevec, x01)
aircraft_2 = Simulation(timevec, x02)
asif = ASIF()
controller = Controller() 

for i in range(Nsteps-1):

    x = aircraft_1.get_cstate()
    udes = controller.main(x)
    u = asif.main(x, udes)

    aircraft_1.step(u, udes)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#############################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# fig = plt.figure()
# ax = plt.axes()
# plt.plot(aircraft.get_xpos(), aircraft.get_theta())
# # plt.show()

from visualization.animations import *
animate_aircraft(aircraft, 20)

exit()

