from controllerInterface import controllerInterface
import time

controllerPort = '/dev/ttyACM0'
resetPort = '/dev/ttyACM2'
ctr = controllerInterface(controllerPort, resetPort)

markerbegin = 536870912
markerbegin = 536870956

looprange = 400
markerloc = markerbegin

resultList = []

for i in range(0, looprange, 4):
    markerloc = markerbegin + i
    flipLocation = 3

    m1 = ctr.move(markerloc)
    o1 = ctr.output()
    f1 = ctr.flip( flipLocation )
    o2 = ctr.output()
    time.sleep(0.2)

    if ( not m1 ):
        faultType = 3
    elif ( not f1 ):
        faultType = 1
    elif ( markerloc != o1[2] or markerloc != o2[2] ):
        faultType = 4
    else:
        faultType = 0
    ##faultType:
    #   0: No error detected
    #   1: Lockup - no reaction from controller after a flip
    #   2: Data corruption - reference states do not equal their preset values
    #   3: Move failure -> Locks controller state when moving to specific pointers
    #   4: Move fault -> pointer is not moved to the correct state

    resultList.append( (markerloc, flipLocation, faultType) )
    print m1, o1, f1, o2
    print ctr.serialLog