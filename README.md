# picobot

This repo contains a visualizer, three sets of rules, a set of maps, and a rule compiler. Picobot is the first programming assignment in Harvey Mudd College's CS5 class. The goal is to program Picobot to visit all parts of a given map - but picobot only knows its immediate surroundings and its own 'state'. Previously, Picobot was hosted on a website, where students could enter their rules and then run them. This visualizer was created so that students could test their programs locally. 

## Dependencies

This set of programs (excluding the rules, which are written in Picobot) is written in Python 3, and also requires the matplotlib and numpy libraries.

## How to Run Picobot

In picobot.py, there is a place to add the filename where your rules are written (it should have a default set already there). Then go to a terminal, cd into the directory where this group of files and your rules are saved, and run picobot.py with the command `python3 picobot.py`. To play/unpause, press the spacebar. To reset the map and picobot, press 'r'. To step forward, press 'n' (for 'next'). To change the map, press a number key 1-7. Map 1 is the default map. Map 2 is a maze, map 3 is a diamond, and maps 4 through 7 are increasingly complex to solve. You can teleport picobot by pressing arrow keys.
