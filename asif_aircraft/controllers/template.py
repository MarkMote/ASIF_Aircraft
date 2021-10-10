#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: <your name here>

A template for creating controllers, returns zero input 

The main loop will call the controller's "main" class and expect 
a control signal of appropriate size and type to be returned 

In order for this script to work correctly with the main script, avoid 
changing the name of the "Controller" class, or the inputs and outputs of 
the "main" function.  

"""

# General Imports 
import numpy as np 
import os, sys, inspect

# Import Local Directories 
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))) # add parent directory to path  
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utilities')) # add utilities to path 
from parameters import Parameters 


class Controller(Parameters): 
    def __init__(self):
        self.zero_input = [0,0]
        
        ######################################################################
        # Set up the controller parameters and options here
        ######################################################################
        
        
    def main(self, x0, t=0):
        """
        Parameters
        ----------
        x0 : state
            x = [x_pos, y_pos, theta]
        t: time since start 


        Returns
        -------
        u : control input 
            u = [v omega] 
        """
        
        ######################################################################
        # Insert your code here 
        ######################################################################
        
        u = self.zero_input
        
        return u
        
        
        