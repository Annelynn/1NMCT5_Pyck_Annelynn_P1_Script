import mysql.connector as mc

connection = mc.connect(host = "localhost",
                        user = "flaskuser",
                        passwd = "flaskpassword",
                        db = "P1_Database")

cursor = connection.cursor()
cursor.execute("SELECT * FROM Boek")
result = cursor.fetchall()
for r in result:
    print(r)

cursor.close()
connection.close()