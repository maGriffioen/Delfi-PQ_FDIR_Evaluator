'''
This is the main python script for the host PC running the FDIR verification software
This contains the search loops and patterns for finding problems on the controller.
23/4/2018
'''

#Interface to the two microcontrollers.
#controllerInterface uses signal.timer(), which is only available on UNIX
from controllerInterface import controllerInterface

#External libraries
import time
import numpy
from matplotlib import pyplot

#Ports of the two microcontrollers
controllerPort = '/dev/ttyACM1'
resetPort = '/dev/ttyACM2'

#Open controller interface
ctr = controllerInterface(controllerPort, resetPort)


##############################################################
#################### SEARCH PATTERN SETUP ####################
##############################################################

#Start of SRAM memory, where flips will be performed
markerbegin = 536870912

#Number of bytes after start where program is allowed to make bitflips
searchspace = 1048576
searchspace = 64000

looprange = 20      #Number of location to search per group
locnumber = 5       #Number of random groups to search

#Generate groups of random locations to search
numpy.random.seed(5)
floatarray = numpy.around(markerbegin + searchspace * numpy.random.rand(1, locnumber))
randloc = floatarray.astype(int).tolist()[0]
randloc.append( markerbegin )   #Include start of memory to search -> known failure locations
randloc.append( 536875136 )     #Include know data location to find data corruption
randloc.sort()

#Generate a list of all location to search
fulllist = []
for i in randloc:
    for j in range(0, looprange * 4, 4):
        addition = i + j
        fulllist.append(addition)

flipLocations = [3]


###########################################################
#################### PERFORMING SEARCH ####################
###########################################################
starttime = time.time()     #Measures total runtime
resultList = []             #Stores results
print "Start FDIR verification"

#Main program loop to search for faults
for markerloc in fulllist:
    for flipLocation in flipLocations:
        print markerloc - markerbegin, flipLocation

        m1 = ctr.move( markerloc )      #Move pointer on controller
        o1 = ctr.output()               #Show pointer location content
        f1 = ctr.flip( flipLocation )   #Flip bit
        o2 = ctr.output()               #Show pointer location content

        time.sleep(0.1)                 #Prevent outperforming the controller
        dataVerified = ctr.verifyData() #Verify on-board data


        #Determine fault type
        if ( not m1 ):
            faultType = 3
        elif ( not f1 ):
            faultType = 1
        elif ( markerloc != o1[2] or markerloc != o2[2] ):
            faultType = 4
        elif ( not dataVerified ):
            faultType = 2
            ctr.reset() #Remove present data error
        else:
            faultType = 0

        ##faultType:
        #   0: No error detected
        #   1: Lockup - no reaction from controller after a flip
        #   2: Data corruption - reference states do not equal their preset values
        #   3: Move failure -> Locks controller state when moving to specific pointers
        #   4: Move fault -> pointer is not moved to the correct state

        resultList.append( (markerloc, flipLocation, faultType) )
        print m1, o1, f1, o2, dataVerified
 
print "FDIR-Verification done. Runtime: " + str(time.time() - starttime) + " s"

########################################################
#################### SAVING RESULTS ####################
########################################################

#Open .dat file
thefile = open('FDIR-Results.dat', 'w')
#Store results per line
for result in resultList:
    thefile.write( str(result[0]) + ', ' + str(result[1]) + ', ' + str(result[2]) + '\n' )
thefile.close()


#########################################################
#################### POST-PROCESSING ####################
#########################################################

#Determine total number of each failure
numberOfFailureTypes = 5
failureCount = [0 for i in range(numberOfFailureTypes)]
for result in resultList:
    failureCount[ result[2] ] += 1

#Create pie chart
legend = ['None', 'Lockup', 'Data corruption', 'Move failure', 'Move fault']
legend = [legend[i] + " " + str( failureCount[i]) for i in range(numberOfFailureTypes)]
pyplot.pie(failureCount, labels = legend)
pyplot.title("Failure distributions")
pyplot.show()


#Create history plot
loclist = []
errorlist = []
for i in resultList[:]:
    loc = i[0]
    loclist.append(loc)
    error = i[2]
    errorlist.append(error)

y_values = ['No error', 'Lockup', 'Data corruption', 'Move failure', 'Move fault']
y_axis = numpy.arange(0, 5, 1)
pyplot.scatter(loclist, errorlist)
pyplot.yticks(y_axis, y_values)
pyplot.yticks(rotation=45)
pyplot.xlabel('Location in Memory')
pyplot.ylabel('Error mode')
pyplot.grid()
pyplot.show()
