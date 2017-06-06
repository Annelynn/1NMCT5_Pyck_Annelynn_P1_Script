#from model.DbClass import DbClass

#database = DbClass()

import serial
f = open ('/dev/hidraw0', 'rb')
try:
    while 1:
        buffer = f.read(8)
        #for c in buffer:
            #print (c)
            #print(",")
        print(buffer)

except KeyboardInterrupt:
    print("Gelukt!")

