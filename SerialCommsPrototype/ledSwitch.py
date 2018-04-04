print "Start inclusion of code"

import serial		#-Install this module first-

ser = serial.Serial('/dev/ttyACM0', 9600)	#TI-MSP432 - Linux
#ser = serial.Serial('/dev/ttyUSB0', 9600)	#Arduino clone - Linux

def ledOn():
	ser.write('L;')

def ledOff():
	ser.write('l;')

def ledBlink(time):
	ser.write('B'+ str(time) +';')


