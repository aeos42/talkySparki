## Packets

Packets are wrapped in a start and end tag and should be in the form of:

Packets have a variable number of parameters, and so are variable in size.


|Byte Number | 0               | 1          | 2     | 3     | ... | n-2   | n-1           |
|--          |              -- |          --|    -- | --    |  -- | --    | --            |
|Meaning     | Start of Packet | Command ID | Param | Param | ... | Param | End of Packet | 


for n bytes, indexed from zero because computer science.

examples:

### scanData packet:


|Byte Number | 0               | 1          | 2      | 3      | 4     | 5     | 6    |   7            |
|--          |              -- |          --|    --  |    --  | --    |  --   | --   |  --            |
|Meaning     | Start of Packet | Scan ID    | xCoord | yCoord | theta | alpha | ping |  End of Packet | 



Where:

command is "Scan ID"

Robot coordinates are *(xCoord, yCoord)*

robot is at bearing *theta* (0 - 360)

UltraSonic Sensor is at angle *alpha* (-30 - 30)

Distance recorded is *ping* (cm)


### moveTo packet:


|Byte Number | 0               | 1          | 2      | 3      | 4     | 5 |
|--          |              -- |          --|    --  |    --  | --    | --|
|Meaning     | Start of Packet | moveTo ID  | xCoord | yCoord | theta | End of Packet | 


Where:

Robot goal coordinates are (xCoord, yCoord)

goal robot is at bearing *theta* (0 - 360)



