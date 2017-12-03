'''
purpose: a two-way command handling layer that provides command encoding
and decoding for serial communication to sparki
'''

import serial


class sparkiConnection:
    def __init__(self, port, baudrate):

        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.SIZE_LIMIT = 50

        if self.ser.is_open:
            print("port is open at " + self.ser.name)

        else:
            print("error: port not opened")

    # input: command in packet form (list)
    # output: serial send to Sparki
    def sendCommand(self, command):

        if (type(command[0]) is str):

            command.insert(0, 'S')
            command.append('E')

            space = ' '.encode('utf-8')

            commandToSend = space.join([item.encode('utf-8') for item in command])

            self.ser.write(commandToSend)

        else:
            print("command not formatted correctly")



    def checkBuffer(self):

        return (self.ser.in_waiting)

    # input: serial buffer
    # output: parsed
    def receiveCommand(self):

        received = ""

        sop = False
        eop = False

        eopOverflow = 0
        sopOverflow = 0

        if (self.checkBuffer() > 0):

            while not sop:

                char = self.ser.read().decode('utf-8')

                if (char == 'S'):
                    sop = True
                if (sopOverflow > self.SIZE_LIMIT):
                    sop = True
                    print("exceeded size limit looking for start")


            while not eop:

                char = self.ser.read().decode('utf-8')
                eopOverflow += 1
                received += char

                if (char == 'E'):
                    eop = True

                if (eopOverflow > self.SIZE_LIMIT):
                    eop = True
                    print("exceeded size limit looking for end")

            recievedList = received[4:-2].split(" ")

            for i in range(0, len(recievedList)):
                recievedList[i] = float(recievedList[i])

            return recievedList

        else:
            print("buffer was empty at time of receiveCommand call")



    def closeConnection(self):

        self.ser.close()
