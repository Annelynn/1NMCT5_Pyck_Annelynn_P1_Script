from model.DbClass import DbClass
from model.BarcodeScanner import BarcodeScanner
from model.LightSensors import LightSensors
from time import sleep
import datetime

from model.LCDScreen import LCDScreen

database = DbClass()
#barcodeScanner = BarcodeScanner()
lightSensors = LightSensors()
LCDScreen = LCDScreen(21, 20, 16, 25, 24, 23)


# Test database
# -------------------------------------------------------------------------------------
# isbn = "9780747532743"
# book = database.getDataFromDatabaseWithCondition("Book", "PlaceID", isbn)
# place=database.getDataFromDatabaseWithCondition("Place", "Book", isbn)
# print(book[0][8])
# print(place)
# -------------------------------------------------------------------------------------


# Test database + barcode scanner
# -------------------------------------------------------------------------------------
# barcode = barcodeScanner.readBarcode()
# ISBN = barcodeScanner.convertBarcodeToISBN(barcode)
#
# if(barcode != ""):
#     book = database.getDataFromDatabaseWithCondition("Book", "ISBN13", ISBN)
#     print(book[0][1])
# -------------------------------------------------------------------------------------

# Test light sensors
# -------------------------------------------------------------------------------------

# beginDataLS = lightSensors.readChannels()
# print(beginDataLS)
#
# right_place = 6
#
# sleep(1)
# #print(lightSensors.detectLightToDark(beginDataLS))
#
# detected_place = lightSensors.checkIfPlaceIsRight(beginDataLS, right_place)
# print(detected_place)
#
# sleep(1)
# detected_place = lightSensors.checkIfPlaceIsRight(beginDataLS, right_place)
# print(detected_place)
# -------------------------------------------------------------------------------------

# Test LCD
# --------------------------------------------------------------------------------------
LCDScreen.show_text_on_second_line("test")
sleep(10)
LCDScreen.shut_down_LCD()
