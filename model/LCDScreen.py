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

        if (type == "instruction"):         # Status RS is dependend on what kind gets send through
            statusRS = GPIO.LOW             # If byte=instruction --> RS should receive 0V
        else:
            statusRS = GPIO.HIGH            # If byte != instruction, RS should receive a HIGH signal
            byte = ord(byte)                # and incoming byte should be converted to ASCII

        MSB = byte >> 4                     # MSB = 0000MMMM
        LSB = byte & 0x0f                   # LSB = 0000LLLL

        GPIO.output(self.E, GPIO.HIGH)      # Send MSB
        GPIO.output(self.RS, statusRS)
        for x in range(0, 4):
            GPIO.output(self.dbus[x], MSB & (1 << x))
        GPIO.output(self.E, GPIO.LOW)
        sleep(0.1)

        GPIO.output(self.E, GPIO.HIGH)      # Send LSB
        GPIO.output(self.RS, statusRS)
        for x in range(0, 4):
            GPIO.output(self.dbus[x], LSB & (1 << x))
        GPIO.output(self.E, GPIO.LOW)
        sleep(0.1)

    def __init_display(self):

        self.__send_GPIO_bits(0x28, "instruction")  # Function Set: set to 4bit mode
        self.__send_GPIO_bits(0x0E, "instruction")  # Display On
        self.__send_GPIO_bits(0x01, "instruction")  # Clear Display

    def empty_line(self, linenumber):
        if (linenumber == 1):
            place = 0x80
        else:
            place = 0xC0

        self.__send_GPIO_bits(place, "instruction")  # Set cursor at beginning of line

        for segment in range(0, 16):                 # Empty line
            self.__send_GPIO_bits(" ", "character")

    def show_text_on_first_line(self, text):
        self.__send_GPIO_bits(0x80, "instruction")   # Set cursor at beginning of first line
        for letter in text:                          # Print text
            self.__send_GPIO_bits(letter, "character")

    def show_text_on_second_line(self, text):
        self.__send_GPIO_bits(0xC0, "instruction")  # Set cursor at beginning of second line
        for letter in text:                         # Print text
            self.__send_GPIO_bits(letter, "character")

    def shut_down_LCD(self):
        self.__send_GPIO_bits(0x01, "instruction")  # Clear display
        self.__send_GPIO_bits(0x08, "instruction")  # Display off


