#from rulessource import rules?

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from random import choice
from maps import *

#get map, rules, etc. ...
pmap = maptions[1]

rules = ['001***N00','000*1*W01', '000*0*E02', '0201**E02', '0200**S01', '01***1S01', '01***0X00']

#randomly place picobot
def place_picobot():
    """ randomly places picobot in
        a valid (nonwall) location
    """
    i = choice(range(len(pmap)))
    j = choice(range(len(pmap[i])))
    while pmap[i,j] == 0: #check if picobot is in a wall
        # i know this is a potentially infinite loop im sorry
        i = choice(range(len(pmap)))
        j = choice(range(len(pmap[i])))
    return i, j

i, j = place_picobot()

pmap[i,j] = 2 #set picobot's color
picostate = '00' #set picobot's state to default of '00' == 0
stop = False # so we can stop the simulation when we want to


def update(data):
    global pmap
    global stop
    new_pmap = pmap.copy()

    if isFinished(new_pmap) or stop:
        cid3 = fig.canvas.mpl_connect('key_press_event', on_step)
        cid5 = fig.canvas.mpl_connect('key_press_event', on_reset)
        return [mat] #don't update if done
    else:
        picomove()


def picomove():
    global pmap
    global rules
    global picostate
    global i 
    global j
    global stop

    new_pmap = pmap.copy()
    for rule in rules: #check rules in order
        if picostate != rule[:2]: #check if state is the same as in the rule
            continue

        surround = getsurr(pmap, i, j) #get surrounding state
        if not checksurr(rule, surround): #check if surroundings match the rule
            continue

        else: #then...
            new_pmap[i,j] = -1.5 #it's been visited
            new_i, new_j = picosubmove(rule[6], [i,j], surround) #move picobot
            picostate = rule[7:] #update picobot's state
            new_pmap[new_i, new_j] = 2 #move picobot marker
            mat.set_data(new_pmap) #update variables
            pmap = new_pmap
            i = new_i
            j = new_j
            return [mat]
            
    stop = True
    raise Exception('no rule applies')

def picosubmove(direction, coords, surr):
    """ updates picobot's coordinates based on
        direction specified (unless there is a wall)
    """    
    d = {'N':0, 'E':1, 'W':2, 'S':3}
    d2 = {'N':'north', 'E':'east', 'W':'west', 'S':'south'}
    if direction == 'X':
        return coords 
    else:
        index = d[direction]
        if surr[index] == '0':
            stop = True
            raise Exception("can't move %s" % d2[direction])
        else:
            if direction == 'N':
                return coords[0]-1, coords[1]
            elif direction == 'E':
                return coords[0], coords[1]+1
            elif direction == 'W':
                return coords[0], coords[1]-1
            elif direction == 'S':
                return coords[0]+1, coords[1]
            else:
                stop = True
                raise Exception("direction not understood")

def unvisit():
    """ resets all visited cells
        to unvisited state
    """
    global pmap
    grid = pmap.tolist()
    for k in range(len(grid)):
        for l in range(len(grid[k])):
            if grid[k][l] != 0:
                grid[k][l] = 1
    pmap = np.array(grid)

def getsurr(picomap, i, j):
    """ returns surroundings of picobot in 
        NEWS form, with 1 == open and 0 == wall
    """
    out = ''
    if i == 0: out += '0'
    else: out += str(pmap[i-1][j]%2)
    try: out += str(pmap[i][j+1]%2)
    except: out += '0'
    if j == 0: out += 0
    else: out += str(pmap[i][j-1]%2)
    try: out += str(pmap[i+1][j]%2)
    except: out += 0
    return out

def reset(given_map=None):
    """ resets board
    """
    global pmap
    global stop
    global i
    global j 
    global picostate
    stop = True
    unvisit()
    picostate = '00'
    if type(given_map) == 'NoneType':
        pmap[i,j] = 1  # remove old location of picobot    
    else:
        pmap[i,j] = given_map[i,j] # keep wall/nonwall of new map
    
    i, j = place_picobot()
    pmap[i,j] = 2 # set new location of picobot
    mat.set_data(pmap)
    return [mat]

def isFinished(picomap):
    """ returns False if there are still 
        (nonwall) squares picobot has not 
        visited; returns True otherwise
    """
    grid = picomap.tolist()
    for k in range(len(grid)):
        for l in range(len(grid[k])):
            if grid[k][l] == 1:
                return False
    return True

def checksurr(rule, surr):
    """ returns True if the current surroundings
        match those specified in a given rule;
        returns False otherwise
    """
    for k in range(4):
        if rule[k+2] + surr[k] == '01':
            return False
        elif rule[k+2] + surr[k] == '10':
            return False
    return True


def on_click(event):
    """ flips cell state when cell is clicked,
        and resets all visited cells to unvisited
        (not necessarily in that order)     
    """
    global pmap
    global i
    global j
    unvisit()
    col = int(np.round(event.xdata))
    row = int(np.round(event.ydata))
    if pmap[row,col] == 0:
        pmap[row,col] = 1
    else:
        pmap[row,col] = 0
    pmap[i,j] = 2
    mat.set_data(pmap)
    return [mat]

def on_keypress(event):
    """ changes map to one specified by 
        the key pressed
    """
    global pmap
    global stop
    global i
    global j
    if event.key in '01234567':
        stop = True
        index = int(event.key)
        pmap = map_options[index]
        reset(given_map = pmap)
        mat.set_data(pmap)
        return [mat]
        
def on_step(event):
    """ goes one step forward
    """
    if event.key == 'n': 
        picomove()

def on_space(event):
    """ pauses animation when the
        spacebar is pressed
    """
    global stop
    if event.key == ' ':
        stop = not stop

def on_reset(event):
    """ resets picobot - sets all visited 
        squares to unvisited, and moves 
        picobot to a nonwall location
    """
    if event.key == 'r':
        reset()

# set colors to values in picomap
cmap = colors.ListedColormap(['#808080','blue','white','xkcd:electric green'])
bounds = [-1.5, -.5, .5, 1.5, 2.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

#show animation!!
fig, ax = plt.subplots()

cid = fig.canvas.mpl_connect('button_press_event', on_click)
cid2 = fig.canvas.mpl_connect('key_press_event', on_keypress)
cid4 = fig.canvas.mpl_connect('key_press_event', on_space)
cid5 = fig.canvas.mpl_connect('key_press_event', on_reset)


mat = ax.matshow(pmap, cmap=cmap, norm=norm)
ani = animation.FuncAnimation(fig, update, interval=5, save_count=50)
plt.show()