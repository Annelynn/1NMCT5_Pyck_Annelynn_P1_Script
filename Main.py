from model.DbClass import DbClass
from model.BarcodeScanner import BarcodeScanner
from model.LightSensors import LightSensors
from model.LCDScreen import LCDScreen
from model.NeoPixels import NeoPixels
from time import sleep


try:
    barcodeScanner = BarcodeScanner()
    database = DbClass()
    lightSensors = LightSensors()
    LCDScreen = LCDScreen(21, 20, 16, 25, 24, 23)
    LEDstrip = NeoPixels()

    detected_barcode = ""
    detected_isbn = ""
    right_place = ""
    detected_place = ""

    while True:
        # detect light status
        beginDataLS = lightSensors.readChannels()

        # Print instruction LCD Screen
        LCDScreen.show_text_on_multiple_lines("Please scan a barcode")

        # detect barcode
        while(detected_barcode == ""):
            # this is a loop, and nothing will happen until a barcode is scanned
            detected_barcode = barcodeScanner.readBarcode()

            if(detected_barcode != "" and detected_isbn == ""):
                # convert barcode to ISBN
                detected_isbn = barcodeScanner.convertBarcodeToISBN(detected_barcode)

                # get right place from database
                right_place = database.getDataFromDatabaseWithCondition("Book", "ISBN13", detected_isbn)[0][8]
                # display the right place onto the LED strip
                LEDstrip.write_number(right_place)

                # show title of book on LCD screen
                LCDScreen.show_text_on_multiple_lines(database.getDataFromDatabaseWithCondition("Book", "ISBN13", detected_isbn)[0][1])

        # detect place
        while(right_place != "" and detected_place == ""):
            detected_place = lightSensors.checkIfPlaceIsRight(beginDataLS, right_place)
            # Display detected place onto LED strip
            LEDstrip.write_number(detected_place)

            # book is placed on wrong place
            if(detected_place >= 0 and detected_place <= 7):
                # Show info on LCD screen
                LCDScreen.clear_screen()
                LCDScreen.show_text_on_one_line("Wrong place", 0)
                # update database
                database.updateDataWithCondition("Place", "Book", "null", "Book", detected_isbn)
                database.updateDataWithCondition("Place", "Book", detected_isbn, "PlaceID", str(detected_place))

            # book is placed on right place, so True="9" (see LightSensors class for more info)
            elif(detected_place == 9):
                # Show info on LCD screen
                LCDScreen.clear_screen()
                LCDScreen.show_text_on_one_line("Right place", 0)
                # update database
                database.updateDataWithCondition("Place", "Book", "null", "Book", detected_isbn)
                database.updateDataWithCondition("Place", "Book", detected_isbn, "PlaceID", str(right_place))

            # book wasn't returned to a place, so False="8" --> it is borrowed by someone
            elif(detected_place ==  8):
                # Display status of book on LCD screen
                LCDScreen.clear_screen()
                LCDScreen.show_text_on_one_line("Borrowed", 0)
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
        LCDScreen.clear_screen()
        LEDstrip.write_clear()

except KeyboardInterrupt:
    print("end")
    database.closeCursor()
    LCDScreen.shut_down_LCD()
    LEDstrip.shut_down_LED()