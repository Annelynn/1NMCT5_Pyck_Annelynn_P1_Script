from model.DbConnection import DbConnection
from model.BarcodeScanner import BarcodeScanner
from model.LightSensors import LightSensors
from model.LCDScreen import LCDScreen
from model.NeoPixels import NeoPixels
from time import sleep


try:
    barcodeScanner = BarcodeScanner()
    database = DbConnection("P1_Database")
    lightSensors = LightSensors()
    LCDScreen = LCDScreen(21, 20, 16, 25, 24, 23)
    LEDstrip = NeoPixels()

    detected_logincode = ""
    user = ""
    detected_barcode = ""
    detected_isbn = ""
    right_place = ""
    detected_place = ""

    while True:
        # detect light status
        beginDataLS = lightSensors.readChannels()

        if(detected_logincode == ""):
            # Print instruction LCD Screen
            LCDScreen.show_text_on_multiple_lines("Please scan your card to log in")

        # ask for login code until user is logged in
        while(detected_logincode == ""):

            detected_logincode = barcodeScanner.readBarcode()
            login_code = barcodeScanner.convertBarcodeToNumbers(detected_logincode)
            # when a login code is detected and it is not a barcode from a book
            if(login_code != "" and len(login_code) != 13):
                # get user from database
                user = database.getDataFrom_TableUser_ColumnUserID_ConditionForUSerID(login_code)
                # greet user
                LCDScreen.show_text_on_multiple_lines("Welcome " + user[0]["FirstName"])
            # if a barcode from a book got scanned
            elif (len(login_code) == 13):
                LCDScreen.show_text_on_multiple_lines("You are not logged in!")
                LCDScreen.show_text_on_multiple_lines("Please scan your card to log in")
                # clear variables to go to beginning of this while-loop
                detected_logincode = ""
                login_code = ""

        # show instruction on LCD screen
        LCDScreen.show_text_on_multiple_lines("Please scan a barcode")
        # ask for barcode until it is detected
        while(detected_logincode != "" and detected_barcode == ""):

            detected_barcode = barcodeScanner.readBarcode()

            # log out
            if(detected_barcode == detected_logincode):
                # say goodbye
                LCDScreen.show_text_on_multiple_lines("Goodbye " + user[0]["FirstName"])
                # empty variables
                detected_logincode = ""
                login_code = ""
                user = ""
                detected_barcode = ""

            # if barcode got detected
            elif(detected_barcode != "" and detected_isbn == ""):
                # convert barcode to ISBN
                detected_isbn = barcodeScanner.convertBarcodeToNumbers(detected_barcode)

                # get right place from database
                right_place = database.getDataFrom_TableBook_ColumnISBN13_ConditionForISBN13(detected_isbn)[0]["PlaceID"]
                # display the right place onto the LED strip
                LEDstrip.write_number(right_place)

                # show title of book on LCD screen
                LCDScreen.show_text_on_multiple_lines(database.getDataFrom_TableBook_ColumnISBN13_ConditionForISBN13(detected_isbn)[0]["Title"])

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
                database.addValue_TablePlace_ColumnBook_ConditionForBook("null", detected_isbn)
                database.addValue_TablePlace_ColumnBook_ConditionForPlaceID(detected_isbn, detected_place)
                # remove book from borrowed books
                borrowed_books = user[0]["BorrowedBooks"]
                if(detected_isbn + "-" in borrowed_books):
                    borrowed_books = borrowed_books.replace(detected_isbn + "-", "")
                    database.addValue_TableUser_ColumnBorrowedBooks_ConditionForUserID(borrowed_books, login_code)
                elif("-" + detected_isbn in borrowed_books): # if book at end of string
                    borrowed_books = borrowed_books.replace("-" + detected_isbn, "")
                    database.addValue_TableUser_ColumnBorrowedBooks_ConditionForUserID(borrowed_books, login_code)

            # book is placed on right place, so True="9" (see LightSensors class for more info)
            elif(detected_place == 9):
                # Show info on LCD screen
                LCDScreen.clear_screen()
                LCDScreen.show_text_on_one_line("Right place", 0)
                # update database
                database.addValue_TablePlace_ColumnBook_ConditionForBook("null", detected_isbn)
                database.addValue_TablePlace_ColumnBook_ConditionForPlaceID(detected_isbn, right_place)
                # remove book from borrowed books
                borrowed_books = user[0]["BorrowedBooks"]
                if(detected_isbn + "-" in borrowed_books):
                    borrowed_books = borrowed_books.replace(detected_isbn + "-", "")
                    database.addValue_TableUser_ColumnBorrowedBooks_ConditionForUserID(borrowed_books, login_code)
                elif("-" + detected_isbn in borrowed_books): # if book at end of string
                    borrowed_books = borrowed_books.replace("-" + detected_isbn, "")
                    database.addValue_TableUser_ColumnBorrowedBooks_ConditionForUserID(borrowed_books, login_code)

            # book wasn't returned to a place, so False="8" --> it is borrowed by someone
            elif(detected_place ==  8):
                # Display status of book on LCD screen
                LCDScreen.clear_screen()
                LCDScreen.show_text_on_one_line("Borrowed", 0)
                # update database
                # get the right book
                book = database.getDataFrom_TableBook_ColumnISBN13_ConditionForISBN13(detected_isbn)
                # update borrowed amount
                # update amount borrowed with one
                timesBorrowed = book[0]["BorrowedAmount"] + 1
                # place new value into database
                database.addValue_TableBook_ColumnBorrowedAmount_ConditionForISBN13(timesBorrowed, detected_isbn)
                # tell database, book is absent
                database.addValue_TablePlace_ColumnBook_ConditionForBook("null", detected_isbn)
                #update borrowed books by user
                borrowed_books = user[0]["BorrowedBooks"]
                if(detected_isbn not in borrowed_books):
                    borrowed_books += "-" + detected_isbn
                    database.addValue_TableUser_ColumnBorrowedBooks_ConditionForUserID(borrowed_books, login_code)

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
    LCDScreen.shut_down_LCD()
    LEDstrip.shut_down_LED()