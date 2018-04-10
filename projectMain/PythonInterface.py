import serial		#-Install this module first-
import time

#ser = serial.Serial('/dev/ttyACM0', 9600)	#TI-MSP432 - Linus
#ser = serial.Serial('/dev/ttyUSB0', 9600)	#Arduino clone - Linux
control = serial.Serial('COM3', 115200)	#TI-MSP432 - Windows
#debug = serial.Serial('COM4', 9600)	#TI-MSP432 - Windows

markerbegin = 536870912
control.write("m"+str(markerbegin)+";")
print control.readline()

#looprange = 1048576
looprange = 40
markerloc = markerbegin
for i in range(0, looprange, 4):
    markerloc = markerbegin + i
    control.write("m"+str(markerloc)+";")
    control.write("o;")
    control.write("f3;")
    control.write("o;")
    print control.readline()
    control.readline()
    print control.readline()
    control.readline()
    control.readline()
    print control.readline()
control.close()