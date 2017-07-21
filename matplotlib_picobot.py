import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import AnchoredText
from matplotlib import colors
from random import choice

from maps import *

def get_rules(filename):
    f = open(filename)
    lines = f.readlines()
    rules_list = []
    for line in lines:
        if line[0] in '0123456789':
            line = line.rstrip()
            rules_list += [line]
    f.close()
    return rules_list

##############################################################
##############################################################
#insert here the name of the file where your rules are written
rule_list = get_rules('hw0pr3.txt') 
# how to interact:
#   spacebar: pause/play
#   r: resets map/picobot
#   n: steps ("next")
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
        if self.isFinished() or self.stop:
            cid3 = fig.canvas.mpl_connect('key_press_event', self.on_step)
            cid5 = fig.canvas.mpl_connect('key_press_event', self.on_reset)
            cid6 = fig.canvas.mpl_connect('key_press_event', self.on_teleport)
            self.getsurr()
            self.create_labels()
            mat.set_data(self.pmap)
            return [mat]
        else:
            self.message = 'none'
            self.picomove()
            self.annotate()
            return [mat]
    
    def picomove(self):
        for rule in self.rules:
            self.currentrule = rule
            if self.picostate != rule[:2]:
                continue

            self.getsurr()
            if not self.checksurr():
                continue
            
            else:
                self.pmap[self.i, self.j] = -1
                self.picosubmove(self.currentrule[6])
                self.picostate = rule[7:]
                mat.set_data(self.pmap)
                self.create_labels()
                return [mat]
        
        self.stop = True
        self.message = "no rule applies \nstopping..."
        self.create_labels()

    def picosubmove(self, direction):
        """ updates picobot's coordinates based on
            direction specified (unless there is a wall)
        """    
        d = {'N':0, 'E':1, 'W':2, 'S':3}
        d2 = {'N':'north', 'E':'east', 'W':'west', 'S':'south'}
        if direction in 'xX':
            self.pmap[self.i, self.j] = 2
            pass
        else:
            index = d[direction]
            if self.surround[index] == '0':
                self.stop = True
                self.pmap[self.i, self.j] = 2
                self.message = "can't move %s \nstopping..." % d2[direction]
                self.create_labels()
            elif direction not in 'NEWS':
                self.stop = True
                raise Exception('direction not understood')
            else:
                if direction == 'N':
                    self.i -= 1
                elif direction == 'E':
                    self.j += 1
                elif direction == 'W':
                    self.j -= 1
                else:
                    self.i += 1
                self.pmap[self.i, self.j] = 2
    
    def getsurr(self):
        """ returns surroundings of picobot in 
            NEWS form, with 1 == open and 0 == wall
        """
        out = ''
        if self.i == 0: out += '0'
        else: out += str(self.pmap[self.i-1, self.j]%2)
        try: out += str(self.pmap[self.i, self.j+1]%2)
        except: out += '0'
        if j == 0: out += '0'
        else: out += str(self.pmap[self.i, self.j-1]%2)
        try: out += str(self.pmap[self.i+1, self.j]%2)
        except: out += '0'
        
        self.surround = out

    def isFinished(self):
        """ returns False if there are still 
            (nonwall) squares picobot has not 
            visited; returns True otherwise
        """
        grid = self.pmap.tolist()
        for k in range(len(grid)):
            for l in range(len(grid[k])):
                if grid[k][l] == 1:
                    return False
        self.message = "map complete!"
        return True
    
    def checksurr(self):
        """ returns True if the current surroundings
            match those specified in a given rule;
            returns False otherwise
        """
        rule = self.currentrule
        for k in range(4):
            if rule[k+2] + self.surround[k] == '01' or rule[k+2] + self.surround[k] == '10':
                return False
        return True
    
    def reset(self, given_map=None):
        """ resets board
        """
        self.stop = True
        self.unvisit()
        self.picostate = '00'
        if type(given_map) == type(None):
            self.pmap[self.i, self.j] = 1
        else:
            self.pmap[self.i, self.j] = given_map[self.i, self.j]
        
        self.place_picobot()
        self.pmap[self.i, self.j] = 2
        mat.set_data(self.pmap)
        self.message = 'none'
        self.create_labels()
        self.annotate()

        return [mat]

    def unvisit(self):
        """ resets all visited cells
            to unvisited state
        """
        grid = self.pmap.tolist()
        for k in range(len(grid)):
            for l in range(len(grid[k])):
                if grid[k][l] != 0:
                    grid[k][l] = 1
        self.pmap = np.array(grid)
    
    def countUnvisited(self):
        """ returns number of
            unvisited cells
        """
        grid = self.pmap.tolist()
        count = 0
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
        anchored_label = AnchoredText(s=text, loc=2, pad=.3, bbox_to_anchor=location, bbox_transform=ax.transAxes,)
        return anchored_label
    
    def create_labels(self):
        """ creates labels for state, 
            surroundings, remaining cells,
            and current rule
        """
        for label in self.labels:
              label.remove()
        
        state_label = self.make_label("State: %s" % self.picostate, (1,1))
        surr_label = self.make_label("Surroundings: %s" % self.surr_deconverter(self.surround), (.6,0))
        cells_label = self.make_label("Cells to go: %s" % str(self.countUnvisited()), (1, .8))
        rule_label = self.make_label("Current rule: %s" % self.rule_deconverter(self.currentrule), (0,0))
        message_label = self.make_label("Messages: \n%s" % self.message, (1, .6))
        
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
            out += rule[:2]
            out += ' '
            for i in range(4):
                if rule[i+2] == '*':
                    out += rule[i+2]
                elif rule[i+2] == '0':
                    out += d[i]
                elif rule[i+2] == '1':
                    out += 'X'
            out += ' -> '
            out += rule[6]
            out += ' '
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
        self.unvisit()
        self.pmap[self.i, self.j] = 2
        col = int(np.round(event.xdata))
        row = int(np.round(event.ydata))
        if self.pmap[row,col] == 0:
            self.pmap[row,col] = 1
        else:
            self.pmap[row,col] = 0
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
            self.reset(given_map=map_options[index])
            return [mat]
    
    def on_step(self, event):
        """ goes one step forward
        """
        self.message = 'none'
        if event.key == 'n':
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
            self.reset()
    
    def on_teleport(self, event):
        """ teleports picobot in
            direction suggested, 
            unless there exists a wall
        """
        self.message = 'none'
        self.getsurr()
        d = {'up':[0,'N','north'], 'right':[1,'E','east'], 'left':[2,'W','west'], 'down':[3,'S','south']}
        if event.key in d:
            if self.surround[d[event.key][0]] == '0':
                self.message = "wall to the %s\nnot moving robot" % d[event.key][2]
            else:
                self.unvisit()
                self.picosubmove(d[event.key][1])
                self.annotate()
        
picosim = Picobot()

def rule_converter(rule):
    """ converts old-style rules 
        into nine character string 
        used by matplotlib program
    """
    out = ''
    rule = rule.split(' ')
    state = '0'*(2-len(rule[0])) + rule[0]
    out += state
    surr = ''
    for i in range(4):
        if rule[1][i] == '*':
            surr += rule[1][i]
        elif rule[1][i] in 'xX':
            surr += '1'
        elif rule[1][i] in 'NEWS':
            surr += '0'
        else:
            raise Exception("surrounding not recognized")
    out += surr
    out += rule[3]
    newstate = '0'*(2-len(rule[4])) + rule[4]
    out += newstate
    return out


picosim.place_picobot()
picosim.rules = [rule_converter(rule) for rule in rule_list]

#set colors to values in picomap
cmap = colors.ListedColormap(['#808080','blue','white','xkcd:electric green'])
bounds = [-1.5, -.5, .5, 1.5, 2.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

#show animation!!
fig, ax = plt.subplots()

cid = fig.canvas.mpl_connect('button_press_event', picosim.on_click)
cid2 = fig.canvas.mpl_connect('key_press_event', picosim.on_keypress)
cid4 = fig.canvas.mpl_connect('key_press_event', picosim.on_space)
cid5 = fig.canvas.mpl_connect('key_press_event', picosim.on_reset)


mat = ax.matshow(picosim.pmap, cmap=cmap, norm=norm)
annotation = plt.annotate(picosim.picostate, xy=[picosim.j-.6, picosim.i+.4])
ani = animation.FuncAnimation(fig, picosim.update, interval=50, save_count=50, blit=False)
plt.show()    