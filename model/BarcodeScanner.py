class BarcodeScanner():

    def __init__(self, poort='/dev/hidraw0', modus='r'):
        self.f = f = open(poort, modus)   #barcode scanner wordt weergegeven als toetsenbord

    def leesBarcode(self):
        barcode = ""
        for i in range (0,13):
            karakter = self.f.read(13)
            barcode += karakter
        return barcode
