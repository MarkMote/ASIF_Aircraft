#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: <your name here>

A template for creating RTA filters. 

The main loop will call the ASIF's "main" class and expect 
a control signal of appropriate size and type to be returned. 

In order for this script to work correctly with the main script, avoid 
changing the name of the "ASIF" class, or the inputs and outputs of 
the "main" function.  

"""

# General Imports 
import numpy as np 
import os, sys, inspect

# Import Local Directories 
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))) # add parent directory to path  
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utilities')) # add utilities to path 
from parameters import Parameters 



class ASIF(Parameters): 
    def __init__(self):
        self.zero_input = [0]
        self.Rmin = self.speed/self.omega_max  
        self.OMGmin = []      
        self.OMG = []       
        self.OMGmax = [] 
        
    def main(self, x0, u_des):
        """
        Parameters
        ----------
        x0 : state
            x = [x_pos, y_pos, theta]
        u_des: desired control input 
            u_des = [omega_des]


        Returns
        -------
        u : actual control input 
            u = [omega_act] 
        """
        sx = x0[0]

        # x0[0] = x0[0]-1000

        theta = x0[2]
        omg_des = u_des[0]

        if np.cos(theta) >= 0: # facing boundary 
            if np.sin(theta) <= 0: # boundary on left 
                omg_min = -self.omega_max
                omg_max = (self.speed*np.cos(theta))-self.alpha(self.h_s(x0))
                den = max(0.0000001,self.Rmin*np.cos(theta))
                omg_max = -omg_max/(den)
                omg_max = self.saturate(omg_max)
            else:
                omg_max = self.omega_max
                omg_min = (self.speed*np.cos(theta))-self.alpha(self.h_s(x0))
                den = max(0.0000001,self.Rmin*np.cos(theta))
                omg_min = omg_min/(den)
                omg_min = self.saturate(omg_min)
        else: # away from boundary 
            omg_min = -self.omega_max 
            omg_max =  self.omega_max

        # bound omg to safe values 
        omg = omg_des 
        omg = max(omg, omg_min)
        omg = min(omg, omg_max)

        # Saturate 
        omg = self.saturate(omg)
        
        self.OMGmin.append(omg_min)
        self.OMGmax.append(omg_max)
        self.OMG.append(omg)

        return [omg]
    
    def h_s(self, x):
        """
        h_s(x) >= 0 defines the set of all "safe states". The goal of the ASIF 
        is to ensure that this constraint remains satisfied 

        """
        sx = x[0]
        theta = x[2] 
        
        if np.sin(theta)>=0: # wall on right 
            return self.Rmin*( np.sin(theta)-1)-sx
        else: # wall on left 
            return self.Rmin*(-np.sin(theta)-1)-sx 

    def alpha(self, h): 
        return  0.000001*h**3

    def h_a(self, x):
        return -x[0] 

    def saturate(self, omg):
        return  min(max(-self.omega_max, omg), self.omega_max)


