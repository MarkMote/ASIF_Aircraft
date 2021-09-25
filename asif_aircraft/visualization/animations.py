import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib import animation 
import numpy as np 

def animate_aircraft(ac): 
    playx = 50 # factor to speed up animation from real time 

    global aircraft
    global j 
    aircraft = ac 

    # set up figure and animation
    fig = plt.figure(figsize=(9,9))
    lims = 4
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                        xlim=(-lims,lims), ylim=(-lims, lims))
    ax.grid(alpha=0.25)

    line, = ax.plot([], [], 'o-', lw=2)
    trail, = ax.plot([], [], '-', lw=1, color=[0.090, 0.870, 0.933, 0.4])
    dpath, = ax.plot([], [], '-', lw=1, color=[0, 0, 0, 0.3]) # desired path 
    fpath, = ax.plot([], [], '-', lw=1.5, color=[0.090, 0.192, 0.933, 0.5]) # path taken 
    lpath, = ax.plot([], [], '-', lw=2, color=[1,0,0, 0.25]) # hard left 
    rpath, = ax.plot([], [], '-', lw=2, color=[0,1,0, 0.25]) # hard right 

    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    j = 0 
    umax_left = np.array([aircraft.omega_max,0])
    umax_right = np.array([-aircraft.omega_max, 0])

    def init():
        """initialize animation"""
        line.set_data([], [])
        trail.set_data([], [])
        fpath.set_data([], [])
        dpath.set_data([], [])
        lpath.set_data([], [])
        rpath.set_data([], [])
        time_text.set_text('')
        return line, time_text, trail, fpath, lpath, rpath, dpath 


    def animate(i):
        """perform animation step"""
        global aircraft, j
        if j<len(aircraft.timevec)-2:
            j+=1
        else: 
            j=0
        x1 = 0.001*aircraft.get_xpos()[j]
        y1 = 0.001*aircraft.get_ypos()[j]


        fs_state = aircraft.forcast(j,10,10, aircraft.control_des[j])
        dpath.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft.forcast(j,10,10)
        fpath.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft.forcast(j,10,10, umax_left)
        lpath.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft.forcast(j,10,10, umax_right)
        rpath.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])

        line.set_data(0.001*aircraft.get_pos(j))
        trail.set_data(0.001*aircraft.get_xpos()[:j], 0.001*aircraft.get_ypos()[:j])

        time_text.set_text('time = %.1f with dt = %.2f s and rmin = %.2f km' %(aircraft.timevec[j], aircraft.dt, aircraft.get_rmin('km') ))
        return line, time_text, trail, fpath, lpath, rpath, dpath   

    # choose the interval based on dt and the time to animate one step
    from time import time
    dt = aircraft.dt/playx
    t0 = time()
    animate(0)
    t1 = time()
    interval = 1000 * dt - (t1 - t0)

    ani = animation.FuncAnimation(fig, animate, frames=300,
                                interval=interval, blit=True, init_func=init)

    plt.show()
