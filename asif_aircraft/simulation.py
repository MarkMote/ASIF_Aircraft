# General Imports 
import numpy as np
import sys, os, inspect
import pathlib
sys.path.append(pathlib.Path(__file__).parent.resolve())

# Import Local Directories 
# from parameters import Parameters
# sys.path.append('..')
# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))) # add parent directory to path  
# sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
# sys.path.append(os.getcwd())
print(os.getcwd())
from parameters import Parameters 

class Simulation(Parameters):

    def __init__(self, timevec, x0) :
        self.dim_state = len(x0)
        self.dim_control = 2 

        self.num_steps = len(timevec)
        self.timevec = timevec; 
        self.dt = timevec[1]-timevec[0]; 
        self.cur_ind = 0

        self.state = np.zeros([len(timevec), self.dim_state])
        self.state[0] = x0  
        self.control = np.zeros([len(timevec)-1, self.dim_control])
        self.control_des = np.zeros([len(timevec)-1, self.dim_control])

    
    def xdot(self, x, u):
        '''
        Dynamics Function 
        x = [sx, sy, theta]
        u = [v, omg]
        '''

        return [self.speed*np.cos(x[2]), 
                self.speed*np.sin(x[2]),
                u[1] ]

    def integrate(self):
        i = self.cur_ind 
        xdot = self.xdot(self.state[i], self.control[i])
        self.state[i+1] = self.state[i] + np.multiply( self.dt , xdot  )

    
    def step(self, u=[0,0], udes=[]):
        i = self.cur_ind

        # Save Control Inputs 
        self.control[i] = u
        if udes==[]:
            self.control_des[i] = u
        else:
            self.control_des[i] = udes 
        
        # Integrate 
        self.integrate()

        # Update Current Index 
        if self.cur_ind<=self.num_steps:
            self.cur_ind+=1


    #############################################################################
    # Trajectory Forcasting                                                               #
    #############################################################################
    def forcast(self, j, T=10, N=10, u=[]):
        if u==[]:
            u = self.control[j]

        fs_timevec = np.linspace(0 ,T ,N) # forward simulation time vector 
        fs_state = np.zeros([N, self.dim_state]) # 

        fs_state[0] = self.get_state(j)
        for i in range(len(fs_timevec)-1):
            xdot = self.xdot(fs_state[i], u)
            fs_state[i+1] = fs_state[i] + np.multiply(xdot, fs_timevec[i+1]-fs_timevec[i]) 
        
        return fs_state

    #############################################################################
    # Get Methods                                                               #
    #############################################################################

    def get_ctime(self): # returns current time 
        return self.timevec[self.cur_ind] 

    def get_cstate(self): # returns current state 
        return self.state[self.cur_ind]

    def get_state(self, i=[]):
        if i==[]:
            return self.state[:,0:3]
        else:
            return self.state[i,0:3]

    def get_pos(self, i=[]):
        if i==[]:
            return self.state[:,0:2]
        else:
            return self.state[i,0:2]

    def get_xpos(self, i=[]):
        if i==[]:
            return self.state[:,0]
        else:
            return self.state[i,0]

    def get_ypos(self, i=[]):
        if i==[]:
            return self.state[:,1]
        else:
            return self.state[i,1]

    def get_theta(self, i=[]):
        if i==[]:
            return self.state[:,2]
        else:
            return self.state[i,2]

    def get_xvel(self, i=[]):
        return self.speed*np.cos(self.get_theta(i))

    def get_yvel(self, i):
        return self.speed*np.sin(self.get_theta(i))

    def get_rmin(self, units='m'):
        rmin = self.speed/self.omega_max
        if units=='km':
            rmin = rmin*0.001 
        return rmin


