## Purpose
Small satellites often have a low hardware budget. Therefore, no resources for commercial radiation-hardened hardware is available, as often found on large satellites. As an alternative, these satellites are based on bulk electronic hardware, and therefore, SEUs (single event upsets) are to be expected in the memory of the system due to the radiation in the space environment. This problem can be solved with FDIR algorithms. These are used on the flight software of the small satellites. These algorithms detect faults caused by SEUs, and try to correct them.

Testing the flight software, and in particular the FDIR (fault detection, isolation and recovery) algorithm, is often an expensive endeavour, since the flight controller needs to be brought to a radiation software, and tested near such a source. Moreover, due to the random nature of radiation, one has little control over where, when and how often SEUs happen in the memory of the system.

This project proposes the design and implementation of an alternative solution to the testing of the Delfi-PQ FDIR software; by forcing controlled changes in the system memory. This is done by simulating single bit mutations in the memory of the microcontroller, called fault injection. Besides reducing the cost of the test, this solution is more controlled, and therefore it maps the memory better. Furthermore, this method is less labour intensive, since one system is capable of controlling and resetting the tests, allowing them to be performed completely automated.

## General Concept
The purpose of the software files in this repository is to assess the performance of the FDIR. The software runs on a SimpleLink™ MSP432P401R LaunchPad™ Development Kit next to the flight software. The software will invoke bitflips in the memory, as commanded by the host running the python code. By flipping various bits, and assessing the performance of the controller, before and after, the influence of bitflips on the controller performance is assessed.

![Errors](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator/blob/master/errorHistory.png)

## Literature Study

##### SEUs 
SEUs are so-called single event upsets. They are a type of soft error and are caused by ionising particles hitting the hardware components of a computer. The impact causes the state of the part to change. When this part contains data, it will show a deviating output. Because there is a lot of radiation in the outer space environment, SEUs are common for computers onboard spacecraft.

##### SEUs location
The targeted location of the SEUs is the SRAM.The entire address space the MSP432 can access runs from 0x0000 0000 to 0xFFFF FFFF. The Code and SRAM zones are only a subset of this. It should be noted that the SRAM region in the SRAM zone (0x2000 0000 - 0x2010 0000) is the same as the SRAM region in the Code zone (0x0100 0000 - 0x0110 0000). It is between these boundaries where the bitflips are generated.

http://energia.nu/wordpress/wp-content/uploads/2015/03/2016-06-09-LaunchPads-MSP432-2.0-%E2%80%94-Pins-Maps.jpg
For pin allocation.


## Required Soft- and Hardware
In order to use the scripts found in this repository, the user needs to have the following programs installed in his computer: 

**Python 2.7:** This open source software provides a hands-on interface that the user will easily familiarise with. It is this program that will initialise the controller and send the desired commands. The following modules are used: Pyserial, signal (Unix only), numpy and time.

**2x SimpleLink MSP432P401R LaunchPad Development Kit:** All software runs on these controllers.


(**Energia:** This program is used to compile the code for the controller. If the user wishes to make some improvements to it, he needs this to get it running on the controller.) 

**Wires and 1kΩ resistor:** Used to connect an output pin from one controller to the reset pin of the other controller.

#### Software Setup

##### Flight controller
The required scripts that run on the controller are found in the folder bitflipSoftware. It contains three .ino files, which will be explained below.

**bitflipSoftware.ino**
This is the main file which is used to use the software. This file contains three main parts:
Initialization of global variables
Setup function for the controller (opening serial ports): setup
Main loop function: loop
In general one execution of the loop function can be described as follows:
First, a call to delay() is made to limit the speed of the controller. Then the controller (when needed) output the current value of the loop counter to the serial port. Finally, the serial port is checked for incoming messages. If these are present the execCommand function is executed in order to perform the correct command.

**execCommand.ino**
This file, with its function execCommand, defines all the commands that can be executed by the controller. They are all in the same format, i.e. a letter followed by a number and a semicolon. The commands are defined as follows:

**p:** Returns the given input value to the serial port. Can be used as a ‘ping’ to verify the working of the controller.

**m:** Move the flipPointer to the specified address in the memory.

**f:** Flip a bit at the input location, where bit 0 is the least significant bit.

**s:** Set the value at the current flipPointer location.

**t:** Output the test string, which is by default defined as “Hello world”.

**o:** Output the current memory location of flipPointer, and the content at that location.

**c:** Count the loop numbers through the serial output.


**flipBit.ino**
This file contains the function flipBit, which performs the actual bitflip at the bit given by the input parameter (0-31). The location of flipPointer determines the memory address where this bitflip is performed.


##### Reset trigger controller
The required scripts that run on the reset trigger controller (secondary controler) are found in the folder resetTrigger. It contains two .ino files, which are similar to the ones for the flight controller.

**resetTrigger.ino**
This is the main file which is used to use the software. It contains the same general structure as the main project file for the flight controller software.
Variable initialization
Setup function setup, for opening serial communications and various pins
Main loop function loop, which contains required code for receiving commands and passing these to execCommand.


**execCommand.ino**
This file, with its function execCommand, is similar to the file with the same name mentioned above. This time the following commands are available:

**l:** Turn on LED

**L:** Turn off LED

**p:** Returns the given input value to the serial port. Can be used as a ‘ping’ to verify the working of the controller.

**r:** Trigger a reset on the primary controller

##### Python host software
The python code running on the host computer can be found in the pythonHost folder. To files are present within this folder: [pythonHost.py](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator/blob/master/pythonHost/pythonHost.py) and [controllerInterface.py](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator/blob/master/pythonHost/controllerInterface.py).

**[pythonHost.py](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator/blob/master/pythonHost/pythonHost.py)**
This is the main python script running on the host computer. It starts off with determining the search pattern through the memory by creating a list of memory addresses. Furthermore, this file defines the sequence of actions when performing a bitflip, the actions taken to verify the controller, and the assignment of the error type. Finally, the script includes some post-processing actions. This includes: outputting the raw data in text format, plotting the distributions of errors / fault in a pie chart, and plotting the error per memory address. 

**[controllerInterface.py](https://github.com/FlyOHolic/Delfi-PQ_FDIR_Evaluator/blob/master/pythonHost/controllerInterface.py)**
This script consists of two major parts: The definition of a timeout exception, and the controller interface class. The timeoutHandler function is a function which raises a timeout exception. This is used in combination with the signal.timer() and a ‘try-except’ structure to prevent the software from getting stuck in a serial.readline() call, which will last forever when no data is present on the serial port. The controllerInterface class is created to provide a robust layer between the main python script, and the controller (and pyserial). This decision was made since the software is supposed to function under non-nominal circumstances and deal with data corruption, irresponsiveness, and crashes of the controller. Therefore, this code has been written in a way that it does not pose a problem when a function cannot be successfully executed, however, it will (generally) report a success or failure in a command. A short description of each function will follow:

**_init\_**: constructor function that opens the serial ports and creates required variables.

**close:** closes the serial port connections.

**reset:** resets the flight controller through the secondary controller. Includes a print statement to have an overview of this happening when running the code. Includes another print statement for irresponsiveness of the control trigger controller.

**readController:** Read available data from the controller (without freezing up the python script).

**sendCommand:** Send the given command to the controller, and determines if the controller reacts properly (by returning the given command), or needs a reset.

**output:** Call the ‘o’ (output) command on the microcontroller: returns pointer location and content.

**flip:** Call the ‘f’ (bit flip) command on the micrcontroller. Will return False when the controller directly freezes.

**verifyData:** General function for verification of the data on the microcontroller. This function calls various (currently only verifyTestString) functions which very different data.

**verifyTestString:** Verifies the content of the test string on the controller.

## Issues Encountered

**External reset:** during the process of looping through the memory on the microcontroller while flipping bits, the controller regularly freezes if it encounters an invalid instruction or data structure. Although the controller can be reset through the serial interface, it cannot be reset if it throws an exception because it then halts execution of the program. The only way to reset an interrupted microprocessor is by either pressing the physical hardware button or triggering the reset pin on the chip. 

The first option is not favourable during the loop as manual intervention is required every time the controller hangs. The issue is then to automatically detect a hanging processor and externally triggering the reset pin. Two options were considered:

1. Using the provided debug stack library, which provides an API for the on-board debug chip which can trigger the reset pin. This option is however quite complicated because it requires a C++ program that interfaces this library; another Python glue layer is then required to provide the interface between this C++ program and the main Python script.

2. Using another microcontroller which directly drives the reset pin of the microcontroller. This option was chosen as it is the least complicated because the second controller can also be driven by the same Python script. 

## Recommendations

* Implement interrupt handlers: if the microprocessor halts due to a runtime exception, it halts the execution of the program and will set a designated register flag with the appropriate fault code. It then tries to call a function, called an interrupt handler, which can try to ‘repair’ the fault and give the processor the command to resume execution. In our case, this function has the potential to read the exception code and forward it to the Python host so that the exact cause of the halt can be displayed, which gives extra insight into what happens at which memory location.

* Fix Linux-only compatibility: Currently, the python function signal.timer() in the signal library is used. This function is only available on Unix/ Linux systems. The purpose of this function is to prevent the software from getting stuck in a serial.readline() call after the controller has crashed (it still shows that it has characters available to read). This can be fixed by setting up the secondary controller (currently used to trigger resets) to act as a watchdog and check the status of the primary controller (perhaps using an output pin on the primary controller which alternates High and Low). This can be then used to prevent a serial.readline() call on a crashed controller.

* Tweak program timing: Currently, both the python code and flight controller main loop are set to sleep by respectively time.sleep() and delay() in order to prevent them from outperforming each other. As an effect, verifying the controller by running bitflips over the entire memory will take long (estimated ~18 hours for the SRAM). By reducing those delays, the speed of the program can be vastly increased.

