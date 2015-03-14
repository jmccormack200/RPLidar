"""
Combining threadtest2.py with plottest.py to
try to multithread plotting. This will help
prevent the serial data from being slowed down
by the plotting
"""

import threading, time, random
import matplotlib.pyplot as plt
import numpy as np
import time
try:
    import Queue
except:
    import queue as Queue

class Producer:
    def __init__(self):
        self.y = np.random.randn(100)
    
    def run(self):
        global q
        while (True):
            try:
                self.y[:-10] = self.y[10:]
                self.y[-10:] = np.random.randn(10)
                q.put(self.y)
            except KeyboardInterrupt:
                break

class Plotter:
    def __init__(self):
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        
        self.x = np.arange(100)
        y = np.random.randn(100)
        self.li,= ax.plot(self.x,y)        
        self.fig.canvas.draw()
        plt.show(block=False)
        
    def run(self):
        global q
        while (True):
            try:
                if (not (q.empty())):
                    y = q.get()
                    self.li.set_ydata(y)
                    self.fig.canvas.draw()
                    time.sleep(0.05)
            except KeyboardInterrupt:
                print "Sorry to see you go"
                break

if __name__ == '__main__':
    q = Queue.Queue(10)
    
    pr = Producer()
    pl = Plotter()
    pt = threading.Thread(target=pr.run, args=())
    ptl = threading.Thread(target=pl.run, args=())
    pt.start()
    ptl.start()
            

