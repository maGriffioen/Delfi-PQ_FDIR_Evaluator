print "Start inclusion of code"

import serial		#-Install this module first-

ser = serial.Serial('/dev/ttyACM0', 9600)	#TI-MSP432 - Linus
#ser = serial.Serial('/dev/ttyUSB0', 9600)	#Arduino clone - Linux

def ledOn():
	ser.write('LED ON;')

def ledOff():
	ser.write('LED OFF;')

def ledBlink(time):
	ser.write('LED BLINK '+ str(time) +';')


