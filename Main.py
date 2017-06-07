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
    detected_place = ""

    while True:

        # detect light status
        beginDataLS = lightSensors.readChannels()

        # detect barcode
        if(detected_barcode == ""):
            # scan barcode
            # this is a loop, and nothing will happen until a barcode is scanned
            detected_barcode = barcodeScanner.readBarcode()

        if(detected_barcode != "" and detected_isbn == ""):
            # convert barcode to ISBN
            detected_isbn = barcodeScanner.convertBarcodeToISBN(detected_barcode)
            # this needs to be displayed on LCD
            print(detected_isbn)

            right_place = database.getDataFromDatabaseWithCondition("Book", "ISBN13", detected_isbn)[0][8]
            # this needs to be displayed on LED strip
            print(right_place)

        # detect place
        if(right_place != "" and detected_place == ""):

            detected_place = lightSensors.checkIfPlaceIsRight(beginDataLS, right_place)

            # book is placed on wrong place
            if(detected_place >= 0 and detected_place <= 7):
                # this needs to be displayed on LED strip (red on detected place)
                print("Wrong place")
                # update database
                database.updateDataWithCondition("Place", "Book", "null", "Book", detected_isbn)
                database.updateDataWithCondition("Place", "Book", detected_isbn, "PlaceID", str(detected_place))

            # book is placed on right place, so True="9" (see LightSensors class for more info)
            elif(detected_place == 9):
                # this needs to be displayed on LED strip (green)
                print("Right place")
                # update database
                database.updateDataWithCondition("Place", "Book", "null", "Book", detected_isbn)
                database.updateDataWithCondition("Place", "Book", detected_isbn, "PlaceID", str(right_place))

            # book wasn't returned to a place, so False="8" --> it is borrowed by someone
            elif(detected_place ==  8):
                # this needs to be displayed on LCD
                print("Borrowed")
                # update database
                # get the right book
                book = database.getDataFromDatabaseWithCondition("Book", "ISBN13", detected_isbn)
                # update amount borrowed with one
                timesBorrowed = book[0][7] + 1
                # place new value into database
                database.updateDataWithCondition("Book", "BorrowedAmount", str(timesBorrowed), "ISBN13", detected_isbn)
                # tell database, book is absent
                database.updateDataWithCondition("Place", "Book", "null", "Book", detected_isbn)

        # maybe implement a hardware reset-button as well?
        print("Reset")
        detected_barcode = ""
        detected_isbn = ""
        right_place = ""
        detected_place = ""

except KeyboardInterrupt:
    print("end")
    database.closeCursor()