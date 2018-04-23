##Purpose
Small satellites often have a low hardware budget. Therefore, no resources for commercial radiation-hardened hardware is available, as often found on large satellites. As an
alternative, these satellites are based on bulk electronic hardware, and therefore, SEUs (single event upsets) are to be expected in the memory of the system due to the radiation
in the space environment. This problem can be solved with FDIR algorithms. These are used on the flight software of the small satellites.
These algorithms detect faults caused by SEUs, and try to correct them.

Testing the flight software, and in particular the FDIR (fault detection, isolation and recovery) algorithm, is often an expensive endeavour, since the flight controller needs to
be brought to a radiation software, and tested near such a source. Moreover, due to the random nature of radiation, one has little control over where, when and how often SEUs happen
in the memory of the system.

This project proposes the design and implementation of an alternative solution to the testing of the Delfi-PQ FDIR software; by forcing controlled changes in the system memory. This
is done by simulating single bit mutations in the memory of the microcontroller, called fault injection. Besides reducing the cost of the test, this solution is more controlled, and
therefore it maps the memory better. Furthermore, this method is less labour intensive, since one system is capable of controlling and resetting the tests, allowing them to be
performed completely automated.

##General Concept
The purpose of the software files in this repository is to assess the performance of the FDIR. The software runs on a SimpleLink™ MSP432P401R LaunchPad™ Development Kit next to the
flight software. The software will invoke bitflips in the memory, as commanded by the host running the python code. By flipping various bits, and assessing the performance of the
controller, before and after, the influence of bitflips on the controller performance is assessed.