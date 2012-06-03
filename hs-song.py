
from pyo import *
from headspace import *

s = Server().boot()
s.start()

ui = HeadSpaceUI("Test")

song = SfPlayer("testfiles/carelesswhisper.wav", loop=True)
song_hs = HeadSpace(song, 30, 40).out()

ui.add("Song", song_hs)
ui.show()
