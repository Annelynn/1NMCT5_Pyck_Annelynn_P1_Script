from model.DbClass import DbClass
from model.BarcodeScanner import BarcodeScanner
from model.LightSensors import LightSensors
from time import sleep

try:
    barcodeScanner = BarcodeScanner()
    database = DbClass()
    lightSensors = LightSensors()

    detected_barcode = ""
    detected_isbn = ""
    right_place = ""

    while True:

        # detect light status
        beginDataLS = lightSensors.readChannels()

        # detect barcode
        if(detected_barcode == ""):
            # scan barcode
            # this is a loop, and nothing will happen until a barcode is scanned
            detected_barcode = barcodeScanner.readBarcode()

            # convert barcode to ISBN
            detected_isbn = barcodeScanner.convertBarcodeToISBN(detected_barcode)
            # this needs to be displayed on LCD
            print(detected_isbn)

            right_place = database.getDataFromDatabaseWithCondition("Place", "Book", detected_isbn)[0][0]
            # this needs to be displayed on LED strip
            print(right_place)

        # detect place
        if(right_place != ""):
            detected_place = lightSensors.checkIfPlaceIsRight(beginDataLS, right_place)
            # book is placed on wrong place
            if(type(detected_place) != "boolean"):
                # this needs to be displayed on LED strip (red on detected place)
                print(detected_place)
            # book is placed on right place
            elif(detected_place == True):
                # this needs to be displayed on LED strip (green)
                print(detected_place)
            # book wasn't returned to a place --> it is borrowed by someone
            elif(detected_place ==  False):
                pass
                # update database
            
        # maybe implement a hardware reset-button as well?
        print("Reset")
        detected_barcode=""
        detected_isbn = ""
        right_place = ""

except KeyboardInterrupt:
    print("end")