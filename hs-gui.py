#!/usr/bin/python

# HeadSpace HRTF Library
# Graphical Filter Interface

# Author: Christopher Rabl
# Modified: April 22, 2012

import Tkinter

from pyo import *
from headspace import *

s = Server().boot()
s.start()
signal = SfPlayer("testfiles/voice.wav", loop=True)
hsInstance = HeadSpace(signal, 0, 0).out()

root = Tkinter.Tk()
root.wm_title("HeadSpace Controller")

N=Tkinter.N
E=Tkinter.E
S=Tkinter.S
W=Tkinter.W

azimuthLabel = Tkinter.Label(root, text="Azimuth:").grid(row=0, column=0, padx=10, pady=25, sticky=E)
azimuthSlider = Tkinter.Scale(root, from_=-180, to=180, resolution=1, orient=Tkinter.HORIZONTAL, command=hsInstance.setAzimuth, length=200).grid(row=0, column=1, sticky=N, pady=5)

elevationLabel = Tkinter.Label(root, text="Elevation:").grid(row=1, column=0, padx=10, pady=20, sticky=E)
elevationSlider = Tkinter.Scale(root, from_=-40, to=90, resolution=1, orient=Tkinter.HORIZONTAL, command=hsInstance.setElevation, length=200).grid(row=1, column=1, sticky=N)


root.geometry('310x130+250+250')
root.mainloop()
