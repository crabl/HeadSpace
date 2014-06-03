#!/usr/bin/python
"""
Head-related transfer function for approximating three dimensional
sound placement.
"""
# HeadSpace HRTF Library
# HRTF DSP Object

# Authors: Christopher Rabl and Bryan Smart
# Modified: May 15, 2012

import glob
#import Tkinter
from pyo import *
from hsdata import *

_elev = ["-40", "-30", "-20", "-10", "0", "10", "20", "30", "40", "50", "60", "70", "80", "90"]
_IR_TABLE_LEFT = None
_IR_TABLE_RIGHT = None

class HeadSpace(PyoObject):
    """
	head-related transfer function effect
    
	HeadSpace approximates binaural audio source positioning. When the
	output streams are played through headphones, the sound produced by
	the input signal will seem to originate from a three dimentional
	position relative to the listener.
    
    
	Parent class: PyoObject
    
	Parameters:
    
	signal : PyoObject
		The source audio signal that will be positioned relative to
		the listener.
	azimuth : int, optional
		The azimuth of the signal relative to the listener, between -180
		and 180. Default is 0.
	elevation : int, optional
		The elevation of the signal relative to the listener, between -40
		to 90. Default is 0.
    
	Methods:
    
	setSignal (x) : Replace the signal attribute.
	setAzimuth (x) : Replace the azimuth attribute.
	setElevation (x) : Replace the elevation attribute.
    
	Attributes:
    
	signal : PyoObject. The audio source that will be binaurally
		positioned in this object's output stream.
	azimuth : float. The relative angle between the input signal and the
		listener.
	elevation : The relative altitude of the input signal to the
		listener.
    
	"""
    
    def __dir__ (self):
        return ["input", "azimuth", "elevation", "mul", "add"]
    
    def __init__(self, input, azimuth=0, elevation=0, mul=1, add=0):
        PyoObject.__init__(self)
        self._input = input
        self._azimuth = azimuth
        self._elevation = elevation
        self._mul = mul
        self._add = add
        
        self._buffer_size = 128
        
		# Load impulse response tables if not already.
        global _IR_TABLE_LEFT, _IR_TABLE_RIGHT
        if not (_IR_TABLE_LEFT or _IR_TABLE_RIGHT):
            # Tables are loaded globally so that they can be cached for future instances.
            _IR_TABLE_LEFT, _IR_TABLE_RIGHT = ImpulseResponseTables().getTables()
            
        # Convert arguments to lists that are capable of accepting multiple values.
        mul, add, lmax = convertArgsToLists(mul, add)
            
        self._input_fader = InputFader(input)
        
        leftImp, rightImp = self.getImpulses()
        
        self._outs = []
        self._outs.append(Convolve(self._input_fader, leftImp, size=self._buffer_size, mul=wrap(mul,0), add=wrap(add,0)))
        self._outs.append(Convolve(self._input_fader, rightImp, size=self._buffer_size, mul=wrap(mul,1), add=wrap(add,1)))
        
        self._base_objs = []
        self._base_objs.extend(self._outs[0].getBaseObjects())
        self._base_objs.extend(self._outs[1].getBaseObjects())
            
    def play(self, dur=0, delay=0):
        dur, delay, lmax = convertArgsToLists(dur, delay)
        
        [obj.play(wrap(dur, i), wrap(delay, i)) 
         for i, obj in enumerate(self._outs)]
        
        self._base_objs = [obj.play(wrap(dur, i), wrap(delay, i)) 
                           for i, obj in enumerate(self._base_objs)]
        
        return PyoObject.play(self, dur, delay)
    
    def stop(self):
        [obj.stop() for obj in self._outs]
        [obj.stop() for obj in self._base_objs]
        return PyoObject.stop(self)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        dur, delay, lmax = convertArgsToLists(dur, delay)
        
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._outs)]
        
        if type(chnl) == ListType:
            self._base_objs = [obj.out(chnl=wrap(chnl,i), dur=wrap(dur,i), delay=wrap(delay,i)) 
                               for i, obj in enumerate(self._base_objs)]
        else:
            if chnl < 0:
                self._base_objs = [obj.out(i*inc, dur=wrap(dur,i), delay=wrap(delay,i)) 
                                   for i, obj in enumerate(random.sample(self._base_objs, len(self._base_objs)))]
            else:
                self._base_objs = [obj.out(chnl=(chnl+i*inc), dur=(wrap(dur,i)), delay=(wrap(delay,i))) 
                                   for i, obj in enumerate(self._base_objs)]    
        return PyoObject.out(self, chnl, inc, dur, delay)

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(-180, 180, "lin", "Azimuth", self._azimuth),
                      SLMap(-40, 90, "lin", "Elevation", self._elevation),
                      SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    def __dir__(self):
        return ["input", "azimuth", "elevation", "mul", "add"]
    
    def getImpulses(self):
        el = int(round(float(self._elevation), -1)) # round the elevation to the nearest 10
        elStr = str(el)
        elIndex = _elev.index(elStr)
       	# BEGIN MAGIC
        azIndex = int(round(self._azimuth * len(_IR_TABLE_LEFT[elIndex])/180.)) - 1
        if(self._azimuth >= 0):
            azNeg = False
        else:
            azNeg = True
            azIndex = int(round(-self._azimuth * len(_IR_TABLE_LEFT[elIndex])/180.)) - 1
        # END MAGIC
            
        wavLeft = _IR_TABLE_LEFT[elIndex][azIndex]
        wavRight = _IR_TABLE_RIGHT[elIndex][azIndex]
        
        if(azNeg):
            return wavRight, wavLeft # Mirror impulses
        
        return wavLeft, wavRight
    
    def swapImpulse(self):
        leftImp, rightImp = self.getImpulses()
        self._outs[0].setTable(leftImp)
        self._outs[1].setTable(rightImp)

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        Parameters:
        
        x : PyoObject
        New input signal to process.
        fadetime : float, optional
        Crossfade time between old and new input. Defaults to 0.05.
        
        """
        
        self._input = x
        self._input_fader.setInput(x, fadetime)
    
    def setAzimuth(self, x):
        """
        Replace the `azimuth` attribute.
        
        Parameters:
        
        x : int
        Azimuth of the input signal relative to the listener.
        
        """
        
        self._azimuth = int(x)
        self.swapImpulse()
    
    def setElevation(self, x):
        """
        Replace the `elevation` attribute.
        
        Parameters:
        
        x : int
        The elevation of the input signal relative to the listener,
        between -40 and 90.
        
        """
        
        self._elevation = int(x)
        self.swapImpulse()
    
    @property
    def input(self): return self._input
    @input.setter
    def input(self, x): self.setInput(x)
    
    @property
    def azimuth(self): return self._azimuth
    @azimuth.setter
    def azimuth(self, x): self.setAzimuth(x)
    
    @property
    def elevation(self): return self._elevation
    @elevation.setter
    def elevation(self, x): self.setElevation(x)

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
