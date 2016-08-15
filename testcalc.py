from hsdata import *
from pyo import *

s = Server().boot()

_elev = ["-40", "-30", "-20", "-10", "0", "10", "20", "30", "40", "50", "60", "70", "80", "90"]
_IR_TABLE_LEFT, _IR_TABLE_RIGHT = ImpulseResponseTables().getTables()

def calculateIRTableIndices(azimuth, elevation):
	"""
	calculates impulse response table indices from azimuth and elevation degrees
	"""
	el = int(round(float(elevation), -1)) # round the elevation to the nearest 10
	elStr = str(el)
	elIndex = _elev.index(elStr)
	az = int(round(azimuth * len(_IR_TABLE_LEFT[elIndex])/180.)) # get azimuth based on table vals for given elevation

	# BEGIN MAGIC
	if(azimuth >= 0):
		azIndex = az - 1
	else:
		azIndex = -az - 1
	# END MAGIC

	return [azIndex, elIndex]

print calculateIRTableIndices(10, 50) == [0,9]
print calculateIRTableIndices(100, 75) == [3,12]
print calculateIRTableIndices(-40, 20) == [7,6]
print calculateIRTableIndices(-100, -40) == [15,0]
