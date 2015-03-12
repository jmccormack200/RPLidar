"""
This code is copied from a stack overflow post:
http://stackoverflow.com/questions/24783530/python-real-time-plotting
I will need to plot the lidar data in real time and wanted
to experiment with plotting it first. 
Hopefully I can use this with threading.
"""

import matplotlib.pyplot as plt
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot(111)

x = np.arange(10000)
y = np.random.randn(10000)

li,= ax.plot(x,y)

fig.canvas.draw()
plt.show(block=False)

while True:
    try:
        y[:-10] = y[10:]
        y[-10:] = np.random.randn(10)
        
        li.set_ydata(y)
        
        fig.canvas.draw()
        
        time.sleep(0.01)
    except KeyboardInterrupt:
        break