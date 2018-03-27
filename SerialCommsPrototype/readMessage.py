print "Start inclusion of code"

import serial		#-Install this module first-
import time


ser = serial.Serial('/dev/ttyACM0', 9600)	#TI-MSP432 - Linus
#ser = serial.Serial('/dev/ttyUSB0', 9600)	#Arduino clone - Linux
	

while True:
	time.sleep(0.1)
	print ser.readline()


