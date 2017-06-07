from model.DbClass import DbClass
from model.BarcodeScanner import BarcodeScanner
from model.LightSensors import LightSensors
from time import sleep
import datetime

#database = DbClass()
#barcodeScanner = BarcodeScanner()
lightSensors = LightSensors()

# Test database
# -------------------------------------------------------------------------------------
# isbn = "9780747532743"
# place=database.getDataFromDatabaseWithCondition("Place", "Book", read_isbn)[0][0]
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

beginDataLS = lightSensors.readChannels()
right_place = 7
startTime = datetime.datetime.now()
print(startTime)
sleep(1)


detected_place = lightSensors.checkIfPlaceIsRight(beginDataLS, right_place)
if(detected_place == False):
    print("boek uitgeleend")
else:
    print(detected_place)
# -------------------------------------------------------------------------------------