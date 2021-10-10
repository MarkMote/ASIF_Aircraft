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
        self.Rmin = self.speed/self.omega_max  # [m]
        self.Ds = 10 # [m]
        self.Ds2 = 10**2 # [m^2]
        
    def main(self, X0, u_des):
        """
        Parameters
        ----------
        X0 : combined state
            X0 = [x1_pos, y1_pos, theta1, x2_pos, y2_pos, theta2]
        U_des: desired control input 
            u_des = [v1_des, omega1_des, v2_des, omega2_des]


        Returns
        -------
        U : actual control input 
            u = [v1 omg1 v2 omg2] 
        """
        U = np.zeros(4)


    
        return U
    
    def h_s(self, X):
        """
        h_s(x) >= 0 defines the set of all "safe states". The goal of the ASIF 
        is to ensure that this constraint remains satisfied 

        """
        x1 = X[:3]
        x2 = X[-3:]
        db = x1[0]-self.Rmin*np.sin(x1[2]) - (x2[0]-self.Rmin*np.sin(x2[2]))
        dc = x1[1]+self.Rmin*np.cos(x1[2]) - (x2[1]+self.Rmin*np.cos(x2[2]))
        
        A1 = db**2 + dc**2 + (2*self.Rmin**2)*(1-np.cos(x1[2]-x2[2]))
        A2 = 4*self.Rmin*np.sin(0.5*(x1[2]-x2[2]))*np.sqrt(db**2+dc**2)
        
        return A1-A2-self.Ds2
        
    def grad_hs(self, X):
        # Numerical evaluation of gradient (TODO: add analytic calculation)
        gh = np.array([0,0,0,0,0,0])
        delta = 10e-4
        Delta = 0.5*delta*np.eye(6) 
        for i in range(6): 
            gh[i] = (self.h_s(X+Delta[i])-self.h_s(X-Delta[i]))/delta 
        return gh 

    def alpha(self, h): 
        return  0.000001*h**3

    # def h_a(self, x):
    #     return -x[0] 

    def saturate_omg(self, omg):
        return  min(max(-self.omega_max, omg), self.omega_max)


