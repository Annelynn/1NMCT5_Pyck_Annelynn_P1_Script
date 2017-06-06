from model.DbClass import DbClass
from model.BarcodeScanner import BarcodeScanner

database = DbClass()

BS = BarcodeScanner()
barcode = BS.leesBarcode()

if(barcode != ""):
    boek = database.getDataFromDatabaseWithCondition("Boek", "Barcode", "&$%\'$!$\"&")
    print(boek)

