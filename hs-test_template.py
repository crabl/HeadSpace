from pyo import *
from headspace import *

# Start the PYO server
s = Server().boot()
s.start()

# Make a new HeadSpace UI
ui = HeadSpaceUI("Test")

voiceWav = SfPlayer("testfiles/voice.wav")
voice = HeadSpace(voiceWav, 30, -20).out()
ui.add("Voice", voice)

ui.show()
