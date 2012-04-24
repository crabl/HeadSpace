#!/usr/bin/python

# HeadSpace HRTF Library
# HRTF DSP Object

# Author: Christopher Rabl
# Modified: April 22, 2012

from pyo import *
import glob
import Tkinter

class HeadSpaceHelper:
    def __init__(self):
        self.KEMARDATA = "data/"
        
        self.elev = ["-40", "-30", "-20", "-10", "0", "10", "20", "30", "40", "50", "60", "70", "80", "90"]
        
        # This is really the "least worst" way of doing it... load all filenames into a matrix
        self.elevData_l = [ glob.glob(self.KEMARDATA+"elev-40/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev-30/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev-20/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev-10/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev0/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev10/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev20/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev30/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev40/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev50/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev60/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev70/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev80/left/*.wav"),
                            glob.glob(self.KEMARDATA+"elev90/left/*.wav") ]
        
        self.elevData_r = [ glob.glob(self.KEMARDATA+"elev-40/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev-30/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev-20/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev-10/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev0/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev10/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev20/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev30/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev40/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev50/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev60/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev70/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev80/right/*.wav"),
                            glob.glob(self.KEMARDATA+"elev90/right/*.wav") ]
        
        # As good as GLOB is, it doesn't sort the data...
        for items in self.elevData_l:
            items.sort()
        for items in self.elevData_r:
            items.sort()


    def getImpulse(self, elevation, azimuth):
        el = int(round(float(elevation), -1)) # round the elevation to the nearest 10
        elStr = str(el)
        elIndex = self.elev.index(elStr)
        # BEGIN MAGIC
        azIndex = int(round(azimuth * len(self.elevData_l[elIndex])/180.)) - 1
        if(azimuth >= 0):
            azNeg = False
        else:
            azNeg = True
            azIndex = int(round(-azimuth * len(self.elevData_l[elIndex])/180.)) - 1
        # END MAGIC
        wavLeft = self.elevData_l[elIndex][azIndex]
        wavRight = self.elevData_r[elIndex][azIndex]
        # print wavLeft, wavRight # DEBUG
        if(azNeg):
            return wavRight, wavLeft # return the mirrored values
        return wavLeft, wavRight # return unmirrored values


class HeadSpace:
    def __init__(self, signal, azimuth, elevation):
        self.bufferSize = 128
        self.signal = signal
        self.helper = HeadSpaceHelper()
        
        # Initialize class members so that they aren't destroyed when __init__ ends
        self.azimuth = azimuth
        self.elevation = elevation
        
        # Load the impulse responses into sound tables for each ear
        leftImp, rightImp = self.helper.getImpulse(self.elevation, self.azimuth)
        self.impulse_l = SndTable(leftImp)
        self.impulse_r = SndTable(rightImp)
        
        # Perform convolution on each ear
        self.convolved_l = Convolve(self.signal, self.impulse_l, size=self.bufferSize, mul=.5).out(0)
        self.convolved_r = Convolve(self.signal, self.impulse_r, size=self.bufferSize, mul=.5).out(1)
        
    def swapImpulse(self):
        leftImp, rightImp = self.helper.getImpulse(self.elevation, self.azimuth)
        # Load the new impulses into the tables for each ear (with crossfading)
        self.impulse_l.insert(leftImp, crossfade=0.05) # crossfade 0.05 seconds
        self.impulse_r.insert(rightImp, crossfade=0.05)
        
    def setAzimuth(self, value):
        self.azimuth = int(value)
        # print "Azimuth:", self.azimuth # DEBUG
        self.swapImpulse()

    def setElevation(self, value):
        self.elevation = int(value)
        # print "Elevation", self.elevation # DEBUG
        self.swapImpulse()
        
    def setSignal(self, signal):
        self.signal = signal

class HeadSpaceUI:
    def __init__(self, windowTitle):
        self.root = Tkinter.Tk()
        self.root.wm_title("HeadSpace - "+windowTitle)
        self.hsObjects = {}
    # desc = description string
    # hso = HeadSpace object
    def add(self, desc, hso):
        self.hsObjects[desc] = hso
    def show(self):
        N=Tkinter.N
        E=Tkinter.E
        S=Tkinter.S
        W=Tkinter.W
        rowIndex = 0
        for item in self.hsObjects:
            Tkinter.Label(self.root, text=str(item)).grid(row=rowIndex, column=0, padx=10, pady=5, sticky=E)
            Tkinter.Label(self.root, text="Azimuth:").grid(row=rowIndex, column=1, padx=10, pady=25, sticky=E)
            Tkinter.Scale(self.root, from_=-180, to=180, resolution=1, orient=Tkinter.HORIZONTAL, command=self.hsObjects[item].setAzimuth, length=200).grid(row=rowIndex, column=2, sticky=N, pady=5, padx=10)
            
            Tkinter.Label(self.root, text="Elevation:").grid(row=rowIndex+1, column=1, padx=10, pady=20, sticky=E)
            Tkinter.Scale(self.root, from_=-40, to=90, resolution=1, orient=Tkinter.HORIZONTAL, command=self.hsObjects[item].setElevation, length=200).grid(row=rowIndex+1, column=2, sticky=N, padx=10)
            rowIndex += 2

        self.root.mainloop()
