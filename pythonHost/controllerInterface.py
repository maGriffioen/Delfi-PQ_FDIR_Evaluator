'''
This is the python script that handles the interface between the search logic and the controllers
The various functions can be extended here for more advanced applications

23/4/2018
'''

import serial
import time
import signal

def timeoutHandler(signum, frame):
    '''This function is used to raise an exception using signal.timer() '''
    raise Exception("TimeOut")

class controllerInterface:
    def __init__(self, controllerPort, resetPort):
        '''
        Open serial communication to controllers
        :param controllerPort: Port name of primary controller
        :param resetPort: Port name of reset controller (secondary)
        '''

        #open serial ports
        self.controller = serial.Serial( controllerPort, 115200 )
        self.resetTrigger = serial.Serial( resetPort, 115200 )
        self.serialLog = []

        signal.signal(signal.SIGALRM, timeoutHandler)

        #Wait for startup
        time.sleep(0.5)
        self.serialLog += self.readController()
        self.cleanLog()

        return None


    def close(self):
        '''
        Close serial communication ports
        '''
        self.controller.close()
        self.resetTrigger.close()

        return None


    def reset(self):
        '''
        Resets the flight controller
        :return: resetSucces (bool)
        '''
        #Send command to reset
        self.resetTrigger.write('r;')
        print "Attempt reset"

        #Try to see if command is returned by reset trigger controller
        log = []
        time.sleep(0.05)
        while ( self.resetTrigger.inWaiting() > 0 ):
            log.append( self.resetTrigger.readline() )
            time.sleep(0.005)

        #Remove text formatting
        log = [line[:-2] for line in log]
        if not ( 'r' in log ):
            #Reset controller not responsive??
            print "Reset failed, resetTrigger not responsive!"
            resetSuccess = False
        else:
            resetSuccess = True

        #Wait for the flight controller to reboot
        time.sleep(0.2)

        return resetSuccess


    def readController(self):
        '''
        Reads available information from the flight controller
        :return: log (list of strings) -> contains all available information
        '''
        #Create empty serial log
        log = []

        #While messages are on the controller: read them and add to log
        while ( self.controller.inWaiting() > 0 ):
            #Set 2s timer to prevent theprogram from getting stuck
            signal.alarm( 2 )
            try:
                log.append( self.controller.readline() )
            except Exception as ex:
                if "TimeOut" in ex:
                    pass
            finally:
                #Reset signal alarm to not crash the program
                signal.alarm( 0 )
            time.sleep( 0.005 )

        #Remove text formatting
        log = [line[:-2] for line in log]

        return log


    def sendCommand(self, command):
        '''
        Sends command to flight controller and verifies if it is returned
        (and thus, most likely, executed
        :param command: str, command to execute
        :return: bool, True -> success, False -> failure
        '''
        self.controller.write( command + ";" )
        time.sleep(0.1)
        log = []

        keepReading = True
        timeout = 0
        success = False
        while ( keepReading ):
            if ( self.controller.inWaiting() > 0 ):
                log += self.readController()
                if ( command in log ):
                    if (command != 't'):
                        log.remove( command )
                    keepReading = False
                    success = True
                elif (timeout < 5 ):
                    timeout += 1
                    time.sleep( 0.5 )
                else:
                    self.reset()
                    keepReading = False

            elif ( timeout < 5 ):
                timeout += 1
                time.sleep( 0.2 )
            else:
                self.reset()
                keepReading = False

        self.serialLog += log
        return success


    def move(self, location):
        '''
        Move flightcontroller pointer to desired location
        :param location: Desired memory location
        :return: True -> success, False ->Failure
        '''
        command = 'm' + str(location)
        commandSuccess = self.sendCommand( command )

        return commandSuccess


    def output(self):
        '''
        Send ouput command to flight controller to receive
        current pointer location and content
        :return: (True -> success; False ->failure, value, location)
        '''
        command = 'o'
        commandSuccess = self.sendCommand( command )

        if commandSuccess:
            self.cleanLog()
            removeNums = []
            foundResult = False
            for i, ll in enumerate(self.serialLog):
                if ( ll[:5] == "Val: " ):
                    result = [int(val) for val in ll[5:].split(' at: ')]
                    foundResult = True
                    removeNums.append(i)
                else:
                    pass

            for nn in removeNums[::-1]:
                self.serialLog.remove( self.serialLog[nn] )

            if foundResult:
                return (True, result[0], result[1])
            else:
                return (False, 0, 0)

        else:
            return (False, 0, 0)


    def flip(self, bitNumber):
        '''
        Flip a bit on the flight controller
        :param bitNumber: Bit to flip -> 0 is least significant
        :return: success (True) or failure (False)
        '''
        command = 'f' + str( bitNumber )
        commandSuccess = self.sendCommand( command )

        return commandSuccess


    def verifyData(self):
        '''
        Verify the data on the flightcontroller
        :return: pass (True), data error (False)
        '''
        #Test the content of the test string.
        testStringSuccess = self.verifyTestString()

        ### More verifications can be added here.!
        #
        #


        if (testStringSuccess):
            verificationPass = True
        else:
            verificationPass = False

        return verificationPass


    def verifyTestString(self):
        '''
        Verifies the test string on the flight controller
        Example for data content verification
        :return: pass (True), failure (False)
        '''
        self.clearLog()
        command = 't'
        commandSuccess = self.sendCommand( command )

        #Find where the command 't' is in the commandlog
        #Content of test string is always sent right before it
        if 't' in self.serialLog:
            if self.serialLog[ self.serialLog.index('t') -1 ] == 'Hello World':
                dataVerificationPass = True
            else:
                dataVerificationPass = False
        else:
            dataVerificationPass = False

        #Reset the log to remove 't' and teststring locations
        self.clearLog()
        return dataVerificationPass



    def cleanLog(self):
        '''
        Clears the serial log from loopcounts
        :return: None
        '''
        loopcountString = 'LoopCount: '
#        lastloop = 0
        removeNums = []
        for i, ll in enumerate(self.serialLog):
            if ( ll[:len(loopcountString)] == loopcountString ):
                removeNums.append( i )
#            if ( ll[:11] == "LoopCount: " and lastloop == 0 ):
#                lastloop = int( ll[11:] )
#                removeNums.append( i )

        for nn in removeNums[::-1]:
            self.serialLog.remove( self.serialLog[nn] )

        return None


    def clearLog(self):
        '''
        Resets the serial log to an empty list.
        !!! Only use if you dont need the content anymore !!!
        :return: None
        '''
        self.serialLog = []

        return None