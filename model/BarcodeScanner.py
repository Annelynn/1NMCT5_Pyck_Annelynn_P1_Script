class BarcodeScanner():

    def __init__(self, poort='/dev/hidraw0', modus='rb'):
        self.buffer = open(poort, modus)   #barcode scanner gets used as keyboard

    def readBarcode(self):
        # create empty variable
        barcode = ""

        # while first bit of byte does not equal zero
        while self.buffer.read(8)[0] != 0:
            # read new byte
            character = self.buffer.read(8)

            # '(' gets stored in third bit instead of second bit
            if(character[2:3] == b'\x1e'): # second bit=0, thus slicing from 2:3 otherwise the third bit doesn't get recognised as bit
                symbol = '('
            # '§' gets stored in third bit instead of second bit
            elif(character[2:3] == b'\x1f'): # second bit=0, thus slicing from 2:3 otherwise the third bit doesn't get recognised as bit
                symbol = '§'
            # all other symbols do get stored in second bit
            else:
                ascii_number = int(character[2])
                symbol = chr(ascii_number)

            # add symbol to barcode
            barcode += symbol

        # stop symbol gets included into barcode and this is unnecessary
        return barcode[:-1]

    def convertBarcodeToISBN(self, barcode):
        # create empty variable
        isbn = ""

        # dictionary with symbols translated into numbers
        translation = {'\'' : '0',
                       '('  : '1',
                       '§'  : '2',
                       ' '  : '3',
                       '!'  : '4',
                       '\"' : '5',
                       '#'  : '6',
                       '$'  : '7',
                       '%'  : '8',
                       '&'  : '9'}

        # loop through barcode
        for symbol in barcode:
            # replace symbold with number
            number = translation[symbol]
            # append number to isbn
            isbn += number

        return isbn