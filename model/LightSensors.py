import spidev
from time import sleep
import datetime

class LightSensors():

    def __init__(self):
        # create spi object
        self.spi = spidev.SpiDev()
        # open spi port 0, device (CS) 0
        self.spi.open(0, 0)
        # channel should be an integer between 0 and 7
        self.channels = (0, 1, 2, 3, 4, 5, 6, 7)

    # Function to read SPI data from MCP3008 chip
    def readChannel(self, channel):
        # 3 bytes versturen
        # 1, S D2 D1 D0 xxxx, 0
        adc = self.spi.xfer2([1, (8 + self.channels[channel]) << 4, 0])
        data = ((adc[1] & 3) << 8) | adc[2]  # the result gets stored in byte1 and 2
        return data

    def readChannels(self):
        dataChannels = []
        for i in range(0,8):
            data = self.readChannel(i)
            dataChannels.append(data)
        return dataChannels

    def detectLightToDark(self, oldData):
        #oldData = self.readChannel(channel)
        #sleep(1)

        sensorLtD = False
        newData = self.readChannels()

        for i in range (0,8):
            if(newData[i]-oldData[i] > 100):
                print(i)
                sensorLtD = i

        return sensorLtD

    def detectDarkToLight(self, oldData):
        #oldData = self.readChannel(channel)
        #sleep(1)

        sensorDtL = False
        newData = self.readChannels()

        for i in range (0,8):
            if(oldData[i]-newData[i] > 100):
                sensorDtL = i

        return sensorDtL


    def checkIfPlaceIsRight(self, beginData, right_place):
        startTime = datetime.datetime.now()

        # boolean to check if a place is detected
        place_detected = False
        # variable to store the detected place
        detected_place = ""
        while (type(self.detectLightToDark(beginData)) != "int" and place_detected == False and detected_place != False):
            if (self.detectLightToDark(beginData) == right_place):
                place_detected = True
                detected_place = True
            elif (self.detectLightToDark(beginData) != False and self.detectLightToDark(beginData) != right_place):
                place_detected = True
                detected_place = self.detectLightToDark(beginData)
            elif(datetime.datetime.now() - startTime > datetime.timedelta(minutes=1)):
                detected_place = False

        return detected_place

