'''
This test.py verifies the use of signal as timeout handler.
Signal is used in the main project code to detect when serial.writeline()
is trying to read from a stuck controller.
(It might still shows characters in serial.inWaiting()

23/4/2018
'''


import time
import signal


def timeout_handler(num, stack):
    print("Received SIGALRM")
    raise Exception("TimeOut")



signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)

try:
    time.sleep(8)
except Exception as ex:
    if "TimeOut" in ex:
        print "Stopped sleep-time"
finally:
    print "finally"
    signal.alarm(0)
time.sleep(5)
