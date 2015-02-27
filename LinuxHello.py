import serial
import time

Start_Scan = "\xA5\x20"
Force_Scan = "\xA5\x21"
Health = "\xA5\x52"
Stop_Scan = "\xA5\x25"

output = []


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 5, )
ser.setDTR(False)
print ser.name
ser.write(Start_Scan)

for a in range(100):
    s = ser.read(7)
    print s.encode("hex")
    
