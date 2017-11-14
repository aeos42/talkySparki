# Packets

Packets should be wrapped in a start and end tag and should be in the form of:

"S (command) (parameter1) (parameter2) (parameter3) E"

examples:

### scanData packet:
# "S scan X Y Theta Alpha ping E"

#### where:
command is "scan"

robot coords are (X,Y)

robot is at bearing Theta (0 - 360)

UltraSonic Sensor is at angle Alpha (-30 - 30)

ping is distance recorded


### moveTo packet:
# "S moveTo X Y Theta"

#### where:
goal robot coords are (X,Y)

goal robot is at bearing Theta (0 - 360)

--- 


