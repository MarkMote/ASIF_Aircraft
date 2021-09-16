# ASIF_Aircraft
Control Barrier Functions for 2D Dubbins Aircraft Model. 

__Documentation Resources:__ 
* Dynamics: 
* Explicit CBFs: 
* Implicit CBFs: 

__Development Info:__ 
The project is developed in [Ubuntu 20.04](https://releases.ubuntu.com/20.04/), and the IDE is [Visual Studio Code](https://code.visualstudio.com/). 



# Setup 



1. Install a recent version of Python 

2. Create a virtual environment and activate it 

```zsh 
python -m .env/asif
source .env/asif/bin/activate 
```

This should change the prompt to indiacte that the virtual environment `asif` is active. It can be deactivated with the command `deactivate`. 

3. Install dependencies inside the virtual environment. 

```zsh 
pip install -r requirements.txt
```

# 🚀 Quickstart  

To run a simulation: ... 

To change the controller: 

To change the asif: 

To change model parameters: 




# Directories 

* __asif_aircraft/asif__ 
-- Contains _Active Set Invariance Filters_ (ASIFs), which are defined as classes. ASIFs filter the control signal to prevent unsafe actions. 

* __asif_aircraft/controllers__ 
-- Contains all nominal controllers, which are defined as classes. 

* __asif_aircraft/dynamics__
-- Contains all dynamics functions, which are defined as classes. 

* __asif_aircraft/visualization__
-- Contains all plotting tools. 

* __asif_aircraft/utilities__
-- Contains all other supporting code. 

