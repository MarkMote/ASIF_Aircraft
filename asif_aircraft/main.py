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
from asif.template import ASIF 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Parameters 
T  = 60*2 # total simulation time [s]
Nsteps = math.ceil(5*T) # number steps in simulation time horizon
x0 = [-1000,0,0] # initial state 


# Initialize Aircraft Simulation 
timevec = np.linspace(0, T, Nsteps)
aircraft = Simulation(timevec, x0)

for i in range(Nsteps-1):
    u = aircraft.omega_max*np.sin(0.01*aircraft.get_ctime())

    aircraft.step(u)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#############################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from visualization.animations import *
animate_aircraft(aircraft)

print("mission success! \n")
