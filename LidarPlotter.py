import serial
import time
import math
from time import sleep

import threading, random
import matplotlib.pyplot as plt
import numpy as np
import time
try:
    import Queue
except:
    import queue as Queue


Start_Scan = "\xA5\x20"
Force_Scan = "\xA5\x21"
Health = "\xA5\x52"
Stop_Scan = "\xA5\x25"
RESET = "\xA5\x40"

def getResponseDescriptor(port):
    print "1"
    line = ""
    while True:
        try:
            character = port.read()
            line += character
            if (line[0:2] == "\xa5\x5a"):
                if(len(line) == 7):
                    break
            elif (line[0] != "\xa5"):
                line = ""
        except KeyboardInterrupt:
            break
        except:
            pass
    print (line.encode("hex"))
    #getPoints(port)
    thread1 = threading.Thread(target=getPoints, args=(port,))
    thread2 = threading.Thread(target=graph, args=())
    thread1.start()
    thread2.start()
    

def getPoints(port):
    line = ""
    a = 0
    global q
    while True:
        try:
            character = port.read()
            line += character
            
            if (len(line) == 5):
                q.put(point_XY(line))
                line = ""
                
        except KeyboardInterrupt:
            break
    
def leftshiftbits(line):
    line = int(line, 16)
    line = bin(line)
    line = line[:2] + "0" + line[2:-1]
    line = int(line, 2) #convert to integer
    return line
    
def point_Polar(serial_frame):
    #Get Distance
    distance = serial_frame[4].encode("hex") + serial_frame[3].encode("hex")
    distance = int(distance, 16)
    distance = distance / 4 #instructions from data sheet
    #Get Angle
    angle = serial_frame[2].encode("hex") + serial_frame[1].encode("hex")
    angle = leftshiftbits(angle) #remove check bit, convert to integer
    angle = angle/64 #instruction from data sheet

    
    return(distance,angle)
    
def point_XY(serial_frame):
    circular_coordinates = point_Polar(serial_frame)
    distance = circular_coordinates[0]
    angle = circular_coordinates[1]
    
    #Get X
    x = distance * math.cos(angle)
    
    #Get Y
    y = distance * math.sin(angle)
    return (x,y)

def graph():
    global q    
    while True:
        try:
            if (not (q.empty())):
                point = q.get()
                print point
                print "\n"
                
        except KeyboardInterrupt:
            print "Sorry to see you go"
            break 
"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.arange(10000)
    y = np.arange(10000)
    li,= ax.plot(x,y)
    fig.canvas.draw()
    plt.show(block=False)
    
    global q
    while True:
        try:
            if (not (q.empty())):
                point_xy = q.get()
                self.li.set_ydata(point_xy[1])
                self.li.set_xdata(point_xy[0])
                self.fig.canvas.draw()
                time.sleep(0.05)
        except KeyboardInterrupt:
            print "Sorry to see you go"
            break
    """
    
if __name__ == "__main__":
    
    q = Queue.Queue(0)

    ser = serial.Serial(10, 115200, timeout = 5)
    ser.setDTR(False)
    print ser.name
    
    ser.write(RESET)
    sleep(4)
    ser.write(Start_Scan)
    getResponseDescriptor(ser)
    
    #thread1 = threading.Thread(target=getPoints, args=(ser,))
    #thread2 = threading.Thread(target=graph, args=())
    #thread1.start()
    #thread2.start()

    
        
#C:\Users\johnmccormack2307\Lidar