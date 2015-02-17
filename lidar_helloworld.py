import serial
import time

Start_Scan = "\xA5\x20"
Force_Scan = "\xA5\x21"
Health = "\xA5\x52"
Stop_Scan = "\xA5\x25"

output = []


ser = serial.Serial(10, 115200, timeout = 5, )
print ser.name
for a in range(2500):
    ser.write(Start_Scan)
    s = ser.read(7)
    output.append(s)
    
for a in output:
    print a.encode("hex")
