from model.DbClass import DbClass
from model.BarcodeScanner import BarcodeScanner

database = DbClass()

BS = BarcodeScanner()
barcode = BS.leesBarcode()
ISBN = BS.convertBarcodeToISBN(barcode)

if(barcode != ""):
    boek = database.getDataFromDatabaseWithCondition("Book", "ISBN13", ISBN)
    print(boek[0][1])

