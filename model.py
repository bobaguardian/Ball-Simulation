import controller, sys
import model   #strange, but we need a reference to this module to pass this module to update
from simulton import Simulton
from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special   import Special  


# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running     = False
cycle_count = 0;
simultons   = set();
clicked     = None


#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running,cycle_count,simultons, clicked
    running     = False;
    cycle_count = 0;
    simultons  = set()
    clicked     = None




#start running the simulation
def start ():
    global running
    running = True


#stop running the simulation (freezing it)
def stop ():
    global running
    running = False 


#step just one update in the simulation
def step ():
    new_simultons = set(simultons)
    global cycle_count
    if running:
        cycle_count +=1
        for s in new_simultons:
            s.update(model)
        stop()
        
        
    elif not running:
        start()
        cycle_count +=1
        for s in new_simultons:
            s.update(model)
        stop()


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global clicked
    clicked = kind
    

#add the kind of remembered object to the simulation (or remove any objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    new_simulton = set(simultons)
    if clicked == 'Remove':
        for s in new_simulton:
            d = s.get_location()
            if Simulton.contains(s, (x,y)):
                remove(s)
    else:
        simultons.add(eval(clicked)(x,y))
        



#add simulton s to the simulation
def add(s):
    simultons.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    simultons.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    result = set()
    for s in simultons:
        if p(s):
            result.add(s)
    return result


#call update for every simulton in the simulation
def update_all():
    global cycle_count
        
    if running:
        remove_simultons = set()
        cycle_count += 1
        new_simulton = set(simultons)
        for simulton in new_simulton:
            simulton.update(model)



#delete from the canvas every simulton in the simulation, and then call display for every
#  simulton in the simulation to add it back to the canvas possibly in a new location: to
#  animate it; also, update the progress label defined in the controller
def display_all():
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
    
    for s in simultons:
        s.display(controller.the_canvas)
    
    controller.the_progress.config(text=str(len(simultons))+" simultons/"+str(cycle_count)+" cycles")
