#!/usr/bin/python

# makehs.py (hsdata.py generator)
# Bryan Smart 5/15/2012

# This script is a quick and dirty hack to convert the library of
# HRTF impulse responses from individual WAV files in to a Python
# script so that they can be quickly loaded w/o taking the
# performance hit from accessing lots of small files.

import glob
import time

import pyo

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
        
        ### Init lists of SndTable objects ###
        self.elevData_l_tables = []
        self.elevData_r_tables = []
        # As good as GLOB is, it doesn't sort the data...
        for items in self.elevData_l:
            self.elevData_l_tables.append([])
            items.sort()
            for item in items:
                self.elevData_l_tables[-1].append(pyo.SndTable(item))
        for items in self.elevData_r:
            self.elevData_r_tables.append([])
            items.sort()
            for item in items:
                self.elevData_r_tables[-1].append(pyo.SndTable(item))

# Startup
s = pyo.Server().boot()
s.start()

print "Loading tables..."
h = HeadSpaceHelper()

print "Writing hsdata.py..."
f = open("hsdata.py", "w")

f.write("# HRTF impulse responses for HeadSpace, an HRTF effect for Pyo.\n")
f.write("# This file was automatically generated on " + time.asctime() + "\n\n")
f.write("from pyo import *\n\n")

f.write("class ImpulseResponseTables:\n\n")

f.write("\tdef getTables(self):\n")

f.write("\t\tIR_TABLE_LEFT = []\n\n")

for elevation in h.elevData_l_tables:
	f.write ("\t\tIR_TABLE_LEFT.append([])\n\n")

	for azimuth in elevation:
		f.write("\t\tIR_TABLE_LEFT[len(IR_TABLE_LEFT)-1].append(DataTable(128, init=")
		f.write(str(azimuth[0].getTable()))
		f.write("))\n\n")

f.write("\t\tIR_TABLE_RIGHT = []\n\n")

for elevation in h.elevData_r_tables:
	f.write ("\t\tIR_TABLE_RIGHT.append([])\n\n")

	for azimuth in elevation:
		f.write("\t\tIR_TABLE_RIGHT[len(IR_TABLE_RIGHT)-1].append(DataTable(128, init=")
		f.write(str(azimuth[0].getTable()))
		f.write("))\n\n")

f.write("\t\treturn IR_TABLE_LEFT, IR_TABLE_RIGHT\n\n")

f.close()

print "Done."
