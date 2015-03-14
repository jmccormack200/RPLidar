import serial
import time
import math
from time import sleep

Start_Scan = "\xA5\x20"
Force_Scan = "\xA5\x21"
Health = "\xA5\x52"
Stop_Scan = "\xA5\x25"
RESET = "\xA5\x40"

def getResponseDescriptor(port):
    line = ""
    
    while True:
        try:
            character = port.read()
            line += character
            
            if (line[0:2] == "\xa5\x5a"):
                if(len(line) == 7):
                    print (line.encode("hex"))
                    getPoints(port)
                    line = ""
                    
            elif (line[0] != "\xa5"):
                line = ""
        except KeyboardInterrupt:
            break
        except:
            pass

def getPoints(port):
    line = ""
    testoutput = []
    a = 0
    while True
        try:
            character = port.read()
            line += character
            
            if (len(line) == 5):
                #print point_Polar(line)
                #line = line.encode("hex")
                #print line
                testoutput.append(point_XY(line))
                line = ""
                a += 1

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

def graph(output):
    pass
    
if __name__ == "__main__":
    output = []


    ser = serial.Serial(10, 115200, timeout = 5, )
    ser.setDTR(False)
    print ser.name
    ser.write(RESET)
    sleep(4)
    ser.write(Start_Scan)

    getResponseDescriptor(ser)
        
