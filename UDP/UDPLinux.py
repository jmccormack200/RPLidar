import serial
import time
import math
from time import sleep
import threading, random,sys
import numpy as np 
import requests,json
import socket

###############################
#
#  UDPLidar
#
#  By: John McCormack
#  www.jdmccormack.com
#  
#  A simple class for interfacing to the 
#  Robopeak RPLidar using Python.
#  
#  Built for Windows, sends data out over
#  a UDP stream. 
#
#  For this to work, you need either a
#  valid cross domain xml file or to 
#  use the built in Unity SocketPolicyServer
#  found in C:\Program Files\Unity\Editor
#             \Data\Tools
#  
#
################################


###############################
#
#  Below fields are from the 
#  RPLidar Data Sheets
#
################################
Start_Scan = "\xA5\x20" #Begins scanning
Force_Scan = "\xA5\x21" #Overrides anything preventing a scan
Health = "\xA5\x52" #Returns the state of the Lidar
Stop_Scan = "\xA5\x25" #Stops the scan
RESET = "\xA5\x40" #Resets the device

###############################
#
#  Class Lidar
#
#  Inputs: Port to connect to
#
#  Init will call all necessary
#  functions to start printing.
#
################################
class Lidar():

    def __init__(self,port,id=1):
        #set the port as an instance variable
        self.id = id
        self.port = port
        #lock checks if the connection is made
        lock = False 

        while(True):
            try:
                #Begin by starting the scan
                lock = self.startScan(self.port)

                #Once scan is started, beging printing data
                if lock == True:
                    self.getPoints(self.port)
                else:
                    print "Exiting"
            except KeyboardInterrupt:
                break
###############################
#
#  Start Scan
# 
#  Method connects and starts
#  the Lidar
#
#  Inputs: Port to scan from
#
#  Outputs: true once lock is 
#  acquired. 
#
################################
    def startScan(self, port):
        print "Connecting"
        line = ""
        #Lock is true once connected
        lock = False
        #Continue looping until connected
        while lock == False:
            print "..."
            # First reset the port
            port.write(RESET)
            # Wait
            sleep(2)
            #Start reading
            #Look for the correct start
            #frame of A55A
            port.write(Start_Scan)
            try:
                #If after looping nothing found,
                #Reset and try again
                for a in range(0, 250):
                    character = port.read()
                    line += character
                    if (line[0:2] == "\xa5\x5a"):
                        if(len(line) == 7):
                            lock = True
                            break
                        
                    elif (line[0:2] != "\xa5\x5a" and len(line) == 2):
                        line = ""
            except KeyboardInterrupt:
                break
        return lock

###############################
#
#  Get Points
#
#  Inputs: Port to scan
#  Polar - if true, print polar
#          coordinates, otherwise
#          print rectangular
#
#  Ouput: Prints the recieved data
#
#  Generally this will be the method
#  You want to edit to pipe the data
#  someplace else. 
#
################################

    def getPoints(self,port,polar=True):
        UDP_IP = "192.168.0.112"
        UDP_PORT = 8051

        line = ""
        print("Transmitting on : " + str(UDP_IP) + ":" + str(UDP_PORT))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            try:
                character = port.read()
                line += character
                #Data comes in 5 byte blocks
                if (len(line) == 5):
                    #Switches based on desired output
                    if polar == True:
                        point = self.point_Polar(line)
                        packet = str((self.id, point))
                    	if (point[1] >= 14000):
                    	    break
                        #If having issues, uncomment below line to see what is being sent
			#if (point[0] > 230 and point[0] < 275):
			#print packet
                    else:
                        packet = str((self.id, self.point_XY(line)))

                    sock.sendto(packet, (UDP_IP, UDP_PORT))
                    line = ""
                    
            except KeyboardInterrupt:
                break

###############################
#
# Left Shift Bits
#
# This method is used to properly
# organize the recorded data. 
# Based off of the Application
# notes. 
# 
# Input is the serial frame
# output is the data formated
# properly. 
#
################################
        
    def leftshiftbits(self,line):
        line = int(line, 16)
        line = bin(line)
        line = line[:2] + "0" + line[2:-1]
        line = int(line, 2) #convert to integer
        return line
###############################
#
# Point Polar
#
# This converts the serial frame
# into human readable format. 
#
# All information is based on the
# RPLidar data sheet.
#
# Serial Frame = the line of data
# If radians is false it will print
# in degrees. 
#
################################
    def point_Polar(self,serial_frame,radians=False):
        #Get Distance
        distance = serial_frame[4].encode("hex") + serial_frame[3].encode("hex")
        distance = int(distance, 16)
        distance = distance / 4 #instructions from data sheet
        #Get Angle
        angle = serial_frame[2].encode("hex") + serial_frame[1].encode("hex")
        angle = self.leftshiftbits(angle) #remove check bit, convert to integer
        angle = angle/64 #instruction from data sheet

        if radians == True:
            theta = (angle * np.pi) / 180 #uncomment to use radians
        
            return(theta,distance) #uncomment to return radians

        else:
            return(angle, distance)
###############################
#
# point XY
#
# Converts the polar value into X
# and Y values based on Trigonometry
#
# Inputs - one frame of serial data
# Outputs - The X, Y coordinate. 
#
################################        
    def point_XY(self,serial_frame):
        circular_coordinates = self.point_Polar(serial_frame)
        distance = circular_coordinates[1]
        angle = circular_coordinates[0]
        
        #Get X
        x = distance * math.cos(angle)
        
        #Get Y
        y = distance * math.sin(angle)
        return (x,y)



if __name__ == "__main__":
    #COM21 was used on my computer, this will change based on
    #your setup and whether you're on Windows/Mac/Linux
    port = "/dev/ttyUSB0"
    ser = serial.Serial(port, 115200, timeout = 5)
    ser.setDTR(False)
    print ser.name

    #Create a Lidar instance, this will immidiately start printing.
    #To edit where the data is sent, edit the GetPoints Method
    lidar = Lidar(ser)
