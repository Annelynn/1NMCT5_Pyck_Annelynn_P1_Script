import spidev
from time import sleep
import datetime

class LightSensors():
    # to avoid any confusion between 0 and 1 for False and True
    # an "8" for False, and  a "9" for True will be used
    def __init__(self):
        # create spi object
        self.spi = spidev.SpiDev()
        # open spi port 0, device (CS) 0
        self.spi.open(0, 0)
        # channel should be an integer between 0 and 7
        self.channels = (0, 1, 2, 3, 4, 5, 6, 7)

    # Function to read SPI data from MCP3008 chip
    def readChannel(self, channel):
        # Send 3 bytes
        # 1, S D2 D1 D0 xxxx, 0
        adc = self.spi.xfer2([1, (8 + self.channels[channel]) << 4, 0])
        data = ((adc[1] & 3) << 8) | adc[2]  # the result gets stored in byte1 and 2
        return data

    def readChannels(self):
        # read all channels at once and put them in a list
        dataChannels = []
        # 8 channels so range 0 to 8 (with 8 excluded)
        for i in range(0,8):
            # read one channel
            data = self.readChannel(i)
            # add to list
            dataChannels.append(data)
        return dataChannels

    def detectLightToDark(self, oldData):
        # detect a change from light to dark

        # no change detected = False = "8", see beginning of this class
        sensorLtD = 8
        # read new data
        newData = self.readChannels()

        # check each channel
        for i in range (0,8):
            # if a change bigger than 100 happened
            if(newData[i]-oldData[i] > 100):
                # the sensor where the change happened gets returned
                sensorLtD = i

        return sensorLtD

    def detectDarkToLight(self, oldData):
        # detect a change from dark to light

        # no change detected = False = "8", see beginning of this class
        sensorDtL = 8
        # read new data
        newData = self.readChannels()

        # check each channel
        for i in range (0,8):
            # if a change bigger than 100 happened
            if(oldData[i]-newData[i] > 100):
                # the sensor where the change happened gets returned
                sensorDtL = i

        return sensorDtL


    def checkIfPlaceIsRight(self, beginData, right_place):
        # check if a place is right, or if no place gets detected at all

        # store current time in variable
        startTime = datetime.datetime.now()

        # boolean to check if a place is detected, but to avoid confusion "8" gets used, see top op class
        place_detected = 8
        # variable to store the detected place
        detected_place = ""

        # while , no place was detected, and detected_place is not False ("8")
        while (place_detected == 8 and detected_place != 8):
            # if book was placed on right place
            if (self.detectLightToDark(beginData) != 8 and self.detectLightToDark(beginData) == right_place):
                place_detected = 9
                # 9 instead of "True" so no confusion with 0's and 1's is possible
                detected_place = 9

            # when a detection from light to dark took place, it returns an int
            elif (self.detectLightToDark(beginData) != 8 and self.detectLightToDark(beginData) != right_place):
                place_detected = 9
                detected_place = self.detectLightToDark(beginData)

            # if more than a minute has passed, the book wasn't placed onto the shelf
            elif(datetime.datetime.now() - startTime > datetime.timedelta(minutes=1)):
                # 8 instead of "True" so no confusion with 0's and 1's is possible
                detected_place = 8

        return detected_place


