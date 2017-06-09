from RPi import GPIO
from time import sleep

class LCDScreen():

    def __init__(self, pinRS, pinE, pinD4, pinD5, pinD6, pinD7):
        # currently: RS=21, E=20, D4=16, D5=25, D6=24, D7=23

        self.RS = pinRS
        self.E = pinE

        self.dbus = [pinD4, pinD5, pinD6, pinD7]

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)

        for i in range (0,4):
            GPIO.setup(self.dbus[i], GPIO.OUT)

        self.__init_display()

    def __send_GPIO_bits(self, byte, type): # Byte = MMMMLLLL

        # Status RS is dependend on what kind gets send through
        if (type == "instruction"):
            # If byte=instruction --> RS should receive 0V
            statusRS = GPIO.LOW
        else:
            # If byte != instruction, RS should receive a HIGH signal
            statusRS = GPIO.HIGH
            # and incoming byte should be converted to ASCII
            byte = ord(byte)

        # MSB = 0000MMMM
        MSB = byte >> 4
        # LSB = 0000LLLL
        LSB = byte & 0x0f

        # Send MSB
        GPIO.output(self.E, GPIO.HIGH)
        GPIO.output(self.RS, statusRS)
        for x in range(0, 4):
            GPIO.output(self.dbus[x], MSB & (1 << x))
        GPIO.output(self.E, GPIO.LOW)
        sleep(0.1)

        # Send LSB
        GPIO.output(self.E, GPIO.HIGH)
        GPIO.output(self.RS, statusRS)
        for x in range(0, 4):
            GPIO.output(self.dbus[x], LSB & (1 << x))
        GPIO.output(self.E, GPIO.LOW)
        sleep(0.1)

    def __init_display(self):

        # Function Set: set to 4bit mode
        self.__send_GPIO_bits(0x28, "instruction")
        # Display On
        self.__send_GPIO_bits(0x0E, "instruction")
        # Clear Display
        self.__send_GPIO_bits(0x01, "instruction")

    def __empty_line(self, linenumber):
        # if first line
        if (linenumber %2 != 0):
            # set cursor at beginning of first line
            place = 0x80
        else:
            # set cursor at beginning of second line
            place = 0xC0

        # send instruction
        self.__send_GPIO_bits(place, "instruction")

        # Empty line
        for segment in range(0, 16):
            self.__send_GPIO_bits(" ", "character")

    def clear_screen(self):
        # Clear display
        self.__send_GPIO_bits(0x01, "instruction")

    def show_text_on_one_line(self, text, line):
        # if text is longer than 16 characters, it cannot be displayed on one line
        if(len(text) > 16):
            text = "Text is too long"
        # if there's other text left on the screen, it should be replaced with spaces
        elif(len(text) < 16):
            while len(text) != 16:
                text += " "

        # if line is even
        if(line % 2 == 0):
            # Set cursor at beginning of first line
            self.__send_GPIO_bits(0x80, "instruction")
        # if line is odd
        elif(line % 2 != 0):
            # Set cursor at beginning of second line
            self.__send_GPIO_bits(0xC0, "instruction")

        # Print text
        for letter in text:
            self.__send_GPIO_bits(letter, "character")

    @staticmethod
    def split_text_into_lines(text):
        # split text into words
        words = text.split()
        # add stop-symbol
        words.append(" ")
        # create empty variables
        lines = []
        line = ""
        # while stop-symbol isn't reached
        while words[0] != " ":
            # add first word without spaces
            line += words[0]
            del words[0]
            # add words to string so it doesn't exceed a length of 16 characters
            while len(line) < 16 - len(words[0]) and words[0] != " ":
                # add other words with spaces
                line += " " + words[0]
                # delete every word that was appended and isn't the stop signal
                if words[0] != " ":
                    del words[0]
            # add line to list
            lines.append(line)
            # reset line so loop can start over again
            line = ""
        return lines

    def show_text_on_multiple_lines(self, text):
        # clear display
        self.__send_GPIO_bits(0x01, "instruction")
        # split lines
        lines = LCDScreen.split_text_into_lines(text)
        # initialise counter
        i = 0
        # print lines
        for line in lines:
            self.show_text_on_one_line(line, i)
            i += 1

    def shut_down_LCD(self):
        self.__send_GPIO_bits(0x01, "instruction")  # Clear display
        self.__send_GPIO_bits(0x08, "instruction")  # Display off
        GPIO.cleanup()


