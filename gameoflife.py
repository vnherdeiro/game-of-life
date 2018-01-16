#! /usr/bin/python3

#generates the game of life as defined by Conway

import numpy as np
import matplotlib.pylab as plt
from sys import argv
 
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


SIZE = int( argv[1]) if len(argv) > 1 else 200
#conf = np.random.choice( (0,1), size=(SIZE,SIZE)).astype(int)
conf = np.random.rand( SIZE*SIZE) > .9
if not EVOLVE_WITH_C:
	conf = conf.reshape( SIZE,SIZE)
else:
	conf = conf.astype(np.int32)
	conf_pointer = conf.ctypes.data_as( ctypes.POINTER(ctypes.c_int32))

fig = plt.figure( figsize=(12,12))
ax = plt.gca()
plt.tight_layout(pad=0)
ax.set_xticks(())
ax.set_yticks(())
plt.ion()
colormap = "Greys"
image = ax.imshow(conf.reshape(SIZE,SIZE) if EVOLVE_WITH_C else conf, cmap=colormap)
step = 0
DrawTimeStep = True

def onKeyPress( event):
	if event.key == "e":
		print( "e pressed")
	elif event.key == " ":
		print( "space pressed")

fig.canvas.mpl_connect( "key_pressed_event", onKeyPress)

if DrawTimeStep:
	text = ax.text(0.02, 0.98, step, va="top", ha="left", transform=ax.transAxes, color="red", fontsize=20)
while True:
	image.set_data( conf.reshape(SIZE,SIZE) if EVOLVE_WITH_C else conf)
	if DrawTimeStep:
		text.set_text( step)
	plt.pause(0.1)
	if EVOLVE_WITH_C:
		evolve(conf_pointer, SIZE)
	else:
		conf = evolve(conf)
	step += 1
	if not np.any( conf):
		break
