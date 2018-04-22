import serial
import time
import signal

def handler(signum, frame):
    raise Exception("TimeOut")

class controllerInterface:
    def __init__(self, controllerPort, resetPort):
        self.controller = serial.Serial( controllerPort, 115200 )
        self.resetTrigger = serial.Serial( resetPort, 115200 )
        self.serialLog = []

        signal.signal(signal.SIGALRM, handler)

        time.sleep(0.5)
        self.serialLog += self.readController()
        self.cleanLog()

        return None


    def close(self):
        self.controller.close();
        self.resetTrigger.close();

        return None


    def reset(self):
        self.resetTrigger.write('r;')
        print "Attempt reset"

        log = []
        time.sleep(0.05)
        while ( self.resetTrigger.inWaiting() > 0 ):
            log.append( self.resetTrigger.readline() )
            time.sleep(0.005)

        # Remove text formatting
        log = [line[:-2] for line in log]
        if not ( 'r' in log ):
            print "Reset failed, resetTrigger not responsive!"

        return None


    def readController(self):
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
        self.controller.write( command + ";" );
        time.sleep(0.1)
        log = [];

        keepReading = True
        timeout = 0
        success = False
        while ( keepReading ):
            if ( self.controller.inWaiting() > 0 ):
                log += self.readController()
                if ( command in log ):
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
        return success;


    def move(self, location):
        command = 'm' + str(location)
        commandSuccess = self.sendCommand( command )

        return commandSuccess


    def output(self):
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
        command = 'f' + str( bitNumber )
        commandSuccess = self.sendCommand( command )

        return commandSuccess


    def cleanLog(self):
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




