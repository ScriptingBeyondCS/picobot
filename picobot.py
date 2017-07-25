##############################################################
# by Hanna Hoffman, HMC '20: Summer 2017
##############################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import AnchoredText
from matplotlib import colors
from random import choice

from rule_conversion import get_rules
from maps import *

##############################################################
##############################################################
#insert here the name of the file where your rules are written
rule_list = get_rules('hw0pr3.txt') 
# how to interact:
#   spacebar: pause/play
#   r: resets map/picobot
#   n: steps forward ("next")
#   for i in 1:7: moves to map i
#       (map 1 is the default)
#   arrow keys: teleports picobot
##############################################################
##############################################################

class Picobot:
    
    def __init__(self):
        self.pmap = maptions[1]
        self.i = 0
        self.j = 0
        self.picostate = '00'
        self.surround = '1111'
        self.rules = []
        self.currentrule = 'none'
        self.stop = True
        self.labels = []
        self.message = 'none'
    
    def __repr__(self):
        s = self.pmap.tolist()
        return (str(s))

    def place_picobot(self):
        """ randomly places picobot in
            a valid (nonwall) location
        """
        # all walls are represented by zero
        # so places that are not zero are not a wall
        notwalls = np.transpose(self.pmap.nonzero())
        notwalls = notwalls.tolist()
        loc = choice(range(len(notwalls)))
        self.i = notwalls[loc][0]
        self.j = notwalls[loc][1]
        self.pmap[self.i,self.j] = 2
        
    def update(self, data):
        """ wrapper update function
            called by funcAnimation
        """
        #check if paused
        if self.isFinished() or self.stop:
            #listen for reset/step/teleports
            cid3 = fig.canvas.mpl_connect('key_press_event', self.on_step)
            cid5 = fig.canvas.mpl_connect('key_press_event', self.on_reset)
            cid6 = fig.canvas.mpl_connect('key_press_event', self.on_teleport)
            #update labels, map if anything's changed
            self.getsurr()
            self.create_labels()
            mat.set_data(self.pmap)
            return [mat]
        else: # call to move if not paused
            self.message = 'none'
            self.picomove()
            self.annotate()
            return [mat]
    
    def picomove(self):
        """ wrapper move function;
            goes through rules in order
        """
        for rule in self.rules:
            self.currentrule = rule
            # check if rule matches current state and surroundings
            if self.picostate != rule[:2]:
                continue

            self.getsurr()
            if not self.checksurr():
                continue
            # update according to rule's directions
            else:
                #set old position to visited
                self.pmap[self.i, self.j] = -1
                #call submove with direction to move
                self.picosubmove(self.currentrule[6])
                #set new state
                self.picostate = rule[7:]
                #update map, labels
                mat.set_data(self.pmap)
                self.create_labels()
                return [mat]
        #if no rule matches, pause and say why
        self.stop = True
        self.message = "no rule applies \nstopping..."
        self.create_labels()

    def picosubmove(self, direction):
        """ updates picobot's coordinates based on
            direction specified (unless there is a wall)
        """    
        d = {'N':[0,'north'], 'E':[1,'east'], 'W':[2,'west'], 'S':[3,'south']}
        if direction in 'xX':
            self.pmap[self.i, self.j] = 2
            pass
        else:
            index = d[direction][0]
            #check if there's a wall, refuse if appropriate
            if self.surround[index] == '0':
                self.stop = True
                self.pmap[self.i, self.j] = 2
                self.message = "can't move %s \nstopping..." % d[direction][1]
                self.create_labels()
            else: #move in specified direction
                if direction == 'N':
                    self.i -= 1
                elif direction == 'E':
                    self.j += 1
                elif direction == 'W':
                    self.j -= 1
                else:
                    self.i += 1
                #update color of picobot's location
                self.pmap[self.i, self.j] = 2
    
    def getsurr(self):
        """ returns surroundings of picobot in 
            NEWS form, with 1 == open and 0 == wall
        """
        out = ''
        # check north - if at top, there's a wall
        if self.i == 0: out += '0'
        else: out += str(self.pmap[self.i-1, self.j]%2)
        # check east - if we get an error with index, there's a wall
        try: out += str(self.pmap[self.i, self.j+1]%2)
        except: out += '0'
        # check west - if all the way left, there's a wall
        if j == 0: out += '0'
        else: out += str(self.pmap[self.i, self.j-1]%2)
        # check south - if we get error with index, there's a wall
        try: out += str(self.pmap[self.i+1, self.j]%2)
        except: out += '0'
        
        self.surround = out

    def isFinished(self):
        """ returns False if there are still 
            (nonwall) squares picobot has not 
            visited; returns True otherwise
        """
        # change ndarray to list of lists
        grid = self.pmap.tolist()
        # loop over lists looking for unvisited
        for k in range(len(grid)):
            for l in range(len(grid[k])):
                if grid[k][l] == 1:
                    return False
        # congratulate if done
        self.message = "map complete!"
        return True
    
    def checksurr(self):
        """ returns True if the current surroundings
            match those specified in a given rule;
            returns False otherwise
        """
        rule = self.currentrule
        for k in range(4):
            # if direct conflicts between rule/surround 
            # say it doesn't match
            if rule[k+2] + self.surround[k] == '01' or \
                    rule[k+2] + self.surround[k] == '10':
                return False
        return True
    
    def reset(self, given_map=None):
        """ resets board
        """
        #pause
        self.stop = True
        #unvisit all visited cells
        self.unvisit()
        #set picostate to default
        self.picostate = '00'
        #check if we're passed a map
        if type(given_map) == type(None):
            self.pmap[self.i, self.j] = 1
        else: #(to prevent holes from appearing)
            self.pmap[self.i, self.j] = given_map[self.i, self.j]
        #put picobot somewhere
        self.place_picobot()
        self.pmap[self.i, self.j] = 2
        #update image, message, labels
        mat.set_data(self.pmap)
        self.message = 'none'
        self.create_labels()
        self.annotate()

        return [mat]

    def unvisit(self):
        """ resets all visited cells
            to unvisited state
        """
        #change ndarray to list of lists
        grid = self.pmap.tolist()
        # loop over lists to change back all visited cells
        for k in range(len(grid)):
            for l in range(len(grid[k])):
                if grid[k][l] != 0:
                    grid[k][l] = 1
        self.pmap = np.array(grid)
    
    def countUnvisited(self):
        """ returns number of
            unvisited cells
        """
        #change ndarray to list of lists
        grid = self.pmap.tolist()
        count = 0
        #loop over lists looking for unvisited cells
        for k in range(len(grid)):
            for l in range(len(grid[j])):
                if grid[k][l] == 1:
                    count += 1
        return count
    
    def make_label(self, text, location):
        """ makes box with given text at a given 
            location. location is a tuple that 
            gives the position of the upper left
            corner of the label.
        """
        anchored_label = AnchoredText(s=text, loc=2, pad=.3, \
                bbox_to_anchor=location, bbox_transform=ax.transAxes,)
        return anchored_label
    
    def create_labels(self, init=False):
        """ creates labels for state, 
            surroundings, remaining cells,
            and current rule
        """
        #take off old labels
        if not init:
            for label in self.labels:
                label.remove()
        #make and place all labels
        state_label = self.make_label("State: %s" % self.picostate, (1,1))
        surr_label = self.make_label("Surroundings: %s" % self.surr_deconverter(self.surround), (.6,0))
        cells_label = self.make_label("Cells to go: %s" % str(self.countUnvisited()), (1, .8))
        rule_label = self.make_label("Current rule: %s" % self.rule_deconverter(self.currentrule), (0,0))
        message_label = self.make_label("Messages: \n%s" % self.message, (1, .6))
        #set all labels and add them to the plot
        self.labels = [state_label, surr_label, cells_label, rule_label, message_label]
        for label in self.labels:
            ax.add_artist(label)

    def rule_deconverter(self, rule):
        """ converts nine character strings
            back to old-style rules
        """
        d = {0:'N', 1:'E', 2:'W', 3:'S'}
        if rule == 'none':
            return rule
        else:
            out = ''
            #add state
            out += rule[:2]
            out += ' '
            #add surroundings
            for i in range(4):
                if rule[i+2] == '*':
                    out += rule[i+2]
                elif rule[i+2] == '0':
                    out += d[i]
                elif rule[i+2] == '1':
                    out += 'X'
            out += ' -> '
            #add direction
            out += rule[6]
            out += ' '
            #add newstate
            out += rule[7:]
            return out
    
    def surr_deconverter(self, surr):
        """ converts 4 character binary
            string back to NEWS surroundings
        """
        d = {0:'N', 1:'E', 2:'W', 3:'S'}
        out = ''
        for i in range(4):
            if surr[i] == '0':
                out += d[i]
            elif surr[i] == '1':
                out += 'X'
        return out
    
    def annotate(self):
        """ updates annotation of picostate
        """
        annotation.set_position((self.j-.6, self.i+.4))
        annotation.set_text(self.picostate)

    def on_click(self, event):
        """ flips cell state when cell is clicked,
            and resets all visited cells to unvisited
            (not necessarily in that order)     
        """
        #reset all visited cells
        self.unvisit()
        #replace picobot
        self.pmap[self.i, self.j] = 2
        #get location of click
        col = int(np.round(event.xdata))
        row = int(np.round(event.ydata))
        #flip from wall to nonwall
        if self.pmap[row,col] == 0:
            self.pmap[row,col] = 1
        else:# flip to wall
            self.pmap[row,col] = 0
        #update plot, messages, labels, etc
        mat.set_data(self.pmap)
        self.message = 'none'
        self.create_labels()
        self.annotate()
        return [mat]

    def on_keypress(self, event):
        """ changes map to one specified by 
            the key pressed
        """
        if event.key in '01234567':
            self.stop = True
            index = int(event.key)
            self.pmap = map_options[index]
            #get new map and put picobot somewhere
            self.reset(given_map=map_options[index])
            return [mat]
    
    def on_step(self, event):
        """ goes one step forward
        """
        self.message = 'none'
        if event.key == 'n':
            #do next move
            self.picomove()
            self.annotate()
    
    def on_space(self, event):
        """ (un)pauses animation when
            the spacebar is pressed
        """
        if event.key == ' ':
            self.stop = not self.stop
    
    def on_reset(self, event):
        """ resets picobot - sets all visited 
            squares to unvisited, and moves 
            picobot to a nonwall location
        """
        self.message = 'none'
        if event.key == 'r':
            #just call the reset function
            self.reset()
    
    def on_teleport(self, event):
        """ teleports picobot in
            direction suggested, 
            unless there exists a wall
        """
        d = {'up':[0,'N','north'], 'right':[1,'E','east'], 'left':[2,'W','west'], 'down':[3,'S','south']}
        self.message = 'none'
        #update self.surround
        self.getsurr()
        if event.key in d:
            self.unvisit()
            #check if there's a wall and refuse to move if appropriate
            if self.surround[d[event.key][0]] == '0':
                self.message = "wall to the %s\nnot moving robot" % d[event.key][2]
            else: # teleport appropriately
                self.picosubmove(d[event.key][1])
                self.annotate()

# instantiate the class        
picosim = Picobot()

# put picobot somewhere nice
picosim.place_picobot()
#set up rules 
picosim.rules = rule_list 

#set colors to values in picomap
cmap = colors.ListedColormap(['#808080','blue','white','xkcd:electric green'])
bounds = [-1.5, -.5, .5, 1.5, 2.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

#show animation!!
fig, ax = plt.subplots()
#listen for clicks, pauses, map changes, resets
cid = fig.canvas.mpl_connect('button_press_event', picosim.on_click)
cid2 = fig.canvas.mpl_connect('key_press_event', picosim.on_keypress)
cid4 = fig.canvas.mpl_connect('key_press_event', picosim.on_space)
cid5 = fig.canvas.mpl_connect('key_press_event', picosim.on_reset)

#set up plot
mat = ax.matshow(picosim.pmap, cmap=cmap, norm=norm)
#get first picobot state label
annotation = plt.annotate(picosim.picostate, xy=[picosim.j-.6, picosim.i+.4])
#let the show begin!
ani = animation.FuncAnimation(fig, picosim.update, interval=50, save_count=50, blit=False)
plt.show()    