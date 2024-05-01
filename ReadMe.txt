ENGM015 MEng Inidividual Investigative Project - Code ReadMe

The attached code (KZReseachManuscriptCode.py) is the python code used to read the Arduino output and predict the deformation level based on the previously identified training data.
The code can also be used to identify the optimal k value by commenting out lines 103 - 110 and ensuring line 101 is not commented out.
In order to select the PTFE sample that is being measured the correct deformation type must be selected, the string in lines 101 and 105 must either say "Oven" or "Mech" depending
if the deformation was purely temperature-based or included mechanical deformation.

The code requires an Arduino microcontroller to be connected to the device outputting an analog read of the A0 pin to the serial monitor.