#! /usr/bin/python3

#generates the game of life as defined by Conway

import numpy as np
import matplotlib.pylab as plt
from sys import argv
from os.path import isfile
from datetime import datetime
 
EVOLVE_WITH_C = True #set True for evolving using the C precompiled function, False uses Python instead (much slower)

if not EVOLVE_WITH_C:
	from scipy.signal import convolve2d
	neighbours_layer = np.array( [[1,1,1],[1,0,1],[1,1,1]], dtype=int)
	def evolve( array):
		neighbours_count = convolve2d( array, neighbours_layer, mode="same", boundary="wrap")
		return (neighbours_count == 3) | (array & (neighbours_count == 2))

else:
	import ctypes
	evolve_lib = ctypes.cdll.LoadLibrary("./gameoflife_evolve.so")
	evolve = evolve_lib.evolve


if len(argv) > 1: #size or file with stored configuration is passed as argument
	try:
		SIZE = int( argv[1])
		conf = np.random.rand( SIZE*SIZE) > .8 #80-20 rule, we want ~80% empty pixels at start
	except ValueError:
		if isfile( argv[1]):
			conf = np.load( isfile)
			SIZE = len(conf)
		else:
			raise Exception("Missing input file")
else:
	SIZE = 200
	conf = np.random.rand( SIZE*SIZE) > .8



#conf = np.random.choice( (0,1), size=(SIZE,SIZE)).astype(int)
if not EVOLVE_WITH_C:
	conf = conf.reshape( SIZE,SIZE)
else:
	conf = conf.astype(np.int32)
	conf_pointer = conf.ctypes.data_as( ctypes.POINTER(ctypes.c_int32))

fig = plt.figure( figsize=(12,12))
ax = fig.gca()
fig.tight_layout(pad=0)
ax.set_xticks(())
ax.set_yticks(())
onPause = False

#add keyboard shortcuts for pausing and exporting configuration
def onKeyPress( event):
	if event.key == " ":
		global onPause
		onPause = not onPause
	elif event.key == "e":
		output_filename = "conf_%s" % datetime.now().strftime("%Y%m%d%H%M%S")
		np.save( output_filename, conf)
		print( "Configuration exported to %s ..." % output_filename)
fig.canvas.mpl_connect( "key_press_event", onKeyPress)

colormap = "Greys"
image = ax.imshow(conf.reshape(SIZE,SIZE) if EVOLVE_WITH_C else conf, cmap=colormap)
step = 0
DrawTimeStep = True
if DrawTimeStep:
	text = ax.text(0.02, 0.98, step, va="top", ha="left", transform=ax.transAxes, color="red", fontsize=20, bbox={'facecolor':'.95', "boxstyle":"round,pad=0.25"})

while True:
	image.set_data( conf.reshape(SIZE,SIZE) if EVOLVE_WITH_C else conf)
	if DrawTimeStep:
		text.set_text( step)
	if not onPause:
		plt.pause( 0.05)
		if EVOLVE_WITH_C:
			evolve(conf_pointer, SIZE)
		else:
			conf = evolve(conf)
		step += 1
	else:
		plt.pause( 0.1)
	if not np.any( conf):
		break
