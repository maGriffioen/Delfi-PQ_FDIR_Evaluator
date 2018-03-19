print "Good import"

import serial


ser = serial.Serial('/dev/ttyACM0', 9600)

def ledOn():
	ser.write('LED ON;')

def ledOff():
	ser.write('LED OFF;')

def ledBlink(time):
	ser.write('LED BLINK '+ str(time) +';')


