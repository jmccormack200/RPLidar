import serial
import time

Start_Scan = "\xA5\x20"
Force_Scan = "\xA5\x21"
Health = "\xA5\x52"
Stop_Scan = "\xA5\x25"

def readline(port):
    line = ""
    while True:
        try:
            character = port.read()
            line += character
            
            if (line[0:2] == "\xa5"):
                #if(len(line) == 7):
                print line.encode("hex")
                    
            elif (line[0:2] != "\xa5" and len(line) == 2):
                #print line.encode("hex")
                line = ""
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    output = []


    ser = serial.Serial(10, 115200, timeout = 5, )
    ser.setDTR(False)
    print ser.name
    ser.write(Start_Scan)

    readline(ser)
        
