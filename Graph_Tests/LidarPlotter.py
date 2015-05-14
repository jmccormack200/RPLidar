import serial
import time
import math
from time import sleep
import threading, random
import numpy as np
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
    line = ""
    lock = False
    port.write(RESET)
    sleep(4)
    port.write(Start_Scan)
    while True:
        try:
            character = port.read()
            line += character
            if (line[0:2] == "\xa5\x5a"):
                if(len(line) == 7):
                    lock = True
                    print line.encode("hex")
                    break
                
            elif (line[0:2] != "\xa5\x5a" and len(line) == 2):
                print line.encode("hex")
                line = ""
        except KeyboardInterrupt:
            break
        except:
            pass
    print (line.encode("hex"))
    #getPoints(port)
    if lock == True:
        print "Made it here"
        thread1 = threading.Thread(target=getPoints, args=(port,))
        thread2 = threading.Thread(target=graph, args=())
        thread1.start()
        thread2.start()
    else:
        print "Exiting"

def getPoints(port):
    line = ""
    a = 0
    global q
    while True:
        try:
            character = port.read()
            line += character
            
            if (len(line) == 5):
                q.put(point_Polar(line))
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
    #theta = (angle * np.pi) / 180 #uncomment to use radians
    
    #return(distance,theta) #uncomment to return radians
    return(distance, angle)
    
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
        except KeyboardInterrupt:
            print "Sorry to see you go"
            break
            
if __name__ == "__main__":
    
    q = Queue.Queue(0)

    ser = serial.Serial(3, 115200, timeout = 5)
    ser.setDTR(False)
    print ser.name
    getResponseDescriptor(ser)