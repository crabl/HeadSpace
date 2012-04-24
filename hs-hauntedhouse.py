#!/usr/bin/python

# HeadSpace HRTF Library
# Haunted House Demo

# Author: Christopher Rabl
# Modified: April 24, 2012

from pyo import *
from headspace import *

# Create a PYO server and start it
s = Server().boot()
s.start()

# Create a new UI object
ui = HeadSpaceUI("Haunted House")

backgroundWav = SfPlayer("testfiles/horrorbg.wav", loop=True)
background = HeadSpace(backgroundWav, 0, 0)
ui.add("Background", background)

footstepsWav = SfPlayer("testfiles/footsteps.wav", loop=True)
footsteps = HeadSpace(footstepsWav, 180, -40)
ui.add("Footsteps", footsteps)

owlsWav = SfPlayer("testfiles/owls.wav", loop=True)
owls = HeadSpace(owlsWav, -20, 50)
ui.add("Owls", owls)

skitterWav = SfPlayer("testfiles/skitter.wav", loop=True)
skitter = HeadSpace(skitterWav, 0, 90)
ui.add("Mice", skitter)

screamWav = SfPlayer("testfiles/scream.wav", loop=True)
scream = HeadSpace(screamWav, 50, -30)
ui.add("Scream", scream)

# Don't add this to the UI... we want to scare the user ;-)
laughWav = SfPlayer("testfiles/laugh.wav", loop=True)
laugh = HeadSpace(laughWav, -140, -20)

# Show the UI to the user
ui.show()
