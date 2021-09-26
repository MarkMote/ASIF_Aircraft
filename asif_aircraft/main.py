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
x0 = [-2000,0, -0.1] # initial state 


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

# plt.plot(aircraft.timevec, aircraft.get_xpos())
# plt.show()
# exit()

# plt.plot(aircraft.timevec[:-1], asif.OMGmin,
#  aircraft.timevec[:-1], asif.OMG,
#  aircraft.timevec[:-1], asif.OMGmax)

# exit()
from visualization.animations import *
animate_aircraft(aircraft, 20)

print("mission success! \n")
