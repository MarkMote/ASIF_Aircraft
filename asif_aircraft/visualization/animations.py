import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib import animation 
import numpy as np 

def animate_aircraft(ac, plx=50): 
    playx = plx # factor to speed up animation from real time 

    global aircraft
    global j 
    aircraft = ac 

    # set up figure and animation
    fig = plt.figure(figsize=(8,8))
    lims = 5
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
    umax_left = np.array([0,aircraft.omega_max])
    umax_right = np.array([0,-aircraft.omega_max])

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


###

def animate_aircraft2(ac1, ac2, plx=50): 
    playx = plx # factor to speed up animation from real time 

    global aircraft_1, aircraft_2
    global j 
    aircraft_1 = ac1
    aircraft_2 = ac2 

    # set up figure and animation
    fig = plt.figure(figsize=(8,8))
    lims = 5
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                        xlim=(-lims,lims), ylim=(-lims, lims))
    ax.grid(alpha=0.25)

    line1, = ax.plot([], [], 'o-', lw=2)
    trail1, = ax.plot([], [], '-', lw=1, color=[0.090, 0.870, 0.933, 0.4])
    dpath1, = ax.plot([], [], '-', lw=1, color=[0, 0, 0, 0.3]) # desired path 
    fpath1, = ax.plot([], [], '-', lw=1.5, color=[0.090, 0.192, 0.933, 0.5]) # path taken 
    lpath1, = ax.plot([], [], '-', lw=2, color=[1,0,0, 0.25]) # hard left 
    rpath1, = ax.plot([], [], '-', lw=2, color=[0,1,0, 0.25]) # hard right 

    line2, = ax.plot([], [], 'o-', lw=2)
    trail2, = ax.plot([], [], '-', lw=1, color=[0.090, 0.870, 0.933, 0.4])
    dpath2, = ax.plot([], [], '-', lw=1, color=[0, 0, 0, 0.3]) # desired path 
    fpath2, = ax.plot([], [], '-', lw=1.5, color=[0.090, 0.192, 0.933, 0.5]) # path taken 
    lpath2, = ax.plot([], [], '-', lw=2, color=[1,0,0, 0.25]) # hard left 
    rpath2, = ax.plot([], [], '-', lw=2, color=[0,1,0, 0.25]) # hard right 

    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    j = 0 
    umax_left = np.array([0,aircraft_1.omega_max])
    umax_right = np.array([0,-aircraft_1.omega_max])

    def init():
        """initialize animation"""
        line1.set_data([], [])
        trail1.set_data([], [])
        fpath1.set_data([], [])
        dpath1.set_data([], [])
        lpath1.set_data([], [])
        rpath1.set_data([], [])
        line2.set_data([], [])
        trail2.set_data([], [])
        fpath2.set_data([], [])
        dpath2.set_data([], [])
        lpath2.set_data([], [])
        rpath2.set_data([], [])
        time_text.set_text('')
        return time_text, line1, trail1, fpath1, lpath1, rpath1, dpath1, line2, trail2, fpath2, lpath2, rpath2, dpath2


    def animate(i):
        """perform animation step"""
        global aircraft_1, aircraft_2, j
        if j<len(aircraft_1.timevec)-2:
            j+=1
        else: 
            j=0
        # x1 = 0.001*aircraft_1.get_xpos()[j]
        # y1 = 0.001*aircraft_1.get_ypos()[j]

        fs_state = aircraft_1.forcast(j,10,10, aircraft_1.control_des[j])
        dpath1.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft_1.forcast(j,10,10)
        fpath1.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft_1.forcast(j,10,10, umax_left)
        lpath1.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft_1.forcast(j,10,10, umax_right)
        rpath1.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        line1.set_data(0.001*aircraft_1.get_pos(j))
        trail1.set_data(0.001*aircraft_1.get_xpos()[:j], 0.001*aircraft_1.get_ypos()[:j])

        fs_state = aircraft_2.forcast(j,10,10, aircraft_2.control_des[j])
        dpath2.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft_2.forcast(j,10,10)
        fpath2.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft_2.forcast(j,10,10, umax_left)
        lpath2.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        fs_state = aircraft_2.forcast(j,10,10, umax_right)
        rpath2.set_data(0.001*fs_state[:,0], 0.001*fs_state[:,1])
        line2.set_data(0.001*aircraft_2.get_pos(j))
        trail2.set_data(0.001*aircraft_2.get_xpos()[:j], 0.001*aircraft_2.get_ypos()[:j])


        time_text.set_text('time = %.1f with dt = %.2f s' %(aircraft_1.timevec[j], aircraft_1.dt))
        return time_text, line1, trail1, fpath1, lpath1, rpath1, dpath1, line2, trail2, fpath2, lpath2, rpath2, dpath2

    # choose the interval based on dt and the time to animate one step
    from time import time
    dt = aircraft_1.dt/playx
    t0 = time()
    animate(0)
    t1 = time()
    interval = 1000 * dt - (t1 - t0)

    ani = animation.FuncAnimation(fig, animate, frames=300,
                                interval=interval, blit=True, init_func=init)

    plt.show()


