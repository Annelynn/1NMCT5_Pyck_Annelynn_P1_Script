import serial
class NeoPixels():
    def __init__(self):
        self.__ser = serial.Serial('/dev/serial0', 9600, timeout=1)

    def write_number(self, number):
        if(number == 0):
            self.__ser.write(b'0')
        elif(number == 1):
            self.__ser.write(b'1')
        elif(number == 2):
            self.__ser.write(b'2')
        elif(number == 3):
            self.__ser.write(b'3')
        elif(number == 4):
            self.__ser.write(b'4')
        elif(number == 5):
            self.__ser.write(b'5')
        elif(number == 6):
            self.__ser.write(b'6')
        elif(number == 7):
            self.__ser.write(b'7')
        elif(number == 8):
            self.__ser.write(b'8')
        else:
            self.__ser.write(b'9')

    def write_clear(self):
        self.__ser.write(b'clear')

    def shut_down_LED(self):
        self.write_clear()
        self.__ser.close()
